# 🛡️ AntiRickRoll

**"Never get Rickrolled again."**

AntiRickRoll is a professional Windows 11 application that monitors your computer's audio in real-time to detect and block the famous "Never Gonna Give You Up" song. Built for privacy and performance, it analyzes audio locally using advanced spectral peak hashing—no cloud, no microphone, and no recording.

## 🚀 Beginner Quick Start

**Don't know Python? You don't need it.**

1.  **Download:** Go to [Releases](https://github.com/NotZenith/AntiRickRoll/releases) and download `AntiRickRoll-v0.6.0.zip`.
2.  **Run:** Extract the folder and launch `AntiRickRoll.exe`.
3.  **Protect:** The app will minimize to your system tray and protect you silently.

## ✨ Core Features

- **Windows Loopback Capture:** Intercepts audio directly from the Windows audio engine (Chrome, Spotify, Discord, etc.).
- **Deterministic Detection:** High-accuracy matching using spectral landmarks (Digital Signal Processing).
- **Privacy First:**
    - 🔒 **Local only:** All processing stays on your CPU.
    - 🔒 **No microphone:** We never request mic permissions.
    - 🔒 **No telemetry:** We don't track you.
- **Smart Hysteresis:** Stabilizes detection across multiple audio windows to eliminate false positives.
- **Extensible:** Drop new fingerprint files into the `plugins` folder to detect other sounds.

## 🧠 How It Works

1.  **WASAPI Loopback:** Captures system playback without lag.
2.  **FFT Analysis:** Converts raw waves into frequency spectrograms.
3.  **Landmark Hashing:** Identifies unique "constellations" of audio peaks.
4.  **Temporal Matching:** Matches live hashes against the database using time-offset clustering.
5.  **Alerting:** Triggers native Windows notifications and a short audio beep.

## 🛠️ Developer Workspace

### Setup
```bash
git clone https://github.com/NotZenith/AntiRickRoll.git
pip install -e .[dev]
```

### Commands
- **Run Source:** `python -m antirickroll.app.main`
- **Run Tests:** `pytest`
- **Build EXE:** `python scripts/build.py`

## 📄 License & Privacy
- **License:** MIT
- **Privacy Policy:** AntiRickRoll does not collect, store, or transmit audio data.

---
*Created with ❤️ by the AntiRickRoll Team.*
