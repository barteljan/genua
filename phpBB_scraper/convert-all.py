import shutil
import glob
import re

def copy_json_to_txt():
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
        print(f"Copying {file} to {output_file}...")
        shutil.copy(file, output_file)
        print(f"Completed copying {file} to {output_file}")

if __name__ == "__main__":
    copy_json_to_txt()