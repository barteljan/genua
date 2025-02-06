import json

# Load the JSON data from the file
with open('../build/posts.json', 'r', encoding='utf-8') as file:
    posts = json.load(file)

# Sort the posts first by 'Forum' and then by 'URL'
sorted_posts = sorted(posts, key=lambda x: (x['Forum'], x['URL']))

# Save the sorted JSON data back to the file
with open('../build/posts-sorted.json', 'w', encoding='utf-8') as file:
    json.dump(sorted_posts, file, ensure_ascii=False, indent=4)

print("Posts have been sorted and saved to posts-sorted.json")