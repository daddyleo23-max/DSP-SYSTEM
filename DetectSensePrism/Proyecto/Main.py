from Proyecto.splash_screen import SplashScreen
from MainMenu import LoginScreen
import sys
from PyQt6.QtWidgets import QApplication


if __name__ == "__main__":
    app = QApplication(sys.argv)
    splash = SplashScreen()
    splash.show()
    sys.exit(app.exec())
