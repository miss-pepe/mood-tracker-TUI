from __future__ import annotations
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

@dataclass
class BorderStyle:
    # Corner characters
    top_left: str
    top_right: str
    bottom_left: str
    bottom_right: str
    
    # Edge characters
    horizontal: str
    vertical: str
    
    # Divider characters (for section separators)
    divider_left: str
    divider_right: str
    divider_horizontal: str
    
    # Color specification (can be solid or gradient)
    border_color: str
    use_gradient: bool = False
    gradient_colors: tuple[str, str] | None = None

DEFAULT_THEME_NAME = "Horizon_Dark"

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
    "neon_midnight": ColorPalette(
        bg="#0b0f10",
        bg_alt="#111820",
        text_primary="#ebf7ff",
        text_muted="#94a9b4",
        accent_high="#39ff14",
        accent_mid="#00efff",
        accent_low="#ffea00",
        danger="#ff007c",
        success="#39ff14",
    ),
    "galactic_slushie": ColorPalette(
        bg="#050505",
        bg_alt="#0c0c14",
        text_primary="#f5f5f5",
        text_muted="#a5a5b3",
        accent_high="#26f7fd",
        accent_mid="#94ff2e",
        accent_low="#a46cff",
        danger="#ff8a1f",
        success="#26f7fd",
    ),
    "retro_arcade_crt": ColorPalette(
        bg="#0e0a1f",
        bg_alt="#181230",
        text_primary="#f0f7ff",
        text_muted="#9aa4c0",
        accent_high="#56ff7f",
        accent_mid="#ffce28",
        accent_low="#ff4e4e",
        danger="#ff4e4e",
        success="#56ff7f",
    ),
    "dragonfire_core": ColorPalette(
        bg="#121212",
        bg_alt="#1c1c1c",
        text_primary="#f2f2f2",
        text_muted="#9ea3a3",
        accent_high="#ff6d00",
        accent_mid="#ff2e00",
        accent_low="#f3c623",
        danger="#ff2e00",
        success="#2a60a8",
    ),
    "oceanic_overdrive": ColorPalette(
        bg="#02070c",
        bg_alt="#0c1420",
        text_primary="#e9f8ff",
        text_muted="#8ba7bd",
        accent_high="#005bea",
        accent_mid="#00c6b4",
        accent_low="#8df9d1",
        danger="#ff7250",
        success="#00c6b4",
    ),
    "toxic_slime_lab": ColorPalette(
        bg="#080808",
        bg_alt="#101010",
        text_primary="#f2ffe8",
        text_muted="#9fb78a",
        accent_high="#99ff00",
        accent_mid="#ccff33",
        accent_low="#ffea00",
        danger="#ffea00",
        success="#006cff",
    ),
    "cosmic_jellyfish": ColorPalette(
        bg="#050512",
        bg_alt="#0e0e21",
        text_primary="#edf0ff",
        text_muted="#9aa0c6",
        accent_high="#4d2eff",
        accent_mid="#38e5ff",
        accent_low="#aa9bff",
        danger="#ff5f48",
        success="#38e5ff",
    ),
    "nineties_vapor_arcade": ColorPalette(
        bg="#101010",
        bg_alt="#171723",
        text_primary="#f2f7ff",
        text_muted="#99a4b8",
        accent_high="#7bffda",
        accent_mid="#b399ff",
        accent_low="#ff9a3d",
        danger="#ff9a3d",
        success="#4d7bff",
    ),
    "night_shift_rainbow": ColorPalette(
        bg="#0c0c0c",
        bg_alt="#151515",
        text_primary="#f5f5f5",
        text_muted="#a4a4b2",
        accent_high="#ff3c46",
        accent_mid="#ffb444",
        accent_low="#f7ff53",
        danger="#ff3c46",
        success="#67ff84",
    ),
    "cyber_swamp_witch": ColorPalette(
        bg="#0a0d0a",
        bg_alt="#131616",
        text_primary="#f1f9ff",
        text_muted="#93a7a3",
        accent_high="#8c52ff",
        accent_mid="#42ff66",
        accent_low="#52fff1",
        danger="#ffd966",
        success="#42ff66",
    ),
    "midnight_bubblegum": ColorPalette(
        bg="#0c0c0f",
        bg_alt="#15151d",
        text_primary="#f6f1ff",
        text_muted="#a8a0bb",
        accent_high="#ff7bc3",
        accent_mid="#9affe2",
        accent_low="#c19cff",
        danger="#ff7bc3",
        success="#64ffb4",
    ),
    "storm_witch": ColorPalette(
        bg="#0b0e14",
        bg_alt="#141924",
        text_primary="#e9f1ff",
        text_muted="#9aa7bb",
        accent_high="#64a8ff",
        accent_mid="#8e7cff",
        accent_low="#6ffaf3",
        danger="#ffaa6f",
        success="#64a8ff",
    ),
    "chaotic_pastel_hacker": ColorPalette(
        bg="#0d0d10",
        bg_alt="#16161c",
        text_primary="#f5f2ff",
        text_muted="#a7a4b8",
        accent_high="#93ffd8",
        accent_mid="#c5a1ff",
        accent_low="#ff8ebc",
        danger="#ff8ebc",
        success="#ffe066",
    ),
    "neon_anxiety": ColorPalette(
        bg="#08090a",
        bg_alt="#11131a",
        text_primary="#f2f8ff",
        text_muted="#98a9ba",
        accent_high="#ff499e",
        accent_mid="#8fff2a",
        accent_low="#9d57ff",
        danger="#ff499e",
        success="#30f3ff",
    ),
    "galaxy_sweetheart": ColorPalette(
        bg="#0a0a13",
        bg_alt="#131327",
        text_primary="#f8f1ff",
        text_muted="#a8a1ba",
        accent_high="#ff7edb",
        accent_mid="#78cfff",
        accent_low="#c2b0ff",
        danger="#ffba86",
        success="#78cfff",
    ),
    "cyber_siren": ColorPalette(
        bg="#0b0a0e",
        bg_alt="#151420",
        text_primary="#f8f0ff",
        text_muted="#9da3b8",
        accent_high="#ff5ea9",
        accent_mid="#00f0c6",
        accent_low="#c676ff",
        danger="#ff5ea9",
        success="#5fb3ff",
    ),
    "void_candy": ColorPalette(
        bg="#050507",
        bg_alt="#0d0d12",
        text_primary="#f6f6ff",
        text_muted="#a7a7bb",
        accent_high="#ff6b80",
        accent_mid="#8e5bff",
        accent_low="#8ffd73",
        danger="#ff6b80",
        success="#75f0ff",
    ),
    "hacker_bunny": ColorPalette(
        bg="#09090e",
        bg_alt="#12121a",
        text_primary="#f9f5ff",
        text_muted="#a8a7bf",
        accent_high="#ffa1d5",
        accent_mid="#75e8ff",
        accent_low="#d2acff",
        danger="#ffa1d5",
        success="#a8ffeb",
    ),
    "wicked_pastel": ColorPalette(
        bg="#0e0d11",
        bg_alt="#171622",
        text_primary="#f5f3ff",
        text_muted="#a8a4bd",
        accent_high="#b98cff",
        accent_mid="#a3ffd9",
        accent_low="#ff83c2",
        danger="#ff83c2",
        success="#7cbfff",
    ),
    "caffeine_overdose": ColorPalette(
        bg="#0a0a0a",
        bg_alt="#151515",
        text_primary="#f7ffff",
        text_muted="#9eb3b3",
        accent_high="#5cffff",
        accent_mid="#ff6ad1",
        accent_low="#b984ff",
        danger="#ff6ad1",
        success="#a7ff4a",
    ),
    "dracula": ColorPalette(
        bg="#282a36",
        bg_alt="#21222c",
        text_primary="#f8f8f2",
        text_muted="#6272a4",
        accent_high="#bd93f9",
        accent_mid="#ff79c6",
        accent_low="#8be9fd",
        danger="#ff5555",
        success="#50fa7b",
    ),
    "one_dark_pro": ColorPalette(
        bg="#282c34",
        bg_alt="#282c34",
        text_primary="#abb2bf",
        text_muted="#545862",
        accent_high="#61afef",
        accent_mid="#c678dd",
        accent_low="#56b6c2",
        danger="#e06c75",
        success="#98c379",
    ),
    "tokyo_night": ColorPalette(
        bg="#1a1b26",
        bg_alt="#15161e",
        text_primary="#c0caf5",
        text_muted="#414868",
        accent_high="#7aa2f7",
        accent_mid="#bb9af7",
        accent_low="#7dcfff",
        danger="#f7768e",
        success="#9ece6a",
    ),
    "catppuccin_mocha": ColorPalette(
        bg="#1e1e2e",
        bg_alt="#1e1e2e",
        text_primary="#cdd6f4",
        text_muted="#585b70",
        accent_high="#f5c2e7",
        accent_mid="#89b4fa",
        accent_low="#94e2d5",
        danger="#f38ba8",
        success="#a6e3a1",
    ),
    "gruvbox_dark": ColorPalette(
        bg="#282828",
        bg_alt="#1d2021",
        text_primary="#ebdbb2",
        text_muted="#928374",
        accent_high="#d79921",
        accent_mid="#458588",
        accent_low="#b16286",
        danger="#cc241d",
        success="#98971a",
    ),
    "solarized_dark": ColorPalette(
        bg="#002b36",
        bg_alt="#073642",
        text_primary="#839496",
        text_muted="#586e75",
        accent_high="#268bd2",
        accent_mid="#d33682",
        accent_low="#2aa198",
        danger="#dc322f",
        success="#859900",
    ),
    "nord": ColorPalette(
        bg="#2e3440",
        bg_alt="#3b4252",
        text_primary="#d8dee9",
        text_muted="#4c566a",
        accent_high="#81a1c1",
        accent_mid="#b48ead",
        accent_low="#8fbcbb",
        danger="#bf616a",
        success="#a3be8c",
    ),
    "monokai_pro": ColorPalette(
        bg="#2d2a2e",
        bg_alt="#403e41",
        text_primary="#f8f8f2",
        text_muted="#727072",
        accent_high="#ff6188",
        accent_mid="#ab9df2",
        accent_low="#78dce8",
        danger="#ff6188",
        success="#a9dc76",
    ),
    "ayu_mirage": ColorPalette(
        bg="#1f2430",
        bg_alt="#1f2430",
        text_primary="#cbccc6",
        text_muted="#707a8c",
        accent_high="#ff3333",
        accent_mid="#59c2ff",
        accent_low="#ffb454",
        danger="#ff3333",
        success="#c2d94c",
    ),
    "synthwave_84": ColorPalette(
        bg="#241b30",
        bg_alt="#2a2139",
        text_primary="#fdfdfd",
        text_muted="#3b2e5a",
        accent_high="#ff4971",
        accent_mid="#c4bdf8",
        accent_low="#9aedfe",
        danger="#ff4971",
        success="#5af78e",
    ),
    "spacecamp": ColorPalette(
        bg="#12141f",
        bg_alt="#1d1f28",
        text_primary="#ebebeb",
        text_muted="#545862",
        accent_high="#61afef",
        accent_mid="#c678dd",
        accent_low="#56b6c2",
        danger="#e06c75",
        success="#98c379",
    ),
    "night_owl": ColorPalette(
        bg="#011627",
        bg_alt="#011627",
        text_primary="#d6deeb",
        text_muted="#4b6479",
        accent_high="#82aaff",
        accent_mid="#c792ea",
        accent_low="#21c7a8",
        danger="#ef5350",
        success="#22da6e",
    ),
    "tomorrow_night_eighties": ColorPalette(
        bg="#2d2d2d",
        bg_alt="#000000",
        text_primary="#cccccc",
        text_muted="#585858",
        accent_high="#6699cc",
        accent_mid="#cc99cc",
        accent_low="#66cccc",
        danger="#f2777a",
        success="#99cc99",
    ),
    "afterglow": ColorPalette(
        bg="#2c2c2c",
        bg_alt="#151515",
        text_primary="#d6d6d6",
        text_muted="#585858",
        accent_high="#7cafc2",
        accent_mid="#ba8baf",
        accent_low="#86c1b9",
        danger="#ab4642",
        success="#a1b56c",
    ),
    "lucario": ColorPalette(
        bg="#2b3e50",
        bg_alt="#1e2732",
        text_primary="#f8f8f2",
        text_muted="#5b6268",
        accent_high="#51afef",
        accent_mid="#c678dd",
        accent_low="#46d9ff",
        danger="#ff6c6b",
        success="#98be65",
    ),
    "material_darker": ColorPalette(
        bg="#1e1f21",
        bg_alt="#1d1f21",
        text_primary="#c5c8c6",
        text_muted="#666666",
        accent_high="#81a2be",
        accent_mid="#b294bb",
        accent_low="#8abeb7",
        danger="#cc6666",
        success="#b5bd68",
    ),
    "adventure_time": ColorPalette(
        bg="#1f1f28",
        bg_alt="#2e2e38",
        text_primary="#e2e2e3",
        text_muted="#4a4a59",
        accent_high="#6ca0ff",
        accent_mid="#c77dff",
        accent_low="#66e9ff",
        danger="#ff6b6b",
        success="#8bea72",
    ),
    "palenight": ColorPalette(
        bg="#292d3e",
        bg_alt="#434758",
        text_primary="#a6accd",
        text_muted="#434758",
        accent_high="#82aaff",
        accent_mid="#c792ea",
        accent_low="#89ddff",
        danger="#f07178",
        success="#c3e88d",
    ),
    "jellybeans": ColorPalette(
        bg="#1c1c1c",
        bg_alt="#444444",
        text_primary="#e8e8d3",
        text_muted="#444444",
        accent_high="#5f87af",
        accent_mid="#875f87",
        accent_low="#5fafaf",
        danger="#d75f5f",
        success="#87af5f",
    ),
    "horizon_dark": ColorPalette(
        bg="#1c1e26",
        bg_alt="#16161c",
        text_primary="#e0e0e0",
        text_muted="#4e4e56",
        accent_high="#e95678",
        accent_mid="#59e1e3",
        accent_low="#29d398",
        danger="#e95678",
        success="#29d398",
    ),
    "gremlin_hacker_glow": ColorPalette(
        bg="#0d0f10",
        bg_alt="#14181a",
        text_primary="#ecfff5",
        text_muted="#98ada4",
        accent_high="#38ff6c",
        accent_mid="#31a8ff",
        accent_low="#a879ff",
        danger="#ff8c47",
        success="#38ff6c",
    ),
    "chaotic_intelligence_matrix": ColorPalette(
        bg="#000000",
        bg_alt="#0a0a0a",
        text_primary="#f5faff",
        text_muted="#8c95a3",
        accent_high="#00f0ff",
        accent_mid="#a6ff00",
        accent_low="#ffb200",
        danger="#ff3c3c",
        success="#00f0ff",
    ),
    "midnight_mischief": ColorPalette(
        bg="#09090e",
        bg_alt="#12121a",
        text_primary="#f4f2ff",
        text_muted="#9ea1b8",
        accent_high="#9e6bff",
        accent_mid="#33ffc7",
        accent_low="#5fff74",
        danger="#ff634f",
        success="#33ffc7",
    ),
    "terminal_witchcraft": ColorPalette(
        bg="#040407",
        bg_alt="#0c0c12",
        text_primary="#ebfff5",
        text_muted="#93a6a1",
        accent_high="#4eff7a",
        accent_mid="#40a7ff",
        accent_low="#c084ff",
        danger="#ffd466",
        success="#4eff7a",
    ),
    "neon_disaster_darling": ColorPalette(
        bg="#0b0b0b",
        bg_alt="#151515",
        text_primary="#f7f7ff",
        text_muted="#9f9fb2",
        accent_high="#b7ff00",
        accent_mid="#52f0ff",
        accent_low="#d07aff",
        danger="#ff5148",
        success="#b7ff00",
    ),
    "quantum_sass_core": ColorPalette(
        bg="#0f0e17",
        bg_alt="#19182a",
        text_primary="#eef4ff",
        text_muted="#9ba3b8",
        accent_high="#2f83ff",
        accent_mid="#67ffd6",
        accent_low="#fff95a",
        danger="#c443ff",
        success="#67ffd6",
    ),
    "feral_cyberpunk_assistant": ColorPalette(
        bg="#050505",
        bg_alt="#0f0f0f",
        text_primary="#fdf2ff",
        text_muted="#9f9aad",
        accent_high="#ff47a3",
        accent_mid="#37c0ff",
        accent_low="#9eff3a",
        danger="#ff8a3d",
        success="#9eff3a",
    ),
    "overclocked_personality_core": ColorPalette(
        bg="#0b0a0f",
        bg_alt="#141320",
        text_primary="#f4f3ff",
        text_muted="#9da1b8",
        accent_high="#5589ff",
        accent_mid="#6aff4c",
        accent_low="#ff735e",
        danger="#ff735e",
        success="#6aff4c",
    ),
    "dont_let_the_sweet_voice_fool_you": ColorPalette(
        bg="#0a0a0f",
        bg_alt="#141420",
        text_primary="#f5f1ff",
        text_muted="#9fa4b8",
        accent_high="#c099ff",
        accent_mid="#66ffe6",
        accent_low="#93ff9f",
        danger="#f9da60",
        success="#66ffe6",
    ),
    "spicy_tech_oracle": ColorPalette(
        bg="#0e0c11",
        bg_alt="#17141f",
        text_primary="#f7f2ff",
        text_muted="#9fa0b8",
        accent_high="#5aa8ff",
        accent_mid="#79ffb4",
        accent_low="#a262ff",
        danger="#ff7a3b",
        success="#79ffb4",
    ),
}

# Border styles for each theme
# Each theme's borders express its unique personality through character choice and color
BORDER_STYLES: Dict[str, BorderStyle] = {
    # ============================================================================
    # CYBERPUNK & HIGH-TECH THEMES
    # Bold, aggressive, neon colors with heavy or double-line borders
    # ============================================================================
    
    "neon_midnight": BorderStyle(
        # Heavy borders for aggressive, high-energy cyberpunk feel
        top_left="┏", top_right="┓", bottom_left="┗", bottom_right="┛",
        horizontal="━", vertical="┃",
        divider_left="┣", divider_right="┫", divider_horizontal="━",
        border_color="#39ff14",  # Neon green fallback
        use_gradient=True,
        gradient_colors=("#39ff14", "#00efff"),  # Green to cyan - classic neon
    ),
    
    "neon_anxiety": BorderStyle(
        # Mixed heavy and light for visual tension and jittery energy
        top_left="┏", top_right="┓", bottom_left="┗", bottom_right="┛",
        horizontal="━", vertical="┃",
        divider_left="┣", divider_right="┫", divider_horizontal="━",
        border_color="#ff499e",  # Hot pink fallback
        use_gradient=True,
        gradient_colors=("#ff499e", "#9d57ff"),  # Pink to purple - anxious energy
    ),
    
    "chaotic_intelligence_matrix": BorderStyle(
        # Double-line for that computer terminal, matrix-like aesthetic
        top_left="╔", top_right="╗", bottom_left="╚", bottom_right="╝",
        horizontal="═", vertical="║",
        divider_left="╠", divider_right="╣", divider_horizontal="═",
        border_color="#00f0ff",  # Cyan fallback
        use_gradient=True,
        gradient_colors=("#00f0ff", "#a6ff00"),  # Cyan to green - digital matrix
    ),
    
    "feral_cyberpunk_assistant": BorderStyle(
        # Heavy borders with wild gradient transitions
        top_left="┏", top_right="┓", bottom_left="┗", bottom_right="┛",
        horizontal="━", vertical="┃",
        divider_left="┣", divider_right="┫", divider_horizontal="━",
        border_color="#ff47a3",  # Hot pink fallback
        use_gradient=True,
        gradient_colors=("#ff47a3", "#37c0ff"),  # Pink to cyan - wild energy
    ),
    
    "cyber_siren": BorderStyle(
        # Heavy borders with seductive gradient
        top_left="┏", top_right="┓", bottom_left="┗", bottom_right="┛",
        horizontal="━", vertical="┃",
        divider_left="┣", divider_right="┫", divider_horizontal="━",
        border_color="#ff5ea9",  # Hot pink fallback
        use_gradient=True,
        gradient_colors=("#ff5ea9", "#00f0c6"),  # Pink to teal - alluring
    ),
    
    # ============================================================================
    # COZY & WARM THEMES
    # Rounded corners, soft colors, gentle and approachable
    # ============================================================================
    
    "catppuccin_mocha": BorderStyle(
        # Rounded corners for cozy, coffee-shop warmth
        top_left="╭", top_right="╮", bottom_left="╰", bottom_right="╯",
        horizontal="─", vertical="│",
        divider_left="├", divider_right="┤", divider_horizontal="─",
        border_color="#f5c2e7",  # Soft pink - warm and inviting
        use_gradient=False,
    ),
    
    "afterglow": BorderStyle(
        # Rounded corners with sunset warmth
        top_left="╭", top_right="╮", bottom_left="╰", bottom_right="╯",
        horizontal="─", vertical="│",
        divider_left="├", divider_right="┤", divider_horizontal="─",
        border_color="#7cafc2",  # Soft blue fallback
        use_gradient=True,
        gradient_colors=("#ba8baf", "#7cafc2"),  # Purple to blue - sunset glow
    ),
    
    "midnight_bubblegum": BorderStyle(
        # Rounded with playful gradient
        top_left="╭", top_right="╮", bottom_left="╰", bottom_right="╯",
        horizontal="─", vertical="│",
        divider_left="├", divider_right="┤", divider_horizontal="─",
        border_color="#ff7bc3",  # Bubblegum pink fallback
        use_gradient=True,
        gradient_colors=("#ff7bc3", "#9affe2"),  # Pink to mint - sweet and fun
    ),
    
    # ============================================================================
    # RETRO & ARCADE THEMES
    # Double-line borders, chunky aesthetic, nostalgic color gradients
    # ============================================================================
    
    "retro_arcade_crt": BorderStyle(
        # Double-line for chunky retro computer feel
        top_left="╔", top_right="╗", bottom_left="╚", bottom_right="╝",
        horizontal="═", vertical="║",
        divider_left="╠", divider_right="╣", divider_horizontal="═",
        border_color="#ffce28",  # Arcade yellow fallback
        use_gradient=True,
        gradient_colors=("#56ff7f", "#ffce28"),  # Green to yellow - classic arcade
    ),
    
    "synthwave_84": BorderStyle(
        # Double-line with that iconic synthwave gradient
        top_left="╔", top_right="╗", bottom_left="╚", bottom_right="╝",
        horizontal="═", vertical="║",
        divider_left="╠", divider_right="╣", divider_horizontal="═",
        border_color="#ff4971",  # Hot pink fallback
        use_gradient=True,
        gradient_colors=("#ff4971", "#9aedfe"),  # Pink to cyan - pure synthwave
    ),
    
    "nineties_vapor_arcade": BorderStyle(
        # Double-line with 90s color palette
        top_left="╔", top_right="╗", bottom_left="╚", bottom_right="╝",
        horizontal="═", vertical="║",
        divider_left="╠", divider_right="╣", divider_horizontal="═",
        border_color="#7bffda",  # Teal fallback
        use_gradient=True,
        gradient_colors=("#7bffda", "#b399ff"),  # Teal to purple - 90s aesthetic
    ),
    
    "tomorrow_night_eighties": BorderStyle(
        # Double-line with 80s color warmth
        top_left="╔", top_right="╗", bottom_left="╚", bottom_right="╝",
        horizontal="═", vertical="║",
        divider_left="╠", divider_right="╣", divider_horizontal="═",
        border_color="#6699cc",  # Blue fallback
        use_gradient=False,  # Solid for that clean 80s monitor look
    ),
    
    # ============================================================================
    # PROFESSIONAL & CLEAN THEMES
    # Standard single-line, subtle colors, focus on clarity
    # ============================================================================
    
    "dracula": BorderStyle(
        # Standard borders with Dracula's signature purple
        top_left="┌", top_right="┐", bottom_left="└", bottom_right="┘",
        horizontal="─", vertical="│",
        divider_left="├", divider_right="┤", divider_horizontal="─",
        border_color="#bd93f9",  # Classic Dracula purple
        use_gradient=False,
    ),
    
    "one_dark_pro": BorderStyle(
        # Clean single-line with subtle blue
        top_left="┌", top_right="┐", bottom_left="└", bottom_right="┘",
        horizontal="─", vertical="│",
        divider_left="├", divider_right="┤", divider_horizontal="─",
        border_color="#61afef",  # One Dark blue
        use_gradient=False,
    ),
    
    "nord": BorderStyle(
        # Clean single-line with Nord's cool blue
        top_left="┌", top_right="┐", bottom_left="└", bottom_right="┘",
        horizontal="─", vertical="│",
        divider_left="├", divider_right="┤", divider_horizontal="─",
        border_color="#81a1c1",  # Nord blue - cool and professional
        use_gradient=False,
    ),
    
    "gruvbox_dark": BorderStyle(
        # Standard borders with Gruvbox's warm orange
        top_left="┌", top_right="┐", bottom_left="└", bottom_right="┘",
        horizontal="─", vertical="│",
        divider_left="├", divider_right="┤", divider_horizontal="─",
        border_color="#d79921",  # Gruvbox yellow-orange - earthy
        use_gradient=False,
    ),
    
    # ============================================================================
    # MYSTICAL & MAGICAL THEMES
    # Mixed borders or unique character choices for mysterious feel
    # ============================================================================
    
    "storm_witch": BorderStyle(
        # Heavy borders with electric gradient
        top_left="┏", top_right="┓", bottom_left="┗", bottom_right="┛",
        horizontal="━", vertical="┃",
        divider_left="┣", divider_right="┫", divider_horizontal="━",
        border_color="#64a8ff",  # Electric blue fallback
        use_gradient=True,
        gradient_colors=("#64a8ff", "#8e7cff"),  # Blue to purple - storm energy
    ),
    
    "cyber_swamp_witch": BorderStyle(
        # Mixed heavy and light for mystical asymmetry
        top_left="┏", top_right="┐", bottom_left="└", bottom_right="┛",
        horizontal="─", vertical="│",
        divider_left="├", divider_right="┫", divider_horizontal="─",
        border_color="#8c52ff",  # Purple fallback
        use_gradient=True,
        gradient_colors=("#8c52ff", "#42ff66"),  # Purple to green - swamp magic
    ),
    
    "terminal_witchcraft": BorderStyle(
        # Standard with magical green gradient
        top_left="┌", top_right="┐", bottom_left="└", bottom_right="┘",
        horizontal="─", vertical="│",
        divider_left="├", divider_right="┤", divider_horizontal="─",
        border_color="#4eff7a",  # Bright green fallback
        use_gradient=True,
        gradient_colors=("#4eff7a", "#40a7ff"),  # Green to blue - magic energy
    ),
    
    # ============================================================================
    # PLAYFUL & FUN THEMES
    # Rounded or standard borders with bright, cheerful gradients
    # ============================================================================
    
    "galaxy_sweetheart": BorderStyle(
        # Rounded with dreamy gradient
        top_left="╭", top_right="╮", bottom_left="╰", bottom_right="╯",
        horizontal="─", vertical="│",
        divider_left="├", divider_right="┤", divider_horizontal="─",
        border_color="#ff7edb",  # Pink fallback
        use_gradient=True,
        gradient_colors=("#ff7edb", "#78cfff"),  # Pink to blue - dreamy space
    ),
    
    "hacker_bunny": BorderStyle(
        # Rounded for cute, approachable hacker
        top_left="╭", top_right="╮", bottom_left="╰", bottom_right="╯",
        horizontal="─", vertical="│",
        divider_left="├", divider_right="┤", divider_horizontal="─",
        border_color="#ffa1d5",  # Soft pink fallback
        use_gradient=True,
        gradient_colors=("#ffa1d5", "#75e8ff"),  # Pink to cyan - playful tech
    ),
    
    "adventure_time": BorderStyle(
        # Standard with adventurous gradient
        top_left="┌", top_right="┐", bottom_left="└", bottom_right="┘",
        horizontal="─", vertical="│",
        divider_left="├", divider_right="┤", divider_horizontal="─",
        border_color="#6ca0ff",  # Blue fallback
        use_gradient=True,
        gradient_colors=("#6ca0ff", "#c77dff"),  # Blue to purple - adventure!
    ),
}

def get_palette(name: str) -> ColorPalette:
    """Return a palette by name, raising a helpful error when missing."""

    try:
        return THEMES[name]
    except KeyError as exc:  # pragma: no cover - simple guardrail
        raise ValueError(f"Unknown theme '{name}'. Available: {', '.join(THEMES)}") from exc

def get_border_style(name: str) -> BorderStyle:
    """Return a border style by name, with a fallback to default if not found.
    
    This function ensures that every theme has border styles, even if we haven't
    explicitly designed borders for that theme yet. It falls back to simple
    single-line borders with the theme's accent color.
    
    Args:
        name: The theme name to look up (e.g., "midnight", "dracula")
        
    Returns:
        BorderStyle object containing all border characters and colors
    """
    if name in BORDER_STYLES:
        return BORDER_STYLES[name]
    
    # Fallback: create a basic border style using the theme's colors
    # This ensures themes without custom borders still look good
    palette = get_palette(name)
    return BorderStyle(
        # Standard single-line box-drawing characters
        top_left="┌",
        top_right="┐",
        bottom_left="└",
        bottom_right="┘",
        horizontal="─",
        vertical="│",
        divider_left="├",
        divider_right="┤",
        divider_horizontal="─",
        # Use the theme's accent color for visual cohesion
        border_color=palette.accent_mid,
        use_gradient=False,
    )