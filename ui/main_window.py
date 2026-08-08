"""Main application window."""

import logging
from PySide6.QtWidgets import QMainWindow, QHBoxLayout, QWidget, QStackedWidget, QLabel
from ui.sidebar import Sidebar
from ui.styles import DARK_THEME
from ui.views.status_view import StatusView
from ui.views.stats_view import StatsView
from ui.views.dev_panel import DevPanel
from PySide6.QtGui import QShortcut, QKeySequence

class MainWindow(QMainWindow):
    """Main window with sidebar navigation and content area."""
    def __init__(self, audio_engine, settings):
        super().__init__()
        self.audio_engine = audio_engine
        self.settings = settings

        self.setWindowTitle("AntiRickRoll")
        self.resize(1000, 600)
        self.setStyleSheet(DARK_THEME)
        self._setup_ui()
        self._setup_shortcuts()

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

        # Real views
        self.status_view = StatusView(self.audio_engine)
        self.stats_view = StatsView(self.audio_engine)

        self.content_area.addWidget(self.status_view)
        self.content_area.addWidget(self.stats_view)
        self.content_area.addWidget(QLabel("Detection View"))
        self.content_area.addWidget(QLabel("Settings View"))
        self.content_area.addWidget(QLabel("Plugins View"))
        self.content_area.addWidget(QLabel("About View"))

        self.sidebar.nav_changed.connect(self._on_nav_changed)

        # Hidden Dev Panel
        self.dev_panel = DevPanel(self.audio_engine)

    def _setup_shortcuts(self):
        self.dev_shortcut = QShortcut(QKeySequence("Ctrl+Shift+D"), self)
        self.dev_shortcut.activated.connect(self._toggle_dev_panel)

    def _toggle_dev_panel(self):
        if self.dev_panel.isVisible():
            self.dev_panel.hide()
        else:
            self.dev_panel.show()

    def _on_nav_changed(self, label: str):
        logging.info(f"Navigation changed to: {label}")
        indices = {"Status": 0, "Stats": 1, "Detection": 2, "Settings": 3, "Plugins": 4, "About": 5}
        self.content_area.setCurrentIndex(indices.get(label, 0))
