import threading
import time
from pynput import keyboard
from modules.recorder import AudioRecorder
from modules.ui import UIFeedback
from modules.transcribe import transcribe_audio
from modules.clean_text import clean_transcription
from modules.tray import setup_tray_icon
from modules.settings import Settings
import sys
import os

class VoiceTypingApp:
    def __init__(self):
        # Hide console in Windows if running as .pyw
        if os.name == 'nt':
            import ctypes
            ctypes.windll.user32.ShowWindow(
                ctypes.windll.kernel32.GetConsoleWindow(), 0)

        # Initialize settings
        self.settings = Settings()

        # Initialize components
        self.recorder = AudioRecorder()
        self.ui_feedback = UIFeedback()
        self.ui_feedback.set_click_callback(self.cancel_recording)
        self.recording = False
        self.ctrl_pressed = False
        self.clean_transcription_enabled = self.settings.get('clean_transcription')

        def win32_event_filter(msg, data):
            # Key codes and messages
            VK_CONTROL = 0x11
            VK_LCONTROL = 0xA2
            VK_RCONTROL = 0xA3
            VK_CAPITAL = 0x14

            WM_KEYDOWN = 0x0100
            WM_KEYUP = 0x0101

            # Update Ctrl state for both left and right Ctrl keys
            if data.vkCode in (VK_CONTROL, VK_LCONTROL, VK_RCONTROL):
                if msg == WM_KEYDOWN:
                    self.ctrl_pressed = True
                elif msg == WM_KEYUP:
                    self.ctrl_pressed = False
                return True

            # Handle Caps Lock
            if data.vkCode == VK_CAPITAL and msg == WM_KEYDOWN:
                if self.ctrl_pressed:
                    # Allow normal Caps Lock behavior when Ctrl is pressed
                    return True
                else:
                    # Toggle recording and suppress Caps Lock
                    self.toggle_recording()
                    self.listener.suppress_event()
                    return False

            return True

        # Update listener setup
        self.listener = keyboard.Listener(
            win32_event_filter=win32_event_filter,
            suppress=False
        )

    def toggle_recording(self):
        if not self.recording:
            print("Starting recording...")
            self.recording = True
            self.recorder.start()
            self.ui_feedback.start_listening_animation()
        else:
            print("Stopping recording...")
            self.recording = False
            self.recorder.stop()
            self.ui_feedback.stop_listening_animation()
            self.process_audio()

    def process_audio(self):
        try:
            print("Starting transcription...")
            # Run transcription in a separate thread to prevent UI blocking
            threading.Thread(target=self._process_audio_thread).start()
        except Exception as e:
            print(f"Error starting process_audio thread: {str(e)}")
            self.ui_feedback.insert_text(f"Error: {str(e)[:50]}...")

    def _process_audio_thread(self):
        try:
            text = transcribe_audio(self.recorder.filename)
            if self.clean_transcription_enabled:
                text = clean_transcription(text)
            self.ui_feedback.insert_text(text)
        except Exception as e:
            print(f"Error in _process_audio_thread: {str(e)}")
            self.ui_feedback.insert_text(f"Error: {str(e)[:50]}...")

    def toggle_clean_transcription(self):
        self.clean_transcription_enabled = not self.clean_transcription_enabled
        self.settings.set('clean_transcription', self.clean_transcription_enabled)
        print(f"Clean transcription {'enabled' if self.clean_transcription_enabled else 'disabled'}")

    def run(self):
        # Start keyboard listener
        self.listener.start()

        # Setup tray icon with self reference
        setup_tray_icon(self)

        # Start the UI feedback's tkinter mainloop in the main thread
        try:
            self.ui_feedback.root.mainloop()
        finally:
            self.cleanup()
            sys.exit(0)

    def cleanup(self):
        self.listener.stop()
        if self.recording:
            self.recorder.stop()
            self.ui_feedback.stop_listening_animation()

    def cancel_recording(self):
        """Cancel recording without attempting transcription"""
        if self.recording:
            print("Canceling recording...")
            self.recording = False
            self.recorder.stop()
            self.ui_feedback.stop_listening_animation()
            # Note: We don't call process_audio() here

if __name__ == "__main__":
    app = VoiceTypingApp()
    app.run()