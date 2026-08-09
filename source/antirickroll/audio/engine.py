"""Windows-specific implementation of the AudioEngine."""

import logging
from typing import Optional
from antirickroll.audio.interfaces import AudioEngine
from antirickroll.audio.workers.audio_worker import AudioCaptureWorker

class WindowsAudioEngine(AudioEngine):
    """
    Orchestrates the audio capture and processing subsystem on Windows.
    """

    def __init__(self, settings_manager) -> None:
        self.logger = logging.getLogger(__name__)
        self.settings = settings_manager
        self.worker: Optional[AudioCaptureWorker] = None

    def initialize(self) -> None:
        """Starts the audio engine."""
        self.logger.info("Initializing Windows Audio Engine...")
        if not self.worker:
            self.worker = AudioCaptureWorker(self.settings)
            self.worker.start()

    def shutdown(self) -> None:
        """Stops the audio engine."""
        self.logger.info("Shutting down Windows Audio Engine...")
        if self.worker:
            self.worker.stop()
            self.worker = None

    def pause(self) -> None:
        """Pauses audio capture."""
        if self.worker:
            self.worker.paused = True

    def resume(self) -> None:
        """Resumes audio capture."""
        if self.worker:
            self.worker.paused = False

    @property
    def is_running(self) -> bool:
        return self.worker.running if self.worker else False
