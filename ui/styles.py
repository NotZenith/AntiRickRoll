"""Modern dark theme styles for PySide6."""

DARK_THEME = """
QMainWindow {
    background-color: #121212;
    color: #e0e0e0;
}

QSidebar {
    background-color: #1e1e1e;
    border-right: 1px solid #333333;
}

QPushButton {
    background-color: #333333;
    color: #ffffff;
    border: none;
    padding: 10px;
    border-radius: 5px;
}

QPushButton:hover {
    background-color: #444444;
}

QLabel {
    color: #e0e0e0;
}

QGroupBox {
    border: 1px solid #333;
    border-radius: 5px;
    margin-top: 10px;
    font-weight: bold;
    color: #0078d4;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 3px 0 3px;
}
"""
