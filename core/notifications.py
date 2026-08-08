"""Notification and alert management for Windows."""

import logging
import platform
from typing import Optional

# Only import winsound on Windows
if platform.system() == "Windows":
    import winsound
else:
    winsound = None

class NotificationManager:
    """Handles audible alerts and system tray notifications."""

    def __init__(self, tray_icon, settings):
        self.logger = logging.getLogger(__name__)
        self.tray = tray_icon
        self.settings = settings

    def notify(self, title: str, message: str, icon_type: str = "information"):
        """Displays a system tray notification."""
        if not self.settings.get("enable_notifications", True):
            return

        from PySide6.QtWidgets import QSystemTrayIcon

        icon_map = {
            "information": QSystemTrayIcon.Information,
            "warning": QSystemTrayIcon.Warning,
            "critical": QSystemTrayIcon.Critical
        }

        qt_icon = icon_map.get(icon_type, QSystemTrayIcon.Information)
        self.tray.showMessage(title, message, qt_icon, 5000)
        self.logger.info(f"Notification sent: {title} - {message}")

    def play_alert_sound(self):
        """Plays a short notification beep."""
        if not self.settings.get("enable_beep", True):
            return

        try:
            if winsound:
                # Frequency 1000Hz, Duration 200ms
                winsound.Beep(1000, 200)
            else:
                self.logger.warning("winsound not available on this platform.")
        except Exception as e:
            self.logger.error(f"Failed to play alert sound: {e}")
