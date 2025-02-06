import json
import argparse

def json_to_text(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        posts = json.load(file)

    with open(output_file, 'w', encoding='utf-8') as file:
        for post in posts:
            file.write(f"Username: {post.get('Username', '')}\n")
            file.write(f"URL: {post.get('URL', '')}\n")
            file.write(f"Title: {post.get('Title', '')}\n")
            file.write(f"Forum: {post.get('Forum', '')}\n")
            file.write(f"PostTime: {post.get('PostTime', '')}\n")
            file.write(f"PostText:\n{post.get('PostText', '')}\n")
            file.write(f"QuoteText:\n{post.get('QuoteText', '')}\n")
            file.write('\n' + '-'*80 + '\n\n')  # Add a separator between posts

    print(f"All posts have been written to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='''Convert JSON posts to a text file.
        The input JSON file should contain an array of posts.
        Each post will be written to the output text file in a readable format.''',
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument('input_file', type=str, help='The input JSON file containing posts.')
    parser.add_argument('output_file', type=str, help='The output text file to write posts to.')
    
    args = parser.parse_args()
    
    json_to_text(args.input_file, args.output_file)