"""Status view showing real-time audio visualization."""

import numpy as np
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFrame
)
from antirickroll.audio.visualization.waveform import WaveformWidget, PeakMeter

class StatusView(QWidget):
    """Main status view with audio visualization and controls."""

    def __init__(self, audio_engine, parent=None) -> None:
        super().__init__(parent)
        self.engine = audio_engine
        self._setup_ui()
        self._connect_engine()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # Header
        header = QLabel("Audio Engine Status")
        header.setStyleSheet("font-size: 24px; font-weight: bold; color: white;")
        layout.addWidget(header)

        # Visualization Area
        viz_container = QFrame()
        viz_container.setFrameShape(QFrame.StyledPanel)
        viz_container.setStyleSheet("background-color: #1a1a1a; border-radius: 10px; border: 1px solid #333;")
        viz_layout = QHBoxLayout(viz_container)

        self.waveform = WaveformWidget()
        viz_layout.addWidget(self.waveform, stretch=1)

        self.peak_meter = PeakMeter()
        viz_layout.addWidget(self.peak_meter)

        layout.addWidget(viz_container, stretch=1)

        # Info Area
        self.status_label = QLabel("Status: Idle")
        self.status_label.setStyleSheet("color: #888; font-size: 14px;")
        layout.addWidget(self.status_label)

        # Controls
        controls_layout = QHBoxLayout()
        self.start_btn = QPushButton("Start Engine")
        self.start_btn.setFixedSize(120, 40)
        self.start_btn.setStyleSheet("""
            QPushButton { background-color: #0078d4; color: white; border-radius: 5px; font-weight: bold; }
            QPushButton:hover { background-color: #005a9e; }
        """)
        self.start_btn.clicked.connect(self._toggle_engine)

        self.stop_btn = QPushButton("Stop Engine")
        self.stop_btn.setFixedSize(120, 40)
        self.stop_btn.setStyleSheet("""
            QPushButton { background-color: #444; color: white; border-radius: 5px; font-weight: bold; }
            QPushButton:hover { background-color: #555; }
        """)
        self.stop_btn.setEnabled(False)
        self.stop_btn.clicked.connect(self._toggle_engine)

        controls_layout.addWidget(self.start_btn)
        controls_layout.addWidget(self.stop_btn)
        controls_layout.addStretch()

        layout.addLayout(controls_layout)

    def _connect_engine(self):
        """Connects signals from the audio engine worker."""
        if self.engine.worker:
            self.engine.worker.waveform_data.connect(self._on_waveform_data)
            self.engine.worker.status_changed.connect(self._on_status_changed)

    def _toggle_engine(self):
        if not self.engine.is_running:
            self.engine.initialize()
            self._connect_engine()
        else:
            self.engine.shutdown()

    def _on_waveform_data(self, data: np.ndarray):
        self.waveform.update_data(data)
        # Calculate peak for the meter
        peak = np.max(np.abs(data))
        self.peak_meter.set_level(peak)

    def _on_status_changed(self, msg: str, is_active: bool):
        self.status_label.setText(f"Status: {msg}")
        self.start_btn.setEnabled(not is_active)
        self.stop_btn.setEnabled(is_active)

        if is_active:
            self.status_label.setStyleSheet("color: #00ff7f; font-size: 14px;")
        else:
            self.status_label.setStyleSheet("color: #888; font-size: 14px;")
