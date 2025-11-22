"""Detailed history screen showing comprehensive mood data and statistics."""

from __future__ import annotations

from datetime import datetime, timedelta
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static
from textual.containers import Container, VerticalScroll
from textual import events
from ..models.storage import load_moods

# Box width for the history header
HISTORY_BOX_WIDTH = 78


class DetailedHistoryScreen(Screen):
    """Full-screen view showing detailed mood history and statistics."""
    
    BINDINGS = [
        ("escape", "dismiss", "Back"),
        ("q", "dismiss", "Back"),
        ("h", "dismiss", "Back"),
    ]
    
    def __init__(self, palette, border_style) -> None:
        super().__init__()
        self.palette = palette
        self.border_style = border_style
    
    def compose(self) -> ComposeResult:
        """Build the detailed history view."""
        with Container(id="history-container"):
            yield Static(self._build_header(), id="history-header")
            with VerticalScroll(id="history-scroll"):
                yield Static(self._build_content(), id="history-content")
    
    def _build_header(self) -> str:
        """Build the header section."""
        return (
            f"[bold {self.palette.accent_high}]"
            f"┌{'─' * HISTORY_BOX_WIDTH}┐\n"
            f"│{'Detailed Mood History — your emotional stock chart 📈📉'.center(HISTORY_BOX_WIDTH)}│\n"
            f"└{'─' * HISTORY_BOX_WIDTH}┘"
            f"[/]"
        )
    
    def _build_content(self) -> str:
        """Build the main content with statistics and detailed entries."""
        entries = load_moods()
        
        if not entries:
            return (
                f"\n[{self.palette.text_muted}]"
                "No mood entries yet. Start tracking to see your history here!"
                "[/]"
            )
        
        lines = []
        
        # Statistics section
        lines.append(f"\n[bold {self.palette.accent_high}]📊 Statistics[/]\n")
        lines.append(self._build_statistics(entries))
        
        # Streaks section
        lines.append(f"\n[bold {self.palette.accent_high}]🔥 Streaks[/]\n")
        lines.append(self._build_streaks(entries))
        
        # Recent entries section
        lines.append(f"\n[bold {self.palette.accent_high}]📝 Recent Entries (last 30)[/]\n")
        lines.append(self._build_entries_list(entries))
        
        return "\n".join(lines)
    
    def _build_statistics(self, entries) -> str:
        """Calculate and display mood statistics."""
        if not entries:
            return ""
        
        # Calculate various statistics
        total_entries = len(entries)
        avg_score = sum(e.score for e in entries) / total_entries
        
        # Last 7 days average
        seven_days_ago = datetime.now() - timedelta(days=7)
        recent_entries = [e for e in entries if e.timestamp >= seven_days_ago]
        if recent_entries:
            recent_avg = sum(e.score for e in recent_entries) / len(recent_entries)
        else:
            recent_avg = 0
        
        # Last 30 days average
        thirty_days_ago = datetime.now() - timedelta(days=30)
        monthly_entries = [e for e in entries if e.timestamp >= thirty_days_ago]
        if monthly_entries:
            monthly_avg = sum(e.score for e in monthly_entries) / len(monthly_entries)
        else:
            monthly_avg = 0
        
        # Find best and worst days
        best_entry = max(entries, key=lambda e: e.score)
        worst_entry = min(entries, key=lambda e: e.score)
        
        stats = []
        stats.append(f"[{self.palette.text_primary}]Total entries logged: {total_entries} 💾[/]")
        stats.append(f"[{self.palette.text_primary}]Overall average mood: {avg_score:.1f}/10[/]")
        
        if recent_entries:
            stats.append(f"[{self.palette.accent_low}]Last 7 days average: {recent_avg:.1f}/10[/]")
        
        if monthly_entries:
            stats.append(f"[{self.palette.accent_low}]Last 30 days average: {monthly_avg:.1f}/10[/]")
        
        best_date = best_entry.timestamp.strftime("%Y-%m-%d")
        worst_date = worst_entry.timestamp.strftime("%Y-%m-%d")
        stats.append(f"[{self.palette.success}]Best day: {best_date} ({best_entry.score}/10) {self._ascii_for_score(best_entry.score)}[/]")
        stats.append(f"[{self.palette.danger}]Toughest day: {worst_date} ({worst_entry.score}/10) {self._ascii_for_score(worst_entry.score)}[/]")
        
        return "\n".join(stats)
    
    def _build_streaks(self, entries) -> str:
        """Calculate and display mood streaks."""
        if not entries:
            return ""
        
        # Calculate current "not awful" streak (score >= 3)
        current_streak = 0
        for entry in reversed(entries):
            if entry.score >= 3:
                current_streak += 1
            else:
                break
        
        # Calculate longest "not awful" streak
        longest_streak = 0
        temp_streak = 0
        for entry in entries:
            if entry.score >= 3:
                temp_streak += 1
                longest_streak = max(longest_streak, temp_streak)
            else:
                temp_streak = 0
        
        # Calculate current "good or better" streak (score >= 7)
        good_streak = 0
        for entry in reversed(entries):
            if entry.score >= 7:
                good_streak += 1
            else:
                break
        
        streaks = []
        if current_streak > 0:
            if current_streak >= 3:
                streaks.append(f"[{self.palette.success}]🔥 {current_streak}-day 'not awful' streak! Keep it up![/]")
            else:
                streaks.append(f"[{self.palette.accent_low}]{current_streak}-day 'not awful' streak[/]")
        
        if good_streak > 0:
            if good_streak >= 3:
                streaks.append(f"[{self.palette.success}]✨ {good_streak}-day 'good or better' streak! You're thriving![/]")
            else:
                streaks.append(f"[{self.palette.accent_low}]{good_streak}-day 'good or better' streak[/]")
        
        if longest_streak > current_streak:
            streaks.append(f"[{self.palette.text_muted}]Longest streak ever: {longest_streak} days[/]")
        
        return "\n".join(streaks) if streaks else f"[{self.palette.text_muted}]Start building your streaks![/]"
    
    def _build_entries_list(self, entries) -> str:
        """Build a list of recent entries."""
        recent = entries[-30:]  # Last 30 entries
        recent.reverse()  # Show newest first
        
        lines = []
        for entry in recent:
            date_str = entry.timestamp.strftime("%Y-%m-%d %H:%M")
            ascii_face = self._ascii_for_score(entry.score)
            color = self._color_for_score(entry.score)
            
            # Build the entry line
            note_indicator = " ✏️" if entry.note else ""
            line = f"[{color}]{date_str}: {ascii_face:<4} [{entry.score:2d}/10]{note_indicator}[/]"
            
            # Add note if present
            if entry.note:
                line += f"\n  [{self.palette.text_muted}]↳ {entry.note}[/]"
            
            lines.append(line)
        
        return "\n".join(lines)
    
    def _ascii_for_score(self, score: int) -> str:
        """ASCII face for score."""
        if score >= 9:
            return ":D"
        if score >= 7:
            return ":)"
        if score >= 5:
            return ":|"
        if score >= 3:
            return ":("
        return ":'("
    
    def _color_for_score(self, score: int) -> str:
        """Consistent color coding for mood scores."""
        if score >= 9:  # Great
            return "#00ff00"  # Bright green
        elif score >= 7:  # Good
            return "#00ffff"  # Cyan
        elif score >= 5:  # Meh
            return "#ffff00"  # Yellow
        elif score >= 3:  # Bad
            return "#ff6600"  # Orange
        else:  # Awful
            return "#ff0000"  # Bright red
    
    def action_dismiss(self) -> None:
        """Close the history screen and return to main."""
        self.app.pop_screen()
