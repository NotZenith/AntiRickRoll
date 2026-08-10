"""Main application class for lifecycle management."""

import sys
import logging
from pathlib import Path
from typing import Any
import platform
from PySide6.QtWidgets import QApplication, QMessageBox, QSystemTrayIcon
from antirickroll.core.settings import SettingsManager
from antirickroll.core.logger import setup_logging
from antirickroll.ui.main_window import MainWindow
from antirickroll.ui.tray_icon import AntiRickRollTray
from antirickroll.ui.welcome import WelcomeDialog
from antirickroll.audio.engine import WindowsAudioEngine
from antirickroll.detection.database.manager import FingerprintDatabase
from antirickroll.detection.matching.engine import MatchingEngine
from antirickroll.detection.workers.detection_worker import DetectionWorker
from antirickroll.detection.service import DetectionService
from antirickroll.detection.models import DetectionResult
from antirickroll.core.notifications import NotificationManager
from antirickroll.core.paths import get_user_data_dir, get_plugins_dir

class AntiRickRollApp:
    """Handles application lifecycle, core components, and UI."""
    def __init__(self) -> None:
        self._check_os_compatibility()
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
        self.tray = AntiRickRollTray(self.main_window, self.detection_service)
        self.notifications = NotificationManager(self.tray, self.settings)

        self._connect_signals()

    def _check_os_compatibility(self) -> None:
        """Verifies that the application is running on Windows."""
        if platform.system() != "Windows":
            print("AntiRickRoll is only supported on Windows.")
            sys.exit(1)

    def _connect_signals(self) -> None:
        self.tray.activated.connect(self._on_tray_activated)
        # Handle Exit from tray
        self.tray.exit_action.triggered.connect(self.shutdown)
        # Handle Pause from tray
        self.tray.pause_action.triggered.connect(self._toggle_monitoring)

        # Connect Detection Pipeline
        self.detection_worker.result_ready.connect(self.detection_service.handle_raw_result)
        self.detection_service.detection_confirmed.connect(self._on_detection_confirmed)

    def _on_tray_activated(self, reason: QSystemTrayIcon.ActivationReason) -> None:
        if reason == QSystemTrayIcon.Trigger:
            self.main_window.show()

    def _on_detection_confirmed(self, result: DetectionResult) -> None:
        self.notifications.play_alert_sound()
        self.notifications.notify(
            "AntiRickRoll Alert!",
            f"Detected: {result.name} by {result.artist}\nConfidence: {int(result.confidence*100)}%",
            "warning"
        )

    def _toggle_monitoring(self) -> None:
        if self.audio_engine.worker and not self.audio_engine.worker.paused:
            self.audio_engine.pause()
            self.tray.pause_action.setText("Resume Monitoring")
            self.tray.status_action.setText("Status: Paused")
        else:
            self.audio_engine.resume()
            self.tray.pause_action.setText("Pause Monitoring")
            self.tray.status_action.setText("Status: Monitoring")

    def run(self) -> None:
        """Starts the application."""
        if self.settings.get("first_run", True):
            welcome = WelcomeDialog()
            if welcome.exec() == WelcomeDialog.Accepted:
                self.settings.set("first_run", False)
            else:
                # User clicked settings or closed - maybe show settings later?
                pass

        self.main_window.show()
        self.tray.show()
        self.audio_engine.initialize()
        self.detection_worker.start()
        sys.exit(self.app.exec())

    def shutdown(self) -> None:
        """Gracefully shuts down the application."""
        logging.info("Shutting down...")
        self.detection_worker.stop()
        self.audio_engine.shutdown()
        self.settings.save()
        self.app.quit()

def handle_exception(exc_type: type, exc_value: Exception, exc_traceback: Any) -> None:
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
