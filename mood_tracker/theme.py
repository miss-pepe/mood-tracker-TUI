from dataclasses import dataclass

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


MOOD_THEME = ColorPalette(
    bg="#050814",
    bg_alt="#0b1020",
    text_primary="#f5f5f7",
    text_muted="#8a8fa3",
    accent_high="#ff6bcb",
    accent_mid="#7f5af0",
    accent_low="#2cb67d",
    danger="#ff4d6a",
    success="#3dd68c",
)
