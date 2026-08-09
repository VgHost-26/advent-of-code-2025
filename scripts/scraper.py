import os
import requests
import sys
from datetime import datetime

# Configuration
YEAR = 2025
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_FILE = os.path.join(ROOT_DIR, '.env')

def get_session_cookie():
    """Reads the session cookie from the .env file."""
    if not os.path.exists(ENV_FILE):
        return None
    
    with open(ENV_FILE, 'r') as f:
        for line in f:
            if line.strip().startswith('AOC_SESSION='):
                return line.strip().split('=', 1)[1]
    return None

def fetch_input(day):
    """Fetches the input for the given day."""
    session = get_session_cookie()
    if not session:
        print("Error: AOC_SESSION not found in .env file. Cannot fetch input.")
        return False

    url = f"https://adventofcode.com/{YEAR}/day/{day}/input"
    cookies = {'session': session}
    headers = {'User-Agent': 'github.com/google-deepmind/antigravity by antigravity@google.com'}

    try:
        response = requests.get(url, cookies=cookies, headers=headers)
        response.raise_for_status()
        
        inputs_dir = os.path.join(ROOT_DIR, 'inputs')
        if not os.path.exists(inputs_dir):
            os.makedirs(inputs_dir)
            
        output_file = os.path.join(inputs_dir, f"day{day:02d}.txt")
        with open(output_file, 'w') as f:
            f.write(response.text)
        
        print(f"Successfully downloaded input to {output_file}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error fetching input: {e}")
        return False

def fetch_task_info(day):
    """Fetches the puzzle title and description for the given day."""
    session = get_session_cookie()
    # Note: Task description is public, but getting the personalized part (part 2) might need session.
    # For now, we'll use session if available, but it's not strictly required for part 1 text.
    
    url = f"https://adventofcode.com/{YEAR}/day/{day}"
    cookies = {'session': session} if session else {}
    headers = {'User-Agent': 'github.com/google-deepmind/antigravity by antigravity@google.com'}

    try:
        response = requests.get(url, cookies=cookies, headers=headers)
        response.raise_for_status()
        
        # Simple parsing to extract the article content
        # We want the <article class="day-desc"> content
        from html.parser import HTMLParser

        class AoCHTMLParser(HTMLParser):
            def __init__(self):
                super().__init__()
                self.recording = False
                self.content = []
                self.title = ""
                self.in_title = False

            def handle_starttag(self, tag, attrs):
                if tag == 'article':
                    for name, value in attrs:
                        if name == 'class' and 'day-desc' in value:
                            self.recording = True
                
                if self.recording:
                    # Reconstruct the tag
                    attrs_str = "".join([f' {k}="{v}"' for k, v in attrs])
                    self.content.append(f"<{tag}{attrs_str}>")
                    
                    if tag == 'h2':
                        self.in_title = True

            def handle_endtag(self, tag):
                if self.recording:
                    self.content.append(f"</{tag}>")
                
                if tag == 'article':
                    self.recording = False
                if tag == 'h2':
                    self.in_title = False

            def handle_data(self, data):
                if self.recording:
                    self.content.append(data)
                if self.in_title:
                    self.title += data

        parser = AoCHTMLParser()
        parser.feed(response.text)
        
        # Clean up title (remove "--- Day X: " and " ---")
        clean_title = parser.title.replace(f"--- Day {day}: ", "").replace(" ---", "").strip()
        
        return {
            "title": clean_title,
            "html": "".join(parser.content)
        }

    except requests.exceptions.RequestException as e:
        print(f"Error fetching task info: {e}")
        return None
