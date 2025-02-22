import os
import csv
import requests
from dotenv import load_dotenv
from datetime import datetime

def generate_timeline_csv():
    load_dotenv()
    github_token = os.getenv("GITHUB_PAT")
    if not github_token:
        print("Error: GITHUB_PAT not found in .env file")
        return None

    username = "danielrosehill"  # Replace with your GitHub username

    # Dictionary for expanding abbreviations
    abbreviations = {
        "HA": "Home Assistant",
        "LLM": "Large Language Model",
        "GPT": "Generative Pre-trained Transformer",
        "AI": "Artificial Intelligence",
        "STT": "Speech to Text",
        "TTS": "Text to Speech",
        "RAG": "Retrieval Augmented Generation",
    }

    def prettify_repo_name(name):
        # Split by hyphens and process each word
        words = name.split('-')
        processed_words = []
        
        for word in words:
            # Check if the word is an abbreviation that needs expansion
            if word.upper() in abbreviations:
                processed_words.append(abbreviations[word.upper()])
            else:
                # Capitalize the word
                processed_words.append(word.capitalize())
        
        return ' '.join(processed_words)

    # Function to fetch all repositories with pagination
    def get_all_repos(username, token):
        repos = []
        page = 1
        while True:
            url = f"https://api.github.com/users/{username}/repos?sort=created&direction=desc&page={page}"
            headers = {"Authorization": f"token {token}"}
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                new_repos = response.json()
                if not new_repos:
                    break  # No more repos to fetch
                repos.extend(new_repos)
                page += 1
            else:
                print(f"Error fetching repos: {response.status_code}")
                return None
        return repos

    # Fetch all current repositories
    all_repos = get_all_repos(username, github_token)
    if not all_repos:
        return None

    # Process repositories into a list of dictionaries
    timeline_data = []

    for repo in all_repos:
        if repo["private"]:
            continue

        repo_entry = {
            "name": repo["name"],
            "pretty_name": prettify_repo_name(repo["name"]),
            "description": repo["description"] or "No description provided",
            "url": repo["html_url"],
            "is_fork": repo["fork"],
            "created_at": repo["created_at"]
        }

        timeline_data.append(repo_entry)

    return timeline_data

def save_timeline_csv(timeline_data, output_file="data/exports/repo-index.csv"):
    """Save the timeline data to a CSV file"""
    if timeline_data:
        # Define the field names for the CSV
        fieldnames = ["name", "pretty_name", "description", "url", "is_fork", "created_at"]
        
        # Ensure the directory exists
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()  # Write the header row
            writer.writerows(timeline_data)  # Write all the data rows
        print(f"Timeline data saved to {output_file}")
    else:
        print("No timeline data to save")

if __name__ == "__main__":
    timeline_data = generate_timeline_csv()
    if timeline_data:
        save_timeline_csv(timeline_data)