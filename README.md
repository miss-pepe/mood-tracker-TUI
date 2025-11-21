# Terminal Mood Tracker TUI

A small Textual-powered terminal app to log how you're feeling, add optional tags/notes, and review recent trends without leaving the shell.

## Features
- Log a 1-10 mood rating with optional tag and note.
- See the five most recent entries on the home screen.
- Navigate to the trends screen for an ASCII sparkline and a history table of recent moods.
- Data is persisted to `data/moods.json` so entries survive restarts.

## Getting started
1. Create and activate a virtual environment (optional):
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the app:
   ```bash
   python -m app.main
   ```

## Controls
- `n` — Focus the rating field to log a new mood.
- `g` — Open the trends/history view.
- `q` — Quit the app.
- On the trends screen: `b` to go back, `r` to refresh data.

## Data location
Entries are stored as JSON at `data/moods.json` (created on first save). Delete that file if you want to wipe your log.
