"""Settings management for AntiRickRoll."""

import json
from pathlib import Path
from typing import Any, Dict, Optional
from antirickroll.core.exceptions import SettingsError

class SettingsManager:
    """Manages application settings with auto-save and validation."""

    def __init__(self, config_path: Path) -> None:
        self._config_path = config_path
        self._settings: Dict[str, Any] = self._get_defaults()
        self.load()

    def _get_defaults(self) -> Dict[str, Any]:
        """Returns default application settings."""
        return {
            "theme": "dark",
            "audio_device": "default",
            "sensitivity": 0.8,
            "auto_start": False,
            "minimize_to_tray": True,
            "plugins_enabled": True,
            "first_run": True,
            "detection": {
                "enabled": True,
                "min_confidence": 0.6,
                "fft_size": 2048,
                "hop_length": 512,
                "max_peaks": 500
            }
        }

    def load(self) -> None:
        """Loads settings from the JSON file."""
        if not self._config_path.exists():
            self.save()
            return

        try:
            with open(self._config_path, "r") as f:
                loaded_settings = json.load(f)
                self._settings.update(loaded_settings)
        except (json.JSONDecodeError, OSError) as e:
            raise SettingsError(f"Failed to load settings: {e}")

    def save(self) -> None:
        """Saves settings to the JSON file."""
        try:
            self._config_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self._config_path, "w") as f:
                json.dump(self._settings, f, indent=4)
        except OSError as e:
            raise SettingsError(f"Failed to save settings: {e}")

    def get(self, key: str, default: Any = None) -> Any:
        """Retrieves a setting value."""
        return self._settings.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Sets a setting value and saves it."""
        self._settings[key] = value
        self.save()
