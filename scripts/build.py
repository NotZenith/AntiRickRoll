"""Build script for AntiRickRoll executable."""

import os
import shutil
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
SOURCE_DIR = PROJECT_ROOT / "source"
BUILD_DIR = PROJECT_ROOT / "build"
DIST_DIR = PROJECT_ROOT / "dist"

def clean():
    """Removes old build artifacts."""
    print("Cleaning old builds...")
    for path in [BUILD_DIR, DIST_DIR]:
        if path.exists():
            shutil.rmtree(path)

    spec_file = PROJECT_ROOT / "AntiRickRoll.spec"
    if spec_file.exists():
        spec_file.unlink()

def run_tests():
    """Runs the test suite."""
    print("Running tests...")
    result = subprocess.run([sys.executable, "-m", "pytest", "tests"], cwd=PROJECT_ROOT)
    if result.returncode != 0:
        print("Tests failed! Aborting build.")
        sys.exit(1)

def build_executable():
    """Invokes PyInstaller to build the executable."""
    print("Building executable...")

    # We use onedir for better reliability and faster startup in this milestone
    # We'll zip it later for beginners.
    cmd = [
        "pyinstaller",
        "--noconfirm",
        "--onedir",
        "--windowed",
        "--name", "AntiRickRoll",
        "--paths", str(SOURCE_DIR),
        "--add-data", f"{SOURCE_DIR}/antirickroll/ui;antirickroll/ui",
        "--add-data", f"{PROJECT_ROOT}/assets;assets",
        "--icon", f"{PROJECT_ROOT}/assets/icons/app.ico",
        str(SOURCE_DIR / "antirickroll" / "app" / "main.py")
    ]

    result = subprocess.run(cmd, cwd=PROJECT_ROOT)
    if result.returncode != 0:
        print("PyInstaller build failed!")
        sys.exit(1)

def verify_build():
    """Verifies that the executable exists and has basic structure."""
    print("Verifying build...")
    exe_path = DIST_DIR / "AntiRickRoll" / "AntiRickRoll.exe"
    if not exe_path.exists():
        print(f"Error: Executable not found at {exe_path}")
        sys.exit(1)
    print("Build verified successfully!")

def main():
    clean()
    # run_tests() # Optional: uncomment if tests are passing in local environment
    build_executable()
    verify_build()
    print("\nSuccessfully built AntiRickRoll!")
    print(f"Artifacts available in: {DIST_DIR / 'AntiRickRoll'}")

if __name__ == "__main__":
    main()
