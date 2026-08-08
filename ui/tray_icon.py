"""System tray integration."""

from PySide6.QtWidgets import QSystemTrayIcon, QMenu
from PySide6.QtGui import QIcon

class AntiRickRollTray(QSystemTrayIcon):
    """System tray icon with context menu."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        self.setIcon(QIcon())  # Placeholder
        menu = QMenu()
        restore_action = menu.addAction("Restore")
        exit_action = menu.addAction("Exit")

        self.setContextMenu(menu)
        self.setToolTip("AntiRickRoll is running")
