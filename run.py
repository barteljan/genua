import subprocess
import os
import glob
import configparser
import argparse

def delete_files(skip_posts_json=False, skip_pdfs=False):
    """
    Deletes all JSON, TXT, and PDF files in the build directory.
    If skip_posts_json=True, the posts.json file will not be deleted.
    If skip_pdfs=True, PDF files will not be deleted.
    """
    print("Deleting files in ./build/...")

    build_dir = './build'
    files = glob.glob(os.path.join(build_dir, '*'))

    for file in files:
        # Skip posts.json if skip_posts_json is enabled
        if skip_posts_json and os.path.basename(file) == "posts.json":
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

def run_scrapy():
    print("Running Scrapy to crawl data...")
    subprocess.run(["scrapy", "crawl", "phpBB", "-o", "../build/posts.json"], check=True, cwd="phpBB_scraper")
    print("Scrapy crawl completed.")

def run_sort():
    print("Running sort.py to sort the data...")
    subprocess.run(["python", "sort.py"], check=True, cwd="phpBB_scraper")
    print("Sorting completed.")

    # Build the post tree
    print("Building post tree...")
    input_file = '../build/posts-sorted.json'
    output_file = './data/post_tree.json'
    subprocess.run(["python", "build_post_tree.py", input_file, "." + output_file], check=True, cwd="phpBB_scraper")
    print("Post tree has been built.")

    cleaned_file = output_file.replace(".json", "_cleaned.json")
    subprocess.run(["python", "clean_text_file.py", "." + output_file, "." + cleaned_file], check=True, cwd="phpBB_scraper")
    os.replace(cleaned_file, output_file)



def run_split():
    print("Running split.py to split the text files into multiple files...")
    txt_files = glob.glob('./build/*.txt')  # Nur .txt-Dateien auswählen
    for txt_file in txt_files:
        output_prefix = txt_file.replace('.txt', '')
        subprocess.run(["python", "split.py", "." + txt_file, "." + output_prefix, "480000"], check=True, cwd="phpBB_scraper")
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

def clean_all_txt_files():
    print("Cleaning all .txt files in ./build/...")
    txt_files = glob.glob('./build/*.txt')
    for txt_file in txt_files:
        cleaned_file = txt_file.replace(".txt", "_cleaned.txt")
        subprocess.run(["python", "clean_text_file.py", "." + txt_file, "." + cleaned_file], check=True, cwd="phpBB_scraper")
        os.replace(cleaned_file, txt_file)  # Replace the original file with the cleaned file
        print(f"Cleaned {txt_file} and saved as {txt_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the full pipeline for processing data.")
    parser.add_argument("--skip-delete", action="store_true", help="Skip deleting posts.json in the build folder.")
    parser.add_argument("--generate-pdfs", action="store_true", help="Generate PDFs from .txt files.")
    parser.add_argument("--skip-scrape", action="store_true", help="Skip scraping data with Scrapy.")
    args = parser.parse_args()

    # Delete files based on the options --skip-delete and --generate-pdfs
    delete_files(skip_posts_json=args.skip_delete, skip_pdfs=not args.generate_pdfs)

    if not args.skip_scrape:
        run_scrapy()
    run_sort()
    search_filtered_lists()
    search_user_threads()
    run_to_text()
    #clean_all_txt_files()
    run_split()

    # Generate PDFs only if --generate-pdfs is set
    if args.generate_pdfs:
        convert_txt_to_pdf()