import json
import os

def generate_markdown_files(repo_index_file, categories_dir):
    """Generates markdown files for each category based on repo data and category lists."""

    # Load repo data from JSON
    with open(repo_index_file, 'r') as f:
        repo_data = json.load(f)

    # Create a dictionary to store repos by category
    repos_by_category = {}

    # Create sections directory if it doesn't exist
    sections_dir = 'sections'
    if not os.path.exists(sections_dir):
        os.makedirs(sections_dir)

    # Iterate through category files
    for filename in os.listdir(categories_dir):
        if filename.endswith('.txt'):
            category_name = filename[:-4]  # Remove '.txt' extension
            category_file = os.path.join(categories_dir, filename)

            # Read repo names from category file
            with open(category_file, 'r') as f:
                repo_names = [line.strip() for line in f]

            # Find repos in repo_data that match the names in the category file
            category_repos = [repo for repo in repo_data if repo['name'] in repo_names]

            repos_by_category[category_name] = category_repos

    # Generate markdown files for each category
    for category_name, repos in repos_by_category.items():
        markdown_file = os.path.join(sections_dir, f'{category_name}.md')
        with open(markdown_file, 'w') as f:
            f.write(f'# {category_name.capitalize()} Repositories\n\n')
            for repo in repos:
                f.write(f'## [{repo["pretty_name"]}]({repo["url"]})\n')
                f.write(f'{repo["description"]}\n\n')

    print("Markdown files generated successfully.")


if __name__ == '__main__':
    repo_index_file = 'repo-index.json'
    categories_dir = 'lists/categories'
    generate_markdown_files(repo_index_file, categories_dir)