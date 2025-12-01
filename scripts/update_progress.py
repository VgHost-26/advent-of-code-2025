import os
import json

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LANGUAGES = ['python', 'go', 'cpp']

def scan_progress():
    progress = {}
    
    for day in range(1, 13):
        day_str = f"day{day:02d}"
        day_data = {
            "day": day,
            "status": "not_started",
            "languages": []
        }
        
        started = False
        completed = False # This is hard to determine automatically without running, but we can check for file existence
        
        for lang in LANGUAGES:
            lang_dir = os.path.join(ROOT_DIR, lang, day_str)
            if os.path.exists(lang_dir):
                # Check if solution file exists
                ext = 'py' if lang == 'python' else 'go' if lang == 'go' else 'cpp'
                sol_file = os.path.join(lang_dir, f"solution.{ext}")
                if os.path.exists(sol_file):
                    day_data["languages"].append(lang)
                    started = True
        
        if started:
            day_data["status"] = "in_progress"
            
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
