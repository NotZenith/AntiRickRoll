"""Real-time waveform visualization widget."""

import numpy as np
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QPainter, QPen, QColor, QGradient, QLinearGradient

class WaveformWidget(QWidget):
    """
    A widget that renders a real-time audio waveform.
    Optimized for performance using QPainter.
    """

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setMinimumHeight(150)
        self.data = np.zeros(0)
        self.background_color = QColor(20, 20, 20)
        self.line_color = QColor(0, 255, 127) # Spring Green
        self._max_samples = 1000

    def update_data(self, data: np.ndarray):
        """Updates the waveform data."""
        # Convert to mono if multi-channel
        if len(data.shape) > 1:
            data = np.mean(data, axis=1)

        # Append and truncate
        self.data = np.concatenate((self.data, data))
        if len(self.data) > self._max_samples:
            self.data = self.data[-self._max_samples:]

        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Draw background
        painter.fillRect(self.rect(), self.background_color)

        if len(self.data) < 2:
            return

        # Draw center line
        painter.setPen(QPen(QColor(50, 50, 50), 1, Qt.DashLine))
        painter.drawLine(0, self.height() // 2, self.width(), self.height() // 2)

        # Draw waveform
        painter.setPen(QPen(self.line_color, 2))

        width = self.width()
        height = self.height()
        mid_y = height / 2

        # Map samples to points
        points = []
        x_step = width / (len(self.data) - 1)

        # Scaling factor to make waveform visible
        # We assume data is normalized between -1 and 1
        scale_y = mid_y * 0.8

        for i, val in enumerate(self.data):
            x = i * x_step
            y = mid_y - (val * scale_y)
            points.append(QPointF(x, y))

        painter.drawPolyline(points)

class PeakMeter(QWidget):
    """A simple peak level meter."""
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setFixedWidth(20)
        self.level = 0.0 # 0.0 to 1.0

    def set_level(self, level: float):
        self.level = min(1.0, max(0.0, level))
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        rect = self.rect()

        painter.fillRect(rect, QColor(30, 30, 30))

        h = int(rect.height() * self.level)
        meter_rect = rect.adjusted(2, rect.height() - h, -2, 0)

        gradient = QLinearGradient(0, rect.height(), 0, 0)
        gradient.setColorAt(0, QColor(0, 255, 0))    # Green
        gradient.setColorAt(0.7, QColor(255, 255, 0)) # Yellow
        gradient.setColorAt(1.0, QColor(255, 0, 0))   # Red

        painter.fillRect(meter_rect, gradient)
