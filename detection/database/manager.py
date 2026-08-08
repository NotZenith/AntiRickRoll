"""Management of fingerprint databases and storage."""

import json
import logging
import os
from pathlib import Path
from typing import Dict, List, Optional
from detection.models import FingerprintPackage, FingerprintMetadata

class FingerprintDatabase:
    """
    Handles loading, saving, and querying fingerprint packages.
    Supports a plugin-like architecture where packages are stored in files.
    """

    def __init__(self, storage_path: Path):
        self.logger = logging.getLogger(__name__)
        self.storage_path = storage_path
        self.packages: Dict[str, FingerprintPackage] = {}

        # Inverted index for fast lookup: hash -> list of (package_id, offset)
        self.hash_index: Dict[str, List[tuple]] = {}

    def load_all(self) -> None:
        """Loads all fingerprint packages from the storage directory."""
        if not self.storage_path.exists():
            self.storage_path.mkdir(parents=True, exist_ok=True)
            return

        for file_path in self.storage_path.glob("*.json"):
            try:
                self.load_package(file_path)
            except Exception as e:
                self.logger.error(f"Failed to load package {file_path}: {e}")

    def load_package(self, path: Path) -> None:
        """Loads a single fingerprint package from a JSON file."""
        with open(path, "r") as f:
            data = json.load(f)

        metadata = FingerprintMetadata(**data["metadata"])
        package = FingerprintPackage(metadata=metadata, hashes=data["hashes"])

        self.packages[metadata.id] = package
        self._index_package(package)
        self.logger.info(f"Loaded fingerprint: {metadata.name} by {metadata.artist}")

    def save_package(self, package: FingerprintPackage, filename: Optional[str] = None) -> Path:
        """Saves a fingerprint package to a JSON file."""
        if not filename:
            filename = f"{package.metadata.id}.json"

        path = self.storage_path / filename
        data = {
            "metadata": package.metadata.__dict__,
            "hashes": package.hashes
        }

        with open(path, "w") as f:
            json.dump(data, f, indent=4)

        return path

    def _index_package(self, package: FingerprintPackage) -> None:
        """Adds a package's hashes to the inverted index."""
        pid = package.metadata.id
        for h, offsets in package.hashes.items():
            if h not in self.hash_index:
                self.hash_index[h] = []
            for offset in offsets:
                self.hash_index[h].append((pid, offset))

    def lookup_hash(self, hash_str: str) -> List[tuple]:
        """Returns list of (package_id, offset) for a given hash."""
        return self.hash_index.get(hash_str, [])

    def get_package(self, package_id: str) -> Optional[FingerprintPackage]:
        """Retrieves a package by its ID."""
        return self.packages.get(package_id)
