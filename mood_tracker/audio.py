from __future__ import annotations

from pathlib import Path

# We'll handle the import gracefully in case the library isn't installed
try:
    import pygame.mixer  # type: ignore
    AUDIO_AVAILABLE = True
except ImportError:
    AUDIO_AVAILABLE = False


class SoundManager:
    """Manages audio playback for UI feedback sounds.
    
    This class abstracts away the complexity of cross-platform audio
    playback and handles errors gracefully. If audio isn't available
    or fails to play, the app continues working normally.
    """
    
    def __init__(self):
        """Initialize the sound manager and locate sound files."""
        self.enabled = AUDIO_AVAILABLE
        # Sound files should live alongside this module
        self.sounds_dir = Path(__file__).parent / "sounds"

        if self.enabled:
            try:
                # Initialize pygame mixer with minimal settings
                # We only need the mixer, not the full pygame system
                pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
            except Exception:
                self.enabled = False
        
    def play_selection(self) -> None:
        """Play a sound when the user changes their mood selection.
        
        This provides subtle audio feedback that helps make the interface
        feel more responsive. The sound should be short and pleasant.
        """
        if not self.enabled:
            # Fall back to the terminal bell if we can't play audio
            print("\a", end="", flush=True)
            return
        
        sound_file = self.sounds_dir / "select.wav"
        self._play_sound(sound_file)
    
    def play_save(self) -> None:
        """Play a confirmation sound when a mood is saved.
        
        This sound should feel satisfying and conclusive, giving the
        user confidence that their entry was recorded successfully.
        """
        if not self.enabled:
            print("\a", end="", flush=True)
            return
        
        sound_file = self.sounds_dir / "save.wav"
        self._play_sound(sound_file)
    
    def _play_sound(self, sound_file: Path) -> None:
        """Internal method that handles the actual audio playback.

        We wrap this in try-except because audio can fail for many reasons:
        missing files, no audio device, permission issues, etc. The app
        should never crash because of a sound effect.
        """
        try:
            if sound_file.exists():
                sound = pygame.mixer.Sound(str(sound_file))
                sound.play()
        except Exception:
            # Silently fail - sounds are nice to have but not critical
            pass