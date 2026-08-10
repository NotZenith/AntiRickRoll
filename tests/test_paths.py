"""Unit tests for path resolution utilities."""

import os
from pathlib import Path
from antirickroll.core.paths import get_user_data_dir, get_plugins_dir

def test_get_user_data_dir():
    path = get_user_data_dir()
    assert isinstance(path, Path)
    assert path.name == ".antirickroll"
    assert path.exists()

def test_get_plugins_dir():
    path = get_plugins_dir()
    assert isinstance(path, Path)
    assert "plugins" in str(path)
    assert "fingerprints" in str(path)
    assert path.exists()
