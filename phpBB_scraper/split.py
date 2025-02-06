import json
import argparse

def count_words(text):
    return len(text.split())

def split_json(input_file, output_prefix, max_words):
    with open(input_file, 'r', encoding='utf-8') as file:
        posts = json.load(file)

    total_words = sum(count_words(json.dumps(post, ensure_ascii=False)) for post in posts)
    if total_words <= max_words:
        print(f"No need to split {input_file}, total words ({total_words}) <= max words ({max_words})")
        return

    current_words = 0
    file_index = 1
    current_batch = []

    for post in posts:
        post_words = count_words(json.dumps(post, ensure_ascii=False))
        if current_words + post_words > max_words:
            output_file = f"{output_prefix}_{file_index}.json"
            with open(output_file, 'w', encoding='utf-8') as outfile:
                json.dump(current_batch, outfile, ensure_ascii=False, indent=4)
            print(f"Saved {output_file} with {current_words} words")
            file_index += 1
            current_batch = []
            current_words = 0

        current_batch.append(post)
        current_words += post_words

    if current_batch:
        output_file = f"{output_prefix}_{file_index}.json"
        with open(output_file, 'w', encoding='utf-8') as outfile:
            json.dump(current_batch, outfile, ensure_ascii=False, indent=4)
        print(f"Saved {output_file} with {current_words} words")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Split JSON file into multiple files with a maximum number of words.')
    parser.add_argument('input_file', type=str, help='The input JSON file to split.')
    parser.add_argument('output_prefix', type=str, help='The prefix for the output files.')
    parser.add_argument('max_words', type=int, help='The maximum number of words per output file.')

    args = parser.parse_args()
    
    split_json(args.input_file, args.output_prefix, args.max_words)