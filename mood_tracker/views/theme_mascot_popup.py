"""Theme mascot reveal popup that appears when cycling themes.

This creates a delightful moment when users change themes by showing
the theme's ASCII mascot character with a brief flourish before fading away.
"""

from __future__ import annotations

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static
from textual.containers import Vertical


class ThemeMascotPopup(Screen):
    """A temporary popup showing the new theme's mascot.
    
    This screen appears briefly when users cycle through themes,
    displaying the adorable ASCII mascot for the selected theme.
    It auto-dismisses after a few seconds to avoid interrupting workflow.
    """
    
    def __init__(self, theme_name: str, mascot_art: str, palette) -> None:
        """Initialize the mascot popup.
        
        Args:
            theme_name: Display name of the theme
            mascot_art: The ASCII art for this theme's mascot
            palette: Color palette for styling
        """
        super().__init__()
        self.theme_name = theme_name
        self.mascot_art = mascot_art
        self.palette = palette
    
    def compose(self) -> ComposeResult:
        """Build the popup UI with mascot and theme name."""
        with Vertical(id="mascot-popup"):
            # Theme name at the top
            yield Static(
                self.theme_name,
                id="mascot-theme-name"
            )
            
            # The adorable ASCII mascot
            yield Static(
                self.mascot_art,
                id="mascot-art"
            )
    
    def on_mount(self) -> None:
        """Auto-dismiss the popup after 2 seconds."""
        self.set_timer(2.0, self._auto_dismiss)
    
    def _auto_dismiss(self) -> None:
        """Callback method for auto-dismissing the popup."""
        self.dismiss()
