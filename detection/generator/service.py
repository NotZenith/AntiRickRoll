"""Service for generating fingerprints from audio files."""

import logging
import uuid
import librosa
import numpy as np
from pathlib import Path
from typing import Optional

from detection.analysis.spectrogram import SpectrogramGenerator
from detection.generator.peaks import PeakDetector
from detection.hashing.landmark import LandmarkHasher
from detection.models import FingerprintPackage, FingerprintMetadata

class FingerprintGenerator:
    """
    Orchestrates the creation of a fingerprint package from an audio file.
    """

    def __init__(
        self,
        sample_rate: int = 44100,
        n_fft: int = 2048,
        hop_length: int = 512
    ):
        self.logger = logging.getLogger(__name__)
        self.sample_rate = sample_rate

        self.spectrogram_gen = SpectrogramGenerator(
            n_fft=n_fft, hop_length=hop_length, sample_rate=sample_rate
        )
        self.peak_detector = PeakDetector()
        self.hasher = LandmarkHasher()

    def generate_from_file(
        self,
        file_path: Path,
        name: str,
        artist: str = "Unknown",
        description: str = ""
    ) -> Optional[FingerprintPackage]:
        """
        Loads an audio file and generates a fingerprint package.
        """
        try:
            self.logger.info(f"Loading audio file: {file_path}")
            # Load audio, convert to mono and resample
            y, sr = librosa.load(str(file_path), sr=self.sample_rate, mono=True)

            duration = librosa.get_duration(y=y, sr=sr)

            self.logger.info("Generating spectrogram...")
            f, t, Sxx = self.spectrogram_gen.generate(y)

            self.logger.info("Finding peaks...")
            peaks = self.peak_detector.find_peaks(Sxx)

            self.logger.info(f"Generating hashes for {len(peaks)} peaks...")
            hashes_with_offsets = self.hasher.generate_hashes(peaks)

            # Group offsets by hash
            hash_dict = {}
            for h, offset in hashes_with_offsets:
                if h not in hash_dict:
                    hash_dict[h] = []
                hash_dict[h].append(offset)

            metadata = FingerprintMetadata(
                id=str(uuid.uuid4()),
                name=name,
                artist=artist,
                duration=duration,
                description=description,
                version="1.0.0"
            )

            return FingerprintPackage(metadata=metadata, hashes=hash_dict)

        except Exception as e:
            self.logger.error(f"Failed to generate fingerprint: {e}")
            return None
