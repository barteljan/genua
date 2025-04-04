import json
import argparse
from typing import Callable, Any

def search_threads_in_tree(tree, condition: Callable[[dict], bool]):
    """
    Rekursive Funktion, um Threads im Baum zu durchsuchen und die Struktur beizubehalten.
    Beinhaltet vollständige Threads, wenn ein Post die Bedingung erfüllt.
    """
    if isinstance(tree, dict):
        filtered_tree = {}
        for key, value in tree.items():
            if key == "Threads":
                filtered_threads = {}
                for thread_title, thread_data in value.items():
                    if "Posts" in thread_data:
                        # Prüfe, ob ein Post die Bedingung erfüllt
                        matching_posts = [post for post in thread_data["Posts"] if condition(post)]
                        if matching_posts:
                            # Behalte den gesamten Thread, wenn ein Post passt
                            filtered_threads[thread_title] = thread_data
                    if "Threads" in thread_data:
                        # Rekursiv durch Unterthreads navigieren
                        sub_threads = search_threads_in_tree(thread_data["Threads"], condition)
                        if sub_threads:
                            filtered_threads[thread_title] = {
                                **thread_data,
                                "Threads": sub_threads
                            }
                if filtered_threads:
                    filtered_tree[key] = filtered_threads
            else:
                # Rekursiv durch andere Unterknoten navigieren
                sub_tree = search_threads_in_tree(value, condition)
                if sub_tree:
                    filtered_tree[key] = sub_tree
        return filtered_tree if filtered_tree else None
    return None

def sub_tree(input_file, output_file, condition: Callable[[dict], bool]):
    """
    Durchsucht den Baum in post_tree.json nach Threads, die die Bedingung erfüllen,
    und speichert die Ergebnisse in einer neuen Datei, wobei die Struktur beibehalten wird.
    """
    with open(input_file, 'r', encoding='utf-8') as file:
        post_tree = json.load(file)

    # Suche im Baum
    filtered_tree = search_threads_in_tree(post_tree, condition)

    if not filtered_tree:
        print("No threads found matching the condition.")
        return

    # Ergebnisse speichern
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(filtered_tree, file, ensure_ascii=False, indent=4)

    print(f"Threads matching the condition have been written to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Search the post tree for threads matching a specific condition.')
    parser.add_argument('input_file', type=str, help='The input JSON file containing the post tree.')
    parser.add_argument('output_file', type=str, help='The output JSON file to write matching threads to.')
    parser.add_argument('search_term', type=str, help='The term to search for in the threads.')

    args = parser.parse_args()

    # Definiere die Bedingung für die Suche
    def condition(post: dict) -> bool:
        return args.search_term.lower() in post.get("PostText", "").lower() or \
               args.search_term.lower() in post.get("Title", "").lower()

    sub_tree(args.input_file, args.output_file, condition)