import subprocess
import os
import glob
import configparser
import argparse
import json
import time
from datetime import datetime


def delete_posts_json(skip_posts_json=False):
    """
    Deletes the posts.json file in the build directory.
    If skip_posts_json=True, the posts.json file will not be deleted.
    """
    print("Deleting posts.json in ./build/...")
    posts_json_path = os.path.join('./build', 'posts.json')

    if skip_posts_json:
        print("Skipping deletion of posts.json.")
        return

    if os.path.exists(posts_json_path):
        try:
            os.remove(posts_json_path)
            print(f"Deleted: {posts_json_path}")
        except Exception as e:
            print(f"Failed to delete {posts_json_path}. Reason: {e}")


def delete_files(skip_pdfs=False):
    """
    Deletes all JSON, TXT, and PDF files in the build directory.
    If skip_pdfs=True, PDF files will not be deleted.
    """
    print("Deleting files in ./build/...")

    build_dir = './build'
    files = glob.glob(os.path.join(build_dir, '*'))

    for file in files:

         # Skip posts.json explicitly
        if os.path.basename(file) == "posts.json":
            print(f"Skipping deletion of {file}")
            continue


        # Skip PDF files if skip_pdfs is enabled
        if skip_pdfs and file.endswith('.pdf'):
            continue

        # Delete JSON, TXT, and PDF files
        if file.endswith('.json') or file.endswith('.txt') or file.endswith('.pdf'):
            try:
                os.remove(file)
                print(f"Deleted: {file}")
            except Exception as e:
                print(f"Failed to delete {file}. Reason: {e}")


def run_scrapy(max_retries=3, delay=5):
    """
    Runs Scrapy to crawl data. Retries up to `max_retries` times if no posts are scraped.
    """
    for attempt in range(1, max_retries + 1):
        print(f"Running Scrapy (Attempt {attempt}/{max_retries})...")
        subprocess.run(["scrapy", "crawl", "phpBB", "-o", "../build/posts.json"], check=True, cwd="phpBB_scraper")
        print("Scrapy crawl completed.")

        # Check if posts.json contains at least one post
        posts_json_path = './build/posts.json'
        if os.path.exists(posts_json_path):
            with open(posts_json_path, 'r', encoding='utf-8') as file:
                try:
                    posts = json.load(file)
                    if len(posts) > 0:
                        print(f"Scraping successful: {len(posts)} posts found.")
                        return  # Exit the function if scraping is successful
                except json.JSONDecodeError:
                    print("Error decoding posts.json. Retrying...")

        print(f"No posts found. Retrying in {delay} seconds...")
        delete_posts_json(skip_posts_json=False)  # Delete posts.json before retrying
        time.sleep(delay)

    # If all retries fail, raise an exception
    raise RuntimeError("Scraping failed after multiple attempts. No posts were found.")


def run_sort():
    print("Running sort.py to sort the data...")
    subprocess.run(["python", "sort.py"], check=True, cwd="phpBB_scraper")
    print("Sorting completed.")

    # Build the post tree
    print("Building post tree...")
    input_file = './build/posts-sorted.json'
    output_file = './data/post_tree.json'
    subprocess.run(["python", "build_post_tree.py", "." + input_file, "." + output_file], check=True, cwd="phpBB_scraper")
    print("Post tree has been built.")
    subprocess.run(["python", "count_posts_in_tree.py"], check=True, cwd="phpBB_scraper")

    cleaned_file = output_file.replace(".json", "_cleaned.json")
    subprocess.run(["python", "clean_text_file.py", "." + output_file, "." + cleaned_file], check=True, cwd="phpBB_scraper")
    os.replace(cleaned_file, output_file)


def run_split():
    print("Running split.py to split the text files into multiple files...")
    txt_files = glob.glob('./build/*.txt')  # Nur .txt-Dateien auswählen
    for txt_file in txt_files:
        output_prefix = txt_file.replace('.txt', '')
        subprocess.run(["python", "split.py", "." + txt_file, "." + output_prefix, "450000"], check=True, cwd="phpBB_scraper")
        print(f"Splitting completed for {txt_file}")


def search_filtered_lists():
    print("Reading filtered lists from config file...")
    config = configparser.ConfigParser()
    config_path = os.path.join(os.path.dirname(__file__), 'config/config.ini')
    config.read(config_path)
    filtered_lists = config.get('settings', 'filtered_lists', fallback='').split(', ')
    input_file = '../data/post_tree.json'  # Verwende die post_tree.json als Eingabe

    for item in filtered_lists:
        search_term = item.replace(' ', '_')
        output_file = f'../build/{search_term}.json'
        subprocess.run(["python", "search.py", input_file, output_file, item], check=True, cwd="phpBB_scraper")
        print(f"Results for {item} saved to {output_file}")


def search_user_threads():
    print("Reading filtered lists from config file...")
    config = configparser.ConfigParser()
    config_path = os.path.join(os.path.dirname(__file__), 'config/config.ini')
    config.read(config_path)
    search_items = config.get('settings', 'user_filter', fallback='').split(', ')
    print(f"Search items: {search_items}")  # Debugging-Ausgabe
    input_file = '../data/post_tree.json'  # Verwende die post_tree.json als Eingabe

    for item in search_items:
        search_term = item.replace(' ', '_')
        output_file = f'../build/{search_term}_user.json'
        subprocess.run(["python", "search-user-threads.py", input_file, output_file, item], check=True, cwd="phpBB_scraper")
        print(f"Results for {item} saved to {output_file}")


def run_to_text():
    print("Running to-text.py to convert JSON files to text...")
    json_files = glob.glob('./build/*.json')  # Alle JSON-Dateien im build-Verzeichnis
    for json_file in json_files:
        if json_file.endswith('posts-sorted.json'):
            continue  # Überspringe die posts-sorted.json

        text_file = json_file.replace('.json', '.txt')
        subprocess.run(["python", "to-text.py", "." + json_file, "." + text_file], check=True, cwd="phpBB_scraper")
        print(f"Converted {json_file} to text")

    # Verarbeite die data/post_tree.json separat
    post_tree_file = '../data/post_tree.json'
    post_tree_text_file = '../build/posts.txt'
    subprocess.run(["python", "to-text.py", post_tree_file, post_tree_text_file], check=True, cwd="phpBB_scraper")
    print(f"Converted {post_tree_file} to text")


def convert_txt_to_pdf():
    print("Converting all .txt files in ./build/ to PDFs...")
    txt_files = glob.glob("./build/*.txt")
    for txt_file in txt_files:
        pdf_file = txt_file.replace(".txt", ".pdf")
        subprocess.run(["python", "to-pdf.py", "." + txt_file, "." + pdf_file], check=True, cwd="phpBB_scraper")
        print(f"Converted {txt_file} to {pdf_file}")


def load_statistics(stats_file):
    """
    Lädt die bestehende statistics.json, falls sie existiert.
    """
    if os.path.exists(stats_file):
        with open(stats_file, 'r', encoding='utf-8') as file:
            return json.load(file)
    return {}


def write_statistics(start_time, end_time, last_scrape_time, stats_file='./data/statistics.json'):
    """
    Schreibt die Statistikdaten in eine JSON-Datei im data-Verzeichnis.
    """
    duration = (end_time - start_time).total_seconds()

    # Bestehende Statistikdaten laden
    existing_stats = load_statistics(stats_file)

    # Aktualisiere die Statistikdaten
    statistics = {
        "last_scrape_time": last_scrape_time.isoformat() if last_scrape_time else existing_stats.get("last_scrape_time"),
        "script_start_time": start_time.isoformat(),
        "script_end_time": end_time.isoformat(),
        "total_duration_seconds": duration
    }

    os.makedirs(os.path.dirname(stats_file), exist_ok=True)  # Erstelle das Verzeichnis, falls es nicht existiert
    with open(stats_file, 'w', encoding='utf-8') as file:
        json.dump(statistics, file, ensure_ascii=False, indent=4)
    print(f"Statistics written to {stats_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the full pipeline for processing data.")
    parser.add_argument("--skip-delete", action="store_true", help="Skip deleting posts.json in the build folder.")
    parser.add_argument("--generate-pdfs", action="store_true", help="Generate PDFs from .txt files.")
    parser.add_argument("--skip-scrape", action="store_true", help="Skip scraping data with Scrapy.")
    args = parser.parse_args()

    # Erfasse den Startzeitpunkt des Skripts
    script_start_time = datetime.now()

    delete_posts_json(skip_posts_json=args.skip_delete)

    stats_file = './data/statistics.json'
    existing_stats = load_statistics(stats_file)
    last_scrape_time = existing_stats.get("last_scrape_time")

    if not args.skip_scrape:
        try:
            run_scrapy()
            last_scrape_time = datetime.now()  # Erfasse den Zeitpunkt des letzten Scrapes
        except RuntimeError as e:
            print(str(e))
            exit(1)  # Beende das Skript, wenn Scraping fehlschlägt

    delete_files(skip_pdfs=not args.generate_pdfs)
    run_sort()
    search_filtered_lists()
    search_user_threads()
    run_to_text()
    run_split()

    if args.generate_pdfs:
        convert_txt_to_pdf()

    # Erfasse den Endzeitpunkt des Skripts
    script_end_time = datetime.now()

    # Schreibe die Statistikdaten in die statistics.json
    write_statistics(script_start_time, script_end_time, last_scrape_time, stats_file)