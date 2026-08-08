"""Spectral peak detection for audio fingerprinting."""

import numpy as np
from scipy import ndimage
from typing import List, Tuple

class PeakDetector:
    """
    Detects local maxima in a spectrogram to be used as landmarks.
    """

    def __init__(
        self,
        neighborhood_size: int = 20,
        min_amplitude: float = -50.0,
        max_peaks: int = 1000
    ):
        self.neighborhood_size = neighborhood_size
        self.min_amplitude = min_amplitude
        self.max_peaks = max_peaks

    def find_peaks(self, spectrogram: np.ndarray) -> List[Tuple[int, int]]:
        """
        Finds local maxima in the spectrogram.
        :param spectrogram: 2D numpy array (log-magnitude).
        :return: List of (time_idx, freq_idx) tuples.
        """
        # Define a structural element for local maxima filtering
        # This will compare each pixel with its neighbors
        neighborhood = np.ones((self.neighborhood_size, self.neighborhood_size))

        # local_max will be True where the value is the maximum in its neighborhood
        local_max = (ndimage.maximum_filter(spectrogram, footprint=neighborhood) == spectrogram)

        # Also filter by minimum amplitude to ignore noise
        background = (spectrogram > self.min_amplitude)

        # Combine local max and amplitude threshold
        peaks = local_max & background

        # Extract indices
        time_idxs, freq_idxs = np.where(peaks)

        # Sort by amplitude (descending) and limit if necessary
        amplitudes = spectrogram[time_idxs, freq_idxs]
        sorted_indices = np.argsort(amplitudes)[::-1]

        peak_list = []
        for idx in sorted_indices[:self.max_peaks]:
            peak_list.append((int(time_idxs[idx]), int(freq_idxs[idx])))

        return peak_list
