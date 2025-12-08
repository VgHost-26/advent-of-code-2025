import os
import json
import scraper

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LANGUAGES = ['python', 'go', 'cpp']

def parse_solution(file_path, lang):
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    content = "".join(lines)
    highlight_ranges = []
    
    start_marker = "# % start" if lang == "python" else "// % start"
    end_marker = "# % end" if lang == "python" else "// % end"
    
    current_start = -1
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        if start_marker in stripped:
            current_start = i + 1 # Start highlighting after the marker
        elif end_marker in stripped and current_start != -1:
            highlight_ranges.append([current_start, i]) # End before the marker
            current_start = -1
            
    return {
        "content": content,
        "highlight_ranges": highlight_ranges
    }

def scan_progress():
    # Load existing progress to preserve manual edits if any (though we overwrite mostly)
    dashboard_data_dir = os.path.join(ROOT_DIR, 'dashboard', 'src', 'data')
    progress_file = os.path.join(dashboard_data_dir, 'progress.json')
    existing_progress = {}
    if os.path.exists(progress_file):
        try:
            with open(progress_file, 'r') as f:
                existing_progress = json.load(f)
        except json.JSONDecodeError:
            pass

    progress = {}
    
    for day in range(1, 13):
        day_str = f"day{day:02d}"
        day_key = str(day)
        
        # Start with existing data or default
        day_data = existing_progress.get(day_key, {
            "day": day,
            "status": "not_started",
            "languages": [],
            "solutions": {}
        })
        
        # Reset status and languages to re-scan filesystem (source of truth for code)
        day_data["languages"] = []
        day_data["status"] = "not_started"
        day_data["solutions"] = {} 
        
        started = False
        
        for lang in LANGUAGES:
            lang_dir = os.path.join(ROOT_DIR, lang, day_str)
            if os.path.exists(lang_dir):
                # Check if solution file exists
                ext = 'py' if lang == 'python' else 'go' if lang == 'go' else 'cpp'
                sol_file = os.path.join(lang_dir, f"solution.{ext}")
                if os.path.exists(sol_file):
                    day_data["languages"].append(lang)
                    day_data["solutions"][lang] = parse_solution(sol_file, lang)
                    started = True
        
        if started:
            day_data["status"] = "in_progress"
            
        # Fetch task info if missing (or if we want to update it)
        # We check if 'html' is present. If not, we try to fetch it.
        # We can also fetch it if status is started to ensure we get part 2 if available.
        # Logic: If no HTML, fetch. If started and "Part Two" is not in HTML, fetch (to see if it appeared).
        current_html = day_data.get("html")
        should_fetch = False
        
        if not current_html:
            should_fetch = True
        elif started and "Part Two" not in str(current_html):
            should_fetch = True
            
        if should_fetch:
            print(f"Fetching task info for day {day}...")
            info = scraper.fetch_task_info(day)
            if info:
                day_data["title"] = info["title"]
                day_data["html"] = info["html"]
            
        progress[day] = day_data

    return progress

def update_dashboard_data(data):
    dashboard_data_dir = os.path.join(ROOT_DIR, 'dashboard', 'src', 'data')
    if not os.path.exists(dashboard_data_dir):
        os.makedirs(dashboard_data_dir)
        
    output_file = os.path.join(dashboard_data_dir, 'progress.json')
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"Updated {output_file}")

if __name__ == "__main__":
    data = scan_progress()
    update_dashboard_data(data)
