import tkinter as tk
import threading
from pynput import keyboard
import pyperclip
import pyautogui
import time

class UIFeedback:
    pyautogui_lock = threading.Lock()

    def __init__(self):
        # Create the floating window
        self.root = tk.Tk()
        self.root.withdraw()  # Hide initially
        self.indicator = tk.Toplevel(self.root)
        self.indicator.withdraw()

        # Configure the indicator window
        self.indicator.overrideredirect(True)  # Remove window decorations
        self.indicator.attributes('-topmost', True)  # Keep on top
        self.indicator.configure(bg='red')

        # Add pulsing state variables
        self.pulsing = False
        self.pulse_colors = ['red', 'darkred']
        self.current_color = 0

        # Create label with click binding
        self.label = tk.Label(self.indicator, text="🎤 Recording",
                            fg='white', bg='red', padx=10, pady=5,
                            cursor="hand2")  # Change cursor to hand on hover
        self.label.pack()

        # Add click callback placeholder
        self.on_click_callback = None

        # Bind click events to both the label and the indicator
        self.label.bind('<Button-1>', self._handle_click)
        self.indicator.bind('<Button-1>', self._handle_click)

        # Position window in top-right corner
        screen_width = self.root.winfo_screenwidth()
        self.indicator.geometry(f'+{screen_width-150}+10')

    def _handle_click(self, event):
        if self.on_click_callback:
            self.on_click_callback()

    def set_click_callback(self, callback):
        """Set the function to be called when the indicator is clicked"""
        self.on_click_callback = callback

    def _pulse(self):
        if self.pulsing:
            self.current_color = (self.current_color + 1) % 2
            color = self.pulse_colors[self.current_color]
            self.indicator.configure(bg=color)
            self.label.configure(bg=color)
            self.indicator.after(500, self._pulse)  # Pulse every 500ms

    def start_listening_animation(self):
        self.indicator.deiconify()
        self.pulsing = True
        self._pulse()

    def stop_listening_animation(self):
        self.pulsing = False
        self.indicator.withdraw()
        # Reset colors
        self.current_color = 0
        self.indicator.configure(bg=self.pulse_colors[0])
        self.label.configure(bg=self.pulse_colors[0])

    def insert_text(self, text):
        """Insert text at the current cursor position using clipboard"""
        try:
            with self.pyautogui_lock:
                pyperclip.copy(text)
                pyautogui.hotkey('ctrl', 'v')
        except Exception as e:
            print(f"UIFeedback: Error during text insertion: {str(e)}")


if __name__ == "__main__":
    import time

    class UITester:
        def __init__(self):
            print("Starting UI feedback test...")
            print("Press Caps Lock to toggle recording indicator")
            print("Press Ctrl+C to exit")

            self.ui = UIFeedback()
            self.recording = False
            self.listener = None

        def on_press(self, key):
            if key == keyboard.Key.caps_lock:
                self.recording = not self.recording
                if self.recording:
                    print("Recording started")
                    self.ui.start_listening_animation()
                else:
                    print("Recording stopped")
                    self.ui.stop_listening_animation()

        def run(self):
            self.listener = keyboard.Listener(on_press=self.on_press)
            self.listener.start()

            try:
                self.ui.root.mainloop()
            except KeyboardInterrupt:
                self.cleanup()

        def cleanup(self):
            if self.listener:
                self.listener.stop()
            if self.recording:
                self.ui.stop_listening_animation()
            self.ui.root.destroy()
            print("\nTest ended")

    # Create and run the tester
    tester = UITester()
    tester.run()