"""Unit tests for the audio detection engine."""

import numpy as np
import pytest
from pathlib import Path
from detection.analysis.spectrogram import SpectrogramGenerator
from detection.generator.peaks import PeakDetector
from detection.hashing.landmark import LandmarkHasher
from detection.database.manager import FingerprintDatabase
from detection.matching.engine import MatchingEngine
from detection.models import FingerprintPackage, FingerprintMetadata

def test_spectrogram_gen():
    gen = SpectrogramGenerator(n_fft=1024, hop_length=256)
    data = np.random.rand(44100).astype(np.float32) # 1 second
    f, t, Sxx = gen.generate(data)
    assert Sxx.shape[0] > 0
    assert Sxx.shape[1] > 0

def test_peak_detector():
    # Create a dummy spectrogram with a few clear peaks
    spec = np.zeros((100, 100))
    spec[10, 10] = 10.0
    spec[50, 50] = 10.0

    detector = PeakDetector(neighborhood_size=5, min_amplitude=0.0)
    peaks = detector.find_peaks(spec)

    assert (10, 10) in peaks
    assert (50, 50) in peaks
    assert len(peaks) == 2

def test_landmark_hasher():
    peaks = [(10, 20), (15, 25), (30, 40)]
    hasher = LandmarkHasher(fan_value=3, max_time_delta=100)
    hashes = hasher.generate_hashes(peaks)

    assert len(hashes) > 0
    # Each hash should be a tuple (hash_str, offset)
    assert isinstance(hashes[0][0], str)
    assert isinstance(hashes[0][1], int)

def test_matching_engine(tmp_path):
    # Setup database
    db = FingerprintDatabase(tmp_path)

    # Create a dummy package
    metadata = FingerprintMetadata(id="test-1", name="Test Song", artist="Artist")
    hashes = {"hash1": [10, 50], "hash2": [100]}
    package = FingerprintPackage(metadata=metadata, hashes=hashes)
    db.packages["test-1"] = package
    db._index_package(package)

    engine = MatchingEngine(db, min_confidence=0.1)

    # Simulate sample hashes that match hash1 and hash2 with offset diff of 1000
    # song_time - sample_time = offset_diff
    # 10 - (-990) = 1000
    # 100 - (-900) = 1000
    sample_hashes = [("hash1", -990), ("hash2", -900)]

    result = engine.match(sample_hashes)

    assert result.success is True
    assert result.name == "Test Song"
    assert result.offset == 1000.0
