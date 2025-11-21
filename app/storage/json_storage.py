from __future__ import annotations

import json
from pathlib import Path
from typing import List

from app.models.mood import MoodEntry

# project_root / data / moods.json
DATA_FILE = Path(__file__).resolve().parents[2] / "data" / "moods.json"


def load_moods() -> List[MoodEntry]:
    """Load mood entries from the JSON file.

    Returns an empty list if the file doesn't exist or is invalid.
    """
    if not DATA_FILE.exists():
        return []

    try:
        with DATA_FILE.open("r", encoding="utf-8") as f:
            raw = json.load(f)
    except (json.JSONDecodeError, OSError):
        return []

    if not isinstance(raw, list):
        return []

    entries: list[MoodEntry] = []
    for item in raw:
        try:
            entries.append(MoodEntry.from_dict(item))
        except (KeyError, TypeError, ValueError):
            # Skip malformed rows instead of crashing the app
            continue

    return entries


def save_moods(entries: List[MoodEntry]) -> None:
    """Save mood entries to the JSON file."""
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    raw = [entry.to_dict() for entry in entries]

    with DATA_FILE.open("w", encoding="utf-8") as f:
        json.dump(raw, f, indent=2)
