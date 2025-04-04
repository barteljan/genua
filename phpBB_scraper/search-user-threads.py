import json
import argparse
from sub_tree import sub_tree  # Importiere die generische Funktion aus sub_tree.py

def condition(post: dict, search_username: str) -> bool:
    """
    Bedingung für die Suche: Überprüft, ob ein Post vom angegebenen Benutzer stammt.
    """
    return post.get("Username", "").strip().lower() == search_username.lower()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Search the post tree for threads containing posts from a specific user.')
    parser.add_argument('input_file', type=str, help='The input JSON file containing the post tree.')
    parser.add_argument('output_file', type=str, help='The output JSON file to write matching threads to.')
    parser.add_argument('search_username', type=str, help='The username to search for in the threads.')

    args = parser.parse_args()

    # Definiere die Bedingung für die Suche
    def user_condition(post: dict) -> bool:
        return condition(post, args.search_username)

    # Verwende die generische Funktion aus sub_tree.py
    sub_tree(args.input_file, args.output_file, user_condition)
"""
def search_threads_in_tree(tree, search_username):
    if isinstance(tree, dict):
        filtered_tree = {}
        for key, value in tree.items():
            if key == "Threads":
                filtered_threads = {}
                for thread_title, thread_data in value.items():
                    if "Posts" in thread_data:
                        # Prüfe, ob ein Post vom Benutzer vorhanden ist
                        user_posts = [
                            post for post in thread_data["Posts"]
                            if post.get("Username", "").strip().lower() == search_username.lower()
                        ]
                        if user_posts:
                            # Behalte den gesamten Thread, wenn ein Post passt
                            filtered_threads[thread_title] = thread_data
                    if "Threads" in thread_data:
                        # Rekursiv durch Unterthreads navigieren
                        sub_threads = search_threads_in_tree(thread_data["Threads"], search_username)
                        if sub_threads:
                            filtered_threads[thread_title] = {
                                **thread_data,
                                "Threads": sub_threads
                            }
                if filtered_threads:
                    filtered_tree[key] = filtered_threads
            else:
                # Rekursiv durch andere Unterknoten navigieren
                sub_tree = search_threads_in_tree(value, search_username)
                if sub_tree:
                    filtered_tree[key] = sub_tree
        return filtered_tree if filtered_tree else None
    return None

def search_threads(input_file, output_file, search_username):
    with open(input_file, 'r', encoding='utf-8') as file:
        post_tree = json.load(file)

    # Suche im Baum
    filtered_tree = search_threads_in_tree(post_tree, search_username)
    filtered_tree = clean_thread_structure(filtered_tree)  # Bereinige die Struktur

    # Ergebnisse speichern
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(filtered_tree, file, ensure_ascii=False, indent=4)

    print(f"Threads containing posts from user '{search_username}' have been written to {output_file}")

def clean_thread_structure(tree):
    if isinstance(tree, dict):
        cleaned_tree = {}
        for key, value in tree.items():
            if key == "Threads" and isinstance(value, dict):
                # Entferne redundante unterste Keys
                cleaned_threads = {}
                for thread_key, thread_value in value.items():
                    if "Threads" in thread_value and len(thread_value["Threads"]) == 1:
                        # Wenn der unterste Key redundant ist, entferne ihn
                        sub_key, sub_value = next(iter(thread_value["Threads"].items()))
                        if thread_key == sub_key:
                            thread_value = sub_value
                    cleaned_threads[thread_key] = clean_thread_structure(thread_value)
                cleaned_tree[key] = cleaned_threads
            else:
                cleaned_tree[key] = clean_thread_structure(value)
        return cleaned_tree
    elif isinstance(tree, list):
        return [clean_thread_structure(item) for item in tree]
    return tree



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Search the post tree for threads containing posts from a specific user.')
    parser.add_argument('input_file', type=str, help='The input JSON file containing the post tree.')
    parser.add_argument('output_file', type=str, help='The output JSON file to write matching threads to.')
    parser.add_argument('search_username', type=str, help='The username to search for in the threads.')

    args = parser.parse_args()
    
    search_threads(args.input_file, args.output_file, args.search_username)
"""