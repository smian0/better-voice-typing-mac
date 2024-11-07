import pystray
from PIL import Image
import threading
import os
import pyperclip

def create_image():
    # Get the directory where this script is located
    current_dir = os.path.dirname(os.path.abspath(__file__))
    icon_path = os.path.join(current_dir, 'microphone.png')
    return Image.open(icon_path)

def on_exit(icon, item):
    icon.stop()
    # Ensure clean exit of the application
    os._exit(0)

def create_copy_menu(app):
    """Creates dynamic menu of recent transcriptions"""
    def make_copy_handler(text):
        return lambda icon, item: pyperclip.copy(text)

    return [
        pystray.MenuItem(
            app.history.get_preview(text),
            make_copy_handler(text)
        )
        for text in app.history.get_recent()
    ]

def setup_tray_icon(app):
    icon = pystray.Icon('Voice Typing')
    icon.icon = create_image()

    def get_menu():
        # Dynamic menu that updates when called
        copy_menu = create_copy_menu(app)
        return pystray.Menu(
            pystray.MenuItem(
                'Recent Transcriptions',
                pystray.Menu(*copy_menu) if copy_menu else pystray.Menu(
                    pystray.MenuItem('No transcriptions yet', None, enabled=False)
                ),
                enabled=bool(copy_menu)
            ),
            pystray.MenuItem(
                'Settings',
                pystray.Menu(
                    pystray.MenuItem(
                        'Clean Transcription',
                        lambda icon, item: app.toggle_clean_transcription(),
                        checked=lambda item: app.settings.get('clean_transcription')
                    ),
                    pystray.MenuItem(
                        'Continuous Capture',
                        lambda icon, item: None,
                        checked=lambda item: app.settings.get('continuous_capture')
                    ),
                    pystray.MenuItem(
                        'Smart Capture',
                        lambda icon, item: None,
                        enabled=False
                    )
                )
            ),
            pystray.MenuItem('Exit', on_exit)
        )

    # Initial menu setup
    icon.menu = get_menu()
    # Store the update function in the app to call it from elsewhere
    app.update_icon_menu = lambda: setattr(icon, 'menu', get_menu()) # Updates the tray icon's menu

    # Start the icon's event loop in its own thread
    threading.Thread(target=icon.run).start()