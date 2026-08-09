"""Background worker for continuous audio detection."""

import logging
import numpy as np
from PySide6.QtCore import QThread, Signal
from antirickroll.detection.analysis.spectrogram import SpectrogramGenerator
from antirickroll.detection.generator.peaks import PeakDetector
from antirickroll.detection.hashing.landmark import LandmarkHasher
from antirickroll.detection.matching.engine import MatchingEngine
from antirickroll.detection.models import DetectionResult

class DetectionWorker(QThread):
    """
    Worker thread that continuously analyzes audio from the buffer
    and attempts to match it against the fingerprint database.
    """

    result_ready = Signal(DetectionResult)
    status_changed = Signal(str)
    error_occurred = Signal(str)

    def __init__(self, audio_engine, matching_engine, settings) -> None:
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.audio_engine = audio_engine
        self.matcher = matching_engine
        self.settings = settings

        self.running = False

        # Detection components
        det_settings = settings.get("detection", {})
        self.spec_gen = SpectrogramGenerator(
            n_fft=det_settings.get("fft_size", 2048),
            hop_length=det_settings.get("hop_length", 512)
        )
        self.peak_detector = PeakDetector(
            max_peaks=det_settings.get("max_peaks", 500)
        )
        self.hasher = LandmarkHasher()

        # Sliding window configuration
        # 1024 * 16 is ~0.37s at 44.1kHz. We'll take a larger chunk for better fingerprinting.
        self.window_size = 44100 * 5  # 5 seconds of audio
        self.poll_interval = 0.5     # Run detection every 0.5s

    def run(self):
        """Main loop for the detection worker."""
        self.running = True
        self.logger.info("Detection worker started.")

        while self.running:
            if not self.audio_engine.is_running:
                self.msleep(500)
                continue

            try:
                self._perform_detection()
            except Exception as e:
                self.logger.exception("Error during live detection")
                self.error_occurred.emit(str(e))

            self.msleep(int(self.poll_interval * 1000))

        self.logger.info("Detection worker stopped.")

    def _perform_detection(self):
        """Pulls audio from buffer and runs the matching pipeline."""
        # Peek at the latest audio in the buffer
        buffer = self.audio_engine.worker.buffer
        data = buffer.peek(self.window_size)

        if data is None or len(data) < self.window_size // 2:
            return

        self.status_changed.emit("Processing...")

        # 1. Spectrogram
        f, t, Sxx = self.spec_gen.generate(data)

        # 2. Peaks
        peaks = self.peak_detector.find_peaks(Sxx)

        # 3. Hashing
        sample_hashes = self.hasher.generate_hashes(peaks)

        # 4. Matching
        if sample_hashes:
            result = self.matcher.match(sample_hashes)
            self.result_ready.emit(result)

            if result.success:
                self.status_changed.emit(f"Match Found: {result.name}")
            else:
                self.status_changed.emit("Listening...")
        else:
            self.status_changed.emit("Listening...")

    def stop(self):
        """Requests the worker to stop."""
        self.running = False
        self.wait()
