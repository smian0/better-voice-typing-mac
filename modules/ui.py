import rumps
import pyperclip
from typing import Callable, Optional

class UIFeedback:
    def __init__(self, app: rumps.App) -> None:
        self.animation_active = False
        self._click_callback: Optional[Callable[[], None]] = None
        self.app = app  # Store reference to the rumps.App
        self.app.title = "🎤 Voice Typing                    "
        
    def set_click_callback(self, callback: Callable[[], None]) -> None:
        self._click_callback = callback
        
    def update_audio_level(self, level: float) -> None:
        """Update the audio level indicator"""
        if not self.animation_active:
            return
        # Create a visual representation of the audio level
        bars = int(level * 10)
        self.app.title = f"🎤 Recording {'|' * bars}{'  ' * (10 - bars)}"
        
    def start_listening_animation(self) -> None:
        """Show recording indicator"""
        self.animation_active = True
        self.app.title = "🎤 Recording...                    "
        
    def stop_listening_animation(self) -> None:
        """Hide recording indicator"""
        self.animation_active = False
        self.app.title = "🎤 Voice Typing                    "
        
    def update_stats(self, tokens_sent: int, tokens_received: int, session_cost: float) -> None:
        """Update the menu bar with session stats"""
        if not self.animation_active:  # Only update when not recording
            # Format with fixed width and padding
            stats = f"🎤 ↑{tokens_sent:>5} ↓{tokens_received:>5} ${session_cost:>7.4f}"
            self.app.title = stats
        
    def insert_text(self, text: str) -> None:
        """Insert text at current cursor position using clipboard"""
        if text:
            pyperclip.copy(text)
            # Note: On macOS, we'll rely on Command+V for pasting
            # The user will need to paste manually after transcription