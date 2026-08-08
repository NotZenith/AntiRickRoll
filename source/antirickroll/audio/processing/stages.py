"""Audio processing stages for the pipeline."""

import numpy as np
from abc import ABC, abstractmethod
from scipy import signal
from typing import Optional

class ProcessingStage(ABC):
    """Abstract base class for a processing stage."""
    @abstractmethod
    def process(self, data: np.ndarray) -> np.ndarray:
        pass

class Normalizer(ProcessingStage):
    """Normalizes audio amplitude."""
    def __init__(self, target_peak: float = 0.9):
        self.target_peak = target_peak

    def process(self, data: np.ndarray) -> np.ndarray:
        peak = np.max(np.abs(data))
        if peak > 0:
            return data * (self.target_peak / peak)
        return data

class ChannelConverter(ProcessingStage):
    """Converts audio between channel counts."""
    def __init__(self, target_channels: int = 1):
        self.target_channels = target_channels

    def process(self, data: np.ndarray) -> np.ndarray:
        current_channels = data.shape[1] if len(data.shape) > 1 else 1

        if current_channels == self.target_channels:
            return data

        if self.target_channels == 1:
            # Multi-channel to Mono
            return np.mean(data, axis=1, keepdims=True)
        elif self.target_channels == 2 and current_channels == 1:
            # Mono to Stereo
            return np.column_stack((data, data))

        return data

class Resampler(ProcessingStage):
    """Resamples audio to a target sample rate."""
    def __init__(self, source_sr: int, target_sr: int):
        self.source_sr = source_sr
        self.target_sr = target_sr

    def process(self, data: np.ndarray) -> np.ndarray:
        if self.source_sr == self.target_sr:
            return data

        num_samples = int(len(data) * self.target_sr / self.source_sr)
        resampled_data = signal.resample(data, num_samples)
        return resampled_data

class Windowing(ProcessingStage):
    """Applies a window function (e.g., Hann) to the audio frames."""
    def __init__(self, window_type: str = "hann"):
        self.window_type = window_type
        self._window_cache: Optional[np.ndarray] = None
        self._last_size = 0

    def process(self, data: np.ndarray) -> np.ndarray:
        n = data.shape[0]
        if n != self._last_size:
            self._window_cache = signal.get_window(self.window_type, n).reshape(-1, 1)
            self._last_size = n

        return data * self._window_cache
