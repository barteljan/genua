from fpdf import FPDF
import argparse

def text_to_pdf(input_file, output_file):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Verwenden Sie eine Unicode-kompatible Schriftart
    pdf.add_font("NotoSans", "", "./fonts/NotoSans-Regular.ttf", uni=True)
    pdf.set_font("NotoSans", size=12)

    print(f"start converting {input_file} to {output_file}")

    with open(input_file, 'r', encoding='utf-8') as file:
        for line in file:
            # Verwende multi_cell, um Zeilenumbrüche innerhalb der Seite zu ermöglichen
            pdf.multi_cell(0, 10, txt=line.strip())

    pdf.output(output_file)
    print(f"PDF saved as {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert a text file to a PDF.")
    parser.add_argument("input_file", type=str, help="Path to the input text file.")
    parser.add_argument("output_file", type=str, help="Path to the output PDF file.")
    args = parser.parse_args()

    text_to_pdf(args.input_file, args.output_file)