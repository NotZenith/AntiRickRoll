"""Statistics view for audio engine metrics."""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLabel, QGroupBox
from PySide6.QtCore import Qt

class StatsView(QWidget):
    """Displays real-time performance and audio metrics."""

    def __init__(self, audio_engine, parent=None):
        super().__init__(parent)
        self.engine = audio_engine
        self._setup_ui()
        self._connect_engine()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        header = QLabel("Audio Engine Statistics")
        header.setStyleSheet("font-size: 24px; font-weight: bold; color: white;")
        layout.addWidget(header)

        grid = QGridLayout()
        layout.addLayout(grid)

        # Device Info Group
        device_group = QGroupBox("Device Information")
        device_layout = QGridLayout(device_group)
        self.labels = {}

        metrics = [
            ("Device Name:", "n/a"),
            ("Sample Rate:", "n/a"),
            ("Channels:", "n/a"),
            ("Bit Depth:", "32-bit float")
        ]

        for i, (text, val) in enumerate(metrics):
            device_layout.addWidget(QLabel(text), i, 0)
            lbl = QLabel(val)
            lbl.setStyleSheet("color: #00ff7f; font-weight: bold;")
            device_layout.addWidget(lbl, i, 1)
            self.labels[text] = lbl

        grid.addWidget(device_group, 0, 0)

        # Buffer Stats Group
        buffer_group = QGroupBox("Buffer Statistics")
        buffer_layout = QGridLayout(buffer_group)

        metrics = [
            ("Buffer Usage:", "0%"),
            ("Latency:", "0 ms"),
            ("Dropped Frames:", "0"),
            ("Overflows:", "0"),
            ("Underflows:", "0")
        ]

        for i, (text, val) in enumerate(metrics):
            buffer_layout.addWidget(QLabel(text), i, 0)
            lbl = QLabel(val)
            lbl.setStyleSheet("color: #00ff7f; font-weight: bold;")
            buffer_layout.addWidget(lbl, i, 1)
            self.labels[text] = lbl

        grid.addWidget(buffer_group, 0, 1)

        layout.addStretch()

    def _connect_engine(self):
        if self.engine.worker:
            self.engine.worker.metrics_updated.connect(self._update_metrics)

    def _update_metrics(self, metrics: dict):
        # Update labels based on metrics dict
        self.labels["Buffer Usage:"].setText(f"{metrics.get('usage_pct', 0):.1f}%")
        self.labels["Latency:"].setText(f"{metrics.get('latency', 0)*1000:.1f} ms")
        self.labels["Dropped Frames:"].setText(str(metrics.get("dropped_frames", 0)))
        self.labels["Overflows:"].setText(str(metrics.get("overflow_count", 0)))
        self.labels["Underflows:"].setText(str(metrics.get("underflow_count", 0)))
        self.labels["Sample Rate:"].setText(f"{metrics.get('sample_rate', 0)} Hz")
        self.labels["Channels:"].setText(str(metrics.get("channels", 0)))

        # We need device name too, but it might not be in the metrics dict
        # We can fetch it once or periodically from engine
