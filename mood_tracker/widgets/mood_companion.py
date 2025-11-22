"""Mood companion widget that reacts to your current mood selection.

This widget displays an adorable ASCII mascot that changes expressions and
messages based on the mood you've selected. It's designed to add personality
and emotional support to the mood tracking experience.
"""

from __future__ import annotations

import random
from textual.widgets import Static


# Mood mascots mapped to score ranges
MOOD_MASCOTS = {
    "great": r"""  (ﾉ◕ヮ◕)ﾉ*:･ﾟ✧""",
    "good": r"""     (•‿•)""",
    "meh": r"""     (ಠ_ಠ)""",
    "bad": r"""     (ಥ﹏ಥ)""",
    "awful": r"""     (x_x)""",
}

# Supportive messages for each mood category
MOOD_MESSAGES = {
    "great": [
        "You're glowing, bestie! ✨",
        "Look at you thriving! 🌟",
        "That energy is contagious! 💫",
        "Main character vibes! 🎬",
    ],
    "good": [
        "Solid day, friend! 😊",
        "We love to see it! 💚",
        "Keep that momentum! 🌱",
        "You're doing great! 👏",
    ],
    "meh": [
        "Surviving is still progress. 💪",
        "Meh days are valid too. 🤷",
        "Tomorrow's a new start. 🌅",
        "We all have these days. 🫂",
    ],
    "bad": [
        "Okay, who pissed you off? 😤",
        "This too shall pass, friend. 🌧️",
        "Be gentle with yourself. 💙",
        "I see you struggling. 🫂",
    ],
    "awful": [
        "I'm here with you. 💜",
        "You're still showing up. 🌙",
        "One breath at a time. 🌊",
        "It's okay to not be okay. 🕊️",
    ],
}


def get_mood_category(score: int) -> str:
    """Map a numeric mood score to a category name.
    
    Args:
        score: The mood score (1-10)
        
    Returns:
        Category name: "great", "good", "meh", "bad", or "awful"
    """
    if score >= 9:
        return "great"
    elif score >= 7:
        return "good"
    elif score >= 5:
        return "meh"
    elif score >= 3:
        return "bad"
    else:
        return "awful"


class MoodCompanion(Static):
    """A cute ASCII companion that reacts to your mood selection."""
    
    def __init__(self, initial_score: int = 5, palette=None) -> None:
        super().__init__(id="mood-companion")
        self.current_score = initial_score
        self.palette = palette
        self._update_display()
    
    def update_mood(self, score: int) -> None:
        self.current_score = score
        self._update_display()
    
    def _update_display(self) -> None:
        category = get_mood_category(self.current_score)
        mascot = MOOD_MASCOTS[category]
        message = random.choice(MOOD_MESSAGES[category])
        
        if self.palette:
            mascot_color = self._get_mascot_color(category)
            content = (
                f"[{mascot_color}]{mascot}[/{mascot_color}]\n"
                f"[{self.palette.text_muted}]{message}[/{self.palette.text_muted}]"
            )
        else:
            content = f"{mascot}\n{message}"
        
        self.update(content)
    
    def _get_mascot_color(self, category: str) -> str:
        if not self.palette:
            return "white"
        
        color_map = {
            "great": self.palette.success,
            "good": self.palette.accent_low,
            "meh": self.palette.text_primary,
            "bad": "#ff6600",
            "awful": self.palette.danger,
        }
        return color_map.get(category, self.palette.text_primary)