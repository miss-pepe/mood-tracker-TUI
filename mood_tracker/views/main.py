from __future__ import annotations
from .reflection import ReflectionPromptScreen
from .export import ExportScreen
from .theme_mascot_popup import ThemeMascotPopup
from .history import DetailedHistoryScreen
from datetime import date, datetime
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static
from textual import events
from ..models.storage import load_moods, save_moods, MoodEntry
from ..theme import DEFAULT_THEME_NAME, THEMES, get_palette, get_border_style
from ..models.preferences import load_preferences, save_preferences, UserPreferences
from .calendar import MonthlyCalendarScreen
from ..audio import SoundManager
from ..widgets.mood_companion import MoodCompanion
from ..utils import ascii_for_score, get_mood_color
from textual import work
import asyncio
import random

# Box sizing - made responsive
MIN_BOX_WIDTH = 100                 # Minimum box width
MAX_BOX_WIDTH = 140                 # Maximum box width
BOX_WIDTH = 125                     # Default/preferred box width
INNER_WIDTH = BOX_WIDTH - 2

# Chaos and glitch effect constants
GLITCH_ACTIVATION_CHANCE = 0.08     # 8% chance of glitch on app start or theme change
GLITCH_EFFECT_CHANCE = 0.3          # 30% chance of glitch effects when glitch is active

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
                "│    V  -  Detailed history view           │\n"
                "│    M  -  Monthly calendar view           │\n"
                "│    E  -  Export data                     │\n"
                "│    ?  -  Show this help dialog           │\n"
                "│    Q  -  Quit application                │\n"
                "│                                          │\n"
                "│  Easter Eggs:                            │\n"
                "│    Type C-H-A-O-S for chaos mode 🔥      │\n"
                "│                                          │\n"
                "│  Press ESC or Q to close this dialog     │\n"
                "│                                          │\n"
                "└──────────────────────────────────────────┘",
                id="help-content"
            )
    
    def action_dismiss(self) -> None:
        """Close the help dialog and return to main screen."""
        self.app.pop_screen()

class MoodOption(Static):
    """Individual mood option widget with animation support."""
    
    def __init__(self, label: str, score: int, is_selected: bool = False, palette=None):
        super().__init__()
        self.label = label
        self.score = score
        self.is_selected = is_selected
        self.palette = palette
        self._render()
    
    def _render(self):
        """Render the mood option with appropriate styling."""
        marker = "(x)" if self.is_selected else "( )"
        if self.is_selected and self.palette:
            self.update(f"[bold {self.palette.accent_high}]  {marker} {self.label}[/]")
        else:
            self.update(f"  {marker} {self.label}")
    
    def highlight(self, palette):
        """Animate highlighting this option."""
        self.is_selected = True
        self.palette = palette
        self._render()
        # Pulse animation on selection
        self.styles.animate("opacity", value=1.0, duration=0.15, easing="out_cubic")
    
    def dim(self):
        """Dim this option when deselected."""
        self.is_selected = False
        self._render()
        self.styles.opacity = 0.7

class HistoryBar(Static):
    """Animated history bar widget."""
    
    def __init__(self, date_str: str, ascii_face: str, final_length: int, color: str):
        super().__init__()
        self.date_str = date_str
        self.ascii_face = ascii_face
        self.final_length = final_length
        self.color = color
        self.current_length = 0
        self._update_display()
    
    def _update_display(self):
        """Update the bar display."""
        bar = "█" * self.current_length
        line_text = f"{self.date_str}: {self.ascii_face:<4} {bar}"
        self.update(f"[{self.color}]{line_text}[/]")
    
    async def animate_growth(self):
        """Gradually grow the bar to its final length."""
        step = max(1, self.final_length // 10)  # Grow in ~10 steps
        while self.current_length < self.final_length:
            self.current_length = min(self.current_length + step, self.final_length)
            self._update_display()
            await asyncio.sleep(0.02)

class ToastNotification(Static):
    """Toast notification that slides in and fades out."""
    
    def __init__(self):
        super().__init__("")
        self.styles.visibility = "hidden"
        self.styles.align = ("center", "bottom")
        self.styles.padding = (1, 2)
    
    async def show(self, message: str, palette):
        """Show the toast with animation."""
        self.update(f"[bold {palette.success}]{message}[/]")
        self.styles.visibility = "visible"
        self.styles.opacity = 0.0
        
        # Fade in
        self.styles.animate("opacity", value=1.0, duration=0.2, easing="out_cubic")
        
        # Wait
        await asyncio.sleep(1.5)
        
        # Fade out
        self.styles.animate("opacity", value=0.0, duration=0.3, easing="in_cubic")
        await asyncio.sleep(0.3)
        
        self.styles.visibility = "hidden"

# Direction label constants
DIRECTION_LABEL_NORMAL = "              lower ←──────────── mood →────────────→ higher"
DIRECTION_LABEL_GLITCHED = "              higher ←──────────── mood →────────────→ lower"

# Dramatic mood confirmations
DRAMATIC_CONFIRMATIONS = {
    9: [  # Great
        "✨ peak slay ✨",
        "THRIVING ENERGY DETECTED",
        "Main character moment!",
        "That's what we like to see! 🌟",
    ],
    7: [  # Good
        "Not bad, not bad.",
        "Solid vibes today 👍",
        "We love to see it!",
        "Good energy detected ✨",
    ],
    5: [  # Meh
        "Emotionally beige accepted.",
        "Surviving counts 🤷",
        "Meh is valid too.",
        "Neutral vibes logged.",
    ],
    3: [  # Bad
        "Logging one certified 'ugh' day.",
        "Rough day noted 😤",
        "This too shall pass, friend.",
        "Oof. Logged. 💙",
    ],
    1: [  # Awful
        "Oh, babe. Logging emergency vibes. 💔",
        "I see you struggling. Logged. 🫂",
        "Sending virtual support 💜",
        "We're here with you. 🌙",
    ],
}

def get_dramatic_confirmation(score: int) -> str:
    """Get a dramatic confirmation message for the given mood score."""
    # Find the closest mood category
    if score >= 9:
        key = 9
    elif score >= 7:
        key = 7
    elif score >= 5:
        key = 5
    elif score >= 3:
        key = 3
    else:
        key = 1
    
    return random.choice(DRAMATIC_CONFIRMATIONS[key])

# Glitch faces for chaos moments
GLITCH_FACES = ["(⊙_☉)", "(◉_◎)", "(⊙﹏⊙)", "(◉‿◎)"]

class MainScreen(Screen):
    """Single-screen UI that matches the ASCII mockup."""
    show_history = True
    chaos_mode = False  # Chaos mode easter egg
    chaos_sequence = []  # Track key sequence for chaos activation
    _mood_widgets = []  # Track mood option widgets
    _history_bars = []  # Track history bar widgets

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
        from textual.containers import Vertical
        
        # Main container for layout
        with Vertical():
            # Mood companion at the top
            self.mood_companion = MoodCompanion(initial_score=5)
            yield self.mood_companion
            
            # Main mood tracker view
            self.main_view = Static(id="main-view")
            yield self.main_view
            
            # Toast notification at the bottom
            self.toast = ToastNotification()
            yield self.toast

    def on_mount(self) -> None:
        self.preferences = load_preferences()           # Load user preferences from disk
        self.selected_index = self.preferences.last_selected_mood_index # Restore last selected mood
        self.show_history = self.preferences.show_history_panel
        self.sound_manager = SoundManager()
        
        # Initialize chaos mode tracking - always start fresh each session
        self.chaos_mode = False
        self.chaos_sequence = []
        self.glitch_active = False
        
        # Random glitch moment (8% chance) - gives occasional surprise glitches
        if random.random() < GLITCH_ACTIVATION_CHANCE:
            self.glitch_active = True

        self.theme_names = list(THEMES.keys())          # Set up theme system using saved preference
        try:
            self.theme_index = self.theme_names.index(self.preferences.current_theme)
        except ValueError:
            self.theme_index = self.theme_names.index(DEFAULT_THEME_NAME)         # If saved theme doesn't exist, fall back to default

        self.palette = get_palette(self.theme_names[self.theme_index])
        self.border_style = get_border_style(self.theme_names[self.theme_index])
        
        # Initialize mood companion with current palette and selected mood
        _, initial_score = MOOD_OPTIONS[self.selected_index]
        self.mood_companion.palette = self.palette
        self.mood_companion.update_mood(initial_score)
        
        self.render_view()

    async def on_key(self, event: events.Key) -> None:
        """Handle keyboard input for navigation and actions."""
        key = event.key.lower()
        
        # Track chaos mode sequence (C-H-A-O-S)
        if key in ['c', 'h', 'a', 'o', 's']:
            self.chaos_sequence.append(key)
            # Keep only last 5 keys
            self.chaos_sequence = self.chaos_sequence[-5:]
            # Check if sequence matches "chaos"
            if self.chaos_sequence == ['c', 'h', 'a', 'o', 's']:
                self.chaos_mode = not self.chaos_mode
                self.chaos_sequence = []  # Reset sequence
                chaos_msg = "🔥 CHAOS MODE: ON 🔥" if self.chaos_mode else "Chaos mode: OFF (calm restored)"
                asyncio.create_task(self.toast.show(chaos_msg, self.palette))
                self.render_view()
                return

        if key in ("up", "k"):
            old_index = self.selected_index
            self.selected_index = (self.selected_index - 1) % len(MOOD_OPTIONS)
            self.preferences.last_selected_mood_index = self.selected_index
            save_preferences(self.preferences)
            self.sound_manager.play_selection()
            # Update mood companion
            if hasattr(self, 'mood_companion'):
                _, score = MOOD_OPTIONS[self.selected_index]
                self.mood_companion.update_mood(score)
            # Animate the mood option change
            self._animate_mood_selection_change(old_index, self.selected_index)
            self.render_view()

        elif key in ("down", "j"):
            old_index = self.selected_index
            self.selected_index = (self.selected_index + 1) % len(MOOD_OPTIONS)
            self.preferences.last_selected_mood_index = self.selected_index
            save_preferences(self.preferences)
            self.sound_manager.play_selection()
            # Update mood companion
            if hasattr(self, 'mood_companion'):
                _, score = MOOD_OPTIONS[self.selected_index]
                self.mood_companion.update_mood(score)
            # Animate the mood option change
            self._animate_mood_selection_change(old_index, self.selected_index)
            self.render_view()

        elif key == "enter" or key == "s":
        # Call the worker method without await
        # The @work decorator handles spawning it in the right context
            self._save_current_mood()

        elif key == "t":
            self._cycle_theme()

        elif key == "h":
            self.show_history = not self.show_history
            self.preferences.show_history_panel = self.show_history
            save_preferences(self.preferences)
            self.render_view()
        
        elif key == "v":
            # Open detailed history screen
            self.app.push_screen(DetailedHistoryScreen(self.palette, self.border_style))

        elif key == "question_mark":
            self._show_help_dialog()

        elif key == "e":
            self.app.push_screen(ExportScreen(self.palette))

        elif key == "m":
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

        # Generate and apply section divider dynamically with playful text
        divider_text = "Mood History — your emotional stock chart 📈📉" if not self.chaos_mode else "Mood History — CHAOTIC EDITION 🔥"
        divider = self._create_section_divider(divider_text)
        lines.append(self._apply_padding(self._apply_border_color(divider), padding))

        # Render history section if enabled
        if self.show_history:
            for content, style in self._build_history_section_lines():
                lines.append(self._wrap_in_box(content, style, padding))

        # Generate and apply bottom border dynamically
        bottom_border = self._create_bottom_border()
        lines.append(self._apply_padding(self._apply_border_color(bottom_border), padding))
        
        # Add status strip
        lines.append(self._build_status_strip(padding))

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
    
    def _build_status_strip(self, padding: int) -> str:
        """Build the status strip at the bottom."""
        entries = load_moods()
        entry_count = len(entries)
        theme_name = self._current_theme_name().replace("_", " ").title()
        chaos_status = "ON 🔥" if self.chaos_mode else "OFF"
        
        status = f"theme: {theme_name} | chaos: {chaos_status} | entries: {entry_count}"
        colored_status = f"[{self.palette.text_muted}]{status}[/]"
        return self._apply_padding(colored_status, padding)
    
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

        for idx, (label, score) in enumerate(MOOD_OPTIONS):        # Mood options
            marker = "(x)" if idx == self.selected_index else "( )"
            # Color-coded moods with consistent colors
            mood_color = get_mood_color(score)
            # Enhanced styling for selected option with pulse effect
            if idx == self.selected_index:
                style = f"bold {mood_color}"
            else:
                style = mood_color
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
            ascii_face = ascii_for_score(entry.score)
            bar_length = self._calculate_scaled_bar_length(
                entry.score, max_score, max_bar_width=30
            )
            
            # Build the bar as plain text first - no color tags yet
            bar = "█" * bar_length
            
            # Add note indicator if present
            note_indicator = " ✏️" if entry.note else ""
            
            # Create the complete line content as plain text
            # This ensures width calculations are accurate
            line_text = f"{date_str}: {ascii_face:<4} {bar}{note_indicator}"
            
            # Use consistent color coding for mood scores
            bar_color = get_mood_color(entry.score)
            
            # Now we can append with the color as the style parameter
            # The _wrap_in_box method will apply this color to the whole line
            lines.append((line_text, bar_color))

        while len(lines) < 5:
            lines.append(("", None))

        lines.append(("", None))
        
        # Glitch effect: occasionally invert the direction label
        if self.glitch_active and random.random() < GLITCH_EFFECT_CHANCE:
            direction_text = DIRECTION_LABEL_GLITCHED
        else:
            direction_text = DIRECTION_LABEL_NORMAL
        
        lines.append((direction_text, self.palette.accent_low))
        lines.append(("", None))

        return lines



    def _cycle_theme(self) -> None:
        """Cycle through available themes and update the UI."""
        self.theme_index = (self.theme_index + 1) % len(self.theme_names)
        self.palette = get_palette(self.theme_names[self.theme_index])            
        self.border_style = get_border_style(self.theme_names[self.theme_index])
        self.preferences.current_theme = self.theme_names[self.theme_index]
        save_preferences(self.preferences)
        
        # Random glitch moment on theme change (8% chance to toggle)
        # This creates unpredictable glitches that can turn on or off randomly
        if random.random() < GLITCH_ACTIVATION_CHANCE:
            self.glitch_active = not self.glitch_active
        
        # Show the theme mascot popup!
        theme_name = self._current_theme_name()
        # Convert snake_case to Title Case for display
        display_name = ' '.join(word.capitalize() for word in theme_name.split('_'))
        mascot_art = THEME_MASCOTS.get(display_name, "No mascot available")
        
        # Occasionally show glitchy mascot (30% chance when glitch is active)
        if self.glitch_active and random.random() < GLITCH_EFFECT_CHANCE:
            mascot_art = random.choice(GLITCH_FACES)
        
        self.app.push_screen(ThemeMascotPopup(display_name, mascot_art, self.palette))
        
        # Update the mood companion with current theme
        if hasattr(self, 'mood_companion'):
            self.mood_companion.palette = self.palette
            _, score = MOOD_OPTIONS[self.selected_index]
            self.mood_companion.update_mood(score)
        
        self.render_view()

    def _current_theme_name(self) -> str:
        return self.theme_names[self.theme_index]

    @work(exclusive=True)
    async def _save_current_mood(self) -> None:
        """Save the currently selected mood, optionally with a reflection note.

        This method runs as a Textual worker, which allows it to wait for
        the reflection screen to close without blocking the main event loop.
        The exclusive=True parameter ensures only one save operation runs
        at a time, preventing users from accidentally saving multiple moods
        if they press Enter repeatedly.

        The async/await pattern here is what makes the modal dialog work.
        We pause execution, show the reflection screen, and only continue
        once the user has made their choice.
        """
        label, score = MOOD_OPTIONS[self.selected_index]

        # Show the reflection prompt and wait for the result
        # This await is now safe because we're running in a worker context
        note_text = await self.app.push_screen_wait(
            ReflectionPromptScreen(label, score, self.palette)
        )

        # Now we have all the information we need to create the entry
        entries = load_moods()
        entries.append(
            MoodEntry(
                timestamp=datetime.now(),
                score=score,
                tag=None,
                note=note_text,
            )
        )
        save_moods(entries)
        self.sound_manager.play_save()

        # Save preferences so the selected mood persists
        self.preferences.last_selected_mood_index = self.selected_index
        save_preferences(self.preferences)

        # Show animated toast notification with dramatic confirmation
        emoji = ascii_for_score(score)
        dramatic = get_dramatic_confirmation(score)
        
        if note_text:
            message = f"✓ SYSTEM: {dramatic}\n{emoji} {label} logged (with note)"
        else:
            message = f"✓ SYSTEM: {dramatic}\n{emoji} {label} logged"
        
        # Trigger toast animation
        asyncio.create_task(self.toast.show(message, self.palette))

        # Refresh the display to show the new entry in history
        self.render_view()
        # Animate the new history bars
        await self._animate_history_bars()

    def _calculate_scaled_bar_length(self, score: int, max_score: int, max_bar_width: int = 20) -> int:
        """Calculate bar length scaled relative to the maximum score in history."""
        if max_score == 100:
            return 0
        return max(1, int((score / max_score) * max_bar_width))
    
    def _animate_mood_selection_change(self, old_index: int, new_index: int) -> None:
        """Animate the mood option selection change with pulse effect."""
        # This creates a visual pulse effect when changing selections
        # The render_view() call will handle the actual visual update
        pass
    
    async def _animate_history_bars(self) -> None:
        """Animate history bars growing from empty to full."""
        entries = load_moods()
        if not entries:
            return
        
        last_entries = entries[-5:]
        max_score = max(entry.score for entry in last_entries)
        
        # Animate each bar sequentially with a slight stagger
        for i, entry in enumerate(last_entries):
            date_str = entry.timestamp.strftime("%m-%d")
            ascii_face = ascii_for_score(entry.score)
            bar_length = self._calculate_scaled_bar_length(
                entry.score, max_score, max_bar_width=30
            )
            
            # Small delay to stagger the animations
            await asyncio.sleep(0.05 * i)