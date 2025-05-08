from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton,
    QHBoxLayout, QListWidget, QComboBox, QMessageBox,
    QLineEdit, QDialog, QSpinBox, QTableWidget, QTableWidgetItem,
    QTabWidget, QFormLayout, QHeaderView, QGroupBox, QFrame, QStackedWidget, QFileDialog, QCheckBox, QTimeEdit
)
import json
from PyQt6.QtCore import Qt, QTimer, QDateTime, QTime
from PyQt6.QtGui import QColor
from datetime import datetime, timedelta
from random import randint, choice

from pdf_reader import extraer_datos_pdf
from database import insertar_datos_pdf


class Dashboard(QMainWindow):
    def __init__(self, user_type):
        super().__init__()
        self.user_type = user_type
        self.clase_activa = False
        self.hora_inicio_clase = None
        self.current_dialog = None

        
        
        # Datos de ejemplo
        self.materias = {
            "Programación": ["Grupo A", "Grupo B"],
            "Base de Datos": ["Grupo C"],
            "Matemáticas": ["Grupo D", "Grupo E"]
        }
        
        self.alumnos = {
            "Grupo A": [
                {"nombre": "Juan Pérez", "matricula": "23000258", "numero_control": "23000258"},
                {"nombre": "María Gómez", "matricula": "23458789", "numero_control": "23458789" },
                {"nombre": "Carlos Ruiz", "matricula": "25457986", "numero_contorl": "25457986"}
            ],
            "Grupo B": [
                {"nombre": "Ana López", "matricula": "24987562", "numero_control": "24987562"},
                {"nombre": "Pedro Sánchez", "matricula": "24523477", "numero_control": "24523477"}
            ]
        }
        
        # Nuevas estructuras para el historial
        self.historial_clases = []
        self.aulas = {
            "Matemáticas - Grupo D": "Laboratorio 3",
            "Física - Grupo A": "Aula 102"
        }
        
        self.setup_ui()

    def setup_ui(self):
        # ===================== ESTILOS (MANTENIDOS) =====================
        self.setStyleSheet("""
            QMainWindow, QWidget, QDialog {
                background-color: #2E3440;
                color: #ECEFF4;
                font-size: 14px;
            }
            QLabel {
                font-size: 16px;
            }
            QPushButton {
                background-color: #81A1C1;
                border: none;
                border-radius: 5px;
                padding: 10px;
                min-width: 120px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #5E81AC;
            }
            QPushButton#success {
                background-color: #A3BE8C;
                font-weight: bold;
            }
            QPushButton#danger {
                background-color: #BF616A;
            }
            QListWidget, QComboBox, QLineEdit, QSpinBox {
                background-color: #3B4252;
                border: 1px solid #4C566A;
                border-radius: 5px;
                padding: 8px;
                min-height: 30px;
            }
            QListWidget {
                min-width: 250px;
            }
            QTableWidget {
                background-color: #3B4252;
                border: 1px solid #4C566A;
                border-radius: 5px;
            }
            QHeaderView::section {
                background-color: #4C566A;
                padding: 5px;
            }
            QGroupBox {
                font-size: 16px;
                font-weight: bold;
                border: 2px solid #4C566A;
                border-radius: 10px;
                margin-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)

        self.materias = {}  # Inicializar el diccionario de materias
        self.cargar_clases()  # Cargar las clases desde el archivo JSON

    # Configuración de la interfaz
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        

        
        

    # Configurar el menú y otras secciones...
        

        # ===================== WIDGET CENTRAL =====================
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ===================== COLUMNA IZQUIERDA (MENÚ) =====================
        left_menu = QWidget()
        left_menu.setFixedWidth(250)
        left_menu.setStyleSheet("background-color: #3B4252;")
        left_layout = QVBoxLayout(left_menu)
        left_layout.setContentsMargins(15, 20, 15, 20)
        left_layout.setSpacing(15)

        # Título de usuario
        lbl_user = QLabel(f"👤 {self.user_type.capitalize()}")
        lbl_user.setStyleSheet("font-size: 18px; font-weight: bold; color: #88C0D0; padding-bottom: 15px;")
        left_layout.addWidget(lbl_user)

        # Botones del menú (conectados a tus métodos originales)
        btn_clases = QPushButton("📚 Gestionar Clases")
        btn_programar = QPushButton("📅 Programar Clases")
        btn_alumnos = QPushButton("👥 Registrar Alumnos")
        btn_exportar = QPushButton("📄 Exportar Archivo")
        btn_historial = QPushButton("⏳ Historial")
        btn_asistencias = QPushButton("🕒 Consultar Alumnos")
        btn_notas = QPushButton("📝 Notas de Curso")
        
        
        

        btn_clases.clicked.connect(self.show_clases_dialog)
        btn_programar.clicked.connect(self.show_programar_clases_dialog)
        btn_alumnos.clicked.connect(self.show_registro_alumnos_dialog)
        btn_asistencias.clicked.connect(self.show_consulta_alumnos_dialog)
        btn_historial.clicked.connect(self.show_historial_dialog)
        btn_notas.clicked.connect(lambda: QMessageBox.information(self, "En desarrollo", "Próximamente"))
        btn_exportar.clicked.connect(self.show_exportar_dialog)
        

        # Estilo de botones del menú
        menu_btn_style = """
            QPushButton {
                text-align: left;
                padding: 12px 15px;
                border-radius: 5px;
                margin: 5px 0;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #4C566A;
            }
        """
        for btn in [btn_clases, btn_alumnos, btn_asistencias, btn_notas, btn_historial, btn_exportar, btn_programar]:
            btn.setStyleSheet(menu_btn_style)
            left_layout.addWidget(btn)

        left_layout.addStretch()
        
        # Botón de cerrar sesión
        btn_logout = QPushButton("🔒 Cerrar Sesión")
        btn_logout.setStyleSheet("background-color: #BF616A;")
        btn_logout.clicked.connect(self.close)
        left_layout.addWidget(btn_logout)

        main_layout.addWidget(left_menu)

        # ===================== COLUMNA DERECHA (CONTENIDO) =====================
         # ===================== COLUMNA DERECHA (CONTENIDO) =====================
        right_content = QWidget()
        right_layout = QVBoxLayout(right_content)
        right_layout.setContentsMargins(30, 30, 30, 30)
        right_layout.setSpacing(20)

    # --- Contenedor para contenido dinámico ---
        self.content_stack = QStackedWidget()
        self.content_stack.setStyleSheet("background-color: #3B4252; border-radius: 10px;")
    
    # Widget vacío inicial
        self.empty_content = QWidget()
        self.content_stack.addWidget(self.empty_content)

        # --------------------- SECCIÓN DE RECORDATORIOS ---------------------
        # --------------------- SECCIÓN DE RECORDATORIOS ---------------------
        reminder_box = QGroupBox("📌 Recordatorios")
        reminder_layout = QVBoxLayout()

# Cargar clases programadas
        clases_programadas = self.cargar_programaciones()
        if clases_programadas:
            for clase in clases_programadas:
                nombre = clase.get("clase", "Sin nombre")
                fecha_inicio = clase.get("fecha_inicio", "¿?")
                fecha_fin = clase.get("fecha_fin", "¿?")
                dias = ", ".join(clase.get("dias", []))
                hora_inicio = clase.get("hora_inicio", "")
                hora_fin = clase.get("hora_fin", "")
                texto = (f"📚 {nombre}\n"
                         f"🗓️ {fecha_inicio} a {fecha_fin}\n"
                         f"🕒 {dias} {hora_inicio}-{hora_fin}")

    # Widget contenedor horizontal
                recordatorio_widget = QWidget()
                recordatorio_layout = QHBoxLayout(recordatorio_widget)
                recordatorio_layout.setContentsMargins(0, 0, 0, 0)

                lbl = QLabel(texto)
                lbl.setStyleSheet("font-size: 14px; font-weight: normal; padding: 3px 0;")
                btn_iniciar = QPushButton("Iniciar Clase")
                btn_iniciar.setStyleSheet("padding: 2px 8px;")
                btn_iniciar.clicked.connect(lambda _, c=clase: self.iniciar_clase_desde_recordatorio(c))

                recordatorio_layout.addWidget(lbl)
                recordatorio_layout.addWidget(btn_iniciar)
                reminder_layout.addWidget(recordatorio_widget)

        else:
            reminder_layout.addWidget(QLabel("No hay clases programadas."))

        reminder_box.setLayout(reminder_layout)
        right_layout.addWidget(reminder_box)
        
    


        # --------------------- SECCIÓN DE HISTORIAL ---------------------
        # Sección de Notas
        notas_box = QGroupBox("📝 Notas")
        notas_layout = QVBoxLayout()

# Botón para agregar una nueva nota
        btn_agregar_nota = QPushButton("Agregar Nota")
        btn_agregar_nota.setObjectName("success")
        btn_agregar_nota.clicked.connect(self.show_agregar_nota_dialog)
        notas_layout.addWidget(btn_agregar_nota)

# Lista de notas
        self.lista_notas = QListWidget()
        self.lista_notas.setStyleSheet("""
            QListWidget {
                background-color: #3B4252;
                border: 1px solid #4C566A;
                border-radius: 5px;
                padding: 8px;
            }
            QListWidget::item {
                padding: 10px;
            }
            QListWidget::item:selected {
                background-color: #5E81AC;
                color: #ECEFF4;
            }
        """)
        notas_layout.addWidget(self.lista_notas)

        notas_box.setLayout(notas_layout)
        right_layout.addWidget(notas_box)

        main_layout.addWidget(right_content)

        # --- Ordenamiento ---
        #right_layout.addWidget(self.content_stack, stretch=2)  # Área dinámica (60%)
        right_layout.addWidget(reminder_box, stretch=1)        # Recordatorios (20%)
        right_layout.addWidget(notas_box, stretch=1)         # Historial (20%)

        # ===================== BARRA DE CLASE ACTIVA (TU IMPLEMENTACIÓN ORIGINAL) =====================
        self.setup_clase_activa_ui(right_layout)

        # ===================== BARRA SUPERIOR =====================
       

        # ===================== BARRA DE CLASE ACTIVA =====================
        self.barra_clase_container = QWidget()
        self.barra_clase_layout = QVBoxLayout(self.barra_clase_container)
        self.barra_clase_layout.setContentsMargins(20, 10, 20, 10)
        
        # Sección superior (Reloj + Detalles clase)
        self.clase_info_container = QWidget()
        clase_info_layout = QHBoxLayout(self.clase_info_container)
        
        # Reloj
        self.lbl_reloj = QLabel("00:00:00")
        self.lbl_reloj.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #A3BE8C;
            padding: 10px;
        """)
        
        # Detalles de la clase
        self.lbl_detalle_clase = QLabel("Clase no iniciada")
        self.lbl_detalle_clase.setStyleSheet("""
            font-size: 18px;
            color: #81A1C1;
            padding: 10px;
        """)
        
        clase_info_layout.addWidget(self.lbl_reloj)
        clase_info_layout.addStretch()
        clase_info_layout.addWidget(self.lbl_detalle_clase)
        
        # Tabla de asistencia
        self.tabla_asistencia = QTableWidget()
        self.tabla_asistencia.setColumnCount(5)
        self.tabla_asistencia.setHorizontalHeaderLabels([
            "#", "Nombre", "Matrícula", "Hora Llegada", "Estado"
        ])
        self.tabla_asistencia.verticalHeader().setVisible(False)
        self.tabla_asistencia.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.tabla_asistencia.setStyleSheet("""
            QTableWidget {
                background-color: #3B4252;
                border: 1px solid #4C566A;
                border-radius: 5px;
            }
            QHeaderView::section {
                background-color: #4C566A;
                padding: 5px;
            }
        """)
        
        self.barra_clase_layout.addWidget(self.clase_info_container)
        self.barra_clase_layout.addWidget(self.tabla_asistencia)
        self.barra_clase_container.hide()
        
        main_layout.addWidget(self.barra_clase_container)

        # ===================== BOTONES PRINCIPALES =====================
    

        # ===================== CERRAR SESIÓN =====================
      

        # ===================== TEMPORIZADORES =====================
        # ===================== TEMPORIZADORES =====================
        self.timer = QTimer()
        self.timer.timeout.connect(self.actualizar_reloj)
        self.timer.start(1000)

        self.simulacion_timer = QTimer()
        self.simulacion_timer.timeout.connect(self.registrar_llegada_simulada)

    def setup_clase_activa_ui(self, parent_layout):
        """TU IMPLEMENTACIÓN ORIGINAL SIN MODIFICAR"""
        self.barra_clase_container = QWidget()
        self.barra_clase_layout = QVBoxLayout(self.barra_clase_container)
        self.barra_clase_layout.setContentsMargins(20, 10, 20, 10)
        
        # Sección superior (Reloj + Detalles clase)
        self.clase_info_container = QWidget()
        clase_info_layout = QHBoxLayout(self.clase_info_container)
        
        self.lbl_reloj = QLabel("00:00:00")
        self.lbl_reloj.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #A3BE8C;
            padding: 10px;
        """)
        
        self.lbl_detalle_clase = QLabel("Clase no iniciada")
        self.lbl_detalle_clase.setStyleSheet("""
            font-size: 18px;
            color: #81A1C1;
            padding: 10px;
        """)
        
        clase_info_layout.addWidget(self.lbl_reloj)
        clase_info_layout.addStretch()
        clase_info_layout.addWidget(self.lbl_detalle_clase)
        
        # Tabla de asistencia
        self.tabla_asistencia = QTableWidget()
        self.tabla_asistencia.setColumnCount(5)
        self.tabla_asistencia.setHorizontalHeaderLabels(["#", "Nombre", "Matrícula", "Hora Llegada", "Estado"])
        self.tabla_asistencia.verticalHeader().setVisible(False)
        self.tabla_asistencia.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.tabla_asistencia.setStyleSheet("""
            QTableWidget {
                background-color: #3B4252;
                border: 1px solid #4C566A;
                border-radius: 5px;
            }
            QHeaderView::section {
                background-color: #4C566A;
                padding: 5px;
            }
        """)
        
        self.barra_clase_layout.addWidget(self.clase_info_container)
        self.barra_clase_layout.addWidget(self.tabla_asistencia)
        self.barra_clase_container.hide()
        
        parent_layout.addWidget(self.barra_clase_container)

    # ===================== GESTIÓN DE CLASES =====================
    # ======================Metodos Modificados Vol.2 ===============
    def show_clases_dialog(self):
        
        self.current_dialog = QDialog(self)
        self.current_dialog.setWindowTitle("Gestionar Clases")
        self.current_dialog.setModal(False)  # Cambiado a no modal
        dialog_layout = QVBoxLayout(self.current_dialog)
        self.setup_clases_section(dialog_layout)
        

    # Botón para agregar materia
        btn_add_materia = QPushButton("Agregar Materia")
        btn_add_materia.setObjectName("success")
        btn_add_materia.setFixedHeight(50)
        btn_add_materia.clicked.connect(self.show_add_materia_dialog)
        dialog_layout.addWidget(btn_add_materia, alignment=Qt.AlignmentFlag.AlignCenter)

    # Botón para agregar grupo
        btn_add_grupo = QPushButton("Agregar Grupo")
        btn_add_grupo.setObjectName("success")
        btn_add_grupo.setFixedHeight(50)
        btn_add_grupo.clicked.connect(self.show_create_grupo_dialog)
        dialog_layout.addWidget(btn_add_grupo, alignment=Qt.AlignmentFlag.AlignCenter)

    # Crear un contenedor para los botones si no existe
        btn_container = QWidget()
        btn_layout = QHBoxLayout(btn_container)
        btn_layout.setSpacing(15)
        btn_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

    # Agregar el contenedor al diálogo
        dialog_layout.addWidget(btn_container)

        self.current_dialog.show()


    def show_inicio_curso_dialog(self):
        self.current_dialog = QDialog(self)
        self.current_dialog.setWindowTitle("Inicio de Curso")
        self.current_dialog.setModal(False)  # Cambiado a no modal
        dialog_layout = QVBoxLayout(self.current_dialog)
        
        form = QFormLayout()
        self.combo_materias_curso = QComboBox()
        self.combo_materias_curso.addItems(self.materias.keys())
        form.addRow("Materia:", self.combo_materias_curso)

        self.combo_grupos_curso = QComboBox()
        form.addRow("Grupo:", self.combo_grupos_curso)
        self.combo_materias_curso.currentTextChanged.connect(self.actualizar_grupos_curso)

        self.actualizar_grupos_curso()

        dialog_layout.addLayout(form)
        dialog_layout.addWidget(QLabel("Seleccione la materia y grupo para iniciar la clase"))

        btn_iniciar = QPushButton("Iniciar Clase")
        btn_iniciar.clicked.connect(lambda: self.iniciar_clase_desde_dialogo(self.current_dialog))
        dialog_layout.addWidget(btn_iniciar)


        self.current_dialog.show()

    def iniciar_clase_desde_dialogo(self, dialog):
        """Maneja el inicio de clase desde diálogos"""
        materia = self.combo_materias_curso.currentText()
        grupo = self.combo_grupos_curso.currentText()

        if not materia or not grupo:
            QMessageBox.warning(self, "Error", "Debe seleccionar una materia y un grupo.")
            return

    # Si necesitas seleccionar el ítem en la lista de materias (opcional)
        items = self.lista_materias.findItems(materia, Qt.MatchFlag.MatchExactly)
        if items:
            self.lista_materias.setCurrentItem(items[0])
            self.combo_grupos.setCurrentText(grupo)
            self.iniciar_clase(materia, grupo)
            dialog.close()
        else:
            QMessageBox.warning(self, "Error", "No se pudo iniciar la clase.")


    def cargar_clases(self):
        try:
            with open("clases.json", "r") as file:
                clases = json.load(file)
                for clase in clases:
                    materia = clase["materia"]
                    grupo = clase["grupo"]
                    if materia not in self.materias:
                        self.materias[materia] = []
                    if grupo not in self.materias[materia]:
                        self.materias[materia].append(grupo)
        except FileNotFoundError:
            QMessageBox.warning(self, "Advertencia", "El archivo clases.json no existe. Se iniciará vacío.")
            self.materias = {}
        except json.JSONDecodeError:
            QMessageBox.critical(self, "Error", "El archivo clases.json tiene un formato inválido.")
            self.materias = {}

    

    def setup_clases_section(self, parent_layout):
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setSpacing(15)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        lbl_titulo = QLabel("Gestión de Clases")
        lbl_titulo.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: #88C0D0;
            margin-bottom: 15px;
        """)
        lbl_titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(lbl_titulo)

        selection_container = QWidget()
        selection_layout = QHBoxLayout(selection_container)
        selection_layout.setSpacing(20)
        selection_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

    # Columna Materias
        materias_frame = QWidget()
        materias_layout = QVBoxLayout(materias_frame)
        materias_layout.setSpacing(10)
        materias_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_materias = QLabel("Materias Disponibles:")
        materias_layout.addWidget(lbl_materias)
        self.lista_materias = QListWidget()
        self.lista_materias.addItems(self.materias.keys())
        self.lista_materias.currentItemChanged.connect(self.actualizar_grupos)
        materias_layout.addWidget(self.lista_materias)

    # Columna Grupos
        grupos_frame = QWidget()
        grupos_layout = QVBoxLayout(grupos_frame)
        grupos_layout.setSpacing(10)
        grupos_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_grupos = QLabel("Grupos Disponibles:")
        grupos_layout.addWidget(lbl_grupos)
        self.combo_grupos = QComboBox()
        grupos_layout.addWidget(self.combo_grupos)

        selection_layout.addWidget(materias_frame)
        selection_layout.addWidget(grupos_frame)
        layout.addWidget(selection_container)

    # Contenedor para los botones
        botones_container = QWidget()
        botones_layout = QHBoxLayout(botones_container)
        botones_layout.setSpacing(20)
        botones_layout.setContentsMargins(0, 20, 0, 0)

    # Botones a la izquierda
        izquierda_layout = QVBoxLayout()
        izquierda_layout.setSpacing(10)
        izquierda_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        btn_add_materia = QPushButton("Agregar Materia")
        btn_add_materia.setObjectName("success")
        btn_add_materia.setFixedHeight(50)
        btn_add_materia.clicked.connect(self.show_add_materia_dialog)
        izquierda_layout.addWidget(btn_add_materia)

        btn_add_grupo = QPushButton("Agregar Grupo")
        btn_add_grupo.setObjectName("success")
        btn_add_grupo.setFixedHeight(50)
        btn_add_grupo.clicked.connect(self.show_create_grupo_dialog)
        izquierda_layout.addWidget(btn_add_grupo)

        botones_layout.addLayout(izquierda_layout)

    # Botones a la derecha
        derecha_layout = QVBoxLayout()
        derecha_layout.setSpacing(10)
        derecha_layout.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.btn_iniciar = QPushButton("INICIAR CLASE")
        self.btn_iniciar.setObjectName("success")
        self.btn_iniciar.setFixedHeight(50)
        self.btn_iniciar.setEnabled(False)
        self.btn_iniciar.clicked.connect(self.iniciar_clase)
        derecha_layout.addWidget(self.btn_iniciar)

        btn_create_clase = QPushButton("CREAR CLASE")
        btn_create_clase.setObjectName("success")
        btn_create_clase.setFixedHeight(50)
        btn_create_clase.setEnabled(False)
        btn_create_clase.clicked.connect(self.crear_clase_desde_gestionar)
        derecha_layout.addWidget(btn_create_clase)

        botones_layout.addLayout(derecha_layout)

        layout.addWidget(botones_container)

    # Actualizar estado de los botones según la selección
        self.lista_materias.currentItemChanged.connect(lambda: self.actualizar_botones(btn_create_clase))
        self.combo_grupos.currentTextChanged.connect(lambda: self.actualizar_botones(btn_create_clase))

        parent_layout.addWidget(container)

    def actualizar_botones(self, btn_create_clase):
        """Habilita o deshabilita los botones según la selección."""
        materia_seleccionada = self.lista_materias.currentItem() is not None
        grupo_seleccionado = self.combo_grupos.currentText() != ""
        btn_create_clase.setEnabled(materia_seleccionada and grupo_seleccionado)
        self.btn_iniciar.setEnabled(materia_seleccionada and grupo_seleccionado)

    def crear_clase_desde_gestionar(self):
        """Guarda la clase seleccionada en un archivo JSON."""
        materia = self.lista_materias.currentItem().text()
        grupo = self.combo_grupos.currentText()

        # Cargar clases existentes
        try:
            with open("clases.json", "r") as file:
                clases = json.load(file)
        except FileNotFoundError:
            clases = []

        # Verificar si la clase ya existe
        for clase in clases:
            if clase["materia"] == materia and clase["grupo"] == grupo:
                QMessageBox.warning(self, "Error", "La clase ya existe.")
                return

        # Agregar la nueva clase
        clases.append({
            "materia": materia,
            "grupo": grupo
        })

        # Guardar en el archivo JSON
        with open("clases.json", "w") as file:
            json.dump(clases, file, indent=4)

        QMessageBox.information(self, "Éxito", f"Clase {materia} - {grupo} creada correctamente.")

    def actualizar_grupos(self, current_item):
        """Actualiza los grupos disponibles cuando se selecciona una materia"""
        if current_item:
            materia = current_item.text()
            self.combo_grupos.clear()
            self.combo_grupos.addItems(self.materias.get(materia, []))
            self.btn_iniciar.setEnabled(self.combo_grupos.count() > 0)
            
    def iniciar_clase(self, materia=None, grupo=None, datos_clase=None):
        """
        Método principal para iniciar una clase.
        Puede recibir materia y grupo directamente, o un diccionario datos_clase con el formato {"clase": "Materia - Grupo"}
        """
    # Permitir llamada con datos_clase (desde recordatorio)
        if datos_clase is not None:
            if "clase" in datos_clase and " - " in datos_clase["clase"]:
                materia, grupo = datos_clase["clase"].split(" - ", 1)
            else:
                QMessageBox.warning(self, "Error", "Datos de clase incompletos.")
                return
        else:
            # Si no se pasan argumentos, obtenerlos de la interfaz
            if materia is None or grupo is None:
                if self.lista_materias.currentItem() is None:
                    QMessageBox.warning(self, "Error", "Debe seleccionar una materia.")
                    return
                materia = self.lista_materias.currentItem().text()
                grupo = self.combo_grupos.currentText()
                if not grupo:
                    QMessageBox.warning(self, "Error", "Debe seleccionar un grupo.")
                    return

    # Busca alumnos
        alumnos = self.alumnos.get(grupo, [])
        if not alumnos:
            QMessageBox.warning(self, "Sin alumnos", f"No hay alumnos registrados en el grupo {grupo}.")
            return

    # Configura la clase activa
        self.clase_activa = True
        self.hora_inicio_clase = datetime.now().time()
        self.barra_clase_container.show()
        self.lbl_detalle_clase.setText(f"{materia} - {grupo} | Iniciada: {self.hora_inicio_clase.strftime('%H:%M')}")

    # Configura la tabla de asistencia
        self.tabla_asistencia.setRowCount(len(alumnos))
        for idx, alumno in enumerate(alumnos):
            self.tabla_asistencia.setItem(idx, 0, QTableWidgetItem(str(idx + 1)))
            self.tabla_asistencia.setItem(idx, 1, QTableWidgetItem(alumno['nombre']))
            self.tabla_asistencia.setItem(idx, 2, QTableWidgetItem(alumno['matricula']))
            self.tabla_asistencia.setItem(idx, 3, QTableWidgetItem("--:--:--"))
            estado_item = QTableWidgetItem("No registrado")
            estado_item.setForeground(QColor(136, 192, 208))
            self.tabla_asistencia.setItem(idx, 4, estado_item)

        self.tabla_asistencia.resizeColumnsToContents()
        self.simular_llegadas_alumnos(grupo)

    # Elimina botones existentes para evitar duplicados
        for i in reversed(range(self.barra_clase_layout.count())):
            widget = self.barra_clase_layout.itemAt(i).widget()
            if isinstance(widget, QPushButton):
                self.barra_clase_layout.removeWidget(widget)
                widget.deleteLater()

    # Botón para finalizar clase
        btn_finalizar = QPushButton("Finalizar Clase")
        btn_finalizar.setObjectName("danger")
        btn_finalizar.clicked.connect(self.finalizar_clase)
        self.barra_clase_layout.addWidget(btn_finalizar, alignment=Qt.AlignmentFlag.AlignCenter)

    # Botón para registro manual
        btn_registro_manual = QPushButton("Registro Manual")
        btn_registro_manual.setObjectName("success")
        btn_registro_manual.clicked.connect(self.registrar_llegada_manual)
        self.barra_clase_layout.addWidget(btn_registro_manual, alignment=Qt.AlignmentFlag.AlignCenter)


    def crear_clase(self, materia, grupo, horario, aula, fecha_inicio, fecha_fin, dialog):
        """Guarda una clase en un archivo JSON."""
        if not materia or not grupo or not horario or not aula or not fecha_inicio or not fecha_fin:
            QMessageBox.warning(self, "Error", "Todos los campos son obligatorios.")
            return

    # Cargar clases existentes
        try:
            with open("clases.json", "r") as file:
                clases = json.load(file)
        except FileNotFoundError:
            clases = []

    # Agregar la nueva clase
        clases.append({
            "materia": materia,
            "grupo": grupo,
            "horario": horario,
            "aula": aula,
            "fecha_inicio": fecha_inicio,
            "fecha_fin": fecha_fin
        })

    # Guardar en el archivo JSON
        with open("clases.json", "w") as file:
            json.dump(clases, file, indent=4)

        QMessageBox.information(self, "Éxito", "Clase creada correctamente.")
        dialog.close()

    # Actualizar la lista de clases en "Gestionar Clases"
        self.actualizar_lista_clases()


    def actualizar_lista_clases(self):
        """Actualiza la lista de clases en 'Gestionar Clases'."""
        try:
        # Cargar clases desde el archivo JSON
            with open("clases.json", "r") as file:
                clases = json.load(file)

        # Mostrar las clases en una tabla o lista
            for clase in clases:
                print(f"Clase: {clase['materia']} - {clase['grupo']} | Horario: {clase['horario']} | Aula: {clase['aula']}")

        except FileNotFoundError:
            QMessageBox.warning(self, "Error", "No hay clases creadas.")

    # ===================== DIÁLOGOS DE GESTIÓN =====================
    def show_add_materia_dialog(self):

        self.show_blur_overlay()
        dialog = QDialog(self)
        dialog.setWindowTitle("Nueva Materia")
        dialog.setModal(True)
        dialog_layout = QVBoxLayout(dialog)

        form = QFormLayout()
        self.input_materia = QLineEdit()
        form.addRow("Nombre de la materia:", self.input_materia)

        btn_guardar = QPushButton("Guardar")
        btn_guardar.clicked.connect(lambda: self.add_materia(dialog))

        dialog_layout.addLayout(form)
        dialog_layout.addWidget(btn_guardar)
        dialog.finished.connect(self.hide_blur_overlay)
        dialog.exec()

    def add_materia(self, dialog):
        nombre = self.input_materia.text().strip()
        if nombre:
            if nombre not in self.materias:
                self.materias[nombre] = []
                self.lista_materias.addItem(nombre)
                dialog.close()
                QMessageBox.information(self, "Éxito", "Materia añadida correctamente")
            else:
                QMessageBox.warning(self, "Error", "El nombre no puede estar vacío")
        else:
            QMessageBox.warning(self, "Error", "El nombre no puede estar vacío")

    def show_create_grupo_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Nuevo Grupo")
        dialog.setModal(True)
        dialog_layout = QVBoxLayout(dialog)

        form = QFormLayout()
        self.combo_materias_grupo = QComboBox()
        self.combo_materias_grupo.addItems(self.materias.keys())
        form.addRow("Materia:", self.combo_materias_grupo)

        self.input_grupo = QLineEdit()
        form.addRow("Nombre del grupo:", self.input_grupo)

        btn_guardar = QPushButton("Guardar")
        btn_guardar.clicked.connect(lambda: self.create_grupo(dialog))

        dialog_layout.addLayout(form)
        dialog_layout.addWidget(btn_guardar)
        dialog.exec()

    def create_grupo(self, dialog):
        """Agrega un nuevo grupo a la materia seleccionada y actualiza el combo de grupos."""
        materia = self.combo_materias_grupo.currentText()
        nombre_grupo = self.input_grupo.text().strip()

        if nombre_grupo:
            if nombre_grupo not in self.materias[materia]:
                self.materias[materia].append(nombre_grupo)  # Agregar el grupo a la materia
                if self.lista_materias.currentItem() and self.lista_materias.currentItem().text() == materia:
                    self.actualizar_grupos(self.lista_materias.currentItem())  # Actualizar el combo de grupos
                dialog.close()
                QMessageBox.information(self, "Éxito", "Grupo creado correctamente")
            else:
                QMessageBox.warning(self, "Error", "El grupo ya existe.")
        else:
            QMessageBox.warning(self, "Error", "El nombre no puede estar vacío")

    # ===================== REGISTRO DE ALUMNOS =====================
    def show_registro_alumnos_dialog(self):
        """Muestra el formulario de registro de alumnos en un QDialog."""
        dialog = QDialog(self)
        dialog.setWindowTitle("Registrar Alumnos")
        dialog.setModal(True)  # Hacer que el diálogo sea modal
        dialog.setMinimumSize(400, 300)
        layout = QVBoxLayout(dialog)

        # Crear el formulario de registro
        form = QFormLayout()

        # Campos del formulario
        input_nombre = QLineEdit()
        input_apellidos = QLineEdit()
        combo_grupo = QComboBox()
        combo_grupo.addItems(sum(self.materias.values(), []))  # Agregar grupos disponibles
        combo_carrera = QComboBox()
        combo_carrera.addItems([
            "Ingeniería en Sistemas Computacionales",
            "Ingeniería Electrónica",
            "Ingeniería Mecatrónica",
            "Ingeniería Industrial",
            "Ingeniería Civil",
            "Ingeniería Química",
            "Ingeniería en Energías Renovables",
            "Ingeniería Biomédica",
            "Ingeniería en Software",
            "Ingeniería en Telecomunicaciones"
        ])

        # Añadir campos al formulario
        form.addRow("Nombre(s):", input_nombre)
        form.addRow("Apellidos:", input_apellidos)
        form.addRow("Grupo:", combo_grupo)
        form.addRow("Carrera:", combo_carrera)

        # Botón para registrar huella dactilar
        btn_registrar_huella = QPushButton("Registrar Huella Dactilar")
        btn_registrar_huella.clicked.connect(self.registrar_huella_dactilar)
        form.addRow("Huella Dactilar:", btn_registrar_huella)


        # Botón para registrar
        btn_registrar = QPushButton("Registrar")
        btn_registrar.clicked.connect(lambda: self.registrar_alumno(
            input_nombre.text(),
            input_apellidos.text(),
            combo_grupo.currentText(),
            combo_carrera.currentText(),
            dialog
        ))

        # Añadir formulario y botón al layout del diálogo
        layout.addLayout(form)
        layout.addWidget(btn_registrar)

        dialog.setLayout(layout)
        dialog.exec()

    def registrar_huella_dactilar(self):
        """Simula el registro de huella dactilar (código comentado para Arduino)."""
        QMessageBox.information(self, "Registro de Huella", "Conecte el sensor de huellas para registrar.")
         # Código para Arduino (comentado por ahora)
        """
        import serial
        arduino = serial.Serial('COM3', 9600, timeout=1)  # Ajustar el puerto COM según tu configuración
        arduino.write(b'REGISTRAR_HUELLA')
        respuesta = arduino.readline().decode('utf-8').strip()
        if respuesta == 'HUELLA_REGISTRADA':
            QMessageBox.information(self, "Éxito", "Huella registrada correctamente.")
        else:
            QMessageBox.warning(self, "Error", "No se pudo registrar la huella.")
        arduino.close()
        """



    def registrar_alumno(self, nombre, apellidos, grupo, carrera, dialog):
        """Registra un alumno con los datos proporcionados."""
        if not nombre or not apellidos:
            QMessageBox.warning(self, "Error", "Todos los campos son obligatorios.")
            return

        # Generar número de control único
        numero_control = self.generar_numero_control()

        # Verificar si el grupo existe
        if grupo not in self.alumnos:
            self.alumnos[grupo] = []

        # Guardar alumno
        self.alumnos[grupo].append({
            'nombre': nombre,
            'apellidos': apellidos,
            'carrera': carrera,
            'numero_control': numero_control,
            'matricula': numero_control
        })

        QMessageBox.information(self, "Éxito", f"Alumno registrado correctamente.\nNúmero de Control: {numero_control}")
        dialog.close()

    def generar_numero_control(self):
        anio_actual = datetime.now().year % 100  # Últimos 2 dígitos (ej: 23 para 2023)
        while True:
            numero = randint(1000, 999999)  # 4 dígitos aleatorios
            numero_control = f"{anio_actual}{numero:04d}"  # Formato: 230001
        
        # Verificar que no exista en ningún grupo
            if not any(
                alumno.get('numero_control') == numero_control
                for grupo in self.alumnos.values()
                for alumno in grupo
            ):
                return numero_control

    # ===================== CONSULTA DE ALUMNOS =====================
    def show_consulta_alumnos_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Consulta de Alumnos")
        dialog.setModal(True)
        dialog.setMinimumSize(800, 500)
        dialog_layout = QVBoxLayout(dialog)

        # --- Campo de búsqueda ---
        search_layout = QHBoxLayout()
        input_busqueda = QLineEdit()
        input_busqueda.setPlaceholderText("Buscar alumno por nombre o matrícula...")
        btn_buscar = QPushButton("Buscar")
        search_layout.addWidget(input_busqueda)
        search_layout.addWidget(btn_buscar)
        dialog_layout.addLayout(search_layout)

        # --- Tabla de alumnos ---
        self.tabla_consulta = QTableWidget()
        self.tabla_consulta.setColumnCount(3)
        self.tabla_consulta.setHorizontalHeaderLabels(["Grupo", "Nombre", "Matrícula"])
        self.tabla_consulta.verticalHeader().setVisible(False)
        self.tabla_consulta.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        dialog_layout.addWidget(self.tabla_consulta)

        # Actualizar la tabla con los datos de los alumnos
        try:
            self.actualizar_tabla_todos_alumnos()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al cargar los alumnos: {e}")
            return

        # --- Botón para añadir a la clase activa ---
        btn_añadir_clase = QPushButton("Añadir a Clase Activa")
        btn_añadir_clase.clicked.connect(lambda: self.agregar_a_clase_activa(dialog))
        dialog_layout.addWidget(btn_añadir_clase)

        # Conectar el botón de búsqueda
        btn_buscar.clicked.connect(lambda: self.buscar_alumno(input_busqueda.text()))

        dialog.exec()
        
    def mostrar_dialogo_agregar_alumno(self, parent_dialog):
        dialog = QDialog(parent_dialog)
        dialog.setWindowTitle("Agregar Alumno")
        layout = QVBoxLayout(dialog)

    # Combo para grupo
        combo_grupo = QComboBox()
        combo_grupo.addItems(self.alumnos.keys())
        layout.addWidget(QLabel("Grupo:"))
        layout.addWidget(combo_grupo)

    # Nombre y matrícula
        input_nombre = QLineEdit()
        input_matricula = QLineEdit()
        layout.addWidget(QLabel("Nombre:"))
        layout.addWidget(input_nombre)
        layout.addWidget(QLabel("Matrícula:"))
        layout.addWidget(input_matricula)

    # Botón guardar
        btn_guardar = QPushButton("Guardar")
        btn_guardar.clicked.connect(lambda: self.guardar_alumno(combo_grupo.currentText(), input_nombre.text(), input_matricula.text(), dialog, parent_dialog))
        layout.addWidget(btn_guardar)

        dialog.exec()
        
    def guardar_alumno(self, grupo, nombre, matricula, dialog, parent_dialog):
        if not nombre or not matricula:
            QMessageBox.warning(dialog, "Error", "Nombre y matrícula son obligatorios.")
            return
    # Agrega el alumno (usa tu función de agregar alumno aquí)
        self.agregar_alumno(grupo, nombre, matricula)
        dialog.accept()
        self.actualizar_tabla_todos_alumnos()
    # Si quieres que el diálogo principal se actualice también:
        parent_dialog.repaint()
        
    def actualizar_tabla_todos_alumnos(self):
        """Llena la tabla de consulta con los datos de los alumnos."""
    # Asegúrate de que la tabla esté inicializada
        if not hasattr(self, 'tabla_consulta'):
            QMessageBox.critical(self, "Error", "La tabla de consulta no está inicializada.")
            return

    # Limpiar la tabla antes de llenarla
        self.tabla_consulta.setRowCount(0)

    # Llenar la tabla con los datos de los alumnos
        for grupo, alumnos in self.alumnos.items():
            for alumno in alumnos:
                row_position = self.tabla_consulta.rowCount()
                self.tabla_consulta.insertRow(row_position)
                self.tabla_consulta.setItem(row_position, 0, QTableWidgetItem(grupo))
                self.tabla_consulta.setItem(row_position, 1, QTableWidgetItem(alumno.get("nombre", "Sin nombre")))
                self.tabla_consulta.setItem(row_position, 2, QTableWidgetItem(alumno.get("matricula", "Sin matrícula")))

    def buscar_alumno(self, texto_busqueda):
        """Filtra los alumnos en la tabla según el texto ingresado."""
        texto_busqueda = texto_busqueda.strip().lower()
        self.tabla_consulta.setRowCount(0)  # Limpiar la tabla

        for grupo, alumnos in self.alumnos.items():
            for alumno in alumnos:
                if (texto_busqueda in alumno.get("nombre", "").lower() or
                    texto_busqueda in alumno.get("matricula", "").lower()):
                    row_position = self.tabla_consulta.rowCount()
                    self.tabla_consulta.insertRow(row_position)
                    self.tabla_consulta.setItem(row_position, 0, QTableWidgetItem(grupo))
                    self.tabla_consulta.setItem(row_position, 1, QTableWidgetItem(alumno.get("nombre", "Sin nombre")))
                    self.tabla_consulta.setItem(row_position, 2, QTableWidgetItem(alumno.get("matricula", "Sin matrícula")))

    def agregar_a_clase_activa(self, dialog):
        """Añade el alumno seleccionado a la clase activa."""
        if not self.clase_activa:
            QMessageBox.warning(self, "Error", "No hay una clase activa.")
            return

    # Obtener la fila seleccionada
        fila_seleccionada = self.tabla_consulta.currentRow()
        if fila_seleccionada == -1:
            QMessageBox.warning(self, "Error", "Debe seleccionar un alumno.")
            return

    # Obtener los datos del alumno
        grupo = self.tabla_consulta.item(fila_seleccionada, 0).text()
        nombre = self.tabla_consulta.item(fila_seleccionada, 1).text()
        matricula = self.tabla_consulta.item(fila_seleccionada, 2).text()

    # Verificar si el grupo coincide con la clase activa
        grupo_clase_activa = self.combo_grupos.currentText()
        if grupo != grupo_clase_activa:
            QMessageBox.warning(self, "Error", f"El alumno pertenece al grupo {grupo}, no al grupo activo {grupo_clase_activa}.")
            return

    # Añadir el alumno a la tabla de asistencia
        row_position = self.tabla_asistencia.rowCount()
        self.tabla_asistencia.insertRow(row_position)
        self.tabla_asistencia.setItem(row_position, 0, QTableWidgetItem(str(row_position + 1)))
        self.tabla_asistencia.setItem(row_position, 1, QTableWidgetItem(nombre))
        self.tabla_asistencia.setItem(row_position, 2, QTableWidgetItem(matricula))
        self.tabla_asistencia.setItem(row_position, 3, QTableWidgetItem("--:--:--"))
        estado_item = QTableWidgetItem("No registrado")
        estado_item.setForeground(QColor(136, 192, 208))
        self.tabla_asistencia.setItem(row_position, 4, estado_item)

        QMessageBox.information(self, "Éxito", f"Alumno {nombre} añadido a la clase activa.")
        dialog.close()

    # ===================== INICIO DE CURSO =====================
    def show_inicio_curso_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Inicio de Curso")
        dialog.setModal(True)
        dialog_layout = QVBoxLayout(dialog)

        form = QFormLayout()
        self.combo_materias_curso = QComboBox()
        self.combo_materias_curso.addItems(self.materias.keys())
        form.addRow("Materia:", self.combo_materias_curso)

        self.combo_grupos_curso = QComboBox()
        form.addRow("Grupo:", self.combo_grupos_curso)
        self.combo_materias_curso.currentTextChanged.connect(self.actualizar_grupos_curso)

        self.actualizar_grupos_curso()

        dialog_layout.addLayout(form)
        dialog_layout.addWidget(QLabel("Seleccione la materia y grupo para iniciar la clase"))

        btn_iniciar = QPushButton("Iniciar Clase")
        btn_iniciar.clicked.connect(lambda: self.iniciar_clase_desde_dialogo(dialog))
        dialog_layout.addWidget(btn_iniciar)

        dialog.exec()

    def actualizar_grupos_curso(self):
        """Actualiza los grupos disponibles en el diálogo de inicio de curso"""
        materia = self.combo_materias_curso.currentText()
        self.combo_grupos_curso.clear()
        self.combo_grupos_curso.addItems(self.materias.get(materia, []))


    #=====================================METODO DE EXPORTACION===========================================================

    def show_exportar_dialog(self):
    # 1. Seleccionar el PDF
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter("Archivos PDF (*.pdf)")
        if file_dialog.exec():
            pdf_path = file_dialog.selectedFiles()[0]
        
        # 2. Extraer los datos
            datos = extraer_datos_pdf(pdf_path)
            if not datos:
                QMessageBox.warning(self, "Error", "No se pudieron extraer datos del PDF.")
                return
        
            materia = datos.get('materia')
            grupo = datos.get('grupo')
            profesor = datos.get('profesor', '')
            horario = datos.get('horario', '')
            alumnos = datos.get('alumnos', [])
        
        # 3. Mostrar confirmación
            dialog = QDialog(self)
            dialog.setWindowTitle("Confirmar importación")
            layout = QVBoxLayout(dialog)
            layout.addWidget(QLabel(f"<b>Materia:</b> {materia}"))
            layout.addWidget(QLabel(f"<b>Grupo:</b> {grupo}"))
            layout.addWidget(QLabel(f"<b>Profesor:</b> {profesor}"))
            layout.addWidget(QLabel(f"<b>Horario:</b> {horario}"))
            layout.addWidget(QLabel(f"<b>Alumnos encontrados:</b> {len(alumnos)}"))
            for alumno in alumnos[:5]:
                layout.addWidget(QLabel(f"- {alumno['nombre']} ({alumno['numero_control']})"))
            if len(alumnos) > 5:
                layout.addWidget(QLabel("..."))
        
            btn_confirmar = QPushButton("Registrar en la base de datos")
            def confirmar():
                exito = insertar_datos_pdf(datos)
                if exito:
                    QMessageBox.information(self, "Éxito", "Datos registrados correctamente.")
                else:
                    QMessageBox.warning(self, "Error", "Ocurrió un error al registrar los datos.")
                dialog.accept()
            btn_confirmar.clicked.connect(confirmar)
            layout.addWidget(btn_confirmar)
            dialog.setLayout(layout)
            dialog.exec()
            
    def mostrar_ventana_confirmacion(self, materia, grupo, alumnos):
        """Muestra una ventana de confirmación después de importar datos."""
        dialog = QDialog(self)
        dialog.setWindowTitle("Importación exitosa")
        layout = QVBoxLayout(dialog)

    # Mensaje de éxito
        layout.addWidget(QLabel(f"<b>¡Clase y grupo agregados correctamente!</b>"))
        layout.addWidget(QLabel(f"<b>Materia:</b> {materia}"))
        layout.addWidget(QLabel(f"<b>Grupo:</b> {grupo}"))
        layout.addWidget(QLabel(f"<b>Alumnos registrados:</b>"))

    # Lista de alumnos
        lista_alumnos = QListWidget()
        for alumno in alumnos:
            lista_alumnos.addItem(f"{alumno['nombre']} ({alumno['numero_control']})")
        layout.addWidget(lista_alumnos)

    # Botón de cierre
        btn_cerrar = QPushButton("Cerrar")
        btn_cerrar.clicked.connect(dialog.accept)
        layout.addWidget(btn_cerrar)

        dialog.setLayout(layout)
        dialog.exec()
            
    def mostrar_ventana_confirmacion(self, materia, grupo, alumnos):
        dialog = QDialog(self)
        dialog.setWindowTitle("Importación exitosa")
        layout = QVBoxLayout(dialog)

    # Mensaje de éxito
        layout.addWidget(QLabel(f"<b>¡Clase y grupo agregados correctamente!</b>"))
        layout.addWidget(QLabel(f"<b>Materia:</b> {materia}"))
        layout.addWidget(QLabel(f"<b>Grupo:</b> {grupo}"))
        layout.addWidget(QLabel(f"<b>Alumnos registrados:</b>"))

    # Lista de alumnos
        lista_alumnos = QListWidget()
        for alumno in alumnos:
            lista_alumnos.addItem(f"{alumno['nombre']} ({alumno['numero_control']})")
        layout.addWidget(lista_alumnos)

    # Botón de cierre
        btn_cerrar = QPushButton("Cerrar")
        btn_cerrar.clicked.connect(dialog.accept)
        layout.addWidget(btn_cerrar)

        dialog.setLayout(layout)
        dialog.exec()


    # ===================== MÉTODOS DE SIMULACIÓN =====================
    def simular_llegadas_alumnos(self, grupo):
        """Inicia la simulación de llegadas de alumnos"""
        self.simulacion_timer.start(3000)  # Simular cada 3 segundos

    def registrar_llegada_simulada(self):
        """Simula la llegada aleatoria de alumnos"""
        if not self.clase_activa:
            self.simulacion_timer.stop()
            return

        grupo = self.combo_grupos.currentText()
        alumnos_grupo = self.alumnos.get(grupo, [])

    # Seleccionar un alumno aleatorio que no haya llegado aún
        alumnos_no_registrados = [
            (i, alumno) for i, alumno in enumerate(alumnos_grupo)
            if self.tabla_asistencia.item(i, 3).text() == "--:--:--"
        ]

        if alumnos_no_registrados:
            idx, alumno = choice(alumnos_no_registrados)
            hora_llegada = datetime.now().strftime("%H:%M:%S")

            self.tabla_asistencia.setItem(idx, 3, QTableWidgetItem(hora_llegada))

            estado_item = QTableWidgetItem("Registrado")
            estado_item.setForeground(QColor(163, 190, 140))  # Verde
            self.tabla_asistencia.setItem(idx, 4, estado_item)
        else:
        # Detener el temporizador si todos los alumnos ya llegaron
            self.simulacion_timer.stop()
            
    def registrar_llegada_manual(self):
        """Permite registrar manualmente la llegada de un alumno ingresando su número de control."""
        dialog = QDialog(self)
        dialog.setWindowTitle("Registro Manual de Asistencia")
        dialog.setModal(True)
        dialog_layout = QVBoxLayout(dialog)

    # Campo para ingresar el número de control
        form = QFormLayout()
        input_numero_control = QLineEdit()
        form.addRow("Número de Control:", input_numero_control)
        dialog_layout.addLayout(form)

    # Botón para registrar
        btn_registrar = QPushButton("Registrar")
        btn_registrar.clicked.connect(lambda: self._registrar_manual(dialog, input_numero_control.text().strip()))
        dialog_layout.addWidget(btn_registrar)

        dialog.exec()

    def _registrar_manual(self, dialog, numero_control):
        grupo = self.combo_grupos.currentText()
        for idx, alumno in enumerate(self.alumnos.get(grupo, [])):
            if alumno.get('numero_control') == numero_control:
                hora_llegada = datetime.now().strftime("%H:%M:%S")
                self.tabla_asistencia.setItem(idx, 3, QTableWidgetItem(hora_llegada))
            # ... (resto del código)

            estado_item = QTableWidgetItem("Registrado")
            estado_item.setForeground(QColor(163, 190, 140))  # Verde
            self.tabla_asistencia.setItem(idx, 4, estado_item)

            QMessageBox.information(self, "Éxito", f"Alumno {alumno['nombre']} registrado correctamente.")
            dialog.close()
            return

        QMessageBox.warning(self, "Error", "Número de control no encontrado.")

    def finalizar_clase(self):
        """Finaliza la clase actual y guarda en historial"""
        if not self.clase_activa:
            QMessageBox.warning(self, "Error", "No hay una clase activa para finalizar.")
            return

        materia = self.lista_materias.currentItem().text()
        grupo = self.combo_grupos.currentText()

    # Calcular asistencia
        total = self.tabla_asistencia.rowCount()
        presentes = sum(1 for row in range(total)
                        if self.tabla_asistencia.item(row, 4).text() != "No registrado")

    # Guardar en historial
        self.historial_clases.append({
            "fecha": datetime.now().strftime("%d/%m/%Y"),
            "materia": f"{materia} - {grupo}",
            "aula": self.aulas.get(f"{materia} - {grupo}", "Sin aula"),
            "duracion": str(datetime.now() - datetime.combine(datetime.today(), self.hora_inicio_clase)).split('.')[0],
            "asistencia": f"{presentes}/{total}",
        })

        self.clase_activa = False
        self.simulacion_timer.stop()
        self.barra_clase_container.hide()
        self.timer.stop()
        self.simulacion_timer.stop()

    # Mostrar opciones al finalizar la clase
        dialog = QDialog(self)
        dialog.setWindowTitle("Clase Finalizada")
        dialog.setModal(True)
        dialog_layout = QVBoxLayout(dialog)

    # Mensaje de resumen
        lbl_resumen = QLabel(f"La clase de {materia} - {grupo} ha finalizado.\n"
                            f"Duración: {str(datetime.now() - datetime.combine(datetime.today(), self.hora_inicio_clase)).split('.')[0]}\n"
                            f"Asistencia: {presentes}/{total}")
        lbl_resumen.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_resumen.setStyleSheet("font-size: 16px; font-weight: bold;")
        dialog_layout.addWidget(lbl_resumen)

    # Botón para cerrar
        btn_cerrar = QPushButton("Cerrar")
        btn_cerrar.clicked.connect(dialog.close)
        dialog_layout.addWidget(btn_cerrar)

        dialog.setLayout(dialog_layout)
        dialog.exec()

    

    # ===================== MÉTODOS COMPLEMENTARIOS =====================
    def actualizar_reloj(self):
        ahora = QDateTime.currentDateTime()
        self.lbl_reloj.setText(ahora.toString("HH:mm:ss"))

        if self.clase_activa:
            if ahora.time().second() == 0:
                self.actualizar_estados_asistencia()

    def actualizar_estados_asistencia(self):
        """Actualiza los colores y estados de la tabla de asistencia"""
        for row in range(self.tabla_asistencia.rowCount()):
            hora_item = self.tabla_asistencia.item(row, 3)
            estado_item = self.tabla_asistencia.item(row, 4)

            if hora_item.text() != "--:--:--":
                hora_llegada = datetime.strptime(hora_item.text(), "%H:%M:%S").time()
                inicio_clase = self.hora_inicio_clase

                diferencia = datetime.combine(datetime.today(), hora_llegada) - datetime.combine(datetime.today(), inicio_clase)

                if diferencia <= timedelta(minutes=20):
                    estado = "🟢 A tiempo"
                    color = QColor(163, 190, 140)  # Verde
                elif diferencia <= timedelta(minutes=60):
                    estado = "🟡 Retardo moderado"
                    color = QColor(235, 203, 139)  # Amarillo
                else:
                    estado = "🔴 Retardo grave"
                    color = QColor(191, 97, 106)  # Rojo

                estado_item.setText(estado)
                estado_item.setForeground(color)

    # ===================== MÉTODOS DEL HISTORIAL =====================
    def show_historial_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Historial Completo")
        dialog.setMinimumSize(800, 500)
        
        layout = QVBoxLayout()
        
        # Tabla de historial
        table = QTableWidget()
        table.setColumnCount(5)
        table.setHorizontalHeaderLabels(["Fecha", "Clase", "Aula", "Duración", "Asistencia"])
        
        for idx, clase in enumerate(self.historial_clases):
            table.insertRow(idx)
            table.setItem(idx, 0, QTableWidgetItem(clase["fecha"]))
            table.setItem(idx, 1, QTableWidgetItem(clase["materia"]))
            table.setItem(idx, 2, QTableWidgetItem(clase.get("aula", "Sin aula")))
            table.setItem(idx, 3, QTableWidgetItem(clase["duracion"]))
            table.setItem(idx, 4, QTableWidgetItem(clase["asistencia"]))
        
        table.resizeColumnsToContents()
        layout.addWidget(table)
        
        dialog.setLayout(layout)
        dialog.exec()

    # ===================== PROGRAMAR CLASES =====================
    def show_programar_clases_dialog(self):
        """Muestra el formulario para programar clases."""
        dialog = QDialog(self)
        dialog.setWindowTitle("Programar Clases")
        dialog.setModal(True)
        dialog.setMinimumSize(400, 500)
        layout = QVBoxLayout(dialog)

        # Seleccionar clase
        form = QFormLayout()
        combo_clase = QComboBox()
        try:
            with open("clases.json", "r") as file:
                clases = json.load(file)
                for clase in clases:
                    combo_clase.addItem(f"{clase['materia']} - {clase['grupo']}")
        except FileNotFoundError:
            QMessageBox.warning(self, "Error", "No hay clases creadas.")
            dialog.close()
            return
        form.addRow("Clase:", combo_clase)

        # Configurar periodo
        input_fecha_inicio = QLineEdit()
        input_fecha_inicio.setPlaceholderText("Ejemplo: 2025-01-31")
        form.addRow("Fecha de Inicio:", input_fecha_inicio)

        input_fecha_fin = QLineEdit()
        input_fecha_fin.setPlaceholderText("Ejemplo: 2025-06-17")
        form.addRow("Fecha de Fin:", input_fecha_fin)
        
        layout.addLayout(form)
        
    # Selección múltiple de días
        dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        layout.addWidget(QLabel("Selecciona los días que se imparte la clase:"))
        checkboxes = []
        dias_layout = QHBoxLayout()
        for dia in dias:
            cb = QCheckBox(dia)
            dias_layout.addWidget(cb)
            checkboxes.append(cb)
        layout.addLayout(dias_layout)

    # Selección de hora de inicio y fin
        horas_layout = QHBoxLayout()
        
        layout.addWidget(QLabel("Selecciona la hora de inicio y fin de la clase:"))
        label_inicio = QLabel("Inicio:")
        time_inicio = QTimeEdit()
        time_inicio.setTime(QTime(8, 0))
        label_fin = QLabel("Fin:")
        time_fin = QTimeEdit()
        time_fin.setTime(QTime(10, 0))
        horas_layout.addWidget(label_inicio)
        horas_layout.addWidget(time_inicio)
        horas_layout.addWidget(label_fin)
        horas_layout.addWidget(time_fin)
        layout.addLayout(horas_layout)

    # Botón para guardar
        btn_guardar = QPushButton("Guardar")
        def guardar():
            dias_seleccionados = [cb.text() for cb in checkboxes if cb.isChecked()]
            hora_inicio = time_inicio.time().toString("HH:mm")
            hora_fin = time_fin.time().toString("HH:mm")
            self.programar_clase(
                combo_clase.currentText(),
                input_fecha_inicio.text(),
                input_fecha_fin.text(),
                dias_seleccionados,
                hora_inicio,
                hora_fin,
                dialog
            )
            
        
        btn_guardar.clicked.connect(guardar)
        layout.addWidget(btn_guardar)

        dialog.setLayout(layout)
        dialog.exec()
        
        

    def programar_clase(self, clase, fecha_inicio, fecha_fin, dias, hora_inicio, hora_fin, dialog):
        if not clase or not fecha_inicio or not fecha_fin:
            QMessageBox.warning(self, "Error", "Todos los campos son obligatorios.")
            return
        if not dias:
            QMessageBox.warning(self, "Error", "Selecciona al menos un día.")
            return
        if hora_inicio >= hora_fin:
            QMessageBox.warning(self, "Error", "La hora de inicio debe ser antes que la de fin.")
            return

        try:
            with open("programaciones.json", "r") as file:
                programaciones = json.load(file)
        except FileNotFoundError:
            programaciones = []

        programaciones.append({
            "clase": clase,
            "fecha_inicio": fecha_inicio,
            "fecha_fin": fecha_fin,
            "dias": dias,
            "hora_inicio": hora_inicio,
            "hora_fin": hora_fin
        })

        with open("programaciones.json", "w") as file:
            json.dump(programaciones, file, indent=4, ensure_ascii=False)

        QMessageBox.information(self, "Éxito", "Clase programada correctamente.")
        dialog.close()
        self.refrescar_recordatorios()


    def show_blur_overlay(self):
        """Muestra un efecto de desenfoque falso en el fondo."""
        self.blur_overlay = QWidget(self)
        self.blur_overlay.setStyleSheet("""
        background-color: rgba(0, 0, 0, 120);  /* Fondo negro semitransparente */
        """)
        self.blur_overlay.setGeometry(self.rect())
        self.blur_overlay.show()
        
    def cargar_programaciones(self):
        try:
            with open("programaciones.json", "r", encoding="latin1") as file:
                data = json.load(file)
                print("Programaciones cargadas:", data)  # <-- Agrega esto
                return data
        except Exception as e:
            print("Error al cargar programaciones:", e)
            return []
    


    def refrescar_recordatorios(self):
        # Limpia el layout
        for i in reversed(range(self.reminder_layout.count())):
            widget = self.reminder_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        # Carga las programaciones
        clases_programadas = self.cargar_programaciones()
        if clases_programadas:
            for clase in clases_programadas:
                nombre = clase.get("clase", "Sin nombre")
                fecha_inicio = clase.get("fecha_inicio", "¿?")
                fecha_fin = clase.get("fecha_fin", "¿?")
                dias = ", ".join(clase.get("dias", []))
                hora_inicio = clase.get("hora_inicio", "")
                hora_fin = clase.get("hora_fin", "")
                texto = (f"📚 {nombre}\n"
                         f"🗓️ {fecha_inicio} a {fecha_fin}\n"
                         f"🕒 {dias} {hora_inicio}-{hora_fin}")

                # Widget horizontal para texto + botón
                recordatorio_widget = QWidget()
                recordatorio_layout = QHBoxLayout()
                recordatorio_layout.setContentsMargins(0, 0, 0, 0)
                recordatorio_widget.setLayout(recordatorio_layout)

                lbl = QLabel(texto)
                lbl.setStyleSheet("font-size: 14px; font-weight: normal; padding: 3px 0;")
                btn_iniciar = QPushButton("Iniciar Clase")
                btn_iniciar.setStyleSheet("padding: 2px 8px;")

                # Conecta el botón para iniciar la clase, pasando el diccionario completo
                btn_iniciar.clicked.connect(lambda _, c=clase: self.iniciar_clase_desde_recordatorio(c))

                recordatorio_layout.addWidget(lbl)
                recordatorio_layout.addWidget(btn_iniciar)

                self.reminder_layout.addWidget(recordatorio_widget)
        else:
            self.reminder_layout.addWidget(QLabel("No hay clases programadas."))
        
    def iniciar_clase_desde_recordatorio(self, clase):
        """Inicia una clase desde los recordatorios"""
        materia_grupo = clase.get('clase', '')
        if " - " in materia_grupo:
            materia, grupo = materia_grupo.split(" - ", 1)
        else:
            materia = materia_grupo
            grupo = ""

    # Verificar que la materia y el grupo sean válidos
        if not materia or not grupo:
            QMessageBox.warning(self, "Error", "Datos de clase incompletos en el recordatorio.")
            return

    # Configurar la clase activa
        self.clase_activa = True
        self.hora_inicio_clase = datetime.now().time()

    # Llamar al método iniciar_clase con los parámetros correctos
        self.iniciar_clase(materia, grupo) 


    def hide_blur_overlay(self):
        """Oculta el efecto de desenfoque falso."""
        if hasattr(self, 'blur_overlay'):
            self.blur_overlay.hide()
            self.blur_overlay.deleteLater()

    def show_agregar_nota_dialog(self):
        """Muestra un diálogo para agregar una nueva nota."""
        dialog = QDialog(self)
        dialog.setWindowTitle("Agregar Nota")
        dialog.setModal(True)
        dialog.setMinimumSize(400, 300)
        layout = QVBoxLayout(dialog)

        # Campo para ingresar el título de la nota
        input_titulo = QLineEdit()
        input_titulo.setPlaceholderText("Título de la nota")
        layout.addWidget(QLabel("Título:"))
        layout.addWidget(input_titulo)

        # Campo para ingresar el contenido de la nota
        input_contenido = QLineEdit()
        input_contenido.setPlaceholderText("Contenido de la nota")
        layout.addWidget(QLabel("Contenido:"))
        layout.addWidget(input_contenido)

        # Botón para guardar la nota
        btn_guardar = QPushButton("Guardar")
        btn_guardar.setObjectName("success")
        btn_guardar.clicked.connect(lambda: self.agregar_nota(input_titulo.text(), input_contenido.text(), dialog))
        layout.addWidget(btn_guardar)

        dialog.setLayout(layout)
        dialog.exec()
        
    def agregar_nota(self, titulo, contenido, dialog):
        """Agrega una nueva nota a la lista de notas."""
        if not titulo or not contenido:
            QMessageBox.warning(self, "Error", "El título y el contenido de la nota son obligatorios.")
            return

    # Agregar la nota a la lista de notas
        self.lista_notas.addItem(f"{titulo}: {contenido}")

    # Guardar la nota en una estructura de datos (opcional)
        if not hasattr(self, 'notas'):
            self.notas = []
        self.notas.append({"titulo": titulo, "contenido": contenido})

        QMessageBox.information(self, "Éxito", "Nota agregada correctamente.")
        dialog.close()
        
    def guardar_notas(self):
        """Guarda las notas en un archivo JSON."""
        try:
            with open("notas.json", "w") as file:
                json.dump(self.notas, file, indent=4)
        except Exception as e:
            print(f"Error al guardar notas: {e}")
            
    def cargar_notas(self):
        """Carga las notas desde un archivo JSON."""
        try:
            with open("notas.json", "r") as file:
                self.notas = json.load(file)
                for nota in self.notas:
                    self.lista_notas.addItem(f"{nota['titulo']}: {nota['contenido']}")
        except FileNotFoundError:
            self.notas = []
        except Exception as e:
            print(f"Error al cargar notas: {e}")


if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    ventana = Dashboard("admin")
    ventana.setWindowTitle("Sistema de Asistencia - Dashboard")
    ventana.resize(1200, 800)
    ventana.show()
    sys.exit(app.exec())
