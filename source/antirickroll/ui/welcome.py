"""Welcome screen for first-time users."""

from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PySide6.QtCore import Qt

class WelcomeDialog(QDialog):
    """Simple onboarding dialog."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Welcome to AntiRickRoll")
        self.setFixedSize(500, 400)
        self.setModal(True)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        title = QLabel("🛡️ AntiRickRoll")
        title.setStyleSheet("font-size: 32px; font-weight: bold; color: #0078d4;")
        layout.addWidget(title, alignment=Qt.AlignCenter)

        desc = QLabel(
            "AntiRickRoll protects your ears by monitoring system audio and "
            "blocking the famous song automatically.\n\n"
            "• <b>Local Processing:</b> No audio leaves your computer.\n"
            "• <b>No Microphone:</b> We only listen to playback audio.\n"
            "• <b>Privacy First:</b> No tracking, no telemetry."
        )
        desc.setWordWrap(True)
        desc.setStyleSheet("font-size: 14px;")
        layout.addWidget(desc)

        layout.addStretch()

        btn_layout = QHBoxLayout()
        self.start_btn = QPushButton("Start Monitoring")
        self.start_btn.setFixedSize(150, 40)
        self.start_btn.setStyleSheet("background-color: #0078d4; font-weight: bold;")
        self.start_btn.clicked.connect(self.accept)

        self.settings_btn = QPushButton("Settings")
        self.settings_btn.setFixedSize(100, 40)
        self.settings_btn.clicked.connect(self.reject) # We'll handle this in app logic

        btn_layout.addWidget(self.start_btn)
        btn_layout.addWidget(self.settings_btn)
        layout.addLayout(btn_layout)
