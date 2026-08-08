"""Basic UI initialization tests."""

import pytest
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow

@pytest.fixture(scope="session")
def qapp():
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    yield app

def test_main_window_init(qapp):
    window = MainWindow()
    assert window.windowTitle() == "AntiRickRoll"
    assert window.sidebar is not None
    assert window.content_area is not None
