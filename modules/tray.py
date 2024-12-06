import rumps  # New import for macOS menu bar
from typing import Any

class VoiceTypingMenuBar(rumps.App):
    def __init__(self, app: Any) -> None:
        super().__init__("Voice Typing", icon="🎤")
        self.app = app
        
        # Add menu items
        self.clean_transcription = rumps.MenuItem(
            "Clean Transcription",
            callback=self.toggle_clean_transcription
        )
        self.menu = [self.clean_transcription]
        
        # Update initial state
        self.clean_transcription.state = app.clean_transcription_enabled

    @rumps.clicked("Clean Transcription")
    def toggle_clean_transcription(self, sender) -> None:
        self.app.toggle_clean_transcription()
        sender.state = self.app.clean_transcription_enabled

def setup_tray_icon(app: Any) -> None:
    """Setup menu bar icon for macOS"""
    menu_bar = VoiceTypingMenuBar(app)
    menu_bar.run()