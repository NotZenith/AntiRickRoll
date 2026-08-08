# AntiRickRoll

A production-quality Windows application to detect and prevent RickRolls using audio fingerprinting and real-time monitoring.

## Architecture

This project follows **Clean Architecture** and **SOLID** principles.

- **app/**: Application entry point and lifecycle management.
- **core/**: Central business logic, settings, logging, and error handling.
- **audio/**: Industrial-grade Windows loopback capture and processing.
  - **capture/**: WASAPI loopback implementation.
  - **processing/**: Modular pipeline (Normalization, Resampling, Channel conversion).
  - **buffer/**: Thread-safe circular buffer with overflow detection.
  - **devices/**: Windows device manager with auto-reconnect.
  - **visualization/**: Real-time waveform and peak meters.
- **core/**: Central business logic, settings, logging, and error handling.
- **ui/**: PySide6 modern dark theme user interface with real-time feedback.
- **detection/**: Core logic for fingerprinting (Interfaces only).
- **plugins/**: Extensible plugin system.
- **assets/**: Static resources like icons and stylesheets.
- **config/**: Default configuration files.

## Fingerprinting Engine

AntiRickRoll uses a deterministic spectral peak landmark hashing system (similar to Shazam) to recognize audio.

### How it works:
1.  **Spectrogram:** Audio is converted to the frequency domain using STFT.
2.  **Peaks:** Local maxima are identified in the spectrogram.
3.  **Hashing:** Peaks are paired into landmarks and hashed to create a robust fingerprint.
4.  **Matching:** Live hashes are compared against the database using time-offset histograms.

### Fingerprint Generator CLI
You can generate your own fingerprint packages for the application:

```bash
python -m detection.cli generate path/to/audio.wav --name "Never Gonna Give You Up" --artist "Rick Astley"
```

The generated `.json` package will be saved in `plugins/fingerprints/` and automatically loaded by the application.

## Real-Time Detection

AntiRickRoll continuously monitors Windows playback audio in the background.

### Live Pipeline:
1.  **Capture:** Audio is captured using WASAPI Loopback.
2.  **Streaming Analysis:** A sliding window analysis is performed on the live buffer.
3.  **Stability Filter:** Detections are confirmed only after multiple consistent matches, reducing false positives.
4.  **Alerts:** Native Windows notifications and audio beeps trigger upon confirmation.

### Features
- **Background Monitoring:** Continues working in the system tray.
- **Stability Hysteresis:** Confirms matches across multiple spectral windows.
- **Customizable Thresholds:** Adjust sensitivity and confidence in Settings.
- **Developer Diagnostics:** View real-time spectrograms and hash matches (Ctrl+Shift+D).

- **Windows Loopback Capture**: Capture ANY system audio using WASAPI.
- **Real-time Visualization**: Smooth waveform and peak levels.
- **Live Metrics**: Sample rate, channels, latency, and buffer health.
- **Auto-Reconnect**: Automatically handles device changes.
- **Clean Architecture**: Decoupled, modular, and unit-tested.
- **System Tray Integration**: Minimize to tray for background monitoring.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the application:
   ```bash
   python -m app.main
   ```

## Roadmap

- [ ] Core Audio Capture Engine
- [ ] Fingerprint Database Plugin
- [ ] Real-time Alert System
- [ ] Advanced Settings UI

## License

MIT
