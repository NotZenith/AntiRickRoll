"""Path resolution utilities for source and bundled modes."""

import os
import sys
from pathlib import Path

def get_app_root() -> Path:
    """Returns the root directory of the application."""
    if getattr(sys, 'frozen', False):
        # Running as a bundled executable
        return Path(sys._MEIPASS)
    # Running from source
    return Path(__file__).parent.parent.parent.parent

def get_user_data_dir() -> Path:
    """Returns the directory for user-specific data (logs, settings, etc.)."""
    path = Path.home() / ".antirickroll"
    path.mkdir(parents=True, exist_ok=True)
    return path

def get_plugins_dir() -> Path:
    """Returns the directory for fingerprint plugins."""
    # We allow plugins to be in the user data dir for better persistence
    path = get_user_data_dir() / "plugins" / "fingerprints"
    path.mkdir(parents=True, exist_ok=True)
    return path

def get_resource_path(relative_path: str) -> Path:
    """Returns the absolute path to a bundled resource."""
    return get_app_root() / relative_path
