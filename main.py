"""
main.py
launches the gui and connects it to the logic
"""
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from gui import Ui_MainWindow
from logic import *

def main() -> None:
    """
    starts the application
    creates the app, main window, ui, and logic controller
    """
    app = QApplication(sys.argv)
    window = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(window)

    logic = Logic(ui)

    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()

