"""Main application class for lifecycle management."""

import sys
import logging
from pathlib import Path
from PySide6.QtWidgets import QApplication, QMessageBox
from antirickroll.core.settings import SettingsManager
from antirickroll.core.logger import setup_logging
from antirickroll.ui.main_window import MainWindow
from antirickroll.ui.tray_icon import AntiRickRollTray
from antirickroll.audio.engine import WindowsAudioEngine
from antirickroll.detection.database.manager import FingerprintDatabase
from antirickroll.detection.matching.engine import MatchingEngine
from antirickroll.detection.workers.detection_worker import DetectionWorker
from antirickroll.detection.service import DetectionService
from antirickroll.core.notifications import NotificationManager
from antirickroll.core.paths import get_user_data_dir, get_plugins_dir

class AntiRickRollApp:
    """Handles application lifecycle, core components, and UI."""
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setApplicationName("AntiRickRoll")

        # Setup paths
        self.app_dir = get_user_data_dir()

        # Initialize core
        setup_logging(self.app_dir / "logs" / "app.log")
        self.settings = SettingsManager(self.app_dir / "config" / "settings.json")

        # Initialize Audio Engine
        self.audio_engine = WindowsAudioEngine(self.settings)

        # Initialize Detection Engine
        self.db = FingerprintDatabase(get_plugins_dir())
        self.db.load_all()
        self.matcher = MatchingEngine(self.db)
        self.detection_worker = DetectionWorker(self.audio_engine, self.matcher, self.settings)
        self.detection_service = DetectionService(self.settings)

        # Initialize UI
        self.main_window = MainWindow(self.audio_engine, self.detection_service, self.db, self.settings)
        self.tray = AntiRickRollTray(self.main_window)
        self.notifications = NotificationManager(self.tray, self.settings)

        self._connect_signals()

    def _connect_signals(self):
        self.tray.activated.connect(self._on_tray_activated)
        # Handle Exit from tray
        self.tray.contextMenu().actions()[1].triggered.connect(self.shutdown)
        # Handle Restore from tray
        self.tray.contextMenu().actions()[0].triggered.connect(self.main_window.show)

        # Connect Detection Pipeline
        self.detection_worker.result_ready.connect(self.detection_service.handle_raw_result)
        self.detection_service.detection_confirmed.connect(self._on_detection_confirmed)

    def _on_tray_activated(self, reason):
        if reason == AntiRickRollTray.Trigger:
            self.main_window.show()

    def _on_detection_confirmed(self, result):
        self.notifications.play_alert_sound()
        self.notifications.notify(
            "AntiRickRoll Alert!",
            f"Detected: {result.name} by {result.artist}\nConfidence: {int(result.confidence*100)}%",
            "warning"
        )

    def run(self):
        """Starts the application."""
        self.main_window.show()
        self.tray.show()
        self.detection_worker.start()
        sys.exit(self.app.exec())

    def shutdown(self):
        """Gracefully shuts down the application."""
        logging.info("Shutting down...")
        self.detection_worker.stop()
        self.audio_engine.shutdown()
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
