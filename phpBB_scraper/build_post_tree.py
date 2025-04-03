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

    # Baum als JSON speichern
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as outfile:
        json.dump(post_tree, outfile, ensure_ascii=False, indent=4)

    print(f"Post tree has been saved to {output_file}")

if __name__ == "__main__":
    input_file = './build/posts-sorted.json'
    output_file = './data/post_tree.json'
    build_post_tree(input_file, output_file)