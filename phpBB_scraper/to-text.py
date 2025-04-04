import json
import argparse
import textwrap

def write_post_to_text(post, file, line_length):
    """
    Schreibt alle Eigenschaften eines einzelnen Posts in die Textdatei.
    Jede Eigenschaft wird untereinander dargestellt, mit ihrem Namen gefolgt von einem Doppelpunkt.
    Fügt am Anfang jedes Posts eine Linie aus '_' ein, die so lang ist wie die line_length.
    """
    # Linie aus '_' einfügen
    file.write("_" * line_length + "\n")
    
    # Schreibe alle Eigenschaften des Posts
    for key, value in post.items():
        if isinstance(value, str):
            # Brich lange Texte um und berücksichtige Zeilenumbrüche
            wrapped_value = wrap_text(value, line_length)
            file.write(f"{key}: {wrapped_value}\n")
        else:
            # Schreibe andere Datentypen direkt
            file.write(f"{key}: {value}\n")
    file.write("\n")  # Leerzeile zwischen Posts

def write_tree_to_text(tree, file, line_length):
    """
    Rekursive Funktion, um den Baum in eine Textdatei zu schreiben.
    Die Hierarchie des Baums wird durch Überschriften dargestellt.
    Der Titel des Threads wird einmal über alle Posts des Threads geschrieben.
    """
    if isinstance(tree, dict):
        for key, value in tree.items():
            if isinstance(value, dict) and "Posts" in value:
                # Schreibe den Thread-Titel
                file.write(f"\nThread: {key}\n")
                file.write("=" * line_length + "\n")  # Linie zur Abgrenzung
                for post in value["Posts"]:
                    write_post_to_text(post, file, line_length)
            elif isinstance(value, list):
                for post in value:
                    write_post_to_text(post, file, line_length)
            elif isinstance(value, dict):
                # Rekursiv durch andere Unterknoten navigieren
                write_tree_to_text(value, file, line_length)
            else:
                # Unerwarteter Wert, Exception auslösen
                raise ValueError(f"Unexpected value for key '{key}': {value}")
    elif isinstance(tree, list):
        for post in tree:
            write_post_to_text(post, file, line_length)
    else:
        # Unerwarteter Typ, Exception auslösen
        raise TypeError(f"Unexpected tree structure: {tree}")

def wrap_text(text, line_length):
    """
    Bricht den Text nach der angegebenen Länge um und berücksichtigt vorhandene Zeilenumbrüche.
    """
    lines = text.split("\n")  # Text anhand von \n in Zeilen aufteilen
    wrapped_lines = [textwrap.fill(line, width=line_length) for line in lines]
    return "\n".join(wrapped_lines)

def convert_tree_to_text(input_file, output_file, line_length):
    """
    Konvertiert einen Baum aus einer JSON-Datei in eine Textdatei.
    """
    with open(input_file, 'r', encoding='utf-8') as infile:
        post_tree = json.load(infile)

    with open(output_file, 'w', encoding='utf-8') as outfile:
        write_tree_to_text(post_tree, outfile, line_length)

    print(f"Tree has been converted to text and saved to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert a post tree JSON file to a structured text file.")
    parser.add_argument("input_file", type=str, help="The input JSON file containing the post tree.")
    parser.add_argument("output_file", type=str, help="The output text file to write the tree to.")
    parser.add_argument("--line-length", type=int, default=75, help="The maximum line length for wrapping text.")
    args = parser.parse_args()

    convert_tree_to_text(args.input_file, args.output_file, args.line_length)