from __future__ import annotations

from datetime import date, datetime

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static
from textual import events

from ..models.storage import load_moods, save_moods, MoodEntry
from ..theme import DEFAULT_THEME_NAME, THEMES, get_palette


# ASCII box pieces
BOX_TOP = "┌───────────────────────────── MOOD TRACKER ─────────────────────────────┐"
BOX_BOTTOM = "└────────────────────────────────────────────────────────────────────────┘"
SECTION_DIVIDER = "├──────────────────────────── Mood History ──────────────────────────────┤"

INNER_WIDTH = len(BOX_TOP) - 2  # number of characters between the vertical borders


# Mood options as (label_for_ui, numeric_score_to_save)
MOOD_OPTIONS = [
    (":D  Great", 9),
    (":)  Good", 7),
    (":|  Meh", 5),
    (":(  Bad", 3),
    (":'( Awful", 1),
]


class MainScreen(Screen):
    """Single-screen UI that matches the ASCII mockup."""

    def compose(self) -> ComposeResult:
        self.main_view = Static(id="main-view")
        yield self.main_view

    def on_mount(self) -> None:
        self.selected_index = 2  # Default selection: "Meh"
        self.theme_names = list(THEMES.keys())
        self.theme_index = self.theme_names.index(DEFAULT_THEME_NAME)
        self.palette = get_palette(self.theme_names[self.theme_index])
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
            self._save_current_mood()
            self.render_view()
        elif event.key.lower() == "t":
            self._cycle_theme()

    # ---------------- Rendering helpers ----------------

    def render_view(self) -> None:
        """Rebuild the full ASCII box and update the Static."""
        mood_lines = self._build_mood_section_lines()
        history_lines = self._build_history_section_lines()

        lines: list[str] = []
        lines.append(self._colorize_line(BOX_TOP, self.palette.accent_mid))

        for content, style in mood_lines:
            lines.append(self._wrap_in_box(content, style))

        lines.append(self._colorize_line(SECTION_DIVIDER, self.palette.accent_mid))

        for content, style in history_lines:
            lines.append(self._wrap_in_box(content, style))

        lines.append(self._colorize_line(BOX_BOTTOM, self.palette.accent_mid))

        self.main_view.update("\n".join(lines))

    def _wrap_in_box(self, content: str, style: str | None = None) -> str:
        """Pad one line of content inside │ ... │ to match box width."""
        padded = content.ljust(INNER_WIDTH)
        line = f"│{padded}│"
        return self._colorize_line(line, style or self.palette.text_primary)

    def _colorize_line(self, line: str, color: str) -> str:
        return f"[{color}]{line}[/{color}]"

    def _build_mood_section_lines(self) -> list[tuple[str, str | None]]:
        """Build the lines for the top 'How are you feeling?' section."""
        today_str = date.today().isoformat()

        lines: list[tuple[str, str | None]] = []
        lines.append((f"Date: {today_str}", self.palette.text_primary))
        lines.append(("", None))
        lines.append(("How are you feeling today?", f"bold {self.palette.accent_high}"))
        lines.append(("", None))
        lines.append(("  [↑/↓ to select, Enter to confirm]", self.palette.text_muted))
        lines.append(
            (f"  Theme: {self._current_theme_name().title()} (press T to change)",
             self.palette.accent_low)
        )
        lines.append(("", None))

        # Mood options
        for idx, (label, _score) in enumerate(MOOD_OPTIONS):
            marker = "(x)" if idx == self.selected_index else "( )"
            style = f"bold {self.palette.accent_high}" if idx == self.selected_index else None
            lines.append((f"  {marker} {label}", style))

        # Pad to stable height
        while len(lines) < 11:
            lines.append(("", None))

        return lines

    def _build_history_section_lines(self) -> list[tuple[str, str | None]]:
        """Build the lines for the bottom 'Mood History' section."""
        entries = load_moods()

        if not entries:
            return [
                ("", None),
                ("No mood history yet. Log something above to get started.",
                 f"dim {self.palette.text_muted}"),
                ("", None),
                ("              lower ←──────────── mood →────────────→ higher",
                 self.palette.accent_low),
                ("", None),
            ]

        last_entries = entries[-5:]

        lines: list[tuple[str, str | None]] = []
        for entry in last_entries:
            date_str = entry.timestamp.strftime("%m-%d")
            ascii_face = self._ascii_for_score(entry.score)
            bar_length = max(1, entry.score * 2)
            bar = "#" * bar_length

            lines.append(
                (
                    f"{date_str}: {ascii_face:<4} {bar}",
                    self._history_color_for_score(entry.score),
                )
            )

        while len(lines) < 5:
            lines.append(("", None))

        lines.append(("", None))
        lines.append(
            ("              lower ←──────────── mood →────────────→ higher",
             self.palette.accent_low)
        )
        lines.append(("", None))

        return lines

    def _ascii_for_score(self, score: int) -> str:
        """ASCII replacement for emojis to preserve alignment."""
        if score >= 9:
            return ":D"
        if score >= 7:
            return ":)"
        if score >= 5:
            return ":|"
        if score >= 3:
            return ":("
        return ":'("

    def _history_color_for_score(self, score: int) -> str:
        if score >= 7:
            return self.palette.success
        if score >= 4:
            return self.palette.accent_low
        return self.palette.danger

    def _cycle_theme(self) -> None:
        self.theme_index = (self.theme_index + 1) % len(self.theme_names)
        self.palette = get_palette(self.theme_names[self.theme_index])
        self.render_view()

    def _current_theme_name(self) -> str:
        return self.theme_names[self.theme_index]

    def _save_current_mood(self) -> None:
        label, score = MOOD_OPTIONS[self.selected_index]
        entries = load_moods()
        entries.append(
            MoodEntry(
                timestamp=datetime.now(),
                score=score,
                tag=None,
                note=label,
            )
        )
        save_moods(entries)
