import os
import sys
import threading
import traceback
from typing import Any, Callable, Optional

from pynput import keyboard
import rumps

from modules.clean_text import clean_transcription
from modules.history import TranscriptionHistory
from modules.recorder import AudioRecorder
from modules.settings import Settings
from modules.transcribe import transcribe_audio, reset_session_stats
from modules.ui import UIFeedback

class VoiceTypingApp(rumps.App):
    def __init__(self) -> None:
        super().__init__("Voice Typing", title="🎤")

        self.settings = Settings()
        self.ui_feedback = UIFeedback(self)
        self.recorder = AudioRecorder(level_callback=self.ui_feedback.update_audio_level)
        self.ui_feedback.set_click_callback(self.cancel_recording)
        self.recording = False
        self.option_pressed = False
        self.clean_transcription_enabled = self.settings.get('clean_transcription')
        self.history = TranscriptionHistory()

        # Reset transcription session stats
        reset_session_stats()
        
        # Setup keyboard listener for macOS
        self.listener = keyboard.Listener(
            on_press=self._on_press,
            on_release=self._on_release
        )
        
        # Setup menu
        self.menu = [
            rumps.MenuItem("Clean Transcription", 
                         callback=self.toggle_clean_transcription,
                         key='c'),
            None,  # Separator
            rumps.MenuItem("Reset Session Stats",
                         callback=self.reset_stats,
                         key='r'),
            None,  # Separator
            rumps.MenuItem("Quit", callback=self.quit_app, key='q')
        ]

    def _on_press(self, key: keyboard.Key) -> None:
        try:
            # Handle Option key (Alt key on Mac)
            if key == keyboard.Key.alt:
                self.option_pressed = True
            # Handle Space when Option is pressed
            elif key == keyboard.Key.space and self.option_pressed:
                self.toggle_recording()
        except AttributeError:
            pass

    def _on_release(self, key: keyboard.Key) -> None:
        try:
            if key == keyboard.Key.alt:
                self.option_pressed = False
        except AttributeError:
            pass

    def toggle_recording(self, sender=None) -> None:
        if not self.recording:
            print("🎙️ Starting recording...")
            self.recording = True
            self.recorder.start()
            self.ui_feedback.start_listening_animation()
        else:
            self.recording = False
            self.recorder.stop()
            self.ui_feedback.stop_listening_animation()
            self.process_audio()

    def process_audio(self) -> None:
        try:
            # Run transcription in a separate thread to prevent UI blocking
            threading.Thread(target=self._process_audio_thread).start()
        except Exception as e:
            print(f"Error starting process_audio thread: {str(e)}")
            self.ui_feedback.insert_text(f"Error: {str(e)[:50]}...")

    def _process_audio_thread(self) -> None:
        try:
            print("✍️ Starting transcription...")
            result = transcribe_audio(self.recorder.filename)
            text = result.text
            if self.clean_transcription_enabled:
                text = clean_transcription(text)
            self.history.add(text)
            self.ui_feedback.insert_text(text)
            
            # Update menu bar stats using session totals
            self.ui_feedback.update_stats(
                result.tokens_sent,
                result.tokens_received,
                result.session_cost
            )
            
            print("\nTranscribed text:")
            print(f"{text}")
            print("\nText ready to paste")
        except Exception as e:
            print("Error in _process_audio_thread:")
            traceback.print_exc()
            self.ui_feedback.insert_text(f"Error: {str(e)[:50]}...")

    @rumps.clicked("Clean Transcription")
    def toggle_clean_transcription(self, sender) -> None:
        self.clean_transcription_enabled = not self.clean_transcription_enabled
        sender.state = self.clean_transcription_enabled
        self.settings.set('clean_transcription', self.clean_transcription_enabled)
        print(f"Clean transcription {'enabled' if self.clean_transcription_enabled else 'disabled'}")

    def quit_app(self, sender) -> None:
        self.cleanup()
        rumps.quit_application()

    def run(self) -> None:
        # Start keyboard listener
        self.listener.start()
        # Start the rumps app
        super().run()

    def cleanup(self) -> None:
        self.listener.stop()
        if self.recording:
            self.recorder.stop()
            self.ui_feedback.stop_listening_animation()

    def cancel_recording(self) -> None:
        """Cancel recording without attempting transcription"""
        if self.recording:
            print("Canceling recording...")
            self.recording = False
            # Start a separate thread for stopping the recorder
            threading.Thread(target=self._stop_recorder).start()
            self.ui_feedback.stop_listening_animation()

    def _stop_recorder(self) -> None:
        """Helper method to stop recorder in a separate thread"""
        try:
            self.recorder.stop()
        except Exception as e:
            print(f"Error stopping recorder: {e}")
            traceback.print_exc()

    def reset_stats(self, sender) -> None:
        """Reset session statistics"""
        reset_session_stats()
        self.ui_feedback.update_stats(0, 0, 0.0)
        print("Session statistics reset")

if __name__ == "__main__":
    app = VoiceTypingApp()
    app.run()