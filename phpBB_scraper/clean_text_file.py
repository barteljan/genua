import os

def clean_text_file(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        for line in infile:
            # Ersetze problematische Zeichen durch '?'
            cleaned_line = ''.join(char if char.isprintable() else '' for char in line)
            outfile.write(cleaned_line)

    print(f"Cleaned file saved as {output_file}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Clean a text file by removing problematic characters.")
    parser.add_argument("input_file", type=str, help="Path to the input text file.")
    parser.add_argument("output_file", type=str, help="Path to the output cleaned text file.")
    args = parser.parse_args()

    clean_text_file(args.input_file, args.output_file)