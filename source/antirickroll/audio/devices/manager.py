"""Audio device management for Windows WASAPI Loopback."""

import logging
import sounddevice as sd
from typing import List, Optional, Dict

class AudioDeviceManager:
    """Manages audio devices and identifies WASAPI loopback sources."""

    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)
        self._wasapi_host_index = self._find_wasapi_host()

    def _find_wasapi_host(self) -> int:
        """Finds the index of the WASAPI host API."""
        hosts = sd.query_hostapis()
        for i, host in enumerate(hosts):
            if "WASAPI" in host["name"]:
                return i
        return -1

    def list_playback_devices(self) -> List[Dict]:
        """Lists all available playback devices using WASAPI."""
        devices = sd.query_devices()
        playback_devices = []
        for i, dev in enumerate(devices):
            # We look for devices with output channels and using WASAPI
            if dev["max_output_channels"] > 0 and dev["hostapi"] == self._wasapi_host_index:
                playback_devices.append({
                    "index": i,
                    "name": dev["name"],
                    "channels": dev["max_output_channels"],
                    "default_sr": dev["default_samplerate"]
                })
        return playback_devices

    def get_default_loopback_device(self) -> Optional[Dict]:
        """
        Attempts to find the loopback device for the default playback output.
        On Windows WASAPI, loopback devices are often input devices with 'loopback' in their name
        or linked to an output device.
        """
        try:
            default_output = sd.default.device[1]
            devices = sd.query_devices()

            # Find the output device name
            output_name = devices[default_output]["name"]

            # Look for an input device that is a loopback for this output
            for i, dev in enumerate(devices):
                if dev["hostapi"] == self._wasapi_host_index and dev["max_input_channels"] > 0:
                    if output_name in dev["name"] and "loopback" in dev["name"].lower():
                        return {
                            "index": i,
                            "name": dev["name"],
                            "channels": dev["max_input_channels"],
                            "default_sr": dev["default_samplerate"]
                        }

            # Fallback: find any WASAPI loopback device
            for i, dev in enumerate(devices):
                 if dev["hostapi"] == self._wasapi_host_index and dev["max_input_channels"] > 0:
                     if "loopback" in dev["name"].lower():
                         return {
                            "index": i,
                            "name": dev["name"],
                            "channels": dev["max_input_channels"],
                            "default_sr": dev["default_samplerate"]
                        }

        except Exception as e:
            self.logger.error(f"Error finding default loopback device: {e}")

        return None

    def get_device_info(self, index: int) -> Dict:
        """Returns detailed information about a device."""
        return sd.query_devices(index)

    def refresh(self) -> None:
        """Refreshes the internal device list."""
        # sounddevice queries are live, but we might want to re-find host if needed
        self._wasapi_host_index = self._find_wasapi_host()
