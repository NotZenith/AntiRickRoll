"""Detection service for stability filtering and alerting."""

import logging
import time
from typing import Optional
from PySide6.QtCore import QObject, Signal
from antirickroll.detection.models import DetectionResult
from antirickroll.core.states import AppState

class DetectionService(QObject):
    """
    Manages the detection lifecycle, applying stability filters to raw results.
    Prevents false positives and rapid repeated alerts.
    """

    # Emitted only when a detection is confirmed after filtering
    detection_confirmed = Signal(DetectionResult)
    # Emitted for every processing cycle to update UI confidence
    confidence_updated = Signal(float, str)  # confidence, name
    status_updated = Signal(str)
    state_changed = Signal(AppState)

    def __init__(self, settings) -> None:
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.settings = settings

        # State
        self.current_match_id: Optional[str] = None
        self.consecutive_matches = 0
        self.last_alert_time = 0.0
        self.is_muted = False
        self.state = AppState.INITIALIZING

        # Filtering parameters from settings
        det_cfg = settings.get("detection", {})
        self.min_confidence = det_cfg.get("min_confidence", 0.6)
        self.confirmation_threshold = 3  # consecutive matches needed
        self.cooldown_period = 30.0      # seconds between alerts for same song

        self._set_state(AppState.IDLE)

    def _set_state(self, state: AppState):
        if self.state != state:
            self.state = state
            self.state_changed.emit(state)

    def handle_raw_result(self, result: DetectionResult):
        """Processes a raw result from the detection worker."""
        if not result.success:
            self._handle_no_match()
            return

        # Smoothed confidence for UI
        self.confidence_updated.emit(result.confidence, result.name)
        self._set_state(AppState.MATCHING)

        if result.fingerprint_id == self.current_match_id:
            self.consecutive_matches += 1
        else:
            self.current_match_id = result.fingerprint_id
            self.consecutive_matches = 1

        self.logger.debug(f"Potential match: {result.name} (Conf: {result.confidence}, Count: {self.consecutive_matches})")

        # Check if confirmed
        if (self.consecutive_matches >= self.confirmation_threshold and
            result.confidence >= self.min_confidence):
            self._confirm_detection(result)

    def _handle_no_match(self):
        """Reset counters if no match is found."""
        self.consecutive_matches = 0
        self.current_match_id = None
        self.confidence_updated.emit(0.0, "None")
        self.status_updated.emit("Monitoring...")
        self._set_state(AppState.MONITORING)

    def _confirm_detection(self, result: DetectionResult):
        """Triggers the confirmation if not in cooldown."""
        now = time.time()
        self._set_state(AppState.DETECTED)

        # Check cooldown
        if now - self.last_alert_time < self.cooldown_period:
            self.status_updated.emit("Detection Confirmed (Cooldown)")
            return

        self.logger.info(f"DETECTION CONFIRMED: {result.name}")
        self.last_alert_time = now
        self.status_updated.emit(f"RICKROLL DETECTED: {result.name}")

        if not self.is_muted:
            self.detection_confirmed.emit(result)

    def toggle_mute(self):
        """Toggles the alert mute state."""
        self.is_muted = not self.is_muted
        self.logger.info(f"Alerts {'muted' if self.is_muted else 'unmuted'}")
        return self.is_muted
