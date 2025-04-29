import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QWidget
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QTimer
from PyQt6.QtGui import QPixmap, QColor

class PrismaticBackground(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(900, 500)
        self.setStyleSheet("background-color: #1e2229;")

class SplashScreen(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        self.container = PrismaticBackground()
        self.setCentralWidget(self.container)
        self.setFixedSize(900, 500)

        # Ruta relativa para la imagen (ajusta 'images/logo.png')
        base_dir = os.path.dirname(__file__)
        image_path = os.path.join(base_dir, "images", "logo DSP normal.png")
        #image_path = os.path.join(base_dir, "images", "logoDSP.png")
        #image_path = os.path.join(base_dir, "images", "nameDSP.png")
        
        
        
        self.image_label = QLabel(self.container)
        self.pixmap = QPixmap(image_path)
        if self.pixmap.isNull():
            print("Error: No se pudo cargar la imagen del splash.")
            self.pixmap = QPixmap(700, 350)
            self.pixmap.fill(QColor("#2d323b"))
        
        self.image_label.setPixmap(self.pixmap.scaled(700, 350, Qt.AspectRatioMode.KeepAspectRatio))
        self.image_label.setGeometry(100, 75, 700, 350)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Animación de fade-in
        self.animation = QPropertyAnimation(self.image_label, b"opacity")
        self.animation.setDuration(2000)
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.setEasingCurve(QEasingCurve.Type.InOutSine)
        self.animation.finished.connect(self._open_login)  # Conexión corregida
        self.animation.start()

    def _open_login(self):
        from login_screen import LoginScreen  # Import aquí para evitar circularidad
        self.login_screen = LoginScreen()
        self.login_screen.show()
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    splash = SplashScreen()
    splash.show()
    sys.exit(app.exec())