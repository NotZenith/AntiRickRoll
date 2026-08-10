"""Unit tests for the SettingsManager."""

import pytest
from pathlib import Path
from antirickroll.core.settings import SettingsManager

def test_settings_default(tmp_path):
    config_file = tmp_path / "settings.json"
    manager = SettingsManager(config_file)
    assert manager.get("theme") == "dark"
    assert manager.get("sensitivity") == 0.8

def test_settings_save_load(tmp_path):
    config_file = tmp_path / "settings.json"
    manager = SettingsManager(config_file)
    manager.set("sensitivity", 0.5)

    # Create new manager to load from file
    new_manager = SettingsManager(config_file)
    assert new_manager.get("sensitivity") == 0.5
