import json
import argparse

def search_threads_in_tree(tree, search_words, matching_posts):
    """
    Rekursive Funktion, um Threads im Baum zu durchsuchen.
    """
    if isinstance(tree, dict):
        for key, value in tree.items():
            if key == "Threads":
                # Navigiere durch die Threads
                for thread_title, thread_data in value.items():
                    print(f"Checking thread: {thread_title}")  # Debugging-Ausgabe
                    if "Threads" in thread_data:
                        # Rekursiv durch die Threads navigieren
                        search_threads_in_tree(thread_data["Threads"], search_words, matching_posts)

                    # Prüfe, ob der Thread Posts enthält
                    if "Posts" in thread_data:
                        for post in thread_data["Posts"]:
                            username = post.get("Username", "").strip().lower()
                            print(f"Checking post by username: {username}")  # Debugging-Ausgabe
                            if any(word in username for word in search_words):
                                print(f"Match found in post: {post}")  # Debugging-Ausgabe
                                matching_posts.append(post)
            else:
                # Rekursiv durch die Unterknoten navigieren
                search_threads_in_tree(value, search_words, matching_posts)
    elif isinstance(tree, list):
        # Wenn tree eine Liste ist, iteriere durch die Elemente
        for item in tree:
            search_threads_in_tree(item, search_words, matching_posts)

def search_threads(input_file, output_file, search_words):
    """
    Durchsucht den Baum in post_tree.json nach Threads, die die Suchwörter enthalten.
    """
    with open(input_file, 'r', encoding='utf-8') as file:
        post_tree = json.load(file)

    

    search_words = [word.lower() for word in search_words]  # Suchwörter in Kleinbuchstaben umwandeln
    print(f"Search words: {search_words}")  # Debugging-Ausgabe
    matching_posts = []

    # Suche im Baum
    search_threads_in_tree(post_tree, search_words, matching_posts)

    # Ergebnisse speichern
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(matching_posts, file, ensure_ascii=False, indent=4)

    print(f"Threads containing the search words have been written to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Search threads in a post tree for specific usernames and write matching threads to a new file.')
    parser.add_argument('input_file', type=str, help='The input JSON file containing the post tree.')
    parser.add_argument('output_file', type=str, help='The output JSON file to write matching threads to.')
    parser.add_argument('search_words', type=str, nargs='+', help='The usernames to search for in the threads.')

    args = parser.parse_args()
    
    search_threads(args.input_file, args.output_file, args.search_words)