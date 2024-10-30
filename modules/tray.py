import pystray
from PIL import Image, ImageDraw
import threading
import os

def create_image():
    # Get the directory where this script is located
    current_dir = os.path.dirname(os.path.abspath(__file__))
    icon_path = os.path.join(current_dir, 'microphone.png')
    return Image.open(icon_path)

def on_exit(icon, item):
    icon.stop()
    # Ensure clean exit of the application
    os._exit(0)

def setup_tray_icon(app):
    icon = pystray.Icon('Voice Typing')
    icon.icon = create_image()
    icon.menu = pystray.Menu(
        pystray.MenuItem(
            'Settings',
            pystray.Menu(
                pystray.MenuItem(
                    'Continuous Capture',
                    lambda: None,
                    checked=lambda item: app.settings.get('continuous_capture')
                ),
                pystray.MenuItem(
                    'Smart Capture',
                    lambda: None,
                    enabled=False
                ),
                pystray.MenuItem(
                    'Clean Transcription',
                    lambda item: app.toggle_clean_transcription(),
                    checked=lambda item: app.settings.get('clean_transcription')
                )
            )
        ),
        pystray.MenuItem('Exit', on_exit)
    )
    threading.Thread(target=icon.run).start()