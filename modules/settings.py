import json
import os
from typing import Any, Dict

class Settings:
    def __init__(self, filename: str = "settings.json") -> None:
        self.filename = os.path.join(os.path.dirname(__file__), filename)
        self.settings: Dict[str, Any] = self._load_settings()

    def _load_settings(self) -> Dict[str, Any]:
        """Load settings from file or create default if not exists"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                pass
        # Default settings
        return {
            "clean_transcription": True
        }

    def _save_settings(self) -> None:
        """Save settings to file"""
        with open(self.filename, 'w') as f:
            json.dump(self.settings, f, indent=4)

    def get(self, key: str, default: Any = None) -> Any:
        """Get a setting value"""
        return self.settings.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Set a setting value and save to file"""
        self.settings[key] = value
        self._save_settings()