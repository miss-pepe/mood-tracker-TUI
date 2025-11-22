from __future__ import annotations

from pathlib import Path
from datetime import datetime

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static, Button
from textual.containers import Vertical, Horizontal

from ..models.storage import load_moods
from ..models.export import export_to_csv, export_to_json, export_to_markdown


class ExportScreen(Screen):
    """Modal screen for choosing export format and exporting data.
    
    This screen presents the user with three export options and handles
    the actual file writing. Files are saved to the user's Downloads
    folder with timestamped names to avoid overwriting.
    """

    def __init__(self, theme_palette) -> None:
        """Initialize the export screen with theme information.
        
        Args:
            theme_palette: Current color palette for styling
        """
        super().__init__()
        self.palette = theme_palette

    def compose(self) -> ComposeResult:
        """Build the export format selection interface."""
        with Vertical(id="export-modal"):
            yield Static(
                "Export Your Mood Data",
                id="export-title"
            )
            
            yield Static(
                "Choose an export format:",
                id="export-prompt"
            )
            
            # Format descriptions to help users choose
            yield Static(
                "• CSV - Open in Excel or Google Sheets\n"
                "• JSON - Developer-friendly structured data\n"
                "• Markdown - Beautiful readable report",
                id="format-descriptions"
            )
            
            # Export format buttons
            with Horizontal(id="format-buttons"):
                yield Button("Export CSV", variant="primary", id="export-csv")
                yield Button("Export JSON", variant="primary", id="export-json")
                yield Button("Export Markdown", variant="primary", id="export-md")
            
            # Cancel button on its own row
            yield Button("Cancel", variant="default", id="cancel")
            
            # Status message area that starts empty
            yield Static("", id="export-status")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle export format selection and file writing.
        
        When a user clicks an export button, we load all mood data,
        write it to a file in their Downloads folder, and show them
        a success message with the file location.
        """
        button_id = event.button.id
        
        if button_id == "cancel":
            # Just close the modal without doing anything
            self.dismiss()
            return
        
        # Load all mood entries from storage
        entries = load_moods()
        
        if not entries:
            # Show an error if there's no data to export
            self._show_status("No mood entries to export!", is_error=True)
            return
        
        # Create a timestamped filename to avoid overwrites
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        downloads_path = Path.home() / "Downloads"
        
        try:
            if button_id == "export-csv":
                output_file = downloads_path / f"mood_tracker_{timestamp}.csv"
                export_to_csv(entries, output_file)
                self._show_status(f"✓ Exported to {output_file}")
                
            elif button_id == "export-json":
                output_file = downloads_path / f"mood_tracker_{timestamp}.json"
                export_to_json(entries, output_file)
                self._show_status(f"✓ Exported to {output_file}")
                
            elif button_id == "export-md":
                output_file = downloads_path / f"mood_tracker_{timestamp}.md"
                export_to_markdown(entries, output_file)
                self._show_status(f"✓ Exported to {output_file}")
            
            # Automatically close the modal after a successful export
            self.set_timer(2.0, self._auto_dismiss)
            
        except Exception as e:
            # Show any errors that occur during file writing
            self._show_status(f"Export failed: {str(e)}", is_error=True)
    
    def _auto_dismiss(self) -> None:
        """Callback method for auto-dismissing the export screen."""
        self.dismiss()
    
    def _show_status(self, message: str, is_error: bool = False) -> None:
        """Update the status message area with feedback.
        
        Args:
            message: The status message to display
            is_error: Whether this is an error message (changes color)
        """
        status_widget = self.query_one("#export-status", Static)
        if is_error:
            status_widget.update(f"[red]{message}[/red]")
        else:
            status_widget.update(f"[green]{message}[/green]")