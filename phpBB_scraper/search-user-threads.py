import json
import argparse

def search_threads_in_tree(tree, search_username, matching_threads):
    """
    Rekursive Funktion, um Threads im Baum zu durchsuchen und Threads zu sammeln,
    die mindestens einen Post vom Benutzer mit dem angegebenen Benutzernamen enthalten.
    """
    if isinstance(tree, dict):
        for key, value in tree.items():
            if key == "Threads":
                # Navigiere durch die Threads
                for thread_title, thread_data in value.items():
                    if "Posts" in thread_data:
                        # Prüfe, ob ein Post vom Benutzer vorhanden ist
                        user_posts = [
                            post for post in thread_data["Posts"]
                            if post.get("Username", "").strip().lower() == search_username.lower()
                        ]
                        if user_posts:
                            # Füge den gesamten Thread hinzu, wenn ein Post gefunden wurde
                            matching_threads[thread_title] = thread_data
                    if "Threads" in thread_data:
                        # Rekursiv durch die Unterthreads navigieren
                        search_threads_in_tree(thread_data["Threads"], search_username, matching_threads)
            else:
                # Rekursiv durch die Unterknoten navigieren
                search_threads_in_tree(value, search_username, matching_threads)

def search_threads(input_file, output_file, search_username):
    """
    Durchsucht den Baum in post_tree.json nach Threads, die Posts vom Benutzer enthalten,
    und speichert die Ergebnisse in einer neuen Datei.
    """
    with open(input_file, 'r', encoding='utf-8') as file:
        post_tree = json.load(file)

    matching_threads = {}

    # Suche im Baum
    search_threads_in_tree(post_tree, search_username, matching_threads)

    # Ergebnisse speichern
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(matching_threads, file, ensure_ascii=False, indent=4)

    print(f"Threads containing posts from user '{search_username}' have been written to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Search the post tree for threads containing posts from a specific user.')
    parser.add_argument('input_file', type=str, help='The input JSON file containing the post tree.')
    parser.add_argument('output_file', type=str, help='The output JSON file to write matching threads to.')
    parser.add_argument('search_username', type=str, help='The username to search for in the threads.')

    args = parser.parse_args()
    
    search_threads(args.input_file, args.output_file, args.search_username)