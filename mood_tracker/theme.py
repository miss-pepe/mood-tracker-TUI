from dataclasses import dataclass
from typing import Dict

@dataclass
class ColorPalette:
    bg: str
    bg_alt: str
    text_primary: str
    text_muted: str
    accent_high: str
    accent_mid: str
    accent_low: str
    danger: str
    success: str

DEFAULT_THEME_NAME = "midnight"

# A few curated palettes to let users pick a vibe.
THEMES: Dict[str, ColorPalette] = {
    "midnight": ColorPalette(
        bg="#050814",
        bg_alt="#0b1020",
        text_primary="#f5f5f7",
        text_muted="#8a8fa3",
        accent_high="#ff6bcb",
        accent_mid="#7f5af0",
        accent_low="#2cb67d",
        danger="#ff4d6a",
        success="#3dd68c",
    ),
    "sunrise": ColorPalette(
        bg="#1b0a14",
        bg_alt="#2a101f",
        text_primary="#fff8f0",
        text_muted="#e0c4c0",
        accent_high="#ffb347",
        accent_mid="#ff7f50",
        accent_low="#ffd479",
        danger="#ff5c8a",
        success="#8bd450",
    ),
    "forest": ColorPalette(
        bg="#0c1210",
        bg_alt="#16211c",
        text_primary="#e9f5ec",
        text_muted="#9bb3a5",
        accent_high="#57e39a",
        accent_mid="#3fa27e",
        accent_low="#9ad8a5",
        danger="#ff6f61",
        success="#6fe3b1",
    ),
}


def get_palette(name: str) -> ColorPalette:
    """Return a palette by name, raising a helpful error when missing."""

    try:
        return THEMES[name]
    except KeyError as exc:  # pragma: no cover - simple guardrail
        raise ValueError(f"Unknown theme '{name}'. Available: {', '.join(THEMES)}") from exc
