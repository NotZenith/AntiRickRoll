"""Custom exceptions for AntiRickRoll."""

class AntiRickRollError(Exception):
    """Base exception for all AntiRickRoll errors."""
    pass

class SettingsError(AntiRickRollError):
    """Raised when there is an error with application settings."""
    pass

class AudioError(AntiRickRollError):
    """Raised when there is an error in the audio engine."""
    pass

class DetectionError(AntiRickRollError):
    """Raised when there is an error in the detection engine."""
    pass
