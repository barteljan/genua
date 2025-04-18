# -*- coding: utf-8 -*-
import re
import scrapy
from bs4 import BeautifulSoup
from scrapy.http import Request
import configparser
import os
import json
from datetime import datetime, timedelta

# Function to load statistics dynamically
def load_statistics(stats_file):
    """
    Loads the statistics.json file if it exists.
    Returns an empty dictionary if the file does not exist.
    """
    if os.path.exists(stats_file):
        with open(stats_file, 'r', encoding='utf-8') as file:
            return json.load(file)
    print(f"Warning: {stats_file} not found. Defaulting to index.php.")
    return {}

# Determine if we should start with search.php or index.php
statistics_file = os.path.join(os.path.dirname(__file__), '../../../data/statistics.json')
use_search_page = False

statistics = load_statistics(statistics_file)
last_scrape_time_str = statistics.get("last_scrape_time")
if last_scrape_time_str:
    try:
        last_scrape_time = datetime.fromisoformat(last_scrape_time_str)
        if datetime.now() - last_scrape_time < timedelta(days=7):
            use_search_page = True
    except ValueError:
        print("Invalid last_scrape_time format in statistics.json. Defaulting to index.php.")
else:
    print("No last_scrape_time found in statistics.json. Defaulting to index.php.")

# Read credentials from the config file
config = configparser.ConfigParser()
config_path = os.path.join(os.path.dirname(__file__), '../../../config/config.ini')

# Explicitly specify the encoding
with open(config_path, 'r', encoding='utf-8') as f:
    config.read_file(f)

# Debugging: Print sections to verify the file is read correctly
print(f"Sections found in config: {config.sections()}")

# Check if the 'login' section exists
if 'login' not in config:
    raise ValueError("No 'login' section found in the config file")

# Check if the 'settings' section exists
if 'settings' not in config:
    raise ValueError("No 'settings' section found in the config file")

# TODO: Please provide values for the following variables
# Domains only, no urls
ALLOWED_DOMAINS = ['forum.genua-bei-nacht.de']
# Starting urls
START_URLS = ['https://forum.genua-bei-nacht.de/']
# Is login required? True or False.
FORM_LOGIN = True
# Login username
USERNAME = config.get('login', 'username')
# Login password
PASSWORD = config.get('login', 'password')
# Login url
LOGIN_URL = 'https://forum.genua-bei-nacht.de/ucp.php?mode=login&redirect=index.php'

#blacklist
BLACKLIST = config.get('settings', 'blacklist', fallback='').split(', ')

class PhpbbSpider(scrapy.Spider):
    
    name = 'phpBB'
    allowed_domains = ALLOWED_DOMAINS
    start_urls = START_URLS
    form_login = FORM_LOGIN
    if form_login is True:
        username = USERNAME
        password = PASSWORD
        login_url = LOGIN_URL
        start_urls.insert(0, login_url)

    username_xpath = '//p[contains(@class, "author")]//a[contains(@class, "username")]//text()'
    post_count_xpath = '//dd[@class="profile-posts" or not(@class)]//a/text()'
    post_time_xpath = '//div[@class="postbody"]//time/@datetime|//div[@class="postbody"]//p[@class="author"]/text()[2]'
    post_text_xpath = '//div[@class="postbody"]//div[@class="content"]'
    breadcrumb_xpath = '//li[contains(@class,breadcrumbs")]//a/text()'

    def parse(self, response):
        # LOGIN TO PHPBB BOARD AND CALL AFTER_LOGIN
        if self.form_login:
            formxpath = '//*[contains(@action, "login")]'
            formdata = {'username': self.username, 'password': self.password}
            form_request = scrapy.FormRequest.from_response(
                    response,
                    formdata=formdata,
                    formxpath=formxpath,
                    callback=self.after_login,
                    dont_click=False
            )
            yield form_request
        else:
            if use_search_page:
                search_url = 'https://forum.genua-bei-nacht.de/search.php?search_id=active_topics'
                yield scrapy.Request(search_url, callback=self.parse_topics)
            else:
                # REQUEST SUB-FORUM TITLE LINKS
                links = response.xpath('//a[@class="forumtitle"]/@href').extract()
                for link in links:
                    yield scrapy.Request(response.urljoin(link), callback=self.parse_topics)

    def after_login(self, response):
        # CHECK LOGIN SUCCESS BEFORE MAKING REQUESTS
        if b'authentication failed' in response.body:
            self.logger.error('Login failed.')
            return
        else:
            if use_search_page:
                search_url = 'https://forum.genua-bei-nacht.de/search.php?search_id=active_topics'
                yield scrapy.Request(search_url, callback=self.parse_topics)
            else:
                # REQUEST SUB-FORUM TITLE LINKS
                links = response.xpath('//a[@class="forumtitle"]/@href').extract()
                for link in links:
                    yield scrapy.Request(response.urljoin(link), callback=self.parse_topics)


    def parse_topics(self, response):

        breadcrumb = response.xpath('//ul[@id="nav-breadcrumbs"]/li[@class="breadcrumbs"]//span/a/span/text()').getall()

        # Check if any item in breadcrumb is in the blacklist
        if breadcrumb and BLACKLIST:
            for item in breadcrumb:
                if item in BLACKLIST:
                    return

        # REQUEST SUB-FORUM TITLE LINKS
        subForumLinks = response.xpath('//a[@class="forumtitle"]/@href').extract()
        for link in subForumLinks:
            yield scrapy.Request(response.urljoin(link), callback=self.parse_topics)

        # REQUEST TOPIC TITLE LINKS
        links = response.xpath('//a[@class="topictitle"]/@href').extract()
        for link in links:
            yield scrapy.Request(response.urljoin(link), callback=self.parse_posts)
        
        # IF NEXT PAGE EXISTS, FOLLOW
        next_page_link = response.xpath('//a[@rel="next"]/@href').get()
        if next_page_link:
            next_page_url = response.urljoin(next_page_link)
            yield scrapy.Request(next_page_url, callback=self.parse_topics)
    
    def clean_quote(self, string):
        # CLEAN HTML TAGS FROM POST TEXT, MARK QUOTES
        soup = BeautifulSoup(string, 'lxml')
        block_quotes = soup.find_all('blockquote')
        for i, quote in enumerate(block_quotes):
            block_quotes[i] = '<quote-%s>=%s' % (str(i + 1), quote.get_text())
        return ''.join(block_quotes).strip()
    
    def clean_text(self, string):
        # CLEAN HTML TAGS FROM POST TEXT, MARK REPLIES TO QUOTES
        tags = ['blockquote']
        soup = BeautifulSoup(string, 'lxml')
        for tag in tags:
            for i, item in enumerate(soup.find_all(tag)):
                item.replaceWith('<reply-%s>=' % str(i + 1))
        return re.sub(r' +', r' ', soup.get_text()).strip()
      
    def parse_posts(self, response):
        # COLLECT FORUM POST DATA
        usernames = response.xpath(self.username_xpath).extract()

        # Extrahiere die Texte der Breadcrumbs
        breadcrumbs = response.xpath('//ul[@id="nav-breadcrumbs"]/li[@class="breadcrumbs"]//span/a/span/text()').getall()
        forum = " / ".join(breadcrumbs)

        # Check if any item in breadcrumb is in the blacklist
        if breadcrumbs and BLACKLIST:
            for item in breadcrumbs:
                if item in BLACKLIST:
                    return

        # Extrahiere den Thread-Titel
        thread_title = response.xpath('//h2[@class="topic-title"]/a/text()').get()

        if breadcrumbs:
            self.logger.info(forum + " / " + thread_title)

        # Kombiniere Breadcrumbs und Thread-Titel zu 'full_path'
        full_path = f"{forum} / {thread_title}" if thread_title else forum

        n = len(usernames)
        if n > 0:
            post_times = response.xpath(self.post_time_xpath).extract() or (n * [''])
            post_texts = response.xpath(self.post_text_xpath).extract() or (n * [''])
            post_quotes = [self.clean_quote(s) for s in post_texts]
            post_texts = [self.clean_text(s) for s in post_texts]

            # YIELD POST DATA
            for i in range(n):
                yield {'Username': str(usernames[i]).strip(), 'URL': response.url,'Title': thread_title, 'Forum': full_path, 
                       'PostTime': str(post_times[i]).strip(), 'PostText': post_texts[i], 'QuoteText': post_quotes[i]}

        # CLICK THROUGH NEXT PAGE
         # Extrahiere den Link zur nächsten Seite und konvertiere ihn in eine absolute URL
        next_page_link = response.xpath('//a[@rel="next"]/@href').get()
        if next_page_link:
            next_page_url = response.urljoin(next_page_link)
            yield scrapy.Request(next_page_url, callback=self.parse_posts)
