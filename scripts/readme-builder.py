import os
from datetime import datetime

# Get the project root directory (parent of scripts directory)
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def generate_readme():
    """Generate a simplified README with links to timeline and section indexes."""
    
    # Get list of section files
    sections_dir = os.path.join(project_root, 'sections')
    section_files = sorted([f[:-3] for f in os.listdir(sections_dir) if f.endswith('.md')])
    
    # Generate section links
    section_links = []
    for section in section_files:
        # Convert filename to display name
        display_name = section.replace('-', ' ').title()
        section_links.append(f'- [{display_name}](sections/{section}.md)')

    # Get current timestamp
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Generate README content
    readme_content = f"""# Daniel Rosehill Github Repository Index

![Banner](banners/index.png)

{open(os.path.join(project_root, 'timeline.md')).read()}

*Last updated: {timestamp}*

This is an automatically generated index of my public GitHub repositories.

## Quick Links

[![View Timeline](https://img.shields.io/badge/View-Timeline-blue?style=for-the-badge)](timeline.md)

### Data Exports
- [Repository Index (JSON)](data/exports/repo-index.json)
- [Repository Index (CSV)](data/exports/repo-index.csv)

## Repository Categories

{chr(10).join(section_links)}"""

    # Write to README.md
    with open(os.path.join(project_root, 'README.md'), 'w') as f:
        f.write(readme_content)

if __name__ == '__main__':
    generate_readme()