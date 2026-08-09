"""Thread-safe circular buffer for audio data."""

import threading
import numpy as np
from typing import Optional

class CircularBuffer:
    """
    A thread-safe circular buffer implementation optimized for audio data.
    Uses numpy for efficient data handling.
    """

    def __init__(self, capacity: int, channels: int = 2, dtype: np.dtype = np.float32) -> None:
        self.capacity = capacity
        self.channels = channels
        self.dtype = dtype
        self.buffer = np.zeros((capacity, channels), dtype=dtype)
        self.write_index = 0
        self.read_index = 0
        self.size = 0
        self._lock = threading.Lock()

        # Metrics
        self.overflow_count = 0
        self.underflow_count = 0
        self.dropped_frames = 0

    def write(self, data: np.ndarray) -> int:
        """
        Writes data to the buffer.
        :param data: numpy array of shape (n_frames, channels)
        :return: number of frames written
        """
        n_frames = data.shape[0]
        with self._lock:
            if n_frames > self.capacity - self.size:
                # Overflow detected
                self.overflow_count += 1
                frames_to_write = self.capacity - self.size
                self.dropped_frames += (n_frames - frames_to_write)
            else:
                frames_to_write = n_frames

            if frames_to_write == 0:
                return 0

            # Linear part until the end of the buffer
            end_frames = min(frames_to_write, self.capacity - self.write_index)
            self.buffer[self.write_index : self.write_index + end_frames] = data[:end_frames]

            # Wrap around part
            if end_frames < frames_to_write:
                wrap_frames = frames_to_write - end_frames
                self.buffer[0:wrap_frames] = data[end_frames:frames_to_write]
                self.write_index = wrap_frames
            else:
                self.write_index = (self.write_index + end_frames) % self.capacity

            self.size += frames_to_write
            return frames_to_write

    def read(self, n_frames: int) -> Optional[np.ndarray]:
        """
        Reads n_frames from the buffer.
        :param n_frames: number of frames to read
        :return: numpy array of shape (n_frames, channels) or None if not enough data
        """
        with self._lock:
            if n_frames > self.size:
                self.underflow_count += 1
                return None

            data = np.empty((n_frames, self.channels), dtype=self.dtype)

            # Linear part until the end of the buffer
            end_frames = min(n_frames, self.capacity - self.read_index)
            data[:end_frames] = self.buffer[self.read_index : self.read_index + end_frames]

            # Wrap around part
            if end_frames < n_frames:
                wrap_frames = n_frames - end_frames
                data[end_frames:] = self.buffer[0:wrap_frames]
                self.read_index = wrap_frames
            else:
                self.read_index = (self.read_index + n_frames) % self.capacity

            self.size -= n_frames
            return data

    def peek(self, n_frames: int) -> Optional[np.ndarray]:
        """
        Peeks at the latest n_frames in the buffer without removing them.
        Returns the data in a linear array.
        """
        with self._lock:
            if n_frames > self.size:
                return None

            # We want the MOST RECENT n_frames
            start_idx = (self.write_index - n_frames) % self.capacity

            data = np.empty((n_frames, self.channels), dtype=self.dtype)
            end_frames = min(n_frames, self.capacity - start_idx)
            data[:end_frames] = self.buffer[start_idx : start_idx + end_frames]

            if end_frames < n_frames:
                wrap_frames = n_frames - end_frames
                data[end_frames:] = self.buffer[0:wrap_frames]

            return data

    def clear(self) -> None:
        """Clears the buffer."""
        with self._lock:
            self.write_index = 0
            self.read_index = 0
            self.size = 0

    def get_metrics(self) -> dict:
        """Returns buffer metrics."""
        with self._lock:
            return {
                "size": self.size,
                "capacity": self.capacity,
                "usage_pct": (self.size / self.capacity) * 100 if self.capacity > 0 else 0,
                "overflow_count": self.overflow_count,
                "underflow_count": self.underflow_count,
                "dropped_frames": self.dropped_frames
            }
