import json
import argparse

def search_threads(input_file, output_file, search_words):
    with open(input_file, 'r', encoding='utf-8') as file:
        posts = json.load(file)

    search_words = [word.lower() for word in search_words]  # Convert search words to lowercase

    matching_threads = []
    for post in posts:
        post_text = post.get('PostText', '').lower()  # Convert post text to lowercase
        title = post.get('Title', '').lower()  # Convert title to lowercase
        if any(word in post_text for word in search_words) or \
           any(word in title for word in search_words):
            matching_threads.append(post.get('Forum'))


    matching_posts = []
    for post in posts:
        forum = post.get('Forum')
        if forum in matching_threads:
            matching_posts.append(post)


    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(matching_posts, file, ensure_ascii=False, indent=4)

    print(f"Threads containing the search words have been written to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Search threads in a JSON file for specific words and write matching threads to a new file.')
    parser.add_argument('input_file', type=str, help='The input JSON file containing posts.')
    parser.add_argument('output_file', type=str, help='The output JSON file to write matching threads to.')
    parser.add_argument('search_words', type=str, nargs='+', help='The words to search for in the threads.')

    args = parser.parse_args()
    
    search_threads(args.input_file, args.output_file, args.search_words)