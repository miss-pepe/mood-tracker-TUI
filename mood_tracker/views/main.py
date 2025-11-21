from __future__ import annotations

from datetime import date, datetime

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static
from textual import events

from ..models.storage import load_moods, save_moods, MoodEntry
from ..theme import DEFAULT_THEME_NAME, THEMES, get_palette
from ..models.preferences import load_preferences, save_preferences, UserPreferences

                                        # ASCII box pieces
BOX_TOP = "┌───────────────────────────── MOOD TRACKER ─────────────────────────────┐"
BOX_BOTTOM = "└────────────────────────────────────────────────────────────────────────┘"
SECTION_DIVIDER = "├──────────────────────────── Mood History ──────────────────────────────┤"

INNER_WIDTH = len(BOX_TOP) - 2                          # number of characters between the vertical borders

MOOD_OPTIONS = [                                        # Mood options as (label_for_ui, numeric_score_to_save)
    (":D  Great", 9),
    (":)  Good", 7),
    (":|  Meh", 5),
    (":(  Bad", 3),
    (":'( Awful", 1),
]


THEME_MASCOTS = {                                   

    "Neon Midnight": """    ✨ ⭐
   (◕‿◕)
    >🌙< 
   /|  |\\
Little Moon Guardian""",
    
    "Galactic Slushie": """    🌈 ❄️
   (☆▽☆)
    \\♡/
   ~~🧊~~
Sparkle Freeze""",
    
    "Retro Arcade CRT": """    ▓▓▓▓
   (◉_◉)
    [█]
   _|▓|_
Pixel Buddy""",
    
    "Dragonfire Core": """    🔥△🔥
   (⚆_⚆)
    ≋≋≋
   /\\/\\/\\
Flame Wyrm""",
    
    "Oceanic Overdrive": """    ~🌊~
   (◕ω◕)
    ≈≈≈
   ~~~🐚~
Wave Rider""",
    
    "Toxic Slime Lab": """    ☢️ ☣️
   (●▽●)
    {💚}
   〰️〰️〰️
Gloop Friend""",
    
    "Cosmic Jellyfish": """    ✧˖°
   (◕‿◕)
    ≋≋≋
   ~★~★~
Stardrift""",
    
    "90s Vapor Arcade": """    ▓▒░
   (◕‿‿◕)
    〜〜
   ∿∿∿∿
Retro Wave""",
    
    "Night-Shift Rainbow": """    🌈💫
   (◠‿◠)
    ▓▒░
   /|☆|\\
Rainbow Shifter""",
    
    "Cyber Swamp Witch": """    🐸✨
   (◉‿◉)
    /🔮\\
   /|▓▓|\\
Hex Hopper""",
    
    "Midnight Bubblegum": """    ○●○
   (◕ω◕)
    >♡
   〰️💕〰️
Bubble Sprite""",
    
    "Storm Witch": """    ⚡🌩️⚡
   (◕‿◕)
    /⚡\\
   /|🌀|\\
Thunder Caster""",
    
    "Chaotic Pastel Hacker": """    🎀💻🎀
   (◕▽◕)
    </>
   ₊˚✧✧
Sugar Code""",
    
    "Neon Anxiety": """    ⚠️✨⚠️
   (⊙_⊙)
    !!!
   /|◉|\\
Jitter Bug""",
    
    "Galaxy Sweetheart": """    💖✨💖
   (◕‿◕✿)
    ★♡★
   ~˖°~
Star Crush""",
    
    "Cyber Siren": """    ⚡💋⚡
   (◕‿↼)
    〜〜
   /|▓|\\ 
Digital Diva""",
    
    "Void Candy": """    ⬛🍭⬛
   (◉‿◉)
    ✧✧
   〰️〰️〰️
Sweet Nothing""",
    
    "Hacker Bunny": """    🐰💻
   (◕‿◕)
    </>
   /|⌨️|\\
Code Cottontail""",
    
    "Wicked Pastel": """    ♡⚡♡
   (◕‿◕✿)
    /▓\\
   〰️💕〰️
Chaos Cutie""",
    
    "Caffeine Overdose": """    ☕⚡☕
   (⊙△⊙)
    !!!
   /|☕|\\
Jitter Bean""",
    
    "Gremlin Hacker Glow": """    ✨🔧✨
   (◕ヮ◕)
    </>
   〰️💚〰️
Chaos Coder""",
    
    "Chaotic Intelligence Matrix": """    ◆◆◆
   (◉_◉)
    ▓▓▓
   [█████]
The Grid Mind""",
    
    "Midnight Mischief": """    😈🌙
   (◕‿◕)
    /▓\\
   /|☆|\\
Night Trickster""",
    
    "Terminal Witchcraft": """    $✨$
   (◕‿◕)
    /🔮\\
   ~/|▓|/~
Command Caster""",
    
    "Neon Disaster Darling": """    💥✨💥
   (◕ω◕)
    !!!
   〰️⚡〰️
Glitch Angel""",
    
    "Quantum Sass Core™": """    Q💫Q
   (◕‿↼)
    |▓|
   /¯\\͜\\¯/
Attitude Algorithm""",
    
    "Feral Cyberpunk Assistant": """    ⚡🤖⚡
   (◉▽◉)
    </>
   /|▓▓|\\
Wild.exe""",
    
    "Overclocked Personality Core": """    🔥⚡🔥
   (⊙▽⊙)
    [!]
   ▓▓▓▓▓
Turbo Spirit""",
    
    "The \"Don't Let the Sweet Voice Fool You\" Palette": """    ♡😈♡
   (◕‿◕✿)
    ~~~
   〰️💕〰️
Sugar Chaos""",
    
    "Spicy Tech Oracle": """    🌶️✨
   (◕‿◕)
    /🔮\\
   〰️🔥〰️
Hot Logic""",
    
    "Dracula": """    🦇🌙
   (◕_◕)
    [▓]
   /|▓|\\
Count Pixel""",
    
    "One Dark Pro": """    ◆◆
   (◕‿◕)
    ▓▓
   /|▓|\\
Dark Matter""",
    
    "Tokyo Night": """    🏮✨
   (◕ω◕)
    |||
   〰️🌸〰️
Neon Bloom""",
    
    "Catppuccin Mocha": """    ☕💤
   (◕‿◕)
    ≈≈≈
   〰️♡〰️
Cozy Brew""",
    
    "Gruvbox Dark": """    🍂🍁
   (◕‿◕)
    ▓▒░
   /|▓|\\
Autumn Code""",
    
    "Solarized Dark": """    ☀️🌙
   (◕‿◕)
    ≈≈≈
   /|▓|\\
Eclipse Pal""",
    
    "Nord": """    ❄️✨
   (◕‿◕)
    ▓▒░
   〰️💙〰️
Arctic Friend""",
    
    "Monokai Pro": """    ◆◆◆
   (◕‿◕)
    [▓]
   /|▓|\\
Pro Coder""",
    
    "Ayu Mirage": """    🌅✨
   (◕ω◕)
    ≈≈≈
   〰️🌸〰️
Desert Dream""",
    
    "SynthWave '84": """    🌴🌆
   (◕▽◕)
    ∿∿∿
   〰️💜〰️
Retro Runner""",
    
    "SpaceCamp": """    🚀✨
   (◕‿◕)
    /|\\
   〰️🌙〰️
Cosmic Cadet""",
    
    "Night Owl": """    🦉🌙
   (◕‿◕)
    /▓\\
   /|^|\\
Wise Watcher""",
    
    "Tomorrow Night Eighties": """    📻✨
   (◕‿◕)
    ▓▒░
   〰️💿〰️
Retro Beat""",
    
    "Afterglow": """    ✨🌅✨
   (◕ω◕)
    ~~~
   〰️💛〰️
Sunset Sprite""",
    
    "Lucario": """    ⚡🔵⚡
   (◕‿◕)
    /▓\\
   /|⚡|\\
Aura Warrior""",
    
    "Material Darker": """    ◆◆◆
   (◕‿◕)
    ▓▓▓
   〰️💎〰️
Shadow Gem""",
    
    "Adventure Time": """    ⚔️👑
   (◕▽◕)
    /!\\
   /|♡|\\
Quest Buddy""",
    
    "Palenight": """    🌙💜
   (◕‿◕)
    ≈≈≈
   〰️✨〰️
Twilight Pal""",
    
    "Jellybeans": """    🍬🍭
   (◕ω◕)
    ♡♡♡
   〰️🌈〰️
Sweet Stack""",
    
    "Horizon Dark": """    🌅🌊
   (◕‿◕)
    ≈≈≈
   〰️🌴〰️
Shore Spirit""",
}

def display_theme_mascot(theme_name):           # Example of how to display a mascot when a user selects a theme
    """Shows the adorable ASCII mascot for the selected theme"""
    mascot = THEME_MASCOTS.get(theme_name)
    if mascot:
        print(mascot)
    else:
        print("No mascot found for this theme!")         # Fallback if theme doesn't have a mascot yet

display_theme_mascot("Neon Midnight")           # Usage example:

from textual.widgets import Static, Label
from textual.containers import Container, Vertical

class HelpScreen(Screen):
    """Modal dialog showing keyboard shortcuts and help information."""
    
    BINDINGS = [
        ("escape", "dismiss", "Close"),
        ("q", "dismiss", "Close"),
    ]
    
    def compose(self) -> ComposeResult:
        with Container(id="help-dialog"):
            yield Static("┌─────────── KEYBOARD SHORTCUTS ───────────┐", id="help-header")
            yield Static(
                "│                                          │\n"
                "│  Navigation:                             │\n"
                "│    ↑/↓ or K/J  -  Select mood            │\n"
                "│    Enter or S  -  Save current mood      │\n"
                "│                                          │\n"
                "│  Actions:                                │\n"
                "│    T  -  Cycle through themes            │\n"
                "│    H  -  Toggle history panel            │\n"
                "│    ?  -  Show this help dialog           │\n"
                "│    Q  -  Quit application                │\n"
                "│                                          │\n"
                "│  Press ESC or Q to close this dialog     │\n"
                "│                                          │\n"
                "└──────────────────────────────────────────┘",
                id="help-content"
            )
    
    def action_dismiss(self) -> None:
        """Close the help dialog and return to main screen."""
        self.app.pop_screen()

class MainScreen(Screen):
    """Single-screen UI that matches the ASCII mockup."""
    show_history = True

    def _get_centered_padding(self) -> int:
        """Calculate left padding needed to center the box on the screen."""
        terminal_width = self.size.width
        box_width = len(BOX_TOP)
        padding = max(0, (terminal_width - box_width) // 2)    # Calculate padding, ensuring it's never negative
        return padding

    def _show_help_dialog(self) -> None:
        """Push the help dialog onto the screen stack."""
        self.app.push_screen(HelpScreen())

    def compose(self) -> ComposeResult:
        self.main_view = Static(id="main-view")
        yield self.main_view

    def on_mount(self) -> None:
        self.preferences = load_preferences()           # Load user preferences from disk
        self.selected_index = self.preferences.last_selected_mood_index # Restore last selected mood
        self.show_history = self.preferences.show_history_panel
    
        self.theme_names = list(THEMES.keys())          # Set up theme system using saved preference
        try:
            self.theme_index = self.theme_names.index(self.preferences.current_theme)
        except ValueError:
            self.theme_index = self.theme_names.index(DEFAULT_THEME_NAME)         # If saved theme doesn't exist, fall back to default

        self.palette = get_palette(self.theme_names[self.theme_index])
        self.render_view()

    async def on_key(self, event: events.Key) -> None:
        """Handle keyboard input for navigation and actions."""
        key = event.key.lower()
    
                        # Navigation keys
        if key in ("up", "k"):
            self.selected_index = (self.selected_index - 1) % len(MOOD_OPTIONS)
            self.preferences.last_selected_mood_index = self.selected_index
            save_preferences(self.preferences)
            self.render_view()
    
        elif key in ("down", "j"):
            self.selected_index = (self.selected_index + 1) % len(MOOD_OPTIONS)
            self.preferences.last_selected_mood_index = self.selected_index
            save_preferences(self.preferences)
            self.render_view()
    
                        # Action keys
        elif key == "enter" or key == "s":  # Enter or S to save
            self._save_current_mood()
            self.render_view()
    
        elif key == "t":        # Toggle theme
            self._cycle_theme()
    
        elif key == "h":        # Toggle history panel
            self.show_history = not self.show_history
            self.preferences.show_history_panel = self.show_history
            save_preferences(self.preferences)
            self.render_view()
    
        elif key == "question_mark":  # ? for help
            self._show_help_dialog()

    # ---------------- Rendering helpers ----------------

    def render_view(self) -> None:
        """Rebuild the full ASCII box and update the Static."""
        # Calculate centering padding once
        padding = self._get_centered_padding()
    
        mood_lines = self._build_mood_section_lines()
        history_lines = self._build_history_section_lines()

        lines: list[str] = []
    
    # Apply padding to box top
        top_line = self._colorize_line(BOX_TOP, self.palette.accent_mid)
        lines.append(" " * padding + top_line if padding > 0 else top_line)

    # Mood section with padding
        for content, style in mood_lines:
            lines.append(self._wrap_in_box(content, style, padding))

    # Divider with padding
        divider_line = self._colorize_line(SECTION_DIVIDER, self.palette.accent_mid)
        lines.append(" " * padding + divider_line if padding > 0 else divider_line)

    # History section (only if not hidden)
        if self.show_history:
            for content, style in history_lines:
                lines.append(self._wrap_in_box(content, style, padding))

    # Bottom border with padding
        bottom_line = self._colorize_line(BOX_BOTTOM, self.palette.accent_mid)
        lines.append(" " * padding + bottom_line if padding > 0 else bottom_line)

        self.main_view.update("\n".join(lines))

    def _wrap_in_box(self, content: str, style: str | None = None, padding: int = 0) -> str:
        """Pad one line of content inside │ ... │ to match box width and center it."""
        padded_content = content.ljust(INNER_WIDTH)
        line = f"│{padded_content}│"
        colored_line = self._colorize_line(line, style or self.palette.text_primary)
    
        if padding > 0:                # Add left padding for centering
            return " " * padding + colored_line
        return colored_line

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

        for idx, (label, _score) in enumerate(MOOD_OPTIONS):        # Mood options
            marker = "(x)" if idx == self.selected_index else "( )"
            style = f"bold {self.palette.accent_high}" if idx == self.selected_index else None
            lines.append((f"  {marker} {label}", style))

        while len(lines) < 11:                  # Pad to stable height
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
    
        max_score = max(entry.score for entry in last_entries)    # Find max score for scaling

        lines: list[tuple[str, str | None]] = []
        for entry in last_entries:
            date_str = entry.timestamp.strftime("%m-%d")
            ascii_face = self._ascii_for_score(entry.score)
            bar_color = self._bar_color_for_score(entry.score)
            bar_length = self._calculate_scaled_bar_length(entry.score, max_score, max_bar_width=30)        # Use scaled bar length
            bar = "█" * bar_length          # Using a solid block character for better visual weight
        
            line_text = f"{date_str}: {ascii_face:<4} [{bar_color}]{bar}[/{bar_color}]"
            lines.append((line_text, self.palette.text_primary))

        while len(lines) < 5:
            lines.append(("", None))

        lines.append(("", None))
        lines.append(
            ("              lower ←──────────── mood →────────────→ higher",
            self.palette.accent_low)
        )
        lines.append(("", None))

        return lines

    def _bar_color_for_score(self, score: int) -> str:
        """Return the specific bar color for a mood score."""
        if score >= 9:  # Great
            return self.palette.success
        elif score >= 7:  # Good
            return self.palette.accent_low
        elif score >= 5:  # Meh
            return "#ffaa00"  # Yellow/orange for neutral
        elif score >= 3:  # Bad
            return "#ff6600"  # Orange for concerning
        else:  # Awful
            return self.palette.danger

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
        """Return color for history bar based on score."""
        if score >= 7:
            return self.palette.success
        if score >= 4:
            return self.palette.accent_low
        return self.palette.danger

    def _cycle_theme(self) -> None:
        """Cycle through available themes and update the UI."""
        self.theme_index = (self.theme_index + 1) % len(self.theme_names)
        self.palette = get_palette(self.theme_names[self.theme_index])
        self.preferences.current_theme = self.theme_names[self.theme_index]
        save_preferences(self.preferences)

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

        self.preferences.last_selected_mood_index = self.selected_index       # Save preferences
        save_preferences(self.preferences)

        self.app.notify(        # Show confirmation toast
            f"✓ Mood saved: {label}",
            severity="information",
            timeout=2
        )

    def _calculate_scaled_bar_length(self, score: int, max_score: int, max_bar_width: int = 20) -> int:
        """Calculate bar length scaled relative to the maximum score in history."""
        if max_score == 100:
            return 0
        return max(1, int((score / max_score) * max_bar_width))