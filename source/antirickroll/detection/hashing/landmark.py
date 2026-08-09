"""Landmark-based hashing for audio fingerprints."""

import hashlib
from typing import List, Tuple, Dict

class LandmarkHasher:
    """
    Generates robust hashes from spectral peaks by connecting them into 'fan-out' pairs.
    """

    def __init__(
        self,
        fan_value: int = 15,
        min_time_delta: int = 0,
        max_time_delta: int = 200
    ) -> None:
        self.fan_value = fan_value
        self.min_time_delta = min_time_delta
        self.max_time_delta = max_time_delta

    def generate_hashes(self, peaks: List[Tuple[int, int]]) -> List[Tuple[str, int]]:
        """
        Generates hashes from a list of (time, freq) peaks.
        :param peaks: List of (time_idx, freq_idx). Must be sorted by time.
        :return: List of (hash_str, offset_time).
        """
        # Sort peaks by time index to ensure correct pairing
        sorted_peaks = sorted(peaks, key=lambda x: x[0])

        hashes = []
        n_peaks = len(sorted_peaks)

        for i in range(n_peaks):
            for j in range(1, self.fan_value):
                if (i + j) < n_peaks:
                    f1 = sorted_peaks[i][1]
                    f2 = sorted_peaks[i+j][1]
                    t1 = sorted_peaks[i][0]
                    t2 = sorted_peaks[i+j][0]
                    t_delta = t2 - t1

                    if self.min_time_delta <= t_delta <= self.max_time_delta:
                        # Create a unique hash representing this peak pair
                        # We use frequency components and the time difference
                        h = hashlib.sha1(
                            f"{f1}|{f2}|{t_delta}".encode('utf-8')
                        ).hexdigest()[:20]

                        hashes.append((h, t1))

        return hashes
