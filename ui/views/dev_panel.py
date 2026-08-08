"""Developer panel for raw audio data and diagnostics."""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QLabel
from PySide6.QtCore import Qt

class DevPanel(QWidget):
    """Hidden developer panel for advanced diagnostics."""

    def __init__(self, audio_engine, parent=None):
        super().__init__(parent)
        self.engine = audio_engine
        self.setWindowTitle("AntiRickRoll Developer Diagnostics")
        self.resize(600, 400)
        self._setup_ui()
        self._connect_engine()

    def _setup_ui(self):
        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("Raw Audio Diagnostics"))

        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        self.log_area.setStyleSheet("background-color: black; color: #00ff00; font-family: monospace;")
        layout.addWidget(self.log_area)

    def _connect_engine(self):
        if self.engine.worker:
            self.engine.worker.metrics_updated.connect(self._log_metrics)

    def _log_metrics(self, metrics: dict):
        if self.isVisible():
            log_msg = "\n".join([f"{k}: {v}" for k, v in metrics.items()])
            self.log_area.setText(log_msg)
