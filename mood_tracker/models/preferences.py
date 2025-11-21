from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
import json
from typing import Any

from .storage import DATA_PATH

PREFERENCES_FILE = DATA_PATH / "preferences.json"


@dataclass
class UserPreferences:
    """Stores user preferences that persist between sessions."""
    current_theme: str = "midnight"
    last_selected_mood_index: int = 2  # Default to "Meh"
    show_history_panel: bool = True
    
    def to_dict(self) -> dict[str, Any]:
        """Convert preferences to dictionary for JSON serialization."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> UserPreferences:
        """Create preferences from dictionary loaded from JSON."""
        return cls(**data)


def load_preferences() -> UserPreferences:
    """Load user preferences from disk, or return defaults if file doesn't exist."""
    if not PREFERENCES_FILE.exists():
        return UserPreferences()
    
    try:
        data = json.loads(PREFERENCES_FILE.read_text(encoding="utf-8"))
        return UserPreferences.from_dict(data)
    except (json.JSONDecodeError, TypeError, KeyError):
        # If the file is corrupted, return defaults
        return UserPreferences()


def save_preferences(prefs: UserPreferences) -> None:
    """Save user preferences to disk."""
    DATA_PATH.mkdir(parents=True, exist_ok=True)
    PREFERENCES_FILE.write_text(
        json.dumps(prefs.to_dict(), indent=2),
        encoding="utf-8"
    )