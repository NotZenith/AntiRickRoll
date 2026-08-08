"""Detection engine interfaces for AntiRickRoll."""

from abc import ABC, abstractmethod
from typing import Any
from antirickroll.detection.models import DetectionResult

class FingerprintGenerator(ABC):
    """Abstract base class for generating audio fingerprints."""
    @abstractmethod
    def generate(self, data: bytes) -> Any:
        pass

class Matcher(ABC):
    """Abstract base class for matching fingerprints against a database."""
    @abstractmethod
    def match(self, fingerprint: Any) -> DetectionResult:
        pass

class Detector(ABC):
    """Main interface for the detection engine."""
    @abstractmethod
    def start_detection(self) -> None:
        pass

    @abstractmethod
    def stop_detection(self) -> None:
        pass
