from __future__ import annotations
from .reflection import ReflectionPromptScreen
from .export import ExportScreen
from datetime import date, datetime
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static, TextArea
from textual import events
from ..models.storage import load_moods, save_moods, MoodEntry
from ..theme import DEFAULT_THEME_NAME, THEMES, get_palette, get_border_style
from ..models.preferences import load_preferences, save_preferences, UserPreferences
from .calendar import MonthlyCalendarScreen
from ..audio import SoundManager




BOX_WIDTH = 74                      # ASCII box pieces
INNER_WIDTH = BOX_WIDTH - 2

MOOD_OPTIONS = [                      # Mood options as (label_for_ui, numeric_score_to_save)
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

# display_theme_mascot("Neon Midnight")          

from textual.widgets import Static, Label
from textual.containers import Container, Vertical

class ReflectionPromptScreen(Screen):
    """Modal dialog for users to add a note/reflection to their mood entry."""
    
    BINDINGS = [
        ("escape", "cancel", "Cancel"),
        ("ctrl+s", "submit", "Save"),
    ]
    
    def __init__(self, label: str, score: int, palette):
        super().__init__()
        self.label = label
        self.score = score
        self.palette = palette
        self.note_text = ""
    
    def compose(self) -> ComposeResult:
        from textual.widgets import TextArea, Button
        with Container(id="reflection-dialog"):
            yield Static(f"Add a reflection for: {self.label}", id="reflection-header")
            yield TextArea(id="reflection-input")
            with Container(id="reflection-buttons"):
                yield Button("Save (Ctrl+S)", id="save-button", variant="primary")
                yield Button("Skip (ESC)", id="cancel-button")
    
    def on_mount(self) -> None:
        text_area = self.query_one("#reflection-input", TextArea)
        text_area.focus()
    
    def action_submit(self) -> None:
        """Save the mood with the reflection note."""
        text_area = self.query_one("#reflection-input", TextArea)
        self.note_text = text_area.text.strip() if text_area.text else None
        self.dismiss(self.note_text)
    
    def action_cancel(self) -> None:
        """Cancel without saving a note."""
        self.dismiss(None)


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

    def _apply_padding(self, text: str, padding: int) -> str:
        return " " * padding + text

    def _get_centered_padding(self) -> int:
        """Calculate left padding needed to center the box on the screen."""
        terminal_width = self.size.width
        box_width = BOX_WIDTH
        padding = max(0, (terminal_width - box_width) // 2)    # Calculate padding, ensuring it's never negative
        return padding

    def _create_top_border(self) -> str:
        """Generate the top border using current theme's border style.
        
        This creates a border like: ┌──────────┐
        The corner characters and horizontal line come from the theme's BorderStyle.
        """
        return (
            self.border_style.top_left + 
            self.border_style.horizontal * INNER_WIDTH + 
            self.border_style.top_right
        )

    def _create_bottom_border(self) -> str:
        """Generate the bottom border using current theme's border style.
        
        This creates a border like: └──────────┘
        The corner characters and horizontal line come from the theme's BorderStyle.
        """
        return (
            self.border_style.bottom_left + 
            self.border_style.horizontal * INNER_WIDTH + 
            self.border_style.bottom_right
        )

    def _create_section_divider(self, label: str) -> str:
        """Generate a section divider with centered text using current theme's style.
        
        This creates a divider like: ├─────── Label ───────┤
        The characters come from the theme's BorderStyle, and the label is centered.
        """
        label_with_spaces = f" {label} "
        remaining = INNER_WIDTH - len(label_with_spaces)
        left_dashes = remaining // 2
        right_dashes = remaining - left_dashes
        
        return (
            self.border_style.divider_left +
            self.border_style.divider_horizontal * left_dashes +
            label_with_spaces +
            self.border_style.divider_horizontal * right_dashes +
            self.border_style.divider_right
        )

    def _apply_border_color(self, border_text: str) -> str:
        """Apply color or gradient to border text based on theme's border style.
        
        If the theme uses gradients and supports them, apply a gradient.
        Otherwise, use the solid fallback color.
        This ensures borders always look good even on terminals without gradient support.
        """
        if self.border_style.use_gradient and self.border_style.gradient_colors:
            # Apply gradient from first color to second color
            color1, color2 = self.border_style.gradient_colors
            # Textual/Rich gradient syntax
            return f"[{color1} on default to {color2} on default]{border_text}[/]"
        else:
            # Use solid color fallback
            return f"[{self.border_style.border_color}]{border_text}[/]"

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
        self.sound_manager = SoundManager()


        self.theme_names = list(THEMES.keys())          # Set up theme system using saved preference
        try:
            self.theme_index = self.theme_names.index(self.preferences.current_theme)
        except ValueError:
            self.theme_index = self.theme_names.index(DEFAULT_THEME_NAME)         # If saved theme doesn't exist, fall back to default

        self.palette = get_palette(self.theme_names[self.theme_index])
        self.border_style = get_border_style(self.theme_names[self.theme_index])  # MOVED UP!
        self.render_view()  # Now this is safe because border_style exists

    async def on_key(self, event: events.Key) -> None:
        """Handle keyboard input for navigation and actions."""
        key = event.key.lower()

        if key in ("up", "k"):                        # Navigation keys
            self.selected_index = (self.selected_index - 1) % len(MOOD_OPTIONS)
            self.preferences.last_selected_mood_index = self.selected_index
            save_preferences(self.preferences)
            self.sound_manager.play_selection()  # Add this line
            self.render_view()
    
        elif key in ("down", "j"):
            self.selected_index = (self.selected_index + 1) % len(MOOD_OPTIONS)
            self.preferences.last_selected_mood_index = self.selected_index
            save_preferences(self.preferences)
            self.sound_manager.play_selection()  # Add this line
            self.render_view()
    
                        # Action keys
        elif key == "enter" or key == "s":  # Enter or S to save
            self.render_view()
            await self._save_current_mood()

        elif key == "t":        # Toggle theme
            self._cycle_theme()
    
        elif key == "h":        # Toggle history panel
            self.show_history = not self.show_history
            self.preferences.show_history_panel = self.show_history
            save_preferences(self.preferences)
            self.render_view()
    
        elif key == "question_mark":  # ? for help
            self._show_help_dialog()

        elif key == "e":  # E for export
            self.app.push_screen(ExportScreen(self.palette))

        elif key == "m":  # M for monthly view
            self.app.push_screen(MonthlyCalendarScreen(self.palette, self.border_style))

    # ---------------- Rendering helpers ----------------

    def render_view(self) -> None:
        """Rebuild the full UI by composing all sections together."""
        padding = self._get_centered_padding()

        lines = []
        
        # Generate and apply top border dynamically from current theme
        top_border = self._create_top_border()
        lines.append(self._apply_padding(self._apply_border_color(top_border), padding))

        # Render mood selection section
        for content, style in self._build_mood_section_lines():
            lines.append(self._wrap_in_box(content, style, padding))

        # Generate and apply section divider dynamically
        divider = self._create_section_divider("Mood History")
        lines.append(self._apply_padding(self._apply_border_color(divider), padding))

        # Render history section if enabled
        if self.show_history:
            for content, style in self._build_history_section_lines():
                lines.append(self._wrap_in_box(content, style, padding))

        # Generate and apply bottom border dynamically
        bottom_border = self._create_bottom_border()
        lines.append(self._apply_padding(self._apply_border_color(bottom_border), padding))

        self.main_view.update("\n".join(lines))

    def _wrap_in_box(self, content: str, style: str | None = None, padding: int = 0) -> str:
        """Wrap content in themed vertical borders."""
        padded_content = content.ljust(INNER_WIDTH)
        # Use the current theme's vertical border character
        vertical = self.border_style.vertical
        line = f"{vertical}{padded_content}{vertical}"
        colored_line = self._colorize(line, style)
        return self._apply_padding(colored_line, padding)

    def _colorize(self, line: str, style: str | None = None) -> str:
        """Apply Textual color/style markup to a line.
    
        This is a convenience wrapper that applies color tags to text.
        If no style is provided, it uses the theme's default text color.
    
        Args:
            line: Text to colorize
            style: Optional Textual style string (e.g., "bold red", "#ff00ff")
               If None, uses the theme's primary text color.
    
        Returns:
            Line wrapped in Textual color markup tags
        """
        color = style or self.palette.text_primary
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
        """Build the lines for the bottom 'Mood History' section.
        
        The key here is to keep the content and styling separate so that
        width calculations work correctly. We build plain text content first,
        let it get padded to the right width, and then the _wrap_in_box
        method handles applying colors uniformly.
        """

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
        max_score = max(entry.score for entry in last_entries)

        lines: list[tuple[str, str | None]] = []
        
        for entry in last_entries:
            date_str = entry.timestamp.strftime("%m-%d")
            ascii_face = self._ascii_for_score(entry.score)
            bar_length = self._calculate_scaled_bar_length(
                entry.score, max_score, max_bar_width=30
            )
            
            # Build the bar as plain text first - no color tags yet
            bar = "█" * bar_length
            
            # Create the complete line content as plain text
            # This ensures width calculations are accurate
            line_text = f"{date_str}: {ascii_face:<4} {bar}"
            
            # Determine the color for the bar based on score
            bar_color = self._bar_color_for_score(entry.score)
            
            # Now we can append with the color as the style parameter
            # The _wrap_in_box method will apply this color to the whole line
            lines.append((line_text, bar_color))

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
        self.border_style = get_border_style(self.theme_names[self.theme_index])  # Add this line
        self.preferences.current_theme = self.theme_names[self.theme_index]
        save_preferences(self.preferences)
        self.render_view()

    def _current_theme_name(self) -> str:
        return self.theme_names[self.theme_index]

    async def _save_current_mood(self) -> None:
        """Save the currently selected mood, optionally with a reflection note.
    
        This method now follows a two-step process:
        1. Show the reflection prompt and wait for user input
        2. Save the mood with whatever note they provided (or None)
    
        The async/await pattern here is what makes the modal dialog work.
        We pause execution, show the reflection screen, and only continue
        once the user has made their choice.
        """
        label, score = MOOD_OPTIONS[self.selected_index]
        # Show the reflection prompt and wait for the result
        # The result will be either a note string or None
        note_text = await self.app.push_screen_wait(
            ReflectionPromptScreen(label, score, self.palette)
        )

        # Now we have all the information we need to create the entry
        entries = load_moods()
        entries.append(
            MoodEntry(
                timestamp=datetime.now(),
                score=score,
                tag=None,  # We're not using tags yet, but the field is ready
                note=note_text,  # This is now the user's reflection
            )
        )
        save_moods(entries)
        self.sound_manager.play_save()  # Add this line


        # Save preferences so the selected mood persists
        self.preferences.last_selected_mood_index = self.selected_index
        save_preferences(self.preferences)

        # Show confirmation feedback to the user
        # The message changes based on whether they added a note
        if note_text:
            self.app.notify(
                f"✓ Mood saved: {label} (with note)",
                severity="information",
                timeout=2
            )
        else:
            self.app.notify(
                f"✓ Mood saved: {label}",
                severity="information",
                timeout=2
            )

        # Refresh the display to show the new entry in history
        self.render_view()

    def _calculate_scaled_bar_length(self, score: int, max_score: int, max_bar_width: int = 20) -> int:
        """Calculate bar length scaled relative to the maximum score in history."""
        if max_score == 100:
            return 0
        return max(1, int((score / max_score) * max_bar_width))