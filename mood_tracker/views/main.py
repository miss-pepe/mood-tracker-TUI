from __future__ import annotations

from datetime import date, datetime

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static
from textual import events

from ..models.storage import load_moods, save_moods, MoodEntry


# ASCII box pieces – sized to match your mockup
BOX_TOP = "┌───────────────────────────── MOOD TRACKER ─────────────────────────────┐"
BOX_BOTTOM = "└───────────────────────────────────────────────────────────────────────┘"
SECTION_DIVIDER = "├──────────────────────────── Mood History ─────────────────────────────┤"

INNER_WIDTH = len(BOX_TOP) - 2  # number of characters between the vertical borders


# Mood options as (label_for_ui, numeric_score_to_save)
MOOD_OPTIONS = [
    ("😄  Great", 9),
    ("🙂  Good", 7),
    ("😐  Meh", 5),
    ("😞  Bad", 3),
    ("😭  Awful", 1),
]


class MainScreen(Screen):
    """Single-screen UI that matches the ASCII mockup."""

    def compose(self) -> ComposeResult:
        # One big Static we’ll keep re-rendering as text
        self.main_view = Static(id="main-view")
        yield self.main_view

    def on_mount(self) -> None:
        # Start with the middle option selected ("Meh")
        self.selected_index = 2
        # Render initial view
        self.render_view()

    async def on_key(self, event: events.Key) -> None:
        """Handle ↑/↓ to change selection, Enter to save."""
        if event.key in ("up", "k"):
            self.selected_index = (self.selected_index - 1) % len(MOOD_OPTIONS)
            self.render_view()
        elif event.key in ("down", "j"):
            self.selected_index = (self.selected_index + 1) % len(MOOD_OPTIONS)
            self.render_view()
        elif event.key == "enter":
            # Save the currently selected mood
            self._save_current_mood()
            self.render_view()

    # ----------------- Rendering helpers -----------------

    def render_view(self) -> None:
        """Rebuild the full ASCII box and update the Static."""
        mood_lines = self._build_mood_section_lines()
        history_lines = self._build_history_section_lines()

        lines: list[str] = []
        lines.append(BOX_TOP)

        # Top (mood) section inside the box
        for content in mood_lines:
            lines.append(self._wrap_in_box(content))

        # Divider between mood + history
        lines.append(SECTION_DIVIDER)

        # History section inside the box
        for content in history_lines:
            lines.append(self._wrap_in_box(content))

        lines.append(BOX_BOTTOM)

        self.main_view.update("\n".join(lines))

    def _wrap_in_box(self, content: str) -> str:
        """Pad one line of content inside │ ... │ to match box width."""
        padded = content.ljust(INNER_WIDTH)
        return f"│{padded}│"

    def _build_mood_section_lines(self) -> list[str]:
        """Build the lines for the top 'How are you feeling?' section."""
        today_str = date.today().isoformat()

        lines: list[str] = []
        lines.append(f"Date: {today_str}")
        lines.append("")  # blank line
        lines.append("How are you feeling today?")
        lines.append("")
        lines.append("  [↑/↓ to select, Enter to confirm]")
        lines.append("")

        # Mood options like:
        #   ( ) 😄  Great
        #   (x) 😐  Meh
        for idx, (label, _score) in enumerate(MOOD_OPTIONS):
            marker = "(x)" if idx == self.selected_index else "( )"
            lines.append(f"  {marker} {label}")

        # Add some blank padding lines so the layout feels roomy
        while len(lines) < 11:
            lines.append("")

        return lines

    def _build_history_section_lines(self) -> list[str]:
        """Build the lines for the bottom 'Mood History' section."""
        entries = load_moods()

        # Show latest 5 entries (most recent at bottom, like your mock)
        if not entries:
            return [
                "",
                "[dim]No mood history yet. Log something above to get started.[/dim]",
                "",
                "              lower ←──────────── mood →────────────→ higher",
                "",
            ]

        last_entries = entries[-5:]

        lines: list[str] = []
        for entry in last_entries:
            date_str = entry.timestamp.strftime("%m-%d")
            emoji = self._emoji_for_score(entry.score)
            # Scale bar length – tweak factor to taste
            bar_length = max(1, entry.score * 2)
            bar = "#" * bar_length
            # Example: "11-20: 😐  ################"
            lines.append(f"{date_str}: {emoji}  {bar}")

        # Pad history lines so the box doesn't collapse
        while len(lines) < 5:
            lines.append("")

        lines.append("")
        lines.append("              lower ←──────────── mood →────────────→ higher")
        lines.append("")

        return lines

    def _emoji_for_score(self, score: int) -> str:
        """Pick an emoji matching the saved numeric score."""
        if score >= 9:
            return "😄"
        if score >= 7:
            return "🙂"
        if score >= 5:
            return "😐"
        if score >= 3:
            return "😞"
        return "😭"

    # ----------------- Data helpers -----------------

    def _save_current_mood(self) -> None:
        """Create a MoodEntry for the selected mood and persist it."""
        label, score = MOOD_OPTIONS[self.selected_index]
        entries = load_moods()
        entries.append(
            MoodEntry(
                timestamp=datetime.now(),
                score=score,
                tag=None,
                note=label,  # stash label in note so you can see it later if needed
            )
        )
        save_moods(entries)
