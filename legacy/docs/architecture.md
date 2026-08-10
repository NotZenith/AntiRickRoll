# Architecture Overview

AntiRickRoll is built using a modular, event-driven architecture designed for low-latency audio processing on Windows.

## Components

### 1. Audio Engine (`antirickroll.audio`)
- **Capture:** Uses WASAPI Loopback to intercept system audio.
- **Buffer:** A thread-safe circular buffer (`numpy`-backed) for streaming data.
- **Processing:** A pipeline for normalization, resampling, and channel conversion.

### 2. Detection Engine (`antirickroll.detection`)
- **Spectrogram:** Generates time-frequency representations of audio.
- **Peaks & Hashing:** Identifies spectral landmarks and generates combinatorial hashes.
- **Matching:** Performs time-offset histogram matching against the fingerprint database.
- **Service:** Applies stability filtering and cooldown logic to confirm detections.

### 3. User Interface (`antirickroll.ui`)
- **PySide6:** Modern Qt-based interface with custom dark styling.
- **Visualizations:** Real-time waveform and peak level monitors.
- **Tray Icon:** Background lifecycle management.

### 4. Core (`antirickroll.core`)
- **Settings:** Persistent JSON configuration.
- **Logging:** Rotating file logs.
- **Paths:** Bundled vs. Source path resolution.

## Data Flow
The following sequence describes the real-time processing chain:
`Windows Audio` -> `WASAPI Capture` -> `Circular Buffer` -> `Spectrogram` -> `Hashing` -> `Matcher` -> `Stability Filter` -> `UI/Notification`
