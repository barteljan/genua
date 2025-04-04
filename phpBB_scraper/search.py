import json
import argparse
from sub_tree import sub_tree  # Importiere die generische Funktion aus sub_tree.py

def condition(post: dict, search_words: list) -> bool:
    """
    Bedingung für die Suche: Überprüft, ob ein Post die Suchwörter enthält.
    """
    post_text = post.get("PostText", "").lower()
    title = post.get("Title", "").lower()
    quote_text = post.get("PostText", "").lower()
    return any(word in post_text or word in title or word in quote_text for word in search_words)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Search the post tree for threads containing specific words.')
    parser.add_argument('input_file', type=str, help='The input JSON file containing the post tree.')
    parser.add_argument('output_file', type=str, help='The output JSON file to write matching threads to.')
    parser.add_argument('search_words', type=str, nargs='+', help='The words to search for in the threads.')

    args = parser.parse_args()

    # Definiere die Bedingung für die Suche
    def search_condition(post: dict) -> bool:
        return condition(post, [word.lower() for word in args.search_words])

    # Verwende die generische Funktion aus sub_tree.py
    sub_tree(args.input_file, args.output_file, search_condition)