import json
from datetime import datetime
import os

def generate_timeline():
    # Read the JSON data
    with open('data/exports/repo-index.json', 'r', encoding='utf-8') as f:
        repos = json.load(f)

    # Group repositories by year and date
    timeline = {}
    for repo in repos:
        created_at = datetime.strptime(repo['created_at'], '%Y-%m-%dT%H:%M:%SZ')
        year = created_at.year
        date_key = created_at.strftime('%-d %b')  # e.g., "22 Feb"
        
        if year not in timeline:
            timeline[year] = {}
        if date_key not in timeline[year]:
            timeline[year][date_key] = []
            
        timeline[year][date_key].append(repo)

    # Generate markdown content
    markdown_content = "# GitHub Repository Timeline\n\n"
    
    # Process years in reverse chronological order
    for year in sorted(timeline.keys(), reverse=True):
        markdown_content += f"# {year}\n\n"
        
        # Process dates in reverse chronological order for each year
        for date in sorted(timeline[year].keys(), reverse=True, 
                         key=lambda x: datetime.strptime(x, '%d %b')):
            markdown_content += f"## {date}\n\n"
            
            # Add repositories for this date
            for repo in timeline[year][date]:
                name = repo['pretty_name']
                desc = repo['description']
                url = repo['url']
                is_fork = repo['is_fork']
                
                markdown_content += f"**{name}**\n\n"
                markdown_content += f"{desc}\n\n"
                if is_fork:
                    markdown_content += "🔱 *This is a fork*\n\n"
                markdown_content += f"[![GitHub Repository]"
                markdown_content += f"(https://img.shields.io/badge/GitHub-Repository-blue)]"
                markdown_content += f"({url})\n\n"

    # Save the timeline
    with open('timeline.md', 'w', encoding='utf-8') as f:
        f.write(markdown_content)

if __name__ == "__main__":
    generate_timeline()