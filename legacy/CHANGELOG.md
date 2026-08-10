# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - 2026-08-09

### Added
- **Stability Pass:** Improved DSP safety for `NaN` and `Inf` values in circular buffer and processing pipeline.
- **Production Ready:** Officially declared v1.0.0 after successful CI fixes and UI polish.
- **Final Audit:** Completed a full maintainer pass for security, performance, and documentation consistency.

### Fixed
- **UI Test Failure:** Resolved `NameError: name 'QHBoxLayout' is not defined` in `AboutView`.
- **Import Cleanup:** Optimized imports and fixed missing dependencies in UI modules.

## [0.6.0] - 2026-08-08

### Added
- **Production Hardening:** Comprehensive reliability pass on the audio engine.
- **Welcome Experience:** New onboarding dialog for first-time users.
- **Categorized Settings:** Organized settings into General, Detection, Alerts, and Privacy.
- **Enhanced System Tray:** Full-featured tray menu with pause, mute, and navigation.
- **Privacy Focus:** Dedicated privacy section and "Local Only" documentation.
- **Asset Bundling:** Support for icons and alert sounds in the executable build.

### Fixed
- Robust recovery for disconnected audio devices.
- Improved sliding-window detection stability.
- Fixed several cross-thread signaling issues in the GUI.

## [0.5.0] - 2026-08-08

### Added
- **Production Packaging:** Established professional Windows distribution pipeline.
- **Build Script:** Automated EXE generation using PyInstaller.
- **Restructured Repository:** Clean separation of source, tests, assets, and docs.
- **Path Resolution:** Implemented professional user data and resource path handling.
- **GitHub Release Workflow:** Automated CI/CD for creating production releases.

## [0.4.0] - 2026-08-08

### Added
- **Real-Time Detection:** Live sliding-window analysis of system audio.
- **Stability Filter:** Confirmed matches across multiple windows to reduce false positives.
- **Dashboard UI:** Live confidence gauge and match history.
- **System Tray:** Background monitoring support.
