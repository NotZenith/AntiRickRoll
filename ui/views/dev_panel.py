"""Developer panel for raw audio data and diagnostics."""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QLabel, QTabWidget
from PySide6.QtCore import Qt
from detection.analysis.spectrogram import SpectrogramGenerator

class DevPanel(QWidget):
    """Hidden developer panel for advanced diagnostics."""

    def __init__(self, audio_engine, parent=None):
        super().__init__(parent)
        self.engine = audio_engine
        self.setWindowTitle("AntiRickRoll Developer Diagnostics")
        self.resize(800, 600)

        self.spec_gen = SpectrogramGenerator()
        self._setup_ui()
        self._connect_engine()

    def _setup_ui(self):
        layout = QVBoxLayout(self)

        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)

        # Log Tab
        log_tab = QWidget()
        log_layout = QVBoxLayout(log_tab)
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        self.log_area.setStyleSheet("background-color: black; color: #00ff00; font-family: monospace;")
        log_layout.addWidget(self.log_area)
        self.tabs.addTab(log_tab, "Metrics")

        # Spectrogram Tab
        spec_tab = QWidget()
        spec_layout = QVBoxLayout(spec_tab)
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        spec_layout.addWidget(self.canvas)
        self.tabs.addTab(spec_tab, "Spectrogram")

    def _connect_engine(self):
        if self.engine.worker:
            self.engine.worker.metrics_updated.connect(self._log_metrics)
            self.engine.worker.waveform_data.connect(self._update_spectrogram)

    def _log_metrics(self, metrics: dict):
        if self.isVisible() and self.tabs.currentIndex() == 0:
            log_msg = "\n".join([f"{k}: {v}" for k, v in metrics.items()])
            self.log_area.setText(log_msg)

    def _update_spectrogram(self, data: np.ndarray):
        if self.isVisible() and self.tabs.currentIndex() == 1:
            # We use a smaller window for real-time visualization
            f, t, Sxx = self.spec_gen.generate(data)

            self.ax.clear()
            self.ax.pcolormesh(t, f, Sxx, shading='gouraud', cmap='magma')
            self.ax.set_ylabel('Frequency [Hz]')
            self.ax.set_xlabel('Time [sec]')
            self.canvas.draw()
