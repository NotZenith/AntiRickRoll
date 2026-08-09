"""Categorized settings view with descriptions."""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QSlider, QCheckBox, QLabel,
    QGroupBox, QPushButton, QHBoxLayout, QTabWidget
)
from PySide6.QtCore import Qt

class SettingsView(QWidget):
    """Professional categorized settings panel."""

    def __init__(self, settings_manager, parent=None) -> None:
        super().__init__(parent)
        self.settings = settings_manager
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        header = QLabel("Application Settings")
        header.setStyleSheet("font-size: 24px; font-weight: bold; color: white;")
        layout.addWidget(header)

        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)

        # 1. General Tab
        gen_tab = QWidget()
        gen_layout = QVBoxLayout(gen_tab)

        self.minimize_cb = QCheckBox("Minimize to System Tray")
        self.minimize_cb.setToolTip("Keep the app running in the background when closed.")
        self.minimize_cb.setChecked(self.settings.get("minimize_to_tray", True))
        gen_layout.addWidget(self.minimize_cb)

        self.auto_start_cb = QCheckBox("Start with Windows")
        self.auto_start_cb.setToolTip("Automatically launch AntiRickRoll when you log in.")
        self.auto_start_cb.setChecked(self.settings.get("auto_start", False))
        gen_layout.addWidget(self.auto_start_cb)

        gen_layout.addStretch()
        self.tabs.addTab(gen_tab, "General")

        # 2. Detection Tab
        det_tab = QWidget()
        det_layout = QFormLayout(det_tab)

        det_cfg = self.settings.get("detection", {})

        self.confidence_slider = QSlider(Qt.Horizontal)
        self.confidence_slider.setRange(10, 95)
        self.confidence_slider.setValue(int(det_cfg.get("min_confidence", 0.6) * 100))
        det_layout.addRow("Detection Confidence (%):", self.confidence_slider)
        det_layout.addRow("", QLabel("<small>Higher values reduce false positives but might miss some matches.</small>"))

        self.sensitivity_slider = QSlider(Qt.Horizontal)
        self.sensitivity_slider.setRange(1, 100)
        self.sensitivity_slider.setValue(int(self.settings.get("sensitivity", 0.8) * 100))
        det_layout.addRow("Input Sensitivity:", self.sensitivity_slider)

        self.tabs.addTab(det_tab, "Detection")

        # 3. Alerts Tab
        alert_tab = QWidget()
        alert_layout = QVBoxLayout(alert_tab)

        self.enable_notif_cb = QCheckBox("Enable Windows Notifications")
        self.enable_notif_cb.setChecked(self.settings.get("enable_notifications", True))
        alert_layout.addWidget(self.enable_notif_cb)

        self.enable_beep_cb = QCheckBox("Enable Audible Alert (Beep)")
        self.enable_beep_cb.setChecked(self.settings.get("enable_beep", True))
        alert_layout.addWidget(self.enable_beep_cb)

        alert_layout.addStretch()
        self.tabs.addTab(alert_tab, "Alerts")

        # 4. Privacy Tab
        priv_tab = QWidget()
        priv_layout = QVBoxLayout(priv_tab)
        priv_text = QLabel(
            "<b>Your Privacy Matters</b><br><br>"
            "AntiRickRoll processes all audio locally on your machine. "
            "No audio data, fingerprints, or listening history are ever "
            "uploaded to the cloud or shared with third parties.<br><br>"
            "The application does NOT use your microphone; it only monitors "
            "the system's playback audio."
        )
        priv_text.setWordWrap(True)
        priv_layout.addWidget(priv_text)
        priv_layout.addStretch()
        self.tabs.addTab(priv_tab, "Privacy")

        # Buttons
        btn_layout = QHBoxLayout()
        self.save_btn = QPushButton("Apply Changes")
        self.save_btn.setStyleSheet("background-color: #0078d4; font-weight: bold; padding: 10px;")
        self.save_btn.clicked.connect(self._save_settings)
        btn_layout.addWidget(self.save_btn)

        self.reset_btn = QPushButton("Reset Defaults")
        self.reset_btn.clicked.connect(self._reset_defaults)
        btn_layout.addWidget(self.reset_btn)

        layout.addLayout(btn_layout)

    def _save_settings(self):
        self.settings.set("sensitivity", self.sensitivity_slider.value() / 100.0)
        self.settings.set("enable_notifications", self.enable_notif_cb.isChecked())
        self.settings.set("enable_beep", self.enable_beep_cb.isChecked())
        self.settings.set("minimize_to_tray", self.minimize_cb.isChecked())
        self.settings.set("auto_start", self.auto_start_cb.isChecked())

        det_cfg = self.settings.get("detection", {})
        det_cfg["min_confidence"] = self.confidence_slider.value() / 100.0
        self.settings.set("detection", det_cfg)

        self.settings.save()

    def _reset_defaults(self):
        self.confidence_slider.setValue(60)
        self.sensitivity_slider.setValue(80)
        self.enable_notif_cb.setChecked(True)
        self.enable_beep_cb.setChecked(True)
        self.minimize_cb.setChecked(True)
        self.auto_start_cb.setChecked(False)
