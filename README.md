# Advent of Code 2025

This repository contains my solutions for [Advent of Code 2025](https://adventofcode.com/2025), along with a progress dashboard and automation scripts.

## Setup

1.  **Python Environment**:
    Create and activate a virtual environment:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```

2.  **Session Cookie**:
    To fetch puzzle inputs and task descriptions automatically, you need your AoC session cookie.
    *   Copy `.env.template` to `.env`.
    *   Log in to Advent of Code in your browser.
    *   Get the `session` cookie value from your browser's developer tools.
    *   Paste it into `.env`: `AOC_SESSION=your_cookie_here`.

3.  **Dashboard**:
    Install Node.js dependencies for the dashboard:
    ```bash
    cd dashboard
    npm install
    ```

## Usage

### Automation Scripts

The `scripts/` directory contains tools to automate your workflow. Run these from the project root using your virtual environment.

*   **Start a New Day**:
    Scaffolds the directory structure for Python, Go, and C++, downloads the input file, and fetches the task description.
    ```bash
    python3 scripts/scaffold.py <day_number>
    # Example: python3 scripts/scaffold.py 1
    ```

*   **Update Progress & Task Info**:
    Scans your solution files to update progress status and refetches task descriptions (useful if you've unlocked Part Two).
    ```bash
    python3 scripts/update_progress.py
    ```

### Dashboard

To view your progress and the puzzle descriptions in a nice interface:

```bash
cd dashboard
npm run dev
```

Open the link provided (usually `http://localhost:5173`) in your browser. The dashboard shows which days you've started or completed. Click on a day to see the puzzle description.

## Directory Structure

*   `python/`, `go/`, `cpp/`: Solution files organized by day.
*   `inputs/`: Puzzle input files (ignored by git).
*   `dashboard/`: React application for tracking progress.
*   `scripts/`: Python automation scripts.
