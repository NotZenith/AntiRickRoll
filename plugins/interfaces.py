"""Plugin system interfaces for AntiRickRoll."""

from abc import ABC, abstractmethod
from typing import Dict, Any

class PluginBase(ABC):
    """Base class for all AntiRickRoll plugins."""

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def version(self) -> str:
        pass

    @abstractmethod
    def initialize(self, context: Dict[str, Any]) -> None:
        """Initializes the plugin with application context."""
        pass

    @abstractmethod
    def shutdown(self) -> None:
        """Cleans up plugin resources."""
        pass

class DatabasePlugin(PluginBase):
    """Specialized plugin for providing RickRoll fingerprint databases."""
    @abstractmethod
    def get_fingerprints(self) -> Any:
        pass
