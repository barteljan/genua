import json
import argparse

def search_in_tree(tree, search_words, matching_posts):
    """
    Rekursive Funktion, um den Baum nach Threads oder Posts zu durchsuchen,
    die die Suchbegriffe enthalten.
    """
    for key, value in tree.items():
        if key == "Threads":
            # Navigiere durch die Threads
            for thread_title, thread_data in value.items():
                # Prüfe, ob der Thread Posts enthält
                if "Posts" in thread_data:
                    for post in thread_data["Posts"]:
                        # Suche in PostText, Title und QuoteText
                        post_text = post.get("PostText", "").lower()
                        title = post.get("Title", "").lower()
                        quote_text = post.get("QuoteText", "").lower()
                        if any(word in post_text or word in title or word in quote_text for word in search_words):
                            matching_posts.append(post)
        else:
            # Rekursiv durch die Unterknoten navigieren
            search_in_tree(value, search_words, matching_posts)

def search_tree(input_file, output_file, search_words):
    """
    Durchsucht den Baum in post_tree.json nach Threads oder Posts,
    die die Suchbegriffe enthalten.
    """
    with open(input_file, 'r', encoding='utf-8') as file:
        post_tree = json.load(file)

    search_words = [word.lower() for word in search_words]  # Suchbegriffe in Kleinbuchstaben umwandeln
    matching_posts = []

    # Suche im Baum
    search_in_tree(post_tree, search_words, matching_posts)

    # Ergebnisse speichern
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(matching_posts, file, ensure_ascii=False, indent=4)

    print(f"Posts containing the search words have been written to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Search the post tree for specific keywords and write matching posts to a new file.')
    parser.add_argument('input_file', type=str, help='The input JSON file containing the post tree.')
    parser.add_argument('output_file', type=str, help='The output JSON file to write matching posts to.')
    parser.add_argument('search_words', type=str, nargs='+', help='The keywords to search for in the posts.')

    args = parser.parse_args()
    
    search_tree(args.input_file, args.output_file, args.search_words)