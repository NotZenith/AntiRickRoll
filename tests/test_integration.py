"""Integration tests for the full detection pipeline."""

import time
import numpy as np
import pytest
from unittest.mock import MagicMock
from antirickroll.detection.service import DetectionService
from antirickroll.detection.models import DetectionResult, FingerprintPackage, FingerprintMetadata
from antirickroll.detection.database.manager import FingerprintDatabase
from antirickroll.detection.matching.engine import MatchingEngine

class MockSettings:
    def get(self, key, default=None):
        if key == "detection":
            return {"min_confidence": 0.5}
        return default

def test_detection_service_stability():
    settings = MockSettings()
    service = DetectionService(settings)
    service.confirmation_threshold = 2

    # Mock confirmation signal
    mock_callback = MagicMock()
    service.detection_confirmed.connect(mock_callback)

    result = DetectionResult(
        success=True,
        fingerprint_id="song-1",
        name="Test Song",
        confidence=0.8
    )

    # First match - should not confirm yet
    service.handle_raw_result(result)
    mock_callback.assert_not_called()
    assert service.consecutive_matches == 1

    # Second match - should confirm
    service.handle_raw_result(result)
    mock_callback.assert_called_once()
    assert service.consecutive_matches == 2

def test_detection_service_cooldown():
    settings = MockSettings()
    service = DetectionService(settings)
    service.confirmation_threshold = 1
    service.cooldown_period = 1.0 # 1 second

    mock_callback = MagicMock()
    service.detection_confirmed.connect(mock_callback)

    result = DetectionResult(
        success=True,
        fingerprint_id="song-1",
        name="Test Song",
        confidence=0.8
    )

    # First alert
    service.handle_raw_result(result)
    assert mock_callback.call_count == 1

    # Immediate second match - should be in cooldown
    service.handle_raw_result(result)
    assert mock_callback.call_count == 1

    # Wait for cooldown
    time.sleep(1.1)
    service.handle_raw_result(result)
    assert mock_callback.call_count == 2
