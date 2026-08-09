"""Basic UI initialization tests."""

import pytest
from PySide6.QtWidgets import QApplication
from antirickroll.ui.main_window import MainWindow
from antirickroll.audio.engine import WindowsAudioEngine
from antirickroll.core.settings import SettingsManager
from antirickroll.detection.service import DetectionService
from antirickroll.detection.database.manager import FingerprintDatabase
from pathlib import Path

@pytest.fixture(scope="session")
def qapp():
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    yield app

def test_main_window_init(qapp, tmp_path):
    settings = SettingsManager(tmp_path / "settings.json")
    engine = WindowsAudioEngine(settings)
    db = FingerprintDatabase(tmp_path / "fingerprints")
    service = DetectionService(settings)
    window = MainWindow(engine, service, db, settings)
    assert window.windowTitle() == "AntiRickRoll"
    assert window.sidebar is not None
    assert window.content_area is not None
