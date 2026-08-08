"""Application and engine state definitions."""

from enum import Enum, auto

class AppState(Enum):
    """States for the main application lifecycle."""
    INITIALIZING = auto()
    IDLE = auto()
    MONITORING = auto()
    MATCHING = auto()
    DETECTED = auto()
    ERROR = auto()
    RECOVERY = auto()

class AudioState(Enum):
    """States for the audio capture engine."""
    STOPPED = auto()
    STARTING = auto()
    CAPTURING = auto()
    PAUSED = auto()
    ERROR = auto()
