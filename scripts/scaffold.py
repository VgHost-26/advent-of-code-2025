import os
import sys
import shutil
import argparse
import scraper

# Configuration
LANGUAGES = ['python', 'go', 'cpp']
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def scaffold_day(day):
    day_str = f"day{day:02d}"
    print(f"Scaffolding {day_str}...")

    # Create input file
    inputs_dir = os.path.join(ROOT_DIR, 'inputs')
    input_file = os.path.join(inputs_dir, f"{day_str}.txt")
    if not os.path.exists(input_file):
        print(f"Fetching input for day {day}...")
        if scraper.fetch_input(day):
            print(f"Created {input_file}")
        else:
            # Fallback to creating empty file if scraping fails
            with open(input_file, 'w') as f:
                f.write("")
            print(f"Created empty input file {input_file} (Scraping failed)")
    else:
        print(f"Input file {input_file} already exists")

    # Create language directories
    for lang in LANGUAGES:
        lang_dir = os.path.join(ROOT_DIR, lang, day_str)
        if not os.path.exists(lang_dir):
            os.makedirs(lang_dir)
            print(f"Created directory {lang_dir}")
            
            # Copy template
            template_file = os.path.join(ROOT_DIR, lang, f"template.{'py' if lang == 'python' else 'go' if lang == 'go' else 'cpp'}")
            target_file = os.path.join(lang_dir, f"solution.{'py' if lang == 'python' else 'go' if lang == 'go' else 'cpp'}")
            
            if os.path.exists(template_file):
                shutil.copy(template_file, target_file)
                print(f"Copied template to {target_file}")
            else:
                print(f"Warning: Template not found at {template_file}")
        else:
            print(f"Directory {lang_dir} already exists")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scaffold Advent of Code day")
    parser.add_argument("day", type=int, help="Day number (1-12)")
    args = parser.parse_args()
    
    if 1 <= args.day <= 12:
        scaffold_day(args.day)
    else:
        print("Day must be between 1 and 12")
