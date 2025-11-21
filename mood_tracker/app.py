from textual.app import App, ComposeResult
from textual.widgets import Header, Footer

from .models.storage import init_storage
from .views.main import MainScreen


class MoodTrackerApp(App):
    """Main Textual application for the Mood Tracker."""

    TITLE = "Mood Tracker TUI"
    SUB_TITLE = "Track your vibes in the terminal"
    CSS_PATH = None

    BINDINGS = [
        ("q", "quit", "Quit"),
    ]

    def on_mount(self) -> None:
        """Run when the app starts."""
        # Make sure the data directory / file exist
        init_storage()
        # Show our single main screen (the big box UI)
        self.push_screen(MainScreen())

    def compose(self) -> ComposeResult:
        """Declare the layout: header, footer, and our screen stack."""
        yield Header(show_clock=True)
        yield Footer()
