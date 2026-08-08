# AntiRickRoll

**Real-time audio fingerprint protection against unwanted Rickrolls.**

AntiRickRoll is a professional Windows application designed to detect and block the famous Rickroll song ("Never Gonna Give You Up") from any audio playing on your computer. It uses advanced Digital Signal Processing (DSP) and spectral landmark hashing to identify audio patterns locally, without uploading any data or requiring an internet connection.

## 🚀 Beginner Quick Start

**Don't know Python? You don't need it.**

1.  **Download:** Go to the [Releases](https://github.com/NotZenith/AntiRickRoll/releases) page.
2.  **Run:** Download `AntiRickRoll.zip`, extract it, and run `AntiRickRoll.exe`.
3.  **Protect:** The application will start monitoring your system audio automatically.

## ✨ Features

- **Windows Loopback Capture:** Captures audio from ANY application (Chrome, Spotify, VLC, etc.) before it hits your speakers.
- **Privacy First:** All analysis happens locally on your machine. No audio is ever uploaded or recorded.
- **Deterministic Recognition:** Uses spectral peak hashing for reliable identification, even in noisy environments.
- **System Tray Integration:** Runs quietly in the background; minimize to the tray for 24/7 protection.
- **Extensible Plugin System:** Add fingerprints for other sounds (John Cena, Vine Boom, etc.) by dropping a file into the plugins folder.
- **Modern UI:** A sleek Windows 11-style dark theme with real-time audio visualization.

## 🛠️ Developer Setup

For those who want to build from source or contribute to the project.

### Prerequisites
- Python 3.9+
- Git

### Installation
1.  **Clone the repository:**
    ```bash
    git clone https://github.com/NotZenith/AntiRickRoll.git
    cd AntiRickRoll
    ```
2.  **Create a virtual environment:**
    ```bash
    python -m venv .venv
    source .venv/Scripts/activate  # Windows
    ```
3.  **Install dependencies:**
    ```bash
    pip install -e .[dev]
    ```

### Running from Source
```bash
python -m antirickroll.app.main
```

### Building the Executable
```bash
python scripts/build.py
```

## 🧠 How It Works

AntiRickRoll processes live audio through a modular pipeline:
1.  **WASAPI Loopback:** Captures system output.
2.  **FFT & Spectrogram:** Converts time-domain audio to frequency-domain landmarks.
3.  **Landmark Hashing:** Generates unique hashes based on spectral peaks.
4.  **Temporal Matching:** Compares live hashes against a local database using a time-offset histogram.
5.  **Stability Filter:** Confirms detection only after multiple consistent matches to prevent false positives.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to get started.

---
*AntiRickRoll is an open-source project dedicated to preserving your sanity in a world of surprise links.*
