"""Main application class for lifecycle management."""

import sys
import logging
from pathlib import Path
from PySide6.QtWidgets import QApplication, QMessageBox
from core.settings import SettingsManager
from core.logger import setup_logging
from ui.main_window import MainWindow
from ui.tray_icon import AntiRickRollTray
from audio.engine import WindowsAudioEngine

class AntiRickRollApp:
    """Handles application lifecycle, core components, and UI."""
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setApplicationName("AntiRickRoll")

        # Setup paths
        self.app_dir = Path.home() / ".antirickroll"
        self.app_dir.mkdir(exist_ok=True)

        # Initialize core
        setup_logging(self.app_dir / "logs" / "app.log")
        self.settings = SettingsManager(self.app_dir / "config" / "settings.json")

        # Initialize Audio Engine
        self.audio_engine = WindowsAudioEngine(self.settings)

        # Initialize UI
        self.main_window = MainWindow(self.audio_engine, self.settings)
        self.tray = AntiRickRollTray(self.main_window)

        self._connect_signals()

    def _connect_signals(self):
        self.tray.activated.connect(self._on_tray_activated)
        # Handle Exit from tray
        self.tray.contextMenu().actions()[1].triggered.connect(self.shutdown)
        # Handle Restore from tray
        self.tray.contextMenu().actions()[0].triggered.connect(self.main_window.show)

    def _on_tray_activated(self, reason):
        if reason == AntiRickRollTray.Trigger:
            self.main_window.show()

    def run(self):
        """Starts the application."""
        self.main_window.show()
        self.tray.show()
        sys.exit(self.app.exec())

    def shutdown(self):
        """Gracefully shuts down the application."""
        logging.info("Shutting down...")
        self.settings.save()
        self.app.quit()

def handle_exception(exc_type, exc_value, exc_traceback):
    """Global exception handler to show a crash dialog."""
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    logging.critical("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)
    msg.setText("A critical error occurred.")
    msg.setInformativeText(str(exc_value))
    msg.setWindowTitle("AntiRickRoll Error")
    msg.exec()

    sys.exit(1)
