from __future__ import annotations

import csv
import json
from datetime import datetime
from pathlib import Path
from typing import List

from .storage import MoodEntry


def export_to_csv(entries: List[MoodEntry], output_path: Path) -> None:
    """Export mood entries to a CSV file for spreadsheet analysis.
    
    CSV is perfect for opening in Excel, Google Sheets, or any data
    analysis tool. Each row represents one mood entry with all its fields.
    
    Args:
        entries: List of mood entries to export
        output_path: Where to write the CSV file
    """
    with output_path.open("w", newline="", encoding="utf-8") as csvfile:
        # Define the columns we want in our CSV
        fieldnames = ["timestamp", "score", "tag", "note"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Write the header row so people know what each column means
        writer.writeheader()
        
        # Write each entry as a row
        for entry in entries:
            writer.writerow({
                "timestamp": entry.timestamp.isoformat(),
                "score": entry.score,
                "tag": entry.tag or "",  # Empty string for missing tags
                "note": entry.note or "",  # Empty string for missing notes
            })


def export_to_json(entries: List[MoodEntry], output_path: Path) -> None:
    """Export mood entries to a JSON file for programmatic access.
    
    JSON preserves the full structure of your data and is easy to
    load back into Python or other programming languages. This is
    essentially a backup format that maintains all information.
    
    Args:
        entries: List of mood entries to export
        output_path: Where to write the JSON file
    """
    # Convert each entry to a dictionary using the existing method
    data = [entry.to_dict() for entry in entries]
    
    # Write with nice formatting so humans can read it if needed
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def export_to_markdown(entries: List[MoodEntry], output_path: Path) -> None:
    """Export mood entries to a Markdown file with visual mood graphs.
    
    Markdown creates a beautiful readable report that renders nicely
    on GitHub, in markdown viewers, or even printed to PDF. We organize
    entries by month and create visual bar charts using block characters.
    
    Args:
        entries: List of mood entries to export
        output_path: Where to write the markdown file
    """
    with output_path.open("w", encoding="utf-8") as f:
        # Write the document header with generation timestamp
        f.write("# Mood Tracker Export\n\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
        
        if not entries:
            f.write("No mood entries found.\n")
            return
        
        # Calculate some overall statistics to show at the top
        total_entries = len(entries)
        average_mood = sum(e.score for e in entries) / total_entries
        highest_mood = max(entries, key=lambda e: e.score)
        lowest_mood = min(entries, key=lambda e: e.score)
        
        f.write("## Summary Statistics\n\n")
        f.write(f"- **Total entries:** {total_entries}\n")
        f.write(f"- **Average mood:** {average_mood:.1f}/10\n")
        f.write(f"- **Highest mood:** {highest_mood.score}/10 on {highest_mood.timestamp.strftime('%Y-%m-%d')}\n")
        f.write(f"- **Lowest mood:** {lowest_mood.score}/10 on {lowest_mood.timestamp.strftime('%Y-%m-%d')}\n\n")
        
        # Group entries by month for better organization
        by_month = {}
        for entry in entries:
            month_key = entry.timestamp.strftime("%Y-%m")
            if month_key not in by_month:
                by_month[month_key] = []
            by_month[month_key].append(entry)
        
        # Write each month as its own section
        f.write("## Monthly Breakdown\n\n")
        for month_key in sorted(by_month.keys(), reverse=True):
            month_entries = by_month[month_key]
            month_name = datetime.strptime(month_key, "%Y-%m").strftime("%B %Y")
            
            # Calculate month statistics
            month_average = sum(e.score for e in month_entries) / len(month_entries)
            
            f.write(f"### {month_name}\n\n")
            f.write(f"**Average mood:** {month_average:.1f}/10 ({len(month_entries)} entries)\n\n")
            
            # Write each entry with a visual bar
            for entry in sorted(month_entries, key=lambda e: e.timestamp):
                date_str = entry.timestamp.strftime("%Y-%m-%d")
                time_str = entry.timestamp.strftime("%H:%M")
                
                # Create a visual bar using block characters
                # Each block represents one point on the 1-10 scale
                bar = "█" * entry.score
                
                # Choose an emoji based on the score for quick visual scanning
                if entry.score >= 8:
                    emoji = "😄"
                elif entry.score >= 6:
                    emoji = "🙂"
                elif entry.score >= 4:
                    emoji = "😐"
                elif entry.score >= 2:
                    emoji = "😕"
                else:
                    emoji = "😢"
                
                f.write(f"- **{date_str}** at {time_str} {emoji} `{bar}` ({entry.score}/10)")
                
                # Include the note if one was provided
                if entry.note:
                    f.write(f"\n  > {entry.note}")
                
                f.write("\n")
            
            f.write("\n")


def _mood_emoji(score: int) -> str:
    """Helper function to get an emoji representation of a mood score.
    
    This is used in markdown exports to make the data more visually
    scannable. People can quickly see how they were feeling without
    reading numbers.
    """
    if score >= 8:
        return "😄"
    elif score >= 6:
        return "🙂"
    elif score >= 4:
        return "😐"
    elif score >= 2:
        return "😕"
    else:
        return "😢"