def check_file_for_unicode_issues(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        for line_number, line in enumerate(file, start=1):
            for char in line:
                try:
                    char.encode('latin-1')  # Simulate encoding to a limited charset
                except UnicodeEncodeError:
                    print(f"Problematic character '{char}' found on line {line_number}: {repr(char)}")

if __name__ == "__main__":
    file_path = "./build/Nicolo_Trevisan_user.txt"
    check_file_for_unicode_issues(file_path)