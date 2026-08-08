"""Background worker for real-time audio capture."""

import logging
import numpy as np
import sounddevice as sd
from PySide6.QtCore import QThread, Signal
from antirickroll.audio.buffer.circular import CircularBuffer
from antirickroll.audio.processing.pipeline import AudioPipeline
from antirickroll.audio.processing.stages import ChannelConverter, Resampler
from antirickroll.audio.devices.manager import AudioDeviceManager

class AudioCaptureWorker(QThread):
    """
    Worker thread that captures audio from WASAPI loopback,
    processes it, and stores it in a circular buffer.
    """

    # Signals for UI integration
    waveform_data = Signal(np.ndarray)  # Raw data for visualization
    metrics_updated = Signal(dict)      # Real-time metrics
    status_changed = Signal(str, bool)  # Status message and is_active flag
    error_occurred = Signal(str)        # Error messages

    def __init__(self, settings_manager):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.settings = settings_manager
        self.device_manager = AudioDeviceManager()

        self.running = False
        self.paused = False

        # Audio configuration (defaults)
        self.sample_rate = 44100
        self.channels = 1
        self.frame_size = 1024

        # Components
        self.buffer = CircularBuffer(capacity=44100 * 10, channels=self.channels)
        self.pipeline = AudioPipeline()

        self._stream = None

    def run(self):
        """Main loop for the capture worker."""
        self.running = True
        self.logger.info("Audio capture worker started.")

        try:
            self._start_capture()
        except Exception as e:
            self.logger.exception("Failed to start audio capture")
            self.error_occurred.emit(str(e))
            self.running = False
            return

        while self.running:
            if self.paused:
                self.msleep(100)
                continue

            # The actual capture is handled by the sounddevice callback
            # We use this loop to emit periodic metrics and health checks
            self.msleep(100)
            self._emit_metrics()
            self._check_device_change()

    def _check_device_change(self):
        """Polls for default device changes."""
        try:
            # Check if default output device changed
            current_default = sd.default.device[1]
            if hasattr(self, '_last_default_device') and current_default != self._last_default_device:
                self.logger.info("Default playback device changed, restarting stream...")
                self._stop_capture()
                self._start_capture()
            self._last_default_device = current_default
        except Exception as e:
            self.logger.error(f"Error checking device change: {e}")

        self._stop_capture()
        self.logger.info("Audio capture worker stopped.")

    def _start_capture(self):
        """Initializes and starts the WASAPI loopback stream."""
        device_info = self.device_manager.get_default_loopback_device()
        if not device_info:
            raise RuntimeError("No WASAPI Loopback device found. Ensure you are on Windows.")

        self.logger.info(f"Using device: {device_info['name']} (Index: {device_info['index']})")

        source_sr = int(device_info['default_sr'])
        source_channels = device_info['channels']

        # Setup pipeline
        self.pipeline.clear()
        self.pipeline.add_stage(ChannelConverter(target_channels=self.channels))
        if source_sr != self.sample_rate:
            self.pipeline.add_stage(Resampler(source_sr=source_sr, target_sr=self.sample_rate))

        self._stream = sd.InputStream(
            device=device_info['index'],
            channels=source_channels,
            samplerate=source_sr,
            callback=self._audio_callback,
            blocksize=self.frame_size
        )
        self._stream.start()
        self.status_changed.emit(f"Capturing: {device_info['name']}", True)

    def _stop_capture(self):
        """Stops the audio stream."""
        if self._stream:
            self._stream.stop()
            self._stream.close()
            self._stream = None
        self.status_changed.emit("Stopped", False)

    def _audio_callback(self, indata, frames, time, status):
        """Callback function for sounddevice to process incoming audio."""
        if status:
            self.logger.warning(f"Audio stream status: {status}")

        if self.paused:
            return

        try:
            # Process through pipeline
            processed_data = self.pipeline.process(indata)

            # Write to circular buffer
            self.buffer.write(processed_data)

            # Emit data for visualization (downsampled if necessary for performance)
            self.waveform_data.emit(processed_data)

        except Exception as e:
            self.logger.error(f"Error in audio callback: {e}")

    def _emit_metrics(self):
        """Gathers and emits performance metrics."""
        metrics = self.buffer.get_metrics()
        metrics.update({
            "sample_rate": self.sample_rate,
            "channels": self.channels,
            "running": self.running,
            "cpu_usage": 0.0, # Placeholder
            "latency": self._stream.latency if self._stream else 0.0
        })
        self.metrics_updated.emit(metrics)

    def stop(self):
        """Requests the worker to stop."""
        self.running = False
        self.wait()
