"""Unit tests for the NotificationManager."""

import pytest
from unittest.mock import MagicMock
from antirickroll.core.notifications import NotificationManager

class MockTray:
    def __init__(self):
        self.showMessage = MagicMock()

def test_notification_enabled():
    tray = MockTray()
    settings = {"enable_notifications": True}
    manager = NotificationManager(tray, settings)

    manager.notify("Title", "Message")
    tray.showMessage.assert_called_once()

def test_notification_disabled():
    tray = MockTray()
    settings = {"enable_notifications": False}
    manager = NotificationManager(tray, settings)

    manager.notify("Title", "Message")
    tray.showMessage.assert_not_called()
