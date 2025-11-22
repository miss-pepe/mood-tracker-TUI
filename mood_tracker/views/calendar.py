from __future__ import annotations

import calendar
from datetime import date, datetime
from typing import Dict

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static
from textual.containers import Vertical
from textual import events

from ..models.storage import load_moods, MoodEntry


class MonthlyCalendarScreen(Screen):
    """Display mood history in a monthly calendar grid format.

    This screen provides a different perspective on mood data by showing
    it organized as a traditional calendar. Users can navigate backward
    and forward through months to see patterns over time. Days with mood
    entries are highlighted with the mood's emoji or score, while days
    without entries show just the day number.

    The calendar uses Python's built-in calendar module to handle all the
    complex date math like figuring out which day of the week a month starts
    on and how many days are in each month.
    """

    BINDINGS = [
        ("escape", "dismiss", "Back"),
        ("q", "dismiss", "Back"),
        ("left", "previous_month", "Previous Month"),
        ("right", "next_month", "Next Month"),
        ("h", "previous_month", "Previous Month"),
        ("l", "next_month", "Next Month"),
    ]

    def __init__(self, theme_palette, border_style) -> None:
        """Initialize the calendar screen with theme information.

        We start by displaying the current month, but users can navigate
        to any month they want using the arrow keys or vim-style navigation.

        Args:
            theme_palette: Current color palette for styling
            border_style: Current border style for box drawing
        """
        super().__init__()
        self.palette = theme_palette
        self.border_style = border_style
        # Start with today's date, but we'll let users navigate away from it
        self.current_month = date.today().replace(day=1)
        # We'll cache mood data to avoid reloading from disk on every render
        self.moods_by_date: Dict[date, MoodEntry] = {}

    def compose(self) -> ComposeResult:
        """Build the calendar display container.

        We use a single Static widget that we'll update whenever the
        displayed month changes. This is simpler than trying to create
        separate widgets for each calendar cell.
        """
        with Vertical(id="calendar-container"):
            yield Static(id="calendar-display")
            yield Static(
                "← / → or H / L to change months  •  ESC or Q to go back",
                id="calendar-help",
            )

    def on_mount(self) -> None:
        """Load mood data and render the initial calendar when the screen appears."""
        self._load_mood_data()
        self._render_calendar()

    def on_resize(self, event) -> None:
        """Handle terminal resize to update calendar display."""
        self._render_calendar()

    def _load_mood_data(self) -> None:
        """Load all mood entries and organize them by date for quick lookup.

        By creating a dictionary mapping dates to mood entries, we can
        quickly check if a given calendar day has a mood entry without
        having to search through the entire list every time.
        """
        entries = load_moods()
        self.moods_by_date = {entry.timestamp.date(): entry for entry in entries}

    def action_previous_month(self) -> None:
        """Navigate to the previous month and re-render the calendar.

        This action is triggered by left arrow or H key. We calculate
        the previous month by subtracting one from the month number,
        but we need to handle the year boundary when going from January
        back to December of the previous year.
        """
        year = self.current_month.year
        month = self.current_month.month

        # Handle year boundary
        if month == 1:
            self.current_month = date(year - 1, 12, 1)
        else:
            self.current_month = date(year, month - 1, 1)

        self._render_calendar()

    def action_next_month(self) -> None:
        """Navigate to the next month and re-render the calendar.

        This action is triggered by right arrow or L key. Similar to
        previous_month but we handle the boundary when going from
        December forward to January of the next year.
        """
        year = self.current_month.year
        month = self.current_month.month

        # Handle year boundary
        if month == 12:
            self.current_month = date(year + 1, 1, 1)
        else:
            self.current_month = date(year, month + 1, 1)

        self._render_calendar()

    def action_dismiss(self) -> None:
        """Close the calendar and return to the main screen."""
        self.app.pop_screen()

    def _render_calendar(self) -> None:
        """Build and display the complete calendar grid for the current month.

        This is where all the calendar magic happens. We use Python's calendar
        module to get the structure of the month, then we iterate through each
        week and day to build the visual representation. Days with mood entries
        get special formatting to make them stand out.
        """
        calendar_display = self.query_one("#calendar-display", Static)

        year = self.current_month.year
        month = self.current_month.month
        month_name = calendar.month_name[month]

        # Calculate responsive width based on terminal size
        terminal_width = self.size.width
        # Calendar should be 60% of screen width, with min/max bounds
        calendar_width = max(40, min(int(terminal_width * 0.6), 60))

        # Get the calendar structure for this month as a list of weeks
        # Each week is a list of day numbers, with 0 for days outside the month
        cal = calendar.monthcalendar(year, month)

        lines = []

        # Create the header with month name and year, nicely centered
        header = f"{month_name} {year}"
        lines.append(
            self._colorize(
                header.center(calendar_width), f"bold {self.palette.accent_high}"
            )
        )
        lines.append("")

        # Day of week headers - abbreviated to save space
        # We use the calendar module's day abbreviations to stay consistent
        day_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        header_row = "  ".join(f"{name:^4}" for name in day_names)
        lines.append(self._colorize(header_row, self.palette.text_muted))

        # Add a subtle separator line under the headers
        separator_width = min(calendar_width, 40)
        lines.append(self._colorize("─" * separator_width, self.palette.text_muted))

        # Now iterate through each week and render it as a row
        today = date.today()
        for week in cal:
            week_line = []
            for day in week:
                if day == 0:
                    # Empty cell for days outside this month
                    week_line.append("    ")
                else:
                    # Create a date object for this day so we can look up moods
                    day_date = date(year, month, day)
                    cell = self._format_day_cell(day, day_date, today)
                    week_line.append(cell)

            lines.append("  ".join(week_line))

        # Add some spacing and statistics at the bottom
        lines.append("")
        lines.append(self._colorize("─" * separator_width, self.palette.text_muted))

        # Calculate and show monthly statistics
        month_entries = [
            entry
            for day_date, entry in self.moods_by_date.items()
            if day_date.year == year and day_date.month == month
        ]

        if month_entries:
            avg_mood = sum(e.score for e in month_entries) / len(month_entries)
            stats = f"Entries: {len(month_entries)}  •  Average: {avg_mood:.1f}/10"
            lines.append(
                self._colorize(stats.center(calendar_width), self.palette.accent_low)
            )
        else:
            lines.append(
                self._colorize(
                    "No entries this month".center(calendar_width),
                    self.palette.text_muted,
                )
            )

        # Update the display widget with our beautifully formatted calendar
        calendar_display.update("\n".join(lines))

    def _format_day_cell(self, day: int, day_date: date, today: date) -> str:
        """Format a single day cell in the calendar grid.

        This method decides how to display each day based on whether it has
        a mood entry, whether it's today, and what the mood value was. The
        formatting needs to be consistent width-wise so the grid stays aligned.

        Args:
            day: The day number (1-31)
            day_date: The full date object for this day
            today: Today's date for highlighting the current day

        Returns:
            A formatted string representing this day cell, exactly 4 characters wide
        """
        # Check if this day has a mood entry
        if day_date in self.moods_by_date:
            mood = self.moods_by_date[day_date]
            emoji = self._mood_emoji(mood.score)

            # Format with emoji and score, colored by mood level
            cell_text = f"{emoji}{mood.score}"
            color = self._mood_color(mood.score)

            # If this is also today, make it bold for extra emphasis
            if day_date == today:
                return f"[bold {color}]{cell_text:^4}[/]"
            else:
                return f"[{color}]{cell_text:^4}[/]"
        else:
            # No mood entry for this day, just show the day number
            cell_text = f"{day:2d}"

            # Highlight today even if there's no mood entry yet
            if day_date == today:
                return f"[bold {self.palette.accent_high}]{cell_text:^4}[/]"
            else:
                return f"[{self.palette.text_primary}]{cell_text:^4}[/]"

    def _mood_emoji(self, score: int) -> str:
        """Get an emoji representation for a mood score.

        These emojis give quick visual feedback about how the person was
        feeling on that day. They match the same logic used in the main
        screen for consistency.
        """
        if score >= 8:
            return "😄"
        elif score >= 6:
            return "🙂"
        elif score >= 4:
            return "😐"
        elif score >= 2:
            return "😕"
        else:
            return "😢"

    def _mood_color(self, score: int) -> str:
        """Get the appropriate color for a mood score.

        We use the same color logic as the history bars so that colors
        have consistent meaning throughout the app. High scores are green,
        medium scores are yellow/orange, low scores are red.
        """
        if score >= 9:
            return self.palette.success
        elif score >= 7:
            return self.palette.accent_low
        elif score >= 5:
            return "#ffaa00"  # Yellow/orange for neutral
        elif score >= 3:
            return "#ff6600"  # Orange for concerning
        else:
            return self.palette.danger

    def _colorize(self, text: str, style: str) -> str:
        """Apply Textual color markup to text.

        This is a helper method to keep the color formatting consistent.
        It wraps text in the appropriate markup tags so Textual's Rich
        integration can render it with colors.
        """
        return f"[{style}]{text}[/{style}]"
