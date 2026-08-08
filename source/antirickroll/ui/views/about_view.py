"""About page for AntiRickRoll."""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt
import webbrowser

class AboutView(QWidget):
    """View showing application information and credits."""

    def __init__(self, parent=None):
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
        version = QLabel("Version 0.5.0")
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
        github_btn = QPushButton("View on GitHub")
        github_btn.setFixedSize(150, 40)
        github_btn.clicked.connect(lambda: webbrowser.open("https://github.com/NotZenith/AntiRickRoll"))
        layout.addWidget(github_btn, alignment=Qt.AlignCenter)

        layout.addSpacing(20)

        # License & Credits
        footer = QLabel("Licensed under MIT License<br>© 2026 AntiRickRoll Open Source Project")
        footer.setAlignment(Qt.AlignCenter)
        footer.setStyleSheet("color: #666; font-size: 12px;")
        layout.addWidget(footer, alignment=Qt.AlignCenter)

        layout.addStretch()
