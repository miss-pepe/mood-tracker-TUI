from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import DataTable, Static, Header, Footer
from textual.containers import Vertical, Horizontal
from ..models.storage import load_moods
from ..constants import MOOD_OPTIONS

class HistoryScreen(Screen):
    """Detailed history view of all mood entries."""

    BINDINGS = [
        ("escape", "app.pop_screen", "Back"),
        ("q", "app.pop_screen", "Back"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        with Vertical(id="history-container"):
            yield Static("Mood History", id="history-title")
            yield Static(id="stats-panel")
            yield DataTable(id="history-table")
        yield Footer()

    def on_mount(self) -> None:
        self._load_data()

    def _load_data(self) -> None:
        entries = load_moods()
        table = self.query_one(DataTable)
        table.add_columns("Date", "Time", "Mood", "Score", "Note")
        
        # Sort entries by timestamp descending
        entries.sort(key=lambda x: x.timestamp, reverse=True)

        for entry in entries:
            date_str = entry.timestamp.strftime("%Y-%m-%d")
            time_str = entry.timestamp.strftime("%H:%M")
            
            # Find label for score
            label = next((label for label, score in MOOD_OPTIONS if score == entry.score), str(entry.score))
            # Clean up label (remove emoji if needed, or keep it)
            # MOOD_OPTIONS has format ":D  Great"
            
            note = entry.note if entry.note else ""
            
            table.add_row(date_str, time_str, label, str(entry.score), note)

        self._update_stats(entries)

    def _update_stats(self, entries) -> None:
        if not entries:
            stats_text = "No entries yet."
        else:
            total = len(entries)
            avg_score = sum(e.score for e in entries) / total
            
            # Count moods
            mood_counts = {}
            for e in entries:
                mood_counts[e.score] = mood_counts.get(e.score, 0) + 1
            
            top_mood_score = max(mood_counts, key=mood_counts.get)
            top_mood_label = next((label for label, score in MOOD_OPTIONS if score == top_mood_score), str(top_mood_score))

            stats_text = (
                f"Total Entries: {total} | "
                f"Average Mood: {avg_score:.1f}/10 | "
                f"Most Frequent: {top_mood_label}"
            )
        
        self.query_one("#stats-panel").update(stats_text)
