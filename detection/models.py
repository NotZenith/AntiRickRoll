"""Data models for detection results."""

from dataclasses import dataclass
from datetime import datetime

@dataclass
class DetectionResult:
    """Represents a single detection event."""
    match_found: bool
    confidence: float
    timestamp: datetime
    track_name: str = "Unknown"
    source_plugin: str = "Internal"
