import os
import requests
from dotenv import load_dotenv

def fetch_repos():
    load_dotenv()
    token = os.getenv('GITHUB_PAT')
    
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    url = 'https://api.github.com/user/repos'
    params = {
        'visibility': 'public',
        'per_page': 100,
        'affiliation': 'owner'
    }
    
    repos = []
    page = 1
    
    while True:
        params['page'] = page
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code != 200:
            print(f"Error fetching repos: {response.status_code}")
            return
            
        page_repos = response.json()
        if not page_repos:
            break
            
        repos.extend((repo['name'], repo['fork']) for repo in page_repos)
        page += 1
    
    # Write repos to file
    os.makedirs('data', exist_ok=True)
    os.makedirs('lists/categories', exist_ok=True)
    
    # Write all repos to repos.txt
    with open('data/repos.txt', 'w') as f:
        for repo, _ in sorted(repos):
            f.write(f"{repo}\n")
    
    # Write fork repos to forks.txt
    with open('lists/categories/forks.txt', 'w') as f:
        for repo, is_fork in sorted(repos):
            if is_fork:
                f.write(f"{repo}\n")

if __name__ == "__main__":
    fetch_repos()