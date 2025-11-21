from __future__ import annotations

from typing import cast

from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Button, DataTable, Footer, Header, Static

from app.models.mood import MoodEntry


class GraphScreen(Screen):
    """Screen that shows basic trends and a table of mood history."""

    BINDINGS = [
        ("b", "back", "Back to logging"),
        ("r", "refresh", "Refresh data"),
        ("q", "quit", "Quit app"),
    ]

    DEFAULT_CSS = """
    #graph_body {
        padding: 1 2;
        row-gap: 1;
    }

    #title {
        content-align: center middle;
        text-style: bold;
    }

    #help {
        color: $text-muted;
    }

    #spark {
        border: round $primary;
        background: $panel;
        padding: 1;
        min-height: 4;
    }

    #history_table {
        height: 16;
        width: 100%;
        max-width: 90;
    }

    #graph_actions {
        column-gap: 1;
        padding-top: 1;
    }
    """

    @property
    def app_moods(self) -> list[MoodEntry]:
        """Convenience accessor to the app's mood list."""
        return cast("MoodTrackerApp", self.app).moods  # type: ignore[name-defined]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Vertical(
            Static("Mood trends & history", id="title"),
            Static("Newest entries appear on the right of the chart. Press [b] to return.", id="help"),
            Static("", id="summary"),
            Static("", id="spark"),
            DataTable(id="history_table", zebra_stripes=True),
            Horizontal(
                Button("Back to logging", id="btn_back"),
                Button("Refresh data", id="btn_refresh"),
                id="graph_actions",
            ),
            id="graph_body",
        )
        yield Footer()

    def on_mount(self) -> None:
        """Called when the screen is mounted."""
        table = self.query_one("#history_table", DataTable)
        table.add_columns("When", "Rating", "Tag", "Note")
        table.cursor_type = "row"
        self.refresh_view()

    # ---------- Actions ----------

    def action_back(self) -> None:
        """Return to the main logging screen."""
        self.app.pop_screen()

    def action_quit(self) -> None:
        """Quit the app from the graph screen."""
        self.app.exit()

    def action_refresh(self) -> None:
        """Reload the data from the app state."""
        self.refresh_view()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses for navigation or refresh."""
        if event.button.id == "btn_back":
            self.action_back()
        elif event.button.id == "btn_refresh":
            self.refresh_view()

    # ---------- Helpers ----------

    def refresh_view(self) -> None:
        """Update the sparkline text and data table."""
        table = self.query_one("#history_table", DataTable)
        summary = self.query_one("#summary", Static)
        spark = self.query_one("#spark", Static)

        table.clear()

        if not self.app_moods:
            summary.update("No moods logged yet. Press [b] to return and add one.")
            spark.update("No data to chart.")
            return

        data = self.app_moods
        avg_rating = sum(entry.rating for entry in data) / len(data)
        latest = data[-1]
        latest_label = f"{latest.rating}/10" + (f" [{latest.tag}]" if latest.tag else "")

        summary.update(
            f"Entries: {len(data)} | Average: {avg_rating:.1f}/10 | Latest: {latest_label}"
        )

        spark.update(self._build_sparkline(data))

        # Show newest first, but limit to a manageable size
        for entry in reversed(data[-30:]):
            ts = entry.timestamp.strftime("%Y-%m-%d %H:%M")
            table.add_row(
                ts,
                f"{entry.rating}/10",
                entry.tag or "-",
                entry.note or "-",
            )

    def _build_sparkline(self, entries: list[MoodEntry]) -> str:
        """Render a simple ASCII sparkline for recent ratings."""
        ratings = [entry.rating for entry in entries[-60:]]
        if not ratings:
            return "No data to chart."

        # Map ratings 1-10 onto a set of ASCII characters from low to high intensity.
        palette = " .:-=+*#%@"

        def clamp(value: int) -> int:
            return max(1, min(10, value))

        spark_chars = "".join(palette[clamp(rating) - 1] for rating in ratings)
        min_rating = min(ratings)
        max_rating = max(ratings)

        return (
            f"Trend (last {len(ratings)} entries, newest to the right)\n"
            f"min {min_rating}/10 |{spark_chars}| max {max_rating}/10"
        )
