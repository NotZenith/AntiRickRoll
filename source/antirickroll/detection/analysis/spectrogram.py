"""Spectrogram generation for audio fingerprinting."""

import numpy as np
from scipy import signal
from typing import Optional, Tuple

class SpectrogramGenerator:
    """
    Generates spectrograms from raw audio data using Short-Time Fourier Transform (STFT).
    """

    def __init__(
        self,
        n_fft: int = 2048,
        hop_length: int = 512,
        window: str = "hann",
        sample_rate: int = 44100
    ):
        self.n_fft = n_fft
        self.hop_length = hop_length
        self.window = window
        self.sample_rate = sample_rate

    def generate(self, data: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Generates a spectrogram.
        :param data: 1D numpy array of audio samples.
        :return: (frequencies, times, spectrogram)
        """
        # Ensure data is 1D (mono)
        if len(data.shape) > 1:
            data = np.mean(data, axis=1)

        f, t, Sxx = signal.spectrogram(
            data,
            fs=self.sample_rate,
            window=self.window,
            nperseg=self.n_fft,
            noverlap=self.n_fft - self.hop_length,
            scaling='spectrum'
        )

        # Convert to decibels (log scale) for better peak detection
        # Add a small epsilon to avoid log(0)
        Sxx_log = 10 * np.log10(Sxx + 1e-10)

        return f, t, Sxx_log

    def get_fft_bins(self) -> np.ndarray:
        """Returns the frequency bin centers."""
        return np.fft.rfftfreq(self.n_fft, 1.0 / self.sample_rate)
