import json
import argparse

def search_threads_in_tree(tree, search_words, matching_threads):
    """
    Rekursive Funktion, um Threads im Baum zu durchsuchen und Threads zu sammeln,
    die mindestens einen Post enthalten, in dem das Suchwort im "PostText", "Title" oder "QuoteText" vorkommt.
    """
    if isinstance(tree, dict):
        for key, value in tree.items():
            if key == "Threads":
                # Navigiere durch die Threads
                for thread_title, thread_data in value.items():
                    if "Posts" in thread_data:
                        # Prüfe, ob ein Post das Suchwort enthält
                        matching_posts = [
                            post for post in thread_data["Posts"]
                            if any(
                                word in post.get("PostText", "").lower() or
                                word in post.get("Title", "").lower() or
                                word in post.get("QuoteText", "").lower()
                                for word in search_words
                            )
                        ]
                        if matching_posts:
                            # Füge den gesamten Thread hinzu, wenn ein Post gefunden wurde
                            matching_threads[thread_title] = thread_data
                    if "Threads" in thread_data:
                        # Rekursiv durch die Unterthreads navigieren
                        search_threads_in_tree(thread_data["Threads"], search_words, matching_threads)
            else:
                # Rekursiv durch die Unterknoten navigieren
                search_threads_in_tree(value, search_words, matching_threads)

def search_tree(input_file, output_file, search_words):
    """
    Durchsucht den Baum in post_tree.json nach Threads, die Posts enthalten,
    in denen das Suchwort im "PostText", "Title" oder "QuoteText" vorkommt,
    und speichert die Ergebnisse in einer neuen Datei.
    """
    with open(input_file, 'r', encoding='utf-8') as file:
        post_tree = json.load(file)

    search_words = [word.lower() for word in search_words]  # Suchbegriffe in Kleinbuchstaben umwandeln
    matching_threads = {}

    # Suche im Baum
    search_threads_in_tree(post_tree, search_words, matching_threads)

    # Ergebnisse speichern
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(matching_threads, file, ensure_ascii=False, indent=4)

    print(f"Threads containing posts with the search words have been written to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Search the post tree for threads containing posts with specific keywords.')
    parser.add_argument('input_file', type=str, help='The input JSON file containing the post tree.')
    parser.add_argument('output_file', type=str, help='The output JSON file to write matching threads to.')
    parser.add_argument('search_words', type=str, nargs='+', help='The keywords to search for in the posts.')

    args = parser.parse_args()
    
    search_tree(args.input_file, args.output_file, args.search_words)