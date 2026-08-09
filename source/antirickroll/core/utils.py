"""General utility functions for AntiRickRoll."""

import sys
from pathlib import Path
import logging

def set_start_on_boot(enabled: bool) -> bool:
    """
    Enables or disables automatic startup with Windows using the Registry.
    Only works on Windows and when the app is bundled as an executable.
    """
    if sys.platform != "win32":
        return False

    import winreg

    app_name = "AntiRickRoll"
    key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"

    try:
        # Determine the executable path
        if getattr(sys, 'frozen', False):
            exe_path = sys.executable
        else:
            # Fallback for development mode (not recommended for actual startup)
            exe_path = f'"{sys.executable}" -m antirickroll.app.main'

        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE)

        if enabled:
            winreg.SetValueEx(key, app_name, 0, winreg.REG_SZ, exe_path)
            logging.info("Enabled startup with Windows.")
        else:
            try:
                winreg.DeleteValue(key, app_name)
                logging.info("Disabled startup with Windows.")
            except FileNotFoundError:
                pass # Already disabled

        winreg.CloseKey(key)
        return True
    except Exception as e:
        logging.error(f"Failed to update startup registry: {e}")
        return False
