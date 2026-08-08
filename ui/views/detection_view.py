"""Main dashboard view for real-time detection monitoring."""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QProgressBar, QListWidget, QFrame
)
from PySide6.QtCore import Qt, Slot
from detection.models import DetectionResult

class DetectionView(QWidget):
    """Real-time detection dashboard."""

    def __init__(self, detection_service, parent=None):
        super().__init__(parent)
        self.service = detection_service
        self._setup_ui()
        self._connect_signals()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # Header
        header = QLabel("Detection Dashboard")
        header.setStyleSheet("font-size: 24px; font-weight: bold; color: white;")
        layout.addWidget(header)

        # Status Card
        status_card = QFrame()
        status_card.setStyleSheet("background-color: #1a1a1a; border-radius: 10px; border: 1px solid #333;")
        status_layout = QVBoxLayout(status_card)

        self.status_lbl = QLabel("Monitoring Status: ACTIVE")
        self.status_lbl.setStyleSheet("font-size: 18px; color: #00ff7f;")
        status_layout.addWidget(self.status_lbl)

        self.current_match_lbl = QLabel("Current Match: None")
        self.current_match_lbl.setStyleSheet("font-size: 14px; color: #888;")
        status_layout.addWidget(self.current_match_lbl)

        layout.addWidget(status_card)

        # Confidence Gauge
        gauge_layout = QVBoxLayout()
        gauge_layout.addWidget(QLabel("Match Confidence"))
        self.confidence_bar = QProgressBar()
        self.confidence_bar.setRange(0, 100)
        self.confidence_bar.setValue(0)
        self.confidence_bar.setTextVisible(True)
        self.confidence_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #333;
                border-radius: 5px;
                background-color: #222;
                text-align: center;
                height: 30px;
            }
            QProgressBar::chunk {
                background-color: #0078d4;
                border-radius: 4px;
            }
        """)
        gauge_layout.addWidget(self.confidence_bar)
        layout.addLayout(gauge_layout)

        # Match History
        history_layout = QVBoxLayout()
        history_layout.addWidget(QLabel("Recent Detections"))
        self.history_list = QListWidget()
        self.history_list.setStyleSheet("background-color: #111; border: 1px solid #333; color: #eee;")
        history_layout.addWidget(self.history_list)
        layout.addLayout(history_layout)

    def _connect_signals(self):
        self.service.confidence_updated.connect(self._on_confidence_updated)
        self.service.detection_confirmed.connect(self._on_detection_confirmed)
        self.service.status_updated.connect(self._on_status_updated)

    @Slot(float, str)
    def _on_confidence_updated(self, confidence: float, name: str):
        self.confidence_bar.setValue(int(confidence * 100))
        self.current_match_lbl.setText(f"Current Match: {name}")

        # Color based on confidence
        if confidence > 0.8:
            color = "#ff4444" # Red for high risk
        elif confidence > 0.4:
            color = "#ffbb33" # Yellow for warning
        else:
            color = "#0078d4" # Blue for normal

        self.confidence_bar.setStyleSheet(self.confidence_bar.styleSheet().replace(
            "background-color: #0078d4", f"background-color: {color}"
        ).replace("background-color: #ff4444", f"background-color: {color}").replace(
            "background-color: #ffbb33", f"background-color: {color}"
        ))

    @Slot(DetectionResult)
    def _on_detection_confirmed(self, result: DetectionResult):
        item = f"[{result.timestamp}] DETECTED: {result.name} ({int(result.confidence*100)}% confidence)"
        self.history_list.insertItem(0, item)

    @Slot(str)
    def _on_status_updated(self, status: str):
        self.status_lbl.setText(f"Monitoring Status: {status}")
        if "DETECTED" in status:
            self.status_lbl.setStyleSheet("font-size: 18px; color: #ff4444;")
        else:
            self.status_lbl.setStyleSheet("font-size: 18px; color: #00ff7f;")
