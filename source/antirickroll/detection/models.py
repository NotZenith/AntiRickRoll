"""Data models for the detection engine."""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
import time

@dataclass
class FingerprintMetadata:
    """Metadata for a fingerprint package."""
    id: str
    name: str
    artist: str = "Unknown"
    version: str = "1.0.0"
    duration: float = 0.0
    created_at: float = field(default_factory=time.time)
    description: str = ""
    tags: List[str] = field(default_factory=list)

@dataclass
class FingerprintPackage:
    """A complete fingerprint package including hashes and metadata."""
    metadata: FingerprintMetadata
    hashes: Dict[str, List[int]]  # Map hash_str -> list of time offsets

@dataclass
class DetectionResult:
    """The result of a detection attempt.
    Contains information about matched fingerprints and confidence scores.
    """
    success: bool
    fingerprint_id: Optional[str] = None
    name: Optional[str] = None
    artist: Optional[str] = None
    confidence: float = 0.0  # 0.0 to 1.0
    offset: float = 0.0      # Offset in the matched song (seconds)
    match_count: int = 0
    processing_time: float = 0.0
    timestamp: float = field(default_factory=time.time)
