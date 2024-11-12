import threading
import tkinter as tk
from typing import Optional, Callable, Any

from pynput import keyboard
import pyautogui
import pyperclip

class UIFeedback:
    pyautogui_lock = threading.Lock()

    def __init__(self):
        # Create the floating window
        self.root = tk.Tk()
        self.root.withdraw()  # Hide initially?
        self.indicator = tk.Toplevel(self.root)
        self.indicator.withdraw()

        # Configure the indicator window
        self.indicator.overrideredirect(True)  # Remove window decorations
        self.indicator.attributes('-topmost', True)  # Keep on top
        self.indicator.configure(bg='red')

        # Create main frame
        self.frame = tk.Frame(self.indicator, bg='red')
        self.frame.pack(expand=True, fill='both', padx=2, pady=2)

        # Create label with click binding
        self.label = tk.Label(self.frame, text="🎤 Recording (click to cancel)",
                            fg='white', bg='red', padx=10, pady=5,
                            cursor="hand2")  # Change cursor to hand on hover
        self.label.pack()

        # Create audio level indicator (initially hidden)
        self.level_canvas = tk.Canvas(self.frame, height=4, bg='darkred',
                                    highlightthickness=0)
        self.level_canvas.pack(fill='x', padx=4, pady=(0, 4))
        self.level_bar = self.level_canvas.create_rectangle(0, 0, 0, 4,
                                                          fill='white', width=0)

        # Add pulsing state variables
        self.pulsing = False
        self.pulse_colors = ['red', 'darkred']
        self.current_color = 0

        # Add click callback placeholder
        self.on_click_callback = None

        # Bind click events
        self.label.bind('<Button-1>', self._handle_click)
        self.indicator.bind('<Button-1>', self._handle_click)
        self.level_canvas.bind('<Button-1>', self._handle_click)

        # Position window in top-right corner
        screen_width = self.root.winfo_screenwidth()
        self.indicator.geometry(f'+{screen_width-150}+10')

    def update_audio_level(self, level: float) -> None:
        """Update the audio level indicator (level should be between 0.0 and 1.0)"""
        if self.pulsing:  # Only update when recording
            width = self.level_canvas.winfo_width()
            bar_width = int(width * min(1.0, max(0.0, level)))
            self.level_canvas.coords(self.level_bar, 0, 0, bar_width, 4)

    def _pulse(self) -> None:
        if self.pulsing:
            self.current_color = (self.current_color + 1) % 2
            color = self.pulse_colors[self.current_color]
            self.indicator.configure(bg=color)
            self.frame.configure(bg=color)
            self.label.configure(bg=color)
            self.indicator.after(500, self._pulse)  # Pulse every 500ms

    def start_listening_animation(self) -> None:
        self.indicator.deiconify()
        self.pulsing = True
        self._pulse()

    def stop_listening_animation(self) -> None:
        self.pulsing = False
        self.indicator.withdraw()
        # Reset colors
        self.current_color = 0
        self.indicator.configure(bg=self.pulse_colors[0])
        self.frame.configure(bg=self.pulse_colors[0])
        self.label.configure(bg=self.pulse_colors[0])
        # Reset audio level
        self.level_canvas.coords(self.level_bar, 0, 0, 0, 4)

    def _handle_click(self, event: tk.Event) -> None:
        if self.on_click_callback:
            self.on_click_callback()

    def set_click_callback(self, callback: Callable[[], None]) -> None:
        """Set the function to be called when the indicator is clicked"""
        self.on_click_callback = callback

    def insert_text(self, text: str) -> None:
        """Insert text at the current cursor position using clipboard while preserving original clipboard content"""
        try:
            with self.pyautogui_lock:
                # Save original clipboard content
                original_clipboard = pyperclip.paste()

                # Copy new text and paste it
                pyperclip.copy(text)
                pyautogui.hotkey('ctrl', 'v')

                # Restore original clipboard content after a small delay (non-blocking)
                self.root.after(100, lambda: pyperclip.copy(original_clipboard))
        except Exception as e:
            print(f"UIFeedback: Error during text insertion: {str(e)}")


if __name__ == "__main__":
    import time

    class UITester:
        def __init__(self) -> None:
            print("Starting UI feedback test...")
            print("Press Caps Lock to toggle recording indicator")
            print("Press Ctrl+C to exit")

            self.ui = UIFeedback()
            self.recording = False
            self.listener = None

        def on_press(self, key: keyboard.Key) -> None:
            if key == keyboard.Key.caps_lock:
                self.recording = not self.recording
                if self.recording:
                    print("Recording started")
                    self.ui.start_listening_animation()
                else:
                    print("Recording stopped")
                    self.ui.stop_listening_animation()

        def run(self) -> None:
            self.listener = keyboard.Listener(on_press=self.on_press)
            self.listener.start()

            try:
                self.ui.root.mainloop()
            except KeyboardInterrupt:
                self.cleanup()

        def cleanup(self) -> None:
            if self.listener:
                self.listener.stop()
            if self.recording:
                self.ui.stop_listening_animation()
            self.ui.root.destroy()
            print("\nTest ended")

    # Create and run the tester
    tester = UITester()
    tester.run()