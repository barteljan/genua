import os

def is_valid_character(char):
    """
    Prüft, ob ein Zeichen druckbar ist und innerhalb des unterstützten Unicode-Bereichs liegt.
    """
    return char.isprintable() and ord(char) <= 65535

def clean_text_file(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        for line in infile:
            # Ersetze problematische Zeichen durch '?'
            cleaned_line = ''.join(char if is_valid_character(char) else '?' for char in line)
            outfile.write(cleaned_line)

    print(f"Cleaned file saved as {output_file}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Clean a text file by removing problematic characters.")
    parser.add_argument("input_file", type=str, help="Path to the input text file.")
    parser.add_argument("output_file", type=str, help="Path to the output cleaned text file.")
    args = parser.parse_args()

    clean_text_file(args.input_file, args.output_file)