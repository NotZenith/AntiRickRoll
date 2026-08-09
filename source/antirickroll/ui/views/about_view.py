"""About page for AntiRickRoll."""

import webbrowser

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QLabel, QMessageBox, QPushButton, QVBoxLayout, QWidget

import antirickroll

class AboutView(QWidget):
    """View showing application information and credits."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setAlignment(Qt.AlignCenter)

        # Title
        title = QLabel("AntiRickRoll")
        title.setStyleSheet("font-size: 36px; font-weight: bold; color: #0078d4;")
        layout.addWidget(title, alignment=Qt.AlignCenter)

        # Version
        version = QLabel(f"Version {antirickroll.__version__}")
        version.setStyleSheet("font-size: 16px; color: #888;")
        layout.addWidget(version, alignment=Qt.AlignCenter)

        layout.addSpacing(20)

        # Description
        desc = QLabel(
            "A production-quality Windows application to detect and prevent "
            "unwanted Rickrolls using real-time audio fingerprinting."
        )
        desc.setWordWrap(True)
        desc.setAlignment(Qt.AlignCenter)
        desc.setStyleSheet("font-size: 14px; max-width: 400px;")
        layout.addWidget(desc, alignment=Qt.AlignCenter)

        layout.addSpacing(30)

        # Links
        btn_layout = QHBoxLayout()
        github_btn = QPushButton("GitHub Repository")
        github_btn.clicked.connect(lambda: webbrowser.open("https://github.com/NotZenith/AntiRickRoll"))

        issue_btn = QPushButton("Report a Problem")
        issue_btn.clicked.connect(lambda: webbrowser.open("https://github.com/NotZenith/AntiRickRoll/issues"))

        btn_layout.addWidget(github_btn)
        btn_layout.addWidget(issue_btn)
        layout.addLayout(btn_layout, alignment=Qt.AlignCenter)

        layout.addSpacing(20)

        privacy_link = QPushButton("Privacy Policy")
        privacy_link.setFlat(True)
        privacy_link.setStyleSheet("color: #0078d4; text-decoration: underline;")
        privacy_link.clicked.connect(self._show_privacy)
        layout.addWidget(privacy_link, alignment=Qt.AlignCenter)

        layout.addSpacing(20)

        # License & Credits
        footer = QLabel("Licensed under MIT License<br>© 2026 AntiRickRoll Open Source Project")
        footer.setAlignment(Qt.AlignCenter)
        footer.setStyleSheet("color: #666; font-size: 12px;")
        layout.addWidget(footer, alignment=Qt.AlignCenter)

        layout.addStretch()

    def _show_privacy(self):
        msg = QMessageBox(self)
        msg.setWindowTitle("AntiRickRoll Privacy Policy")
        msg.setText(
            "<b>AntiRickRoll is built with privacy as a top priority.</b><br><br>"
            "1. <b>Local Processing:</b> All audio analysis is performed on your computer.<br>"
            "2. <b>No Uploads:</b> No audio, fingerprints, or listening history are ever sent to any server.<br>"
            "3. <b>No Microphone:</b> The app only uses Windows Loopback to listen to playback audio.<br>"
            "4. <b>No Telemetry:</b> We do not collect usage statistics or crash reports automatically.<br><br>"
            "Your data stays yours."
        )
        msg.exec()
