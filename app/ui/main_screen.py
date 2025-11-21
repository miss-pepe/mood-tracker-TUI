from __future__ import annotations

from datetime import datetime
from typing import cast

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import (
    Static,
    Header,
    Footer,
    Input,
    Button,
)
from textual.containers import Vertical, Horizontal

from app.models.mood import MoodEntry
from app.ui.graph_screen import GraphScreen


class MainScreen(Screen):
    """Main screen of the Mood Tracker."""

    BINDINGS = [
        ("q", "quit", "Quit app"),
        ("n", "focus_rating", "New mood"),
        ("g", "show_graph", "Trends & history"),
    ]

    DEFAULT_CSS = """
    #top_section, #form_section, #recent_section {
        padding: 1 2;
    }

    #form_section {
        border: round $secondary;
        width: 100%;
        max-width: 70;
        background: $panel;
    }

    #form_section Input {
        width: 34;
    }

    #form_actions {
        padding: 1 0 0 0;
        column-gap: 1;
    }

    #recent_section {
        border: round $primary;
        background: $boost;
        width: 100%;
        max-width: 70;
    }

    #recent_moods {
        padding: 0 0 1 0;
        color: $text-muted;
    }

    #status {
        height: 1;
        color: $success;
    }

    #status.error {
        color: $error;
    }
    """

    def compose(self) -> ComposeResult:
        """Create child widgets for the screen."""
        yield Header()

        # Title + info
        yield Vertical(
            Static("🧠 Mood Tracker TUI", id="title"),
            Static(
                "Log your mood, then view trends and history.\n"
                "Hotkeys: [n] new mood, [g] trends, [q] quit.",
                id="subtitle",
            ),
            id="top_section",
        )

        # Mood form
        yield Vertical(
            Static("Log a new mood", id="form_title"),
            Horizontal(
                Static("Rating (1-10): ", id="label_rating"),
                Input(placeholder="e.g. 7", id="input_rating", max_length=2),
                id="row_rating",
            ),
            Horizontal(
                Static("Tag (optional): ", id="label_tag"),
                Input(placeholder="e.g. anxious, calm", id="input_tag"),
                id="row_tag",
            ),
            Horizontal(
                Static("Note (optional): ", id="label_note"),
                Input(placeholder="Short note about today", id="input_note"),
                id="row_note",
            ),
            Horizontal(
                Button("Save mood", id="btn_save"),
                Button("View trends & history", id="btn_history"),
                id="form_actions",
            ),
            Static("", id="status"),
            id="form_section",
        )

        # Recent moods display
        yield Vertical(
            Static("Recent moods:", id="recent_title"),
            Static("", id="recent_moods"),
            id="recent_section",
        )

        yield Footer()

    # ---------- Helpers ----------

    @property
    def app_moods(self) -> list[MoodEntry]:
        """Convenience accessor to the app's mood list."""
        # `self.app` is the running App instance; we cast for type checkers
        return cast("MoodTrackerApp", self.app).moods  # type: ignore[name-defined]

    def on_mount(self) -> None:
        """Called when the screen is mounted."""
        # Focus rating input initially
        rating_input = self.query_one("#input_rating", Input)
        rating_input.focus()
        self._refresh_recent_moods()

    def _refresh_recent_moods(self) -> None:
        """Update the recent moods display."""
        recent_widget = self.query_one("#recent_moods", Static)

        if not self.app_moods:
            recent_widget.update("No moods logged yet.")
            return

        # Show last 5 moods (most recent last)
        lines: list[str] = []
        for entry in self.app_moods[-5:]:
            ts = entry.timestamp.strftime("%Y-%m-%d %H:%M")
            tag = f" [{entry.tag}]" if entry.tag else ""
            note = f" - {entry.note}" if entry.note else ""
            lines.append(f"{ts}: {entry.rating}/10{tag}{note}")

        recent_widget.update("\n".join(lines))

    # ---------- Actions / Events ----------

    def action_quit(self) -> None:
        """Quit the whole app."""
        self.app.exit()

    def action_focus_rating(self) -> None:
        """Focus the rating field to start a new mood."""
        rating_input = self.query_one("#input_rating", Input)
        rating_input.focus()
        rating_input.value = ""

    def action_show_graph(self) -> None:
        """Navigate to the graph / history screen."""
        self.app.push_screen(GraphScreen())  # type: ignore[attr-defined]

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press events."""
        if event.button.id == "btn_save":
            self._handle_save()
        elif event.button.id == "btn_history":
            self.action_show_graph()

    def _handle_save(self) -> None:
        """Validate form inputs and save the new mood."""
        rating_input = self.query_one("#input_rating", Input)
        tag_input = self.query_one("#input_tag", Input)
        note_input = self.query_one("#input_note", Input)

        # Validate rating
        raw_rating = rating_input.value.strip()
        if not raw_rating.isdigit():
            rating_input.tooltip = "Rating must be a number between 1 and 10."
            rating_input.focus()
            self._set_status("Rating must be a number between 1 and 10.", error=True)
            return

        rating = int(raw_rating)
        if not (1 <= rating <= 10):
            rating_input.tooltip = "Rating must be between 1 and 10."
            rating_input.focus()
            self._set_status("Rating must be between 1 and 10.", error=True)
            return

        tag = tag_input.value.strip() or None
        note = note_input.value.strip() or None

        # Create entry and save through the app
        new_entry = MoodEntry(
            timestamp=datetime.now(),
            rating=rating,
            tag=tag,
            note=note,
        )

        self.app.add_mood(new_entry)  # type: ignore[attr-defined]

        # Clear inputs
        rating_input.value = ""
        tag_input.value = ""
        note_input.value = ""

        # Refresh recent list
        self._refresh_recent_moods()
        self._set_status("Mood saved. Press [g] to see trends.", error=False)

    def _set_status(self, message: str, error: bool = False) -> None:
        """Show status feedback below the form."""
        status = self.query_one("#status", Static)
        status.remove_class("error")
        if error:
            status.add_class("error")
        status.update(message)
