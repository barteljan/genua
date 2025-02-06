import subprocess
import glob
import re

def run_to_text_for_all_files():
    # Find all files matching the pattern posts_{nummer}.json
    files = glob.glob('./build/posts_*.json')
    valid_files = []

    for file in files:
        match = re.search(r'posts_(\d+).json', file)
        if match:
            valid_files.append((file, int(match.group(1))))

    valid_files.sort(key=lambda x: x[1])

    for file, _ in valid_files:
        output_file = file.replace('.json', '.txt')
        print(f"Running to-text.py for {file}...")
        subprocess.run(["python", "to-text.py", file, output_file], check=True)
        print(f"Completed to-text.py for {file}")

if __name__ == "__main__":
    run_to_text_for_all_files()