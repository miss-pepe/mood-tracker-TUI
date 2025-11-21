from __future__ import annotations

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static, Input, Button
from textual.containers import Vertical, Horizontal
from textual import events


class ReflectionPromptScreen(Screen):
    """Modal dialog for optionally adding a note after mood selection.
    
    This screen appears after a user selects their mood, offering them
    a chance to add context or thoughts. The note is completely optional,
    and users can skip past it if they prefer quick logging.
    """

    def __init__(self, mood_label: str, mood_score: int, theme_palette) -> None:
        """Initialize the reflection prompt with mood context.
        
        Args:
            mood_label: The text description of the mood (e.g., ":) Good")
            mood_score: The numeric score for this mood (1-10)
            theme_palette: The current color palette for styling the modal
        """
        super().__init__()
        self.mood_label = mood_label
        self.mood_score = mood_score
        self.palette = theme_palette

    def compose(self) -> ComposeResult:
        """Build the UI components for the reflection prompt.
        
        We're creating a centered modal box that feels conversational
        and gives clear guidance about what's expected. The layout uses
        a vertical container to stack elements naturally.
        """
        with Vertical(id="reflection-modal"):
            # Show them what they just selected as confirmation
            yield Static(
                f"You selected: {self.mood_label}",
                id="mood-confirmation"
            )
            
            # Provide a friendly, conversational prompt
            yield Static(
                "Want to jot down a note? (optional)",
                id="reflection-prompt"
            )
            
            # The input field with helpful placeholder text that
            # shows the kind of detail that's useful to capture
            yield Input(
                placeholder="Had a good morning, drank my iced coffee...",
                id="note-input"
            )
            
            # Action buttons laid out horizontally for easy scanning
            with Horizontal(id="button-row"):
                yield Button(
                    "Save with note",
                    variant="primary",
                    id="save-with-note"
                )
                yield Button(
                    "Skip note",
                    variant="default",
                    id="skip-note"
                )
    
    def on_mount(self) -> None:
        """Focus the input field when the screen appears.
        
        This is a small usability detail that saves the user a keystroke.
        They can immediately start typing their note without needing to
        tab to the input field first.
        """
        input_widget = self.query_one("#note-input", Input)
        input_widget.focus()
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button clicks for saving or skipping the note.
        
        When a button is clicked, we need to dismiss this screen and
        return data to whoever called it. Textual's dismiss() method
        lets us return a value, which the calling screen can then use.
        """
        if event.button.id == "save-with-note":
            # Grab whatever they typed, strip whitespace, and treat
            # empty strings as None so we don't save blank notes
            input_widget = self.query_one("#note-input", Input)
            note_text = input_widget.value.strip() or None
            # Return the note text to the calling screen
            self.dismiss(note_text)
        elif event.button.id == "skip-note":
            # Return None to indicate they don't want to add a note
            self.dismiss(None)
    
    async def on_key(self, event: events.Key) -> None:
        """Handle keyboard shortcuts for power users.
        
        We want to support quick workflows, so Enter should save
        and Escape should skip. This lets keyboard-focused users
        move through the app without reaching for the mouse.
        """
        key = event.key.lower()
        
        if key == "enter":
            # Treat Enter as "save with whatever's in the input"
            input_widget = self.query_one("#note-input", Input)
            note_text = input_widget.value.strip() or None
            self.dismiss(note_text)
        elif key == "escape":
            # Treat Escape as "skip this entirely"
            self.dismiss(None)