"""Utility functions shared across mood tracker views."""

def ascii_for_score(score: int) -> str:
    """Get ASCII face representation for a mood score.
    
    Args:
        score: Mood score from 1-10
        
    Returns:
        ASCII face string (e.g., ":D", ":)", ":|", ":(", ":'(")
    """
    if score >= 9:
        return ":D"
    if score >= 7:
        return ":)"
    if score >= 5:
        return ":|"
    if score >= 3:
        return ":("
    return ":'("


def get_mood_color(score: int) -> str:
    """Get consistent color for mood score across all views.
    
    Args:
        score: Mood score from 1-10
        
    Returns:
        Hex color code string
    """
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
