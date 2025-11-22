# Terminal Mood Tracker TUI

A small Textual-powered terminal app to log how you're feeling, add optional tags/notes, and review recent trends without leaving the shell. Now with chaotic animations, dramatic confirmations, and secret easter eggs! 🔥

There is a live preview of this project for you to view using the link here : 
[TUI Mood Tracking](https://miss-pepe.github.io/mood-tracker-TUI "TUI Mood Tracker")

## Features

### Core Features
- **Quick Mood Logging**: Select from 5 mood options (Great, Good, Meh, Bad, Awful) with easy keyboard navigation
- **Note-Taking**: Add optional notes to mood entries to capture context and thoughts
- **Vim-Style Navigation**: Use K/J or arrow keys to navigate - whichever you prefer!
- **Color-Coded Moods**: Consistent color scheme across all views (Great=green, Good=cyan, Meh=yellow, Bad=orange, Awful=red)
- **Animated UI**: Smooth transitions for mood selection, growing history bars, and toast notifications
- **Dramatic Confirmations**: Overly dramatic system messages when logging moods

### History & Analytics
- **Quick History Panel**: View your last 5 mood entries in the main view (toggle with `H`)
- **Detailed History Screen**: Press `V` to see comprehensive history with:
  - Last 30 entries with timestamps and notes
  - Statistics (average mood, best/worst days for overall, 7-day, and 30-day periods)
  - Mood streaks tracking
  - Scrollable view
- **Monthly Calendar View**: See your moods displayed on a calendar (press `M`)
- **Export Functionality**: Export your mood data for backup or analysis (press `E`)

### Gamification
- **Mood Streaks**: Track consecutive "not awful" days (score ≥ 3) and "good or better" days (score ≥ 7)
- **Entry Counter**: See total entries logged in the status strip
- **Note Indicators**: ✏️ icon shows when entries have notes

### Visual Enhancements & Themes
- **Rich Theme System**: 60+ beautiful themes with custom color palettes and ASCII mascots
- **Status Strip**: Bottom bar showing theme, chaos mode status, and entry count
- **Playful Headers**: "Mood History — your emotional stock chart 📈📉"
- **Sound Effects**: Audio feedback for interactions (when enabled)

### Easter Eggs & Chaos
- **Chaos Mode**: Secret mode activated by typing `C-H-A-O-S` (in sequence) - toggles chaotic visuals 🔥
- **Glitch Effects**: Random glitchy moments (8% chance on app start or theme change)
  - Occasionally inverts mood direction labels
  - Shows glitchy mascot faces
  - 30% chance of glitch effects when glitch mode is active
- **Dramatic Confirmations**: From "✨ peak slay ✨" to "Oh, babe. Logging emergency vibes. 💔"

### Persistence & Help
- **Persistent Storage**: All entries saved to `data/moods.json`
- **Built-in Help**: Press `?` to see all keyboard shortcuts
- **Preference Persistence**: Remembers your last selected mood, theme choice, and panel visibility

## Getting Started

1. **Create and activate a virtual environment** (recommended):
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the app**:
   ```bash
   python run.py
   ```

## Controls

### Navigation
- `↑` or `K` — Move selection up
- `↓` or `J` — Move selection down (Vim-style keys supported!)

### Actions
- `Enter` or `S` — Save current mood entry (with optional note)
- `T` — Cycle through available themes
- `H` — Toggle history panel visibility
- `V` — Open detailed history view with statistics and streaks
- `M` — Open monthly calendar view
- `E` — Export data
- `?` — Show help dialog with keyboard shortcuts
- `Q` — Quit the application

### Easter Eggs
- Type `C-H-A-O-S` (in sequence) — Toggle chaos mode 🔥
- Random glitch moments (8% chance on app start or theme change, 30% chance of effects when active)
- Dramatic mood confirmations when saving entries

## Data Storage

Your mood entries are automatically saved to `data/moods.json` in the project directory. User preferences (theme choice, last selected mood, panel visibility) are stored in `~/.mood_tracker/preferences.json`.

To reset your data:
- Delete `data/moods.json` to clear all mood entries
- Delete `~/.mood_tracker/preferences.json` to reset preferences to defaults

## Themes Available
- Neon Midnight  
- Galactic Slushie  
- Retro Arcade CRT  
- Dragonfire Core  
- Oceanic Overdrive  
- Toxic Slime Lab  
- Cosmic Jellyfish  
- 90s Vapor Arcade  
- Night-Shift Rainbow  
- Cyber Swamp Witch  
- Midnight Bubblegum  
- Storm Witch  
- Chaotic Pastel Hacker  
- Neon Anxiety  
- Galaxy Sweetheart  
- Cyber Siren  
- Void Candy  
- Hacker Bunny  
- Wicked Pastel  
- Caffeine Overdose  
- Gremlin Hacker Glow  
- Chaotic Intelligence Matrix  
- Midnight Mischief  
- Terminal Witchcraft  
- Neon Disaster Darling  
- Quantum Sass Core™  
- Feral Cyberpunk Assistant  
- Overclocked Personality Core  
- The “Don’t Let the Sweet Voice Fool You” Palette  
- Spicy Tech Oracle
- Dracula
- One Dark Pro
- Tokyo Night
- Catppuccin Mocha
- Gruvbox Dark
- Solarized Dark
- Nord
- Monokai Pro
- Ayu Mirage
- SynthWave ’84
- SpaceCamp
- Night Owl
- Tomorrow Night Eighties
- Afterglow
- Lucario
- Material Darker
- Adventure Time
- Palenight
- Jellybeans
- Horizon Dark


## Project Structure

```
mood-tracker-TUI/
├── mood_tracker/           # Main application package
│   ├── models/            # Data models and storage
│   ├── views/             # UI screens (main, calendar, export, etc.)
│   ├── widgets/           # Custom Textual widgets
│   ├── sounds/            # Audio files for sound effects
│   ├── app.py             # Main application class
│   ├── audio.py           # Sound management
│   └── theme.py           # Theme definitions and palettes
├── data/                  # Mood entry storage (auto-created)
├── run.py                 # Application entry point
└── requirements.txt       # Python dependencies
```

## Dependencies

Built with:
- [Textual](https://github.com/Textualize/textual) - Terminal UI framework
- Python 3.9+

## Tips & Tricks

- **Accessibility**: The app works great with screen readers and supports keyboard-only navigation
- **Customization**: Each theme includes a unique ASCII mascot that appears when you select it
- **Performance**: The history panel can be toggled off (`H`) for a cleaner, more minimal view
- **Portability**: Copy the `data/moods.json` file to backup or transfer your mood history between machines

## Contributing

This is a personal hobby project, but suggestions and feedback are welcome! Feel free to fork and experiment.

## License

MIT License - feel free to use and modify as you like.