"""Plugin management view for fingerprints."""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QPushButton, QLabel, QListWidgetItem
)
from PySide6.QtCore import Qt

class PluginsView(QWidget):
    """View to manage fingerprint plugins."""

    def __init__(self, database, parent=None):
        super().__init__(parent)
        self.db = database
        self._setup_ui()
        self.refresh_list()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        header_layout = QHBoxLayout()
        header = QLabel("Fingerprint Plugins")
        header.setStyleSheet("font-size: 24px; font-weight: bold; color: white;")
        header_layout.addWidget(header)

        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.setFixedSize(100, 30)
        self.refresh_btn.clicked.connect(self.refresh_list)
        header_layout.addWidget(self.refresh_btn)

        layout.addLayout(header_layout)

        self.plugin_list = QListWidget()
        self.plugin_list.setStyleSheet("background-color: #1a1a1a; border: 1px solid #333; color: #eee; font-size: 14px;")
        layout.addWidget(self.plugin_list)

        self.detail_lbl = QLabel("Select a plugin to see details.")
        self.detail_lbl.setWordWrap(True)
        self.detail_lbl.setStyleSheet("color: #888; padding: 10px; background-color: #111; border-radius: 5px;")
        layout.addWidget(self.detail_lbl)

        self.plugin_list.itemClicked.connect(self._on_item_clicked)

    def refresh_list(self):
        """Reloads the list from the database."""
        self.plugin_list.clear()
        self.db.load_all()

        for pkg_id, pkg in self.db.packages.items():
            item = QListWidgetItem(f"{pkg.metadata.name} - {pkg.metadata.artist}")
            item.setData(Qt.UserRole, pkg_id)
            self.plugin_list.addItem(item)

        if self.plugin_list.count() == 0:
            self.plugin_list.addItem("No fingerprints found in plugins/fingerprints/")

    def _on_item_clicked(self, item):
        pkg_id = item.data(Qt.UserRole)
        if not pkg_id:
            return

        pkg = self.db.get_package(pkg_id)
        if pkg:
            meta = pkg.metadata
            details = (
                f"<b>ID:</b> {meta.id}<br>"
                f"<b>Name:</b> {meta.name}<br>"
                f"<b>Artist:</b> {meta.artist}<br>"
                f"<b>Duration:</b> {meta.duration:.2f}s<br>"
                f"<b>Hashes:</b> {len(pkg.hashes)}<br>"
                f"<b>Description:</b> {meta.description or 'None'}"
            )
            self.detail_lbl.setText(details)
