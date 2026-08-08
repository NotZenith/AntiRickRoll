"""Main application window."""

import logging
from PySide6.QtWidgets import QMainWindow, QHBoxLayout, QWidget, QStackedWidget, QLabel
from ui.sidebar import Sidebar
from ui.styles import DARK_THEME

class MainWindow(QMainWindow):
    """Main window with sidebar navigation and content area."""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AntiRickRoll")
        self.resize(1000, 600)
        self.setStyleSheet(DARK_THEME)
        self._setup_ui()

    def _setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QHBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.sidebar = Sidebar()
        self.sidebar.setFixedWidth(200)
        layout.addWidget(self.sidebar)

        self.content_area = QStackedWidget()
        layout.addWidget(self.content_area)

        # Placeholder views
        self.content_area.addWidget(QLabel("Status View"))
        self.content_area.addWidget(QLabel("Stats View"))
        self.content_area.addWidget(QLabel("Detection View"))
        self.content_area.addWidget(QLabel("Settings View"))
        self.content_area.addWidget(QLabel("Plugins View"))
        self.content_area.addWidget(QLabel("About View"))

        self.sidebar.nav_changed.connect(self._on_nav_changed)

    def _on_nav_changed(self, label: str):
        logging.info(f"Navigation changed to: {label}")
        indices = {"Status": 0, "Stats": 1, "Detection": 2, "Settings": 3, "Plugins": 4, "About": 5}
        self.content_area.setCurrentIndex(indices.get(label, 0))
