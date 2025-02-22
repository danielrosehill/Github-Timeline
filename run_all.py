import importlib.util
import sys

def import_from_file(file_path):
    spec = importlib.util.spec_from_file_location("module", file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["module"] = module
    spec.loader.exec_module(module)
    return module

def run_all():
    print("Starting GitHub Timeline generation...")
    
    print("\n1. Fetching repository list...")
    repo_fetcher = import_from_file("scripts/repo-fetcher.py")
    repo_fetcher.fetch_repos()
    
    print("\n2. Generating repo-index.json...")
    json_creator = import_from_file("scripts/json-creator.py")
    timeline_data = json_creator.generate_timeline_json()
    if timeline_data:
        json_creator.save_timeline_json(timeline_data)
    
    print("\n3. Generating repo-index.csv...")
    csv_creator = import_from_file("scripts/csv-creator.py")
    timeline_data = csv_creator.generate_timeline_csv()
    if timeline_data:
        csv_creator.save_timeline_csv(timeline_data)

    print("\n4. Generating chronological timeline...")
    timeline_generator = import_from_file("scripts/timeline_generator.py")
    timeline_generator.generate_timeline()

    print("\n5. Generating category markdown files...")
    markdown_generator = import_from_file("scripts/markdown_generator.py")
    markdown_generator.generate_markdown_files('data/exports/repo-index.json', 'lists/categories')
    
    print("\n6. Generating README.md...")
    readme_builder = import_from_file("scripts/readme-builder.py")
    readme_builder.generate_readme()
    
    print("\nAll operations completed!")

if __name__ == "__main__":
    run_all()