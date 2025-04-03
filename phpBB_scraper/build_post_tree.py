import json
import os

def build_post_tree(input_file, output_file):
    """
    Liest die posts-sorted.json und erstellt einen verschachtelten Baum der Posts.
    Speichert das Ergebnis als JSON-Datei im data-Verzeichnis.
    """
    if not os.path.exists(input_file):
        print(f"Input file {input_file} does not exist.")
        return

    # Baumstruktur initialisieren
    post_tree = {}

    # posts-sorted.json laden
    with open(input_file, 'r', encoding='utf-8') as infile:
        posts = json.load(infile)

    # Posts in den Baum einfügen
    for post in posts:
        forum_path = post.get("Forum", "").split(" / ")  # Forum-Pfad splitten
        current_node = post_tree

        # Baumstruktur entlang des Forum-Pfads erstellen
        for level in forum_path:
            if level not in current_node:
                current_node[level] = {"Threads": {}}
            current_node = current_node[level]["Threads"]

        # Thread hinzufügen
        thread_title = post.get("Title", "Unknown Thread")
        if thread_title not in current_node:
            current_node[thread_title] = {"Posts": []}

        # Post hinzufügen, wenn er noch nicht existiert
        existing_posts = current_node[thread_title]["Posts"]
        if post not in existing_posts:
            existing_posts.append(post)

    # Validierung der Baumstruktur
    validate_tree_structure(post_tree)

    # Baum als JSON speichern
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as outfile:
        json.dump(post_tree, outfile, ensure_ascii=False, indent=4)

    print(f"Post tree has been saved to {output_file}")

def validate_tree_structure(tree):
    """
    Validiert die Struktur des Baums und gibt Warnungen für unerwartete Werte aus.
    """
    if isinstance(tree, dict):
        for key, value in tree.items():
            if not isinstance(value, dict):
                print(f"Warning: Unexpected value for key '{key}': {value}")
            elif "Threads" in value and not isinstance(value["Threads"], dict):
                print(f"Warning: 'Threads' for key '{key}' is not a dictionary.")
            elif "Posts" in value and not isinstance(value["Posts"], list):
                print(f"Warning: 'Posts' for key '{key}' is not a list.")
            else:
                validate_tree_structure(value)
    elif isinstance(tree, list):
        for item in tree:
            validate_tree_structure(item)

if __name__ == "__main__":
    input_file = './build/posts-sorted.json'
    output_file = './data/post_tree.json'
    build_post_tree(input_file, output_file)