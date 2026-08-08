"""System tray integration."""

from PySide6.QtWidgets import QSystemTrayIcon, QMenu
from PySide6.QtGui import QIcon
from antirickroll.core.paths import get_resource_path

class AntiRickRollTray(QSystemTrayIcon):
    """System tray icon with context menu for background operation."""
    def __init__(self, main_window, detection_service, parent=None):
        super().__init__(parent)
        self.main_window = main_window
        self.service = detection_service
        self._setup_ui()

    def _setup_ui(self):
        icon_path = get_resource_path("assets/icons/app.ico")
        if icon_path.exists():
            self.setIcon(QIcon(str(icon_path)))
        else:
            self.setIcon(QIcon())

        self.setToolTip("AntiRickRoll - Protecting your sanity")

        menu = QMenu()

        self.status_action = menu.addAction("Status: Monitoring")
        self.status_action.setEnabled(False)
        menu.addSeparator()

        self.pause_action = menu.addAction("Pause Monitoring")
        # Connection will be handled in application.py

        self.mute_action = menu.addAction("Mute Alerts")
        self.mute_action.setCheckable(True)
        self.mute_action.triggered.connect(self._toggle_mute)

        menu.addSeparator()

        menu.addAction("Open AntiRickRoll").triggered.connect(self.main_window.showNormal)
        menu.addAction("Settings").triggered.connect(lambda: self._open_page("Settings"))
        menu.addAction("About").triggered.connect(lambda: self._open_page("About"))

        menu.addSeparator()
        self.exit_action = menu.addAction("Exit")

        self.setContextMenu(menu)

    def _toggle_mute(self):
        is_muted = self.service.toggle_mute()
        self.mute_action.setChecked(is_muted)

    def _open_page(self, name: str):
        self.main_window.showNormal()
        self.main_window._on_nav_changed(name)
