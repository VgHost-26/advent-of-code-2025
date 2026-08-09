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
    # Load existing progress to preserve manual edits
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
    
    for day in range(1, 13): # Scan all days
        day_str = f"day{day:02d}"
        day_key = str(day)
        
        # Start with existing data or default
        # We preserve the ENTIRE existing object structure to keep manual edits
        day_data = existing_progress.get(day_key, {
            "day": day,
            "status": "not_started",
            "languages": [],
            "solutions": {}
        })
        
        # We will re-scan for content, but we want to KEEP the "completed" flags if they exist in solutions
        # And we want to KEEP the "status" of the day if it was manually set to something advanced like "completed"
        # However, we must ensure the "languages" list is up to date with actual files.
        
        found_languages = []
        started_any = False

        for lang in LANGUAGES:
            lang_dir = os.path.join(ROOT_DIR, lang, day_str)
            sol_file = None
            if os.path.exists(lang_dir):
                ext = 'py' if lang == 'python' else 'go' if lang == 'go' else 'cpp'
                candidate = os.path.join(lang_dir, f"solution.{ext}")
                if os.path.exists(candidate):
                    sol_file = candidate

            if sol_file:
                found_languages.append(lang)
                started_any = True
                
                # Re-parse content to get latest code/highlights
                new_parsed = parse_solution(sol_file, lang)
                
                # Merge with existing solution data to preserve 'completed' status
                existing_sol = day_data.get("solutions", {}).get(lang, {})
                merged_sol = {
                    "content": new_parsed["content"],
                    "highlight_ranges": new_parsed["highlight_ranges"],
                    "completed": existing_sol.get("completed", False) # Preserve or default to False
                }
                day_data["solutions"][lang] = merged_sol

        day_data["languages"] = found_languages
        
        # Update day status logic
        # 1. If currently "not_started" but files found -> "in_progress"
        # 2. If files NOT found -> "not_started" (downgrade if files deleted)
        # 3. If "part1_completed" or "completed" is set manually, we usually preserve it unless files are gone.
        
        if not started_any:
            day_data["status"] = "not_started"
        elif day_data["status"] == "not_started" and started_any:
            day_data["status"] = "in_progress"
            
        # Fetch task info if missing
        current_html = day_data.get("html")
        should_fetch = False
        
        if not current_html:
            should_fetch = True
        elif started_any and "Part Two" not in str(current_html):
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
