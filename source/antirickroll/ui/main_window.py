"""Main application window."""

import logging
from PySide6.QtWidgets import QMainWindow, QHBoxLayout, QWidget, QStackedWidget
from antirickroll.ui.sidebar import Sidebar
from antirickroll.ui.styles import DARK_THEME
from antirickroll.ui.views.status_view import StatusView
from antirickroll.ui.views.stats_view import StatsView
from antirickroll.ui.views.dev_panel import DevPanel
from antirickroll.ui.views.detection_view import DetectionView
from antirickroll.ui.views.plugins_view import PluginsView
from antirickroll.ui.views.settings_view import SettingsView
from antirickroll.ui.views.about_view import AboutView
from PySide6.QtGui import QShortcut, QKeySequence

class MainWindow(QMainWindow):
    """Main window with sidebar navigation and content area."""
    def __init__(self, audio_engine, detection_service, database, settings) -> None:
        super().__init__()
        self.audio_engine = audio_engine
        self.detection_service = detection_service
        self.db = database
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
        self.detection_view = DetectionView(self.detection_service)
        self.plugins_view = PluginsView(self.db)
        self.settings_view = SettingsView(self.settings)
        self.about_view = AboutView()

        self.content_area.addWidget(self.status_view)
        self.content_area.addWidget(self.stats_view)
        self.content_area.addWidget(self.detection_view)
        self.content_area.addWidget(self.settings_view)
        self.content_area.addWidget(self.plugins_view)
        self.content_area.addWidget(self.about_view)

        self.sidebar.nav_changed.connect(self._on_nav_changed)

        # Hidden Dev Panel
        self.dev_panel = DevPanel(self.audio_engine)

    def _setup_shortcuts(self):
        self.dev_shortcut = QShortcut(QKeySequence("Ctrl+Shift+D"), self)
        self.dev_shortcut.activated.connect(self._toggle_dev_panel)

        self.mute_shortcut = QShortcut(QKeySequence("Ctrl+M"), self)
        self.mute_shortcut.activated.connect(self._toggle_mute)

        self.reload_shortcut = QShortcut(QKeySequence("Ctrl+R"), self)
        self.reload_shortcut.activated.connect(self.plugins_view.refresh_list)

    def _toggle_mute(self):
        is_muted = self.detection_service.toggle_mute()
        msg = "Alerts Muted" if is_muted else "Alerts Unmuted"
        self.statusBar().showMessage(msg, 3000)

    def _toggle_dev_panel(self):
        if self.dev_panel.isVisible():
            self.dev_panel.hide()
        else:
            self.dev_panel.show()

    def _on_nav_changed(self, label: str) -> None:
        logging.info(f"Navigation changed to: {label}")
        indices = {
            "Status": 0,
            "Stats": 1,
            "Detection": 2,
            "Settings": 3,
            "Plugins": 4,
            "About": 5
        }
        self.content_area.setCurrentIndex(indices.get(label, 0))
