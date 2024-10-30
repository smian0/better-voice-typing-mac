import json
import os

class Settings:
    def __init__(self):
        self.settings_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'settings.json')
        self.default_settings = {
            'continuous_capture': True,
            'smart_capture': False,
            'clean_transcription': True
        }
        self.current_settings = self.load_settings()

    def load_settings(self):
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r') as f:
                    return {**self.default_settings, **json.load(f)}
            return self.default_settings.copy()
        except Exception as e:
            print(f"Error loading settings: {str(e)}")
            return self.default_settings.copy()

    def save_settings(self):
        try:
            with open(self.settings_file, 'w') as f:
                json.dump(self.current_settings, f, indent=4)
        except Exception as e:
            print(f"Error saving settings: {str(e)}")

    def get(self, key):
        return self.current_settings.get(key, self.default_settings.get(key))

    def set(self, key, value):
        self.current_settings[key] = value
        self.save_settings() 