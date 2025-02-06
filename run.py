import subprocess
import os
import glob
import configparser
import json

def delete_files():
    print("Deleting all JSON and TXT files in the build folder...")
    files = glob.glob('./build/*')
    for file in files:
        if file.endswith('.json') or file.endswith('.txt'):
            os.remove(file)
            print(f"Deleted {file}")

def run_scrapy():
    print("Running Scrapy to crawl data...")
    subprocess.run(["scrapy", "crawl", "phpBB","-o","../build/posts.json"], check=True, cwd="phpBB_scraper")
    print("Scrapy crawl completed.")

def run_sort():
    print("Running sort.py to sort the data...")
    subprocess.run(["python", "sort.py"], check=True, cwd="phpBB_scraper")
    print("Sorting completed.")

def run_split():
    print("Running split.py to split the data into multiple files...")
    json_files = glob.glob('./build/*.json')
    for json_file in json_files:
        if json_file.endswith('posts.json'):
            continue
        output_prefix = json_file.replace('.json', '')
        subprocess.run(["python", "split.py", "." + json_file, "." + output_prefix, "480000"], check=True, cwd="phpBB_scraper")
        print(f"Splitting completed for {json_file}")

def search_filtered_lists():
    print("Reading filtered lists from config file...")
    config = configparser.ConfigParser()
    config_path = os.path.join(os.path.dirname(__file__), 'config/config.ini')
    config.read(config_path)
    filtered_lists = config.get('settings', 'filtered_lists').split(', ')
    input_file = '../build/posts-sorted.json'

    for item in filtered_lists:
        search_term = item.replace(' ', '_')
        output_file = f'../build/{search_term}.json'
        subprocess.run(["python", "search.py", input_file, output_file, item], check=True, cwd="phpBB_scraper")
        print(f"Results for {item} saved to {output_file}")

def run_to_text():
    print("Running to-text.py to convert JSON files to text...")
    json_files = glob.glob('./build/*.json')
    for json_file in json_files:
        if json_file.endswith('posts.json'):
            continue
        text_file = json_file.replace('.json', '.txt')
        subprocess.run(["python", "to-text.py", "." + json_file, "." + text_file], check=True, cwd="phpBB_scraper")
        print(f"Converted {json_file} to text")

if __name__ == "__main__":
    delete_files()
    run_scrapy()
    run_sort()
    search_filtered_lists()
    run_split()
    run_to_text()