"""Main entry point for Papa's Games Launcher"""
import sys
from PyQt6.QtWidgets import QApplication
from gui.main_window import MainWindow


def main():
    """Main function"""
    app = QApplication(sys.argv)
    app.setApplicationName("Papa's Games Launcher")
    app.setOrganizationName("sugarypumpkin822")
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == '__main__':
    main()

