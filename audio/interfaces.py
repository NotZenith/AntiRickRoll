"""Audio engine interfaces for AntiRickRoll."""

from abc import ABC, abstractmethod
from typing import List

class AudioBuffer(ABC):
    """Abstract base class for audio data buffering."""
    @abstractmethod
    def add_samples(self, samples: bytes) -> None:
        pass

    @abstractmethod
    def get_data(self) -> bytes:
        pass

class AudioSource(ABC):
    """Abstract base class for audio input sources."""
    @abstractmethod
    def start_streaming(self) -> None:
        pass

    @abstractmethod
    def stop_streaming(self) -> None:
        pass

    @abstractmethod
    def get_available_devices(self) -> List[str]:
        pass

class AudioProcessor(ABC):
    """Abstract base class for processing raw audio data."""
    @abstractmethod
    def process(self, data: bytes) -> bytes:
        pass

class AudioEngine(ABC):
    """Main interface for controlling the audio subsystem."""
    @abstractmethod
    def initialize(self) -> None:
        pass

    @abstractmethod
    def shutdown(self) -> None:
        pass
