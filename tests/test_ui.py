"""Basic UI initialization tests."""

import pytest
from PySide6.QtWidgets import QApplication
from antirickroll.ui.main_window import MainWindow
from antirickroll.audio.engine import WindowsAudioEngine
from antirickroll.core.settings import SettingsManager
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
    window = MainWindow(engine, settings)
    assert window.windowTitle() == "AntiRickRoll"
    assert window.sidebar is not None
    assert window.content_area is not None
