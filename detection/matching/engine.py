"""Matching engine for identifying audio against the database."""

import time
import logging
from collections import Counter
from typing import List, Tuple, Dict, Optional
from detection.database.manager import FingerprintDatabase
from detection.models import DetectionResult

class MatchingEngine:
    """
    Matches live audio hashes against the fingerprint database
    using a time-offset histogram.
    """

    def __init__(self, database: FingerprintDatabase, min_confidence: float = 0.5):
        self.logger = logging.getLogger(__name__)
        self.db = database
        self.min_confidence = min_confidence

    def match(self, samples_hashes: List[Tuple[str, int]]) -> DetectionResult:
        """
        Attempts to find a match for the given hashes.
        :param samples_hashes: List of (hash_str, absolute_time_idx).
        :return: DetectionResult.
        """
        start_time = time.time()

        # Track matches per package: package_id -> list of (offset_diff)
        # offset_diff = time_in_song - time_in_sample
        matches: Dict[str, List[int]] = {}

        for hash_str, sample_time in samples_hashes:
            results = self.db.lookup_hash(hash_str)
            for package_id, song_time in results:
                if package_id not in matches:
                    matches[package_id] = []
                matches[package_id].append(song_time - sample_time)

        # Analyze matches to find the most consistent offset per song
        best_match: Optional[Tuple[str, int, int]] = None  # (package_id, offset_diff, count)

        for package_id, diffs in matches.items():
            if not diffs:
                continue

            # Use a counter to find the mode (the most common time offset)
            counts = Counter(diffs)
            offset_diff, count = counts.most_common(1)[0]

            if not best_match or count > best_match[2]:
                best_match = (package_id, offset_diff, count)

        processing_time = time.time() - start_time

        if not best_match:
            return DetectionResult(success=False, processing_time=processing_time)

        package_id, best_offset, match_count = best_match
        package = self.db.get_package(package_id)

        # Calculate confidence
        # Simple heuristic: matches / average hashes in window
        # For production, we'd use a more complex model
        confidence = self._calculate_confidence(match_count, len(samples_hashes))

        if confidence < self.min_confidence:
            return DetectionResult(success=False, processing_time=processing_time)

        return DetectionResult(
            success=True,
            fingerprint_id=package_id,
            name=package.metadata.name,
            artist=package.metadata.artist,
            confidence=confidence,
            offset=float(best_offset),
            match_count=match_count,
            processing_time=processing_time
        )

    def _calculate_confidence(self, match_count: int, total_sample_hashes: int) -> float:
        """Calculates a confidence score between 0 and 1."""
        if total_sample_hashes == 0:
            return 0.0

        # This is a basic model. A real one would consider entropy, SNR, etc.
        # Here we cap it at 1.0
        score = (match_count * 5.0) / total_sample_hashes
        return min(1.0, score)
