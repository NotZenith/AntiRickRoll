"""Sidebar navigation for the main window."""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QButtonGroup
from PySide6.QtCore import Signal

class Sidebar(QWidget):
    """Navigation sidebar with category buttons."""
    nav_changed = Signal(str)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        self.button_group = QButtonGroup(self)

        buttons = ["Status", "Stats", "Detection", "Settings", "Plugins", "About"]
        for label in buttons:
            btn = QPushButton(label)
            btn.setCheckable(True)
            self.button_group.addButton(btn)
            layout.addWidget(btn)
            btn.clicked.connect(lambda checked, l=label: self.nav_changed.emit(l))

        layout.addStretch()
        self.button_group.buttons()[0].setChecked(True)
