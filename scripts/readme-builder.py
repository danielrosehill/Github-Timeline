import os
from datetime import datetime
import math

# Get the project root directory (parent of scripts directory)
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def generate_readme():
    """Generate a simplified README with links to timeline and section indexes."""
    
    # Get list of section files
    sections_dir = os.path.join(project_root, 'sections')
    section_files = sorted([f[:-3] for f in os.listdir(sections_dir) if f.endswith('.md')])
    
    # Generate section badges in a proper markdown table
    # 2 columns for better readability
    section_table = ['| Category | Category |', '|----------|----------|']  # Restored header for proper table formatting
    
    # Calculate rows needed for 2 columns
    rows = math.ceil(len(section_files) / 2)
    
    for i in range(0, rows):
        row = []
        # First column
        display_name = section_files[i].replace('-', ' ').title()
        badge = f'[![{display_name}](https://img.shields.io/badge/{display_name.replace(" ", "_")}-2ea44f?style=for-the-badge&logo=github)](sections/{section_files[i]}.md)'
        row.append(badge)
        
        # Second column
        second_idx = i + rows
        if second_idx < len(section_files):
            display_name = section_files[second_idx].replace('-', ' ').title()
            badge = f'[![{display_name}](https://img.shields.io/badge/{display_name.replace(" ", "_")}-2ea44f?style=for-the-badge&logo=github)](sections/{section_files[second_idx]}.md)'
            row.append(badge)
        else:
            row.append('')  # Empty cell for last row if odd number
            
        section_table.append(f'| {row[0]} | {row[1]} |')

    # Get current timestamp
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Generate README content
    readme_content = f"""# Daniel Rosehill Github Repository Index

![Banner](banners/index.png)

*Last updated: {timestamp}*

This is an automatically generated index of my public GitHub repositories.

## Repository Views

This index provides two ways to explore my GitHub repositories:

### 1. Chronological Timeline
[![View Timeline](https://img.shields.io/badge/Timeline-blue?style=for-the-badge&logo=github)](timeline.md)

The timeline provides a chronological view of all repositories, showing when each project was created and its current status. This is useful for seeing how my work and interests have evolved over time.

### 2. Category Index
The category index organizes repositories by their primary function or topic. Each category below contains a curated list of related projects:

{chr(10).join(section_table)}

## Data Exports
For programmatic access to this repository data:
- [Repository Index (JSON)](data/exports/repo-index.json)
- [Repository Index (CSV)](data/exports/repo-index.csv)"""

    # Write to README.md
    with open(os.path.join(project_root, 'README.md'), 'w') as f:
        f.write(readme_content)

if __name__ == '__main__':
    generate_readme()