import subprocess

def run_scrapy():
    print("Running Scrapy to crawl data...")
    subprocess.run(["scrapy", "crawl", "phpBB","-o","./build/posts.json"], check=True)
    print("Scrapy crawl completed.")

def run_sort():
    print("Running sort.py to sort the data...")
    subprocess.run(["python", "sort.py"], check=True)
    print("Sorting completed.")


def run_split():
    print("Running split.py to split the data into multiple files...")
    subprocess.run(["python", "split.py", "./build/posts-sorted.json", "./build/posts", "480000"], check=True)
    print("Splitting completed.")

def run_convert():
    print("Running split.py to split the data into multiple files...")
    subprocess.run(["python", "to-text.py", "./build/posts-sorted.json", "./build/posts.txt"], check=True)
    print("converting completed.")

if __name__ == "__main__":
    run_scrapy()
    run_sort()
    run_split()
    run_convert()