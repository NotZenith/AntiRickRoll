"""Entry point for AntiRickRoll."""

import sys
from antirickroll.app.application import AntiRickRollApp, handle_exception

def main():
    """Application entry point.
    Sets up the global exception hook and starts the application.
    """
    sys.excepthook = handle_exception
    app = AntiRickRollApp()
    app.run()

if __name__ == "__main__":
    main()
