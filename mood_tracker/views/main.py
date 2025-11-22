from __future__ import annotations
from .reflection import ReflectionPromptScreen
from .export import ExportScreen
from .history import HistoryScreen
from .theme_mascot_popup import ThemeMascotPopup
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
from ..constants import MOOD_OPTIONS
from textual import work
import asyncio
import random

# Box sizing - made responsive
MIN_BOX_WIDTH = 100                 # Minimum box width
MAX_BOX_WIDTH = 140                 # Maximum box width
BOX_WIDTH = 125                     # Default/preferred box width
INNER_WIDTH = BOX_WIDTH - 2

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
import asyncio

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
                "│    M  -  Monthly calendar view           │\n"
                "│    E  -  Export data                     │\n"
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

class BorderRow(Static):
    """A generic row with borders."""
    def __init__(self, content: str, border_style, palette, style: str = None, centered: bool = False, id: str = None):
        super().__init__(id=id)
        self.content_text = content
        self.border_style = border_style
        self.palette = palette
        self.custom_text_style = style
        self.centered = centered
        self.render_content()

    def render_content(self):
        inner_width = INNER_WIDTH
        if self.centered:
            content = self.content_text.center(inner_width)
        else:
            content = self.content_text.ljust(inner_width)
        
        color = self.custom_text_style or self.palette.text_primary
        # Apply color to content with padding
        content = f" {content} "
        content = f"[{color}]{content}[/]"
        
        # Border
        border_color = self.border_style.border_color
        line = f"[{border_color}]{self.border_style.vertical}[/]{content}[{border_color}]{self.border_style.vertical}[/]"
        self.update(line)

    def update_content(self, content: str, style: str = None):
        self.content_text = content
        if style:
            self.custom_text_style = style
        self.render_content()

class SectionDivider(Static):
    def __init__(self, label: str, border_style):
        super().__init__()
        self.label = label
        self.border_style = border_style
        self.render_content()

    def render_content(self):
        label_with_spaces = f" {self.label} "
        remaining = INNER_WIDTH - len(label_with_spaces)
        left_dashes = remaining // 2
        right_dashes = remaining - left_dashes
        
        b = self.border_style
        line = (
            f"{b.divider_left}"
            f"{b.divider_horizontal * left_dashes}"
            f"{label_with_spaces}"
            f"{b.divider_horizontal * right_dashes}"
            f"{b.divider_right}"
        )
        self.update(f"[{b.border_color}]{line}[/]")

class TopBorder(Static):
    def __init__(self, border_style):
        super().__init__()
        self.border_style = border_style
        self.render_content()
        
    def render_content(self):
        b = self.border_style
        line = f"{b.top_left}{b.horizontal * INNER_WIDTH}{b.top_right}"
        self.update(f"[{b.border_color}]{line}[/]")

class BottomBorder(Static):
    def __init__(self, border_style):
        super().__init__()
        self.border_style = border_style
        self.render_content()

    def render_content(self):
        b = self.border_style
        line = f"{b.bottom_left}{b.horizontal * INNER_WIDTH}{b.bottom_right}"
        self.update(f"[{b.border_color}]{line}[/]")

class MoodOption(Static):
    """Individual mood option widget with animation support."""
    
    def __init__(self, label: str, score: int, border_style, palette, is_selected: bool = False, centered: bool = True):
        super().__init__()
        self.label = label
        self.score = score
        self.border_style = border_style
        self.palette = palette
        self.is_selected = is_selected
        self.centered = centered
        self.render_content()
    
    def render_content(self):
        """Render the mood option with appropriate styling."""
        marker = "(x)" if self.is_selected else "( )"
        
        content = f"{marker} {self.label}"
        if self.centered:
            content = content.center(INNER_WIDTH)
        else:
            content = content.ljust(INNER_WIDTH)
        # Add padding
        content = f" {content} "
        
        if self.is_selected:
            content = f"[bold {self.palette.accent_high}]{content}[/]"
        else:
            content = f"[{self.palette.text_primary}]{content}[/]"
            
        border_color = self.border_style.border_color
        line = f"[{border_color}]{self.border_style.vertical}[/]{content}[{border_color}]{self.border_style.vertical}[/]"
        self.update(line)
    
    def set_selected(self, selected: bool, color: str = None):
        self.is_selected = selected
        # We can use the color if provided
        marker = "(x)" if self.is_selected else "( )"
        content = f"{marker} {self.label}"
        if self.centered:
            content = content.center(INNER_WIDTH)
        else:
            content = content.ljust(INNER_WIDTH)
        # Add padding
        content = f" {content} "
        
        if self.is_selected:
            c = color if color else self.palette.accent_high
            content = f"[bold {c}]{content}[/]"
            # Pulse animation
            self.styles.animate("opacity", value=1.0, duration=0.15, easing="out_cubic")
        else:
            # Dim slightly
            c = color if color else self.palette.text_primary
            content = f"[{c}]{content}[/]"
            
        border_color = self.border_style.border_color
        line = f"[{border_color}]{self.border_style.vertical}[/]{content}[{border_color}]{self.border_style.vertical}[/]"
        self.update(line)

class TimelineEntry(Static):
    """Single mood entry in a timeline card."""
    
    def __init__(self, time_str: str, mood_label: str, bar_length: int, color: str, border_style, palette, frequency_str: str = None):
        super().__init__()
        self.time_str = time_str
        self.mood_label = mood_label
        self.bar_length = bar_length
        self.color = color
        self.border_style = border_style
        self.palette = palette
        self.frequency_str = frequency_str
        self._update_display()
    
    def _update_display(self):
        """Update the entry display."""
        # Add spacing between bar blocks
        bar_blocks = " ".join(["█" for _ in range(self.bar_length)])
        
        # Build line with frequency if available
        if self.frequency_str:
            line_text = f"{self.time_str:<9}  {bar_blocks:<20}  {self.mood_label:<8}  [{self.frequency_str}]"
        else:
            line_text = f"{self.time_str:<9}  {bar_blocks:<20}  {self.mood_label}"
        
        # Pad and border
        content = line_text.ljust(INNER_WIDTH - 2)
        content = f" {content} "
        content = f"[{self.color}]{content}[/]"
        
        border_color = self.border_style.border_color
        line = f"[{border_color}]{self.border_style.vertical}[/]{content}[{border_color}]{self.border_style.vertical}[/]"
        self.update(line)


class TimelineCardTop(Static):
    """Top border of a timeline card."""
    
    def __init__(self, border_style):
        super().__init__()
        self.border_style = border_style
        self.render_content()
    
    def render_content(self):
        b = self.border_style
        # Use box drawing characters for card top
        line = f"{b.top_left}{b.horizontal * (INNER_WIDTH - 2)}{b.top_right}"
        self.update(f"[{b.border_color}]{line}[/]")


class TimelineCardBottom(Static):
    """Bottom border of a timeline card."""
    
    def __init__(self, border_style):
        super().__init__()
        self.border_style = border_style
        self.render_content()
    
    def render_content(self):
        b = self.border_style
        # Use box drawing characters for card bottom
        line = f"{b.bottom_left}{b.horizontal * (INNER_WIDTH - 2)}{b.bottom_right}"
        self.update(f"[{b.border_color}]{line}[/]")


class TimelineDateHeader(Static):
    """Date header for timeline cards."""
    
    def __init__(self, date_str: str, border_style, palette):
        super().__init__()
        self.date_str = date_str
        self.border_style = border_style
        self.palette = palette
        self.render_content()
    
    def render_content(self):
        line_text = f"{self.date_str}"
        content = line_text.ljust(INNER_WIDTH)
        content = f" {content} "
        content = f"[bold {self.palette.accent_high}]{content}[/]"
        
        border_color = self.border_style.border_color
        line = f"[{border_color}]{self.border_style.vertical}[/]{content}[{border_color}]{self.border_style.vertical}[/]"
        self.update(line)


class HorizontalMoodSelector(Static):
    """Horizontal mood selector with color-coded options."""
    
    def __init__(self, border_style, palette, selected_index: int = 0):
        super().__init__()
        self.border_style = border_style
        self.palette = palette
        self.selected_index = selected_index
        self.render_content()
    
    def render_content(self):
        # Build mood options with colors
        options = []
        colors = ["bright_green", "cyan", "yellow", "magenta", "bright_red"]
        labels = ["Great", "Good", "Meh", "Bad", "Awful"]
        
        # Calculate visible text length (without markup)
        visible_parts = []
        for idx, (label, color) in enumerate(zip(labels, colors)):
            if idx == self.selected_index:
                # Selected option: bold and underlined with arrow
                options.append(f"[{color} bold underline]► {label} ◄[/]")
                visible_parts.append(f"► {label} ◄")
            else:
                options.append(f"[{color}]■ {label}[/]")
                visible_parts.append(f"■ {label}")
        
        selector_text = "  ".join(options)
        visible_text = "  ".join(visible_parts)
        
        # Calculate padding needed for centering
        visible_length = len(visible_text)
        padding_needed = max(0, (INNER_WIDTH - visible_length) // 2)
        padding = " " * padding_needed
        
        content = f"{padding}{selector_text}"
        content = content.ljust(INNER_WIDTH)
        content = f" {content} "
        
        border_color = self.border_style.border_color
        line = f"[{border_color}]{self.border_style.vertical}[/]{content}[{border_color}]{self.border_style.vertical}[/]"
        self.update(line)
    
    def set_selected(self, index: int):
        """Update the selected mood index."""
        self.selected_index = index
        self.render_content()


class HistoryBar(Static):
    """Animated history bar widget."""
    
    def __init__(self, date_str: str, ascii_face: str, final_length: int, color: str, border_style, palette):
        super().__init__()
        self.date_str = date_str
        self.ascii_face = ascii_face
        self.final_length = final_length
        self.color = color
        self.border_style = border_style
        self.palette = palette
        self.current_length = 0
        self._update_display()
    
    def _update_display(self):
        """Update the bar display."""
        bar = "█" * self.current_length
        line_text = f"{self.date_str}: {self.ascii_face:<4} {bar}"
        
        # Pad and border
        content = line_text.ljust(INNER_WIDTH)
        # Add padding
        content = f" {content} "
        content = f"[{self.color}]{content}[/]"
        
        border_color = self.border_style.border_color
        line = f"[{border_color}]{self.border_style.vertical}[/]{content}[{border_color}]{self.border_style.vertical}[/]"
        self.update(line)
    
    async def animate_growth(self):
        """Gradually grow the bar to its final length."""
        step = max(1, self.final_length // 10)  # Grow in ~10 steps
        # Reset to 0 before animating
        self.current_length = 0
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

class MainScreen(Screen):
    """Single-screen UI that matches the ASCII mockup."""
    show_history = True
    show_extended_history = False  # Toggle between 12 entries and all entries
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
        self.preferences = load_preferences()
        self.theme_names = list(THEMES.keys())
        try:
            self.theme_index = self.theme_names.index(self.preferences.current_theme)
        except ValueError:
            self.theme_index = self.theme_names.index(DEFAULT_THEME_NAME)
        
        self.palette = get_palette(self.theme_names[self.theme_index])
        self.border_style = get_border_style(self.theme_names[self.theme_index])
        self.selected_index = self.preferences.last_selected_mood_index
        self.show_history = self.preferences.show_history_panel
        self.sound_manager = SoundManager()

        from textual.containers import Vertical
        
        with Vertical():
            self.mood_companion = MoodCompanion(initial_score=5)
            self.mood_companion.palette = self.palette
            yield self.mood_companion
            
            with Vertical(id="box-container"):
                yield TopBorder(self.border_style)
                
                today_str = date.today().isoformat()
                yield BorderRow(f"Date: {today_str}", self.border_style, self.palette, centered=True)
                yield BorderRow("", self.border_style, self.palette)
                
                yield BorderRow("How are you feeling today?", self.border_style, self.palette, style=f"bold {self.palette.accent_high}", centered=True)
                yield BorderRow("", self.border_style, self.palette)
                yield BorderRow("[←/→ to select, Enter to confirm]", self.border_style, self.palette, style=self.palette.text_muted, centered=True)
                yield BorderRow("", self.border_style, self.palette)
                
                # Horizontal Mood Selector
                self.horizontal_selector = HorizontalMoodSelector(self.border_style, self.palette, self.selected_index)
                yield self.horizontal_selector
                
                # Keep mood_options list for compatibility
                self.mood_options = []
                
                yield BorderRow("", self.border_style, self.palette)
                yield BorderRow("", self.border_style, self.palette)
                
                # History Section
                self.history_divider = SectionDivider("Mood History", self.border_style)
                yield self.history_divider
                
                with Vertical(id="history-list"):
                    pass
                
                self.history_footer = BorderRow("", self.border_style, self.palette, style=self.palette.accent_low, id="history-footer", centered=True)
                yield self.history_footer
                yield BorderRow("", self.border_style, self.palette)
                yield BorderRow("", self.border_style, self.palette)
                
                yield BottomBorder(self.border_style)
            
            self.toast = ToastNotification()
            yield self.toast

    def on_mount(self) -> None:
        # Initialize mood companion
        _, initial_score = MOOD_OPTIONS[self.selected_index]
        self.mood_companion.update_mood(initial_score)
        
        # Ensure history is visible by default
        self.show_history = True
        self._refresh_history()
        self._update_history_visibility()

    async def on_key(self, event: events.Key) -> None:
        """Handle keyboard input for navigation and actions."""
        key = event.key.lower()

        if key in ("left", "h"):
            self._change_selection(-1)

        elif key in ("right", "l"):
            self._change_selection(1)

        elif key == "enter" or key == "s":
            self._save_current_mood()

        elif key == "t":
            self._cycle_theme()

        elif key == "h":
            # Toggle extended history view (12 vs all entries)
            self.show_extended_history = not self.show_extended_history
            self._refresh_history()
            
            # Toggle footer visibility too
            if self.history_footer.styles.display == "block":
                self.history_footer.styles.display = "none"
            else:
                self.history_footer.styles.display = "block"

        elif key == "question_mark":
            self.app.push_screen(HelpScreen())

        elif key == "e":
            self.app.push_screen(ExportScreen(self.palette))

        elif key == "v":
            self.app.push_screen(HistoryScreen())

        elif key == "m":
            self.app.push_screen(MonthlyCalendarScreen(self.palette, self.border_style))

    def _change_selection(self, delta: int):
        old_index = self.selected_index
        self.selected_index = (self.selected_index + delta) % len(MOOD_OPTIONS)
        self.preferences.last_selected_mood_index = self.selected_index
        save_preferences(self.preferences)
        self.sound_manager.play_selection()
        
        # Update mood companion
        _, score = MOOD_OPTIONS[self.selected_index]
        self.mood_companion.update_mood(score)
        
        # Update horizontal selector
        self.horizontal_selector.set_selected(self.selected_index)

    def _update_history_visibility(self):
        history_list = self.query_one("#history-list")
        
        if self.show_history:
            self.history_divider.styles.display = "block"
            history_list.styles.display = "block"
            self.history_footer.styles.display = "block"
        else:
            self.history_divider.styles.display = "none"
            history_list.styles.display = "none"
            self.history_footer.styles.display = "none"

    def _refresh_history(self) -> None:
        """Refresh the history list with grouped timeline cards."""
        entries = load_moods()
        history_list = self.query_one("#history-list")
        history_list.remove_children()
        
        if not entries:
            history_list.mount(
                BorderRow("No mood history yet. Log something above to get started.", 
                         self.border_style, self.palette, 
                         style=f"dim {self.palette.text_muted}", centered=True)
            )
            self._update_history_footer(entries)
            return
        
        # Show last 12 entries (or all if extended view)
        display_count = len(entries) if self.show_extended_history else 12
        last_entries = entries[-display_count:]
        
        # Group entries by date
        from collections import defaultdict
        entries_by_date = defaultdict(list)
        for entry in last_entries:
            date_key = entry.timestamp.strftime("%b %d")  # "Nov 22"
            entries_by_date[date_key].append(entry)
        
        # Render grouped timeline cards
        for date_str in entries_by_date.keys():
            # Date header
            history_list.mount(TimelineDateHeader(date_str, self.border_style, self.palette))
            
            # Card top border
            history_list.mount(TimelineCardTop(self.border_style))
            
            # Each mood entry for this day
            day_entries = entries_by_date[date_str]
            for idx, entry in enumerate(day_entries):
                time_str = entry.timestamp.strftime("%I:%M %p")  # "08:00 AM"
                mood_label = self._label_for_score(entry.score)
                bar_length = self._fixed_bar_length_for_score(entry.score)
                color = self._bar_color_for_score(entry.score)
                
                # Calculate frequency (time since previous entry)
                frequency_str = None
                if idx > 0:
                    prev_entry = day_entries[idx - 1]
                    time_gap = (entry.timestamp - prev_entry.timestamp).total_seconds()
                    frequency_str = self._format_time_gap(time_gap)
                elif len(last_entries) > len(day_entries):
                    # Check if there's a previous entry from another day
                    entry_index = last_entries.index(entry)
                    if entry_index > 0:
                        prev_entry = last_entries[entry_index - 1]
                        time_gap = (entry.timestamp - prev_entry.timestamp).total_seconds()
                        frequency_str = self._format_time_gap(time_gap)
                
                timeline_entry = TimelineEntry(time_str, mood_label, bar_length, color,
                                              self.border_style, self.palette, frequency_str)
                history_list.mount(timeline_entry)
            
            # Card bottom border
            history_list.mount(TimelineCardBottom(self.border_style))
            
            # Empty line between cards
            history_list.mount(BorderRow("", self.border_style, self.palette))
        
        # Update footer with stats
        self._update_history_footer(entries)
    
    def _update_history_footer(self, entries) -> None:
        """Update the history footer with streak and stats."""
        if not entries:
            footer_text = "No entries yet"
        else:
            total = len(entries)
            
            # Calculate streak (consecutive days above Meh = score > 5)
            streak = 0
            today = datetime.now().date()
            for i in range(len(entries) - 1, -1, -1):
                entry_date = entries[i].timestamp.date()
                # Check if it's a consecutive day
                if (today - entry_date).days == streak and entries[i].score > 5:
                    streak += 1
                else:
                    break
            
            # Get current theme name
            theme_name = self._current_theme_name().replace('_', ' ').title()
            
            if streak > 0:
                footer_text = f"✨ {streak}-day streak above Meh! | {total} moods logged | Theme: {theme_name}"
            else:
                footer_text = f"{total} moods logged | Theme: {theme_name}"
        
        self.history_footer.update_content(footer_text, style=self.palette.accent_low)

    def _cycle_theme(self) -> None:
        """Cycle through available themes and update the UI."""
        self.theme_index = (self.theme_index + 1) % len(self.theme_names)
        self.palette = get_palette(self.theme_names[self.theme_index])            
        self.border_style = get_border_style(self.theme_names[self.theme_index])
        self.preferences.current_theme = self.theme_names[self.theme_index]
        save_preferences(self.preferences)
        
        # Show the theme mascot popup!
        theme_name = self._current_theme_name()
        display_name = ' '.join(word.capitalize() for word in theme_name.split('_'))
        mascot_art = THEME_MASCOTS.get(display_name, "No mascot available")
        self.app.push_screen(ThemeMascotPopup(display_name, mascot_art, self.palette))
        
        # Update the mood companion
        self.mood_companion.palette = self.palette
        _, score = MOOD_OPTIONS[self.selected_index]
        self.mood_companion.update_mood(score)
        
        # Update Top/Bottom borders
        self.query_one(TopBorder).border_style = self.border_style
        self.query_one(TopBorder).render_content()
        self.query_one(BottomBorder).border_style = self.border_style
        self.query_one(BottomBorder).render_content()
        
        # Update Divider
        self.history_divider.border_style = self.border_style
        self.history_divider.render_content()
        
        # Update BorderRows
        for row in self.query(BorderRow):
            row.border_style = self.border_style
            row.palette = self.palette
            row.render_content()
        
        # Update HorizontalMoodSelector
        self.horizontal_selector.border_style = self.border_style
        self.horizontal_selector.palette = self.palette
        self.horizontal_selector.render_content()
        
        # Update MoodOptions (kept for compatibility)
        for opt in self.mood_options:
            opt.border_style = self.border_style
            opt.palette = self.palette
            opt.render_content()
            
        # Update HistoryBars
        self._refresh_history()

    def _current_theme_name(self) -> str:
        return self.theme_names[self.theme_index]

    @work(exclusive=True)
    async def _save_current_mood(self) -> None:
        label, score = MOOD_OPTIONS[self.selected_index]

        note_text = await self.app.push_screen_wait(
            ReflectionPromptScreen(label, score, self.palette)
        )

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

        self.preferences.last_selected_mood_index = self.selected_index
        save_preferences(self.preferences)

        emoji = self._ascii_for_score(score)
        if note_text:
            message = f"✓ Mood saved! You picked {emoji} {label} today (with note)"
        else:
            message = f"✓ Mood saved! You picked {emoji} {label} today"
        
        asyncio.create_task(self.toast.show(message, self.palette))

        self._refresh_history()

    def _bar_color_for_score(self, score: int) -> str:
        if score >= 9: return "bright_green"
        elif score >= 7: return "cyan"
        elif score >= 5: return "yellow"
        elif score >= 3: return "magenta"
        else: return "bright_red"

    def _ascii_for_score(self, score: int) -> str:
        if score >= 9: return ":D"
        if score >= 7: return ":)"
        if score >= 5: return ":|"
        if score >= 3: return ":("
        return ":'("
    
    def _format_time_gap(self, seconds: float) -> str:
        """Format time gap in human-readable format."""
        if seconds < 60:
            return "< 1m"
        elif seconds < 3600:
            minutes = int(seconds / 60)
            return f"{minutes}m"
        elif seconds < 86400:
            hours = int(seconds / 3600)
            minutes = int((seconds % 3600) / 60)
            if minutes > 0:
                return f"{hours}h {minutes}m"
            return f"{hours}h"
        else:
            days = int(seconds / 86400)
            hours = int((seconds % 86400) / 3600)
            if hours > 0:
                return f"{days}d {hours}h"
            return f"{days}d"
    
    def _label_for_score(self, score: int) -> str:
        """Get mood label for score."""
        if score >= 9: return "Great"
        if score >= 7: return "Good"
        if score >= 5: return "Meh"
        if score >= 3: return "Bad"
        return "Awful"
    
    def _fixed_bar_length_for_score(self, score: int) -> int:
        """Get fixed bar length based on mood intensity (not relative)."""
        # Great = 8 blocks, Awful = 2 blocks
        if score >= 9: return 8
        if score >= 7: return 6
        if score >= 5: return 4
        if score >= 3: return 3
        return 2

    def _calculate_scaled_bar_length(self, score: int, max_score: int, max_bar_width: int = 20) -> int:
        if max_score == 100: return 0
        return max(1, int((score / max_score) * max_bar_width))