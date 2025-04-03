import argparse

def split_text(input_file, output_prefix, max_lines):
    """
    Splittet eine Textdatei in mehrere Dateien, ohne Threads zu unterbrechen.
    Threads werden anhand von 'Thread:' erkannt.
    """
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    current_lines = []
    file_index = 1
    current_line_count = 0

    for line in lines:
        # Prüfen, ob ein neuer Thread beginnt
        if line.startswith("Thread:") and current_line_count + len(current_lines) > max_lines:
            # Speichere die aktuelle Datei und starte eine neue
            output_file = f"{output_prefix}_{file_index}.txt"
            with open(output_file, 'w', encoding='utf-8') as outfile:
                outfile.writelines(current_lines)
            print(f"Saved {output_file} with {len(current_lines)} lines")
            file_index += 1
            current_lines = []
            current_line_count = 0

        # Füge die aktuelle Zeile hinzu
        current_lines.append(line)
        current_line_count += 1

    # Speichere die letzte Datei, falls noch Zeilen übrig sind
    if current_lines:
        output_file = f"{output_prefix}_{file_index}.txt"
        with open(output_file, 'w', encoding='utf-8') as outfile:
            outfile.writelines(current_lines)
        print(f"Saved {output_file} with {len(current_lines)} lines")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Split text file into multiple files without breaking threads.')
    parser.add_argument('input_file', type=str, help='The input text file to split.')
    parser.add_argument('output_prefix', type=str, help='The prefix for the output files.')
    parser.add_argument('max_lines', type=int, help='The maximum number of lines per output file.')

    args = parser.parse_args()
    
    split_text(args.input_file, args.output_prefix, args.max_lines)