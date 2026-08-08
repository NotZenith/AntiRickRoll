"""Settings view for application configuration."""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QSlider, QCheckBox, QLabel, QGroupBox, QPushButton
)
from PySide6.QtCore import Qt

class SettingsView(QWidget):
    """View to modify application settings."""

    def __init__(self, settings_manager, parent=None):
        super().__init__(parent)
        self.settings = settings_manager
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        header = QLabel("Application Settings")
        header.setStyleSheet("font-size: 24px; font-weight: bold; color: white;")
        layout.addWidget(header)

        # Detection Settings
        det_group = QGroupBox("Detection Configuration")
        det_layout = QFormLayout(det_group)

        det_cfg = self.settings.get("detection", {})

        self.confidence_slider = QSlider(Qt.Horizontal)
        self.confidence_slider.setRange(10, 95)
        self.confidence_slider.setValue(int(det_cfg.get("min_confidence", 0.6) * 100))
        det_layout.addRow("Confidence Threshold (%):", self.confidence_slider)

        self.sensitivity_slider = QSlider(Qt.Horizontal)
        self.sensitivity_slider.setRange(1, 100)
        self.sensitivity_slider.setValue(int(self.settings.get("sensitivity", 0.8) * 100))
        det_layout.addRow("General Sensitivity:", self.sensitivity_slider)

        layout.addWidget(det_group)

        # Notification Settings
        notif_group = QGroupBox("Notifications & Alerts")
        notif_layout = QVBoxLayout(notif_group)

        self.enable_notif_cb = QCheckBox("Enable Windows Notifications")
        self.enable_notif_cb.setChecked(self.settings.get("enable_notifications", True))
        notif_layout.addWidget(self.enable_notif_cb)

        self.enable_beep_cb = QCheckBox("Enable Audio Alert (Beep)")
        self.enable_beep_cb.setChecked(self.settings.get("enable_beep", True))
        notif_layout.addWidget(self.enable_beep_cb)

        self.minimize_cb = QCheckBox("Minimize to System Tray")
        self.minimize_cb.setChecked(self.settings.get("minimize_to_tray", True))
        notif_layout.addWidget(self.minimize_cb)

        layout.addWidget(notif_group)

        # Action Buttons
        btn_layout = QHBoxLayout()
        self.save_btn = QPushButton("Save Settings")
        self.save_btn.setStyleSheet("background-color: #0078d4; font-weight: bold;")
        self.save_btn.clicked.connect(self._save_settings)
        btn_layout.addWidget(self.save_btn)

        self.reset_btn = QPushButton("Reset Defaults")
        self.reset_btn.clicked.connect(self._reset_defaults)
        btn_layout.addWidget(self.reset_btn)

        layout.addLayout(btn_layout)
        layout.addStretch()

    def _save_settings(self):
        self.settings.set("sensitivity", self.sensitivity_slider.value() / 100.0)
        self.settings.set("enable_notifications", self.enable_notif_cb.isChecked())
        self.settings.set("enable_beep", self.enable_beep_cb.isChecked())
        self.settings.set("minimize_to_tray", self.minimize_cb.isChecked())

        det_cfg = self.settings.get("detection", {})
        det_cfg["min_confidence"] = self.confidence_slider.value() / 100.0
        self.settings.set("detection", det_cfg)

        self.settings.save()

    def _reset_defaults(self):
        # In a real app, we'd pull from SettingsManager._get_defaults()
        self.confidence_slider.setValue(60)
        self.sensitivity_slider.setValue(80)
        self.enable_notif_cb.setChecked(True)
        self.enable_beep_cb.setChecked(True)
        self.minimize_cb.setChecked(True)
