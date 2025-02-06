# Genua-Bei-Nacht Scraper

Python-based web scraper for genua-bei-nacht.de.

## Requirements: 

1. Python web scraping library, [Scrapy](http://scrapy.org/).   
2. Python HTML/XML parsing library, [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/).

## Install dependencies
create virtual environment

'''python3 -m venv .venv'''

install dependencies

'''./.venv/bin/pip install -r requirements.txt'''

'''source ./.venv/bin/activate'''

## Create `config/config.ini` from `config/config.ini.example`

1. `specify username and password`
2. `have a look on the blacklist. Each Forum which has a word in the blacklist in its title or path will not be parsed` 
3. `have a look at the filters_lists every item will generate a new json list with all threads which contain a specific keyword in a posts test or in a posts title.`


## Running the Scraper:
```bash
./.venv/bin/python run.py
```
NOTE: Please adjust `settings.py` to throttle your requests.