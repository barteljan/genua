import json

def count_posts_in_tree(tree):
    """
    Rekursive Funktion, um die Anzahl der Posts im Baum zu zählen.
    """
    post_count = 0

    if isinstance(tree, dict):
        for key, value in tree.items():
            if key == "Posts" and isinstance(value, list):
                post_count += len(value)
            else:
                post_count += count_posts_in_tree(value)
    elif isinstance(tree, list):
        for item in tree:
            post_count += count_posts_in_tree(item)

    return post_count

def main():
    input_file = "../data/post_tree.json"  # Pfad zur post_tree.json
    with open(input_file, 'r', encoding='utf-8') as file:
        post_tree = json.load(file)

    total_posts = count_posts_in_tree(post_tree)
    print(f"Total number of posts in the tree: {total_posts}")

if __name__ == "__main__":
    main()