import sys
import hashlib
import json
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QLabel, QWidget, QLineEdit,
                            QPushButton, QVBoxLayout, QMessageBox, QStackedWidget, QSizePolicy)
from PyQt6.QtCore import Qt
from dashboard import Dashboard

class LoginScreen(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DetectSensePrism - Login")
        self.setFixedSize(600, 400)
        self.setStyleSheet("background-color: #2E3440;")

        # Cargar usuarios desde JSON (o crear archivo si no existe)
        self.users_file = "users.json"
        self.users = self._load_users()

        # Widget principal con pila (stack) para cambiar entre login/registro
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # Configurar páginas
        self._setup_login_page()
        self._setup_register_page()

    def _load_users(self):
        """Carga los usuarios desde un archivo JSON o crea uno con usuarios predeterminados."""
        if os.path.exists(self.users_file):
            with open(self.users_file, "r") as f:
                return json.load(f)
        else:
            # Usuarios predeterminados (admin:admin123, docente:docente123)
            default_users = {
                "admin": hashlib.sha256("admin123".encode()).hexdigest(),
                "docente": hashlib.sha256("docente123".encode()).hexdigest()
            }
            with open(self.users_file, "w") as f:
                json.dump(default_users, f)
            return default_users

    def _setup_login_page(self):
        """Configura la página de inicio de sesión."""
        self.login_page = QWidget()
        login_layout = QVBoxLayout(self.login_page)
        login_layout.setContentsMargins(40, 40, 40, 40)

        # Título
        title = QLabel("Iniciar Sesión")
        title.setStyleSheet("color: #88C0D0; font-size: 24pt; font-weight: bold;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        login_layout.addWidget(title)

        # Campo Usuario
        user_label = QLabel("Usuario:")
        user_label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)
        login_layout.addWidget(user_label)
        self.login_user = QLineEdit()
        self.login_user.setPlaceholderText("Ej: admin")
        self.login_user.setStyleSheet("background-color: #4C566A; color: #ECEFF4; padding: 8px; border-radius: 5px;")
        login_layout.addWidget(self.login_user)

        # Campo Contraseña
        password_label = QLabel("Contraseña:")
        password_label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)
        login_layout.addWidget(password_label)
        self.login_password = QLineEdit()
        self.login_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.login_password.setStyleSheet("background-color: #4C566A; color: #ECEFF4; padding: 8px; border-radius: 5px;")
        login_layout.addWidget(self.login_password)

        # Botón Login
        btn_login = QPushButton("Ingresar")
        btn_login.setStyleSheet("""
            QPushButton {
                background-color: #81A1C1;
                color: #ECEFF4;
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-size: 12pt;
            }
            QPushButton:hover {
                background-color: #5E81AC;
            }
        """)
        btn_login.clicked.connect(self._handle_login)
        login_layout.addWidget(btn_login)

        # Enlace "¿No tienes cuenta? Regístrate"
        lbl_register_link = QLabel("<a href='#' style='color: #A3BE8C; text-decoration: none;'>¿No tienes cuenta? Regístrate</a>")
        lbl_register_link.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_register_link.linkActivated.connect(self._show_register_page)
        login_layout.addWidget(lbl_register_link)

        self.stack.addWidget(self.login_page)

    def _setup_register_page(self):
        """Configura la página de registro."""
        self.register_page = QWidget()
        register_layout = QVBoxLayout(self.register_page)
        register_layout.setContentsMargins(40, 40, 40, 40)

        # Título
        title_register = QLabel("Registro")
        title_register.setStyleSheet("color: #88C0D0; font-size: 24pt; font-weight: bold;")
        title_register.setAlignment(Qt.AlignmentFlag.AlignCenter)
        register_layout.addWidget(title_register)

        # Campos: Usuario, Contraseña, Confirmar Contraseña
        register_layout.addWidget(QLabel("Nuevo Usuario:"))
        self.register_user = QLineEdit()
        self.register_user.setStyleSheet("background-color: #4C566A; color: #ECEFF4; padding: 8px; border-radius: 5px;")
        register_layout.addWidget(self.register_user)

        register_layout.addWidget(QLabel("Contraseña:"))
        self.register_password = QLineEdit()
        self.register_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.register_password.setStyleSheet("background-color: #4C566A; color: #ECEFF4; padding: 8px; border-radius: 5px;")
        register_layout.addWidget(self.register_password)

        register_layout.addWidget(QLabel("Confirmar Contraseña:"))
        self.register_confirm = QLineEdit()
        self.register_confirm.setEchoMode(QLineEdit.EchoMode.Password)
        self.register_confirm.setStyleSheet("background-color: #4C566A; color: #ECEFF4; padding: 8px; border-radius: 5px;")
        register_layout.addWidget(self.register_confirm)

        # Botón Registrar
        btn_register = QPushButton("Registrarse")
        btn_register.setStyleSheet("""
            QPushButton {
                background-color: #A3BE8C;
                color: #ECEFF4;
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-size: 12pt;
            }
            QPushButton:hover {
                background-color: #748C6A;
            }
        """)
        btn_register.clicked.connect(self._handle_register)
        register_layout.addWidget(btn_register)

        # Enlace "¿Ya tienes cuenta? Inicia sesión"
        lbl_login_link = QLabel("<a href='#' style='color: #81A1C1; text-decoration: none;'>¿Ya tienes cuenta? Inicia sesión</a>")
        lbl_login_link.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_login_link.linkActivated.connect(self._show_login_page)
        register_layout.addWidget(lbl_login_link)

        self.stack.addWidget(self.register_page)

    def _show_register_page(self):
        self.stack.setCurrentWidget(self.register_page)

    def _show_login_page(self):
        self.stack.setCurrentWidget(self.login_page)

    def _handle_login(self):
        user = self.login_user.text().strip()
        password = self.login_password.text().strip()

        if not user or not password:
            QMessageBox.warning(self, "Error", "¡Usuario y contraseña son obligatorios!")
            return

        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        if self.users.get(user) == hashed_password:
            QMessageBox.information(self, "Éxito", f"Bienvenido, {user}!")
            self._open_dashboard(user)
        else:
            QMessageBox.critical(self, "Error", "Usuario o contraseña incorrectos.")

    def _handle_register(self):
        user = self.register_user.text().strip()
        password = self.register_password.text().strip()
        confirm = self.register_confirm.text().strip()

        if not user or not password or not confirm:
            QMessageBox.warning(self, "Error", "¡Todos los campos son obligatorios!")
            return

        if password != confirm:
            QMessageBox.warning(self, "Error", "¡Las contraseñas no coinciden!")
            return

        if user in self.users:
            QMessageBox.warning(self, "Error", "¡El usuario ya existe!")
            return

        # Registrar nuevo usuario (con hash)
        self.users[user] = hashlib.sha256(password.encode()).hexdigest()
        with open(self.users_file, "w") as f:
            json.dump(self.users, f)
        QMessageBox.information(self, "Éxito", "¡Registro exitoso! Ahora inicia sesión.")
        self._show_login_page()

    def _open_dashboard(self, user_type):
        self.dashboard = Dashboard(user_type)  # Ahora usará la clase Dashboard correcta
        self.dashboard.showMaximized()  # Pantalla completa
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginScreen()
    window.show()
    sys.exit(app.exec())
