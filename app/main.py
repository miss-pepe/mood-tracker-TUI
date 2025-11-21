from __future__ import annotations

from typing import List

from textual.app import App

from app.ui.main_screen import MainScreen
from app.models.mood import MoodEntry
from app.storage.json_storage import load_moods, save_moods


class MoodTrackerApp(App):
    """Root Textual application for the Mood Tracker."""

    TITLE = "Mood Tracker TUI"
    SUB_TITLE = "v0.2 - Now with actual feelings"

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        # This will hold all mood entries in memory
        self.moods: List[MoodEntry] = []

    def on_mount(self) -> None:
        """Called when the app is ready."""
        # Load moods from disk when the app starts
        self.moods = load_moods()
        self.push_screen(MainScreen())

    def add_mood(self, entry: MoodEntry) -> None:
        """Add a new mood entry and save to disk."""
        self.moods.append(entry)
        save_moods(self.moods)


if __name__ == "__main__":
    app = MoodTrackerApp()
    app.run()