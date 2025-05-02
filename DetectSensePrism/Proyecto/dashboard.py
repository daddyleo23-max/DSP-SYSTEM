from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton,
    QHBoxLayout, QListWidget, QComboBox, QMessageBox,
    QLineEdit, QDialog, QSpinBox, QTableWidget, QTableWidgetItem,
    QTabWidget, QFormLayout, QHeaderView, QGroupBox, QFrame, QStackedWidget
)
from PyQt6.QtCore import Qt, QTimer, QDateTime
from PyQt6.QtGui import QColor
from datetime import datetime, timedelta
from random import randint, choice

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
        btn_alumnos = QPushButton("👥 Registrar Alumnos")
        btn_asistencias = QPushButton("🕒 Consultar Asistencias")
        btn_notas = QPushButton("📝 Notas de Curso")
        btn_historial = QPushButton("⏳ Historial")
        btn_exportar = QPushButton("📄 Exportar Archivo")

        btn_clases.clicked.connect(self.show_clases_dialog)
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
        for btn in [btn_clases, btn_alumnos, btn_asistencias, btn_notas, btn_historial, btn_exportar]:
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
        reminder_box = QGroupBox("📌 Recordatorios")
        reminder_layout = QVBoxLayout()
        
        # Ejemplo dinámico (usando tus datos)
        lbl_aula = QLabel(f"📍 Aula asignada: {self.aulas.get('Matemáticas - Grupo D', 'No asignada')}")
        lbl_prox_clase = QLabel("⏰ Próxima clase: Matemáticas - Grupo D (18:45)")
        lbl_urgente = QLabel("⚠️ Reunión de profesores mañana a las 10:00 AM")
        
        for widget in [lbl_aula, lbl_prox_clase, lbl_urgente]:
            widget.setStyleSheet("font-size: 14px; font-weight: normal; padding: 3px 0;")
            reminder_layout.addWidget(widget)
        
        reminder_box.setLayout(reminder_layout)
        right_layout.addWidget(reminder_box)

        # --------------------- SECCIÓN DE HISTORIAL ---------------------
        history_box = QGroupBox("📚 Clases Recientes")
        history_layout = QVBoxLayout()
        
        if self.historial_clases:
            for clase in self.historial_clases[-3:]:  # Mostrar 3 más recientes
                card = QFrame()
                card.setStyleSheet("background-color: #3B4252; border-radius: 8px; padding: 12px;")
                card_layout = QVBoxLayout(card)
                
                card_layout.addWidget(QLabel(f"📅 {clase['fecha']} - {clase['materia']}"))
                card_layout.addWidget(QLabel(f"⏱️ Duración: {clase['duracion']}"))
                card_layout.addWidget(QLabel(f"🟢 Asistencia: {clase['asistencia']}"))
                
                history_layout.addWidget(card)
        else:
            history_layout.addWidget(QLabel("No hay clases registradas aún"))
        
        history_box.setLayout(history_layout)
        right_layout.addWidget(history_box)

        main_layout.addWidget(right_content)

        # --- Ordenamiento ---
        right_layout.addWidget(self.content_stack, stretch=2)  # Área dinámica (60%)
        right_layout.addWidget(reminder_box, stretch=1)        # Recordatorios (20%)
        right_layout.addWidget(history_box, stretch=1)         # Historial (20%)

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
        
        items = self.lista_materias.findItems(materia, Qt.MatchFlag.MatchExactly)
        if items:
            self.lista_materias.setCurrentItem(items[0])
            self.combo_grupos.setCurrentText(grupo)
            self.iniciar_clase()
            dialog.close()  # Cerramos explícitamente el diálogo
        else:
            QMessageBox.warning(self, "Error", "No se pudo iniciar la clase")

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

        self.btn_iniciar = QPushButton("INICIAR CLASE")
        self.btn_iniciar.setObjectName("success")
        self.btn_iniciar.setFixedHeight(50)
        self.btn_iniciar.setEnabled(False)
        self.btn_iniciar.clicked.connect(self.iniciar_clase)
        layout.addWidget(self.btn_iniciar, alignment=Qt.AlignmentFlag.AlignCenter)

        # Botones de gestión
        btn_container = QWidget()
        btn_layout = QHBoxLayout(btn_container)
        btn_layout.setSpacing(15)
        btn_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        btn_add_materia = QPushButton("Añadir Materia")
        btn_add_materia.clicked.connect(self.show_add_materia_dialog)
        btn_layout.addWidget(btn_add_materia)

        btn_create_grupo = QPushButton("Crear Grupo")
        btn_create_grupo.clicked.connect(self.show_create_grupo_dialog)
        btn_layout.addWidget(btn_create_grupo)

        layout.addWidget(btn_container)
        parent_layout.addWidget(container)

    def actualizar_grupos(self, current_item):
        """Actualiza los grupos disponibles cuando se selecciona una materia"""
        if current_item:
            materia = current_item.text()
            self.combo_grupos.clear()
            self.combo_grupos.addItems(self.materias.get(materia, []))
            self.btn_iniciar.setEnabled(self.combo_grupos.count() > 0)

    def iniciar_clase(self):
        """Método principal para iniciar una clase"""
        materia = self.lista_materias.currentItem().text()
        grupo = self.combo_grupos.currentText()
        
        self.clase_activa = True
        self.hora_inicio_clase = datetime.now().time()
        self.barra_clase_container.show()
        self.lbl_detalle_clase.setText(f"{materia} - {grupo} | Iniciada: {self.hora_inicio_clase.strftime('%H:%M')}")
        
        # Configurar tabla de asistencia
        alumnos = self.alumnos.get(grupo, [])
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
        
        btn_finalizar = QPushButton("Finalizar Clase")
        btn_finalizar.setObjectName("danger")
        btn_finalizar.clicked.connect(self.finalizar_clase)
        self.barra_clase_layout.addWidget(btn_finalizar, alignment=Qt.AlignmentFlag.AlignCenter)

    # ===================== DIÁLOGOS DE GESTIÓN =====================
    def show_add_materia_dialog(self):
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
        dialog.exec()

    def add_materia(self, dialog):
        nombre = self.input_materia.text().strip()
        if nombre:
            self.materias[nombre] = []
            self.lista_materias.addItem(nombre)
            dialog.close()
            QMessageBox.information(self, "Éxito", "Materia añadida correctamente")
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
        materia = self.combo_materias_grupo.currentText()
        nombre_grupo = self.input_grupo.text().strip()

        if nombre_grupo:
            if nombre_grupo not in self.materias[materia]:
                self.materias[materia].append(nombre_grupo)
                self.actualizar_grupos(self.lista_materias.currentItem())
                dialog.close()
                QMessageBox.information(self, "Éxito", "Grupo creado correctamente")
            else:
                QMessageBox.warning(self, "Error", "El grupo ya existe")
        else:
            QMessageBox.warning(self, "Error", "El nombre no puede estar vacío")

    # ===================== REGISTRO DE ALUMNOS =====================
    def show_registro_alumnos_dialog(self):
        """Muestra el formulario para registrar alumnos."""
        # Limpiar contenido anterior
        self.clear_content_area()

        # Crear widget de registro
        registro_widget = QWidget()
        layout = QVBoxLayout(registro_widget)

        # --- Formulario de registro ---
        form = QFormLayout()

        # Selección de grupo
        self.combo_grupos_registro = QComboBox()
        self.combo_grupos_registro.addItems(sum(self.materias.values(), []))
        form.addRow("Grupo:", self.combo_grupos_registro)

        # Nombre del alumno
        self.input_nombre = QLineEdit()
        form.addRow("Nombre(s):", self.input_nombre)

        # Apellidos del alumno
        self.input_apellidos = QLineEdit()
        form.addRow("Apellidos:", self.input_apellidos)

        # Selección de carrera
        self.combo_carrera = QComboBox()
        self.combo_carrera.addItems([
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
        form.addRow("Carrera:", self.combo_carrera)

        # Número de control (generado automáticamente)
        self.lbl_numero_control = QLabel("Se generará automáticamente")
        form.addRow("Número de Control:", self.lbl_numero_control)

        # Registro de huella dactilar
        self.btn_registrar_huella = QPushButton("Registrar Huella Dactilar")
        self.btn_registrar_huella.clicked.connect(self.registrar_huella_dactilar)
        form.addRow("Huella Dactilar:", self.btn_registrar_huella)

        # Botón para guardar el alumno
        btn_guardar = QPushButton("Registrar Alumno")
        btn_guardar.clicked.connect(self.guardar_alumno)
        layout.addLayout(form)
        layout.addWidget(btn_guardar)

        # Mostrar en el área de contenido
        self.content_stack.addWidget(registro_widget)
        self.content_stack.setCurrentWidget(registro_widget)

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

    def guardar_alumno(self):
        """Guarda los datos del alumno con número de control único."""
        try:
            grupo = self.combo_grupos_registro.currentText()
            nombre = self.input_nombre.text().strip()
            apellidos = self.input_apellidos.text().strip()
            carrera = self.combo_carrera.currentText()

            # Validar campos obligatorios
            if not grupo:
                QMessageBox.warning(self, "Error", "Seleccione un grupo.")
                return
            if not nombre or not apellidos:
                QMessageBox.warning(self, "Error", "Nombre y apellidos son obligatorios.")
                return

        # Generar número de control único (usando tu método)
            numero_control = self.generar_numero_control()

        # Inicializar lista de alumnos si el grupo no existe
            if grupo not in self.alumnos:
                self.alumnos[grupo] = []

        # Guardar alumno con número de control y matrícula (opcional)
            self.alumnos[grupo].append({
                'nombre': f"{nombre} {apellidos}",
                'matricula': numero_control,  # Usamos el número de control como matrícula
                'numero_control': numero_control,  # Campo adicional
                'carrera': carrera
            })

            QMessageBox.information(
                self,
                "Éxito",
                f"Alumno registrado.\nNúmero de Control: {numero_control}"
            )
            self.clear_content_area()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al registrar: {str(e)}")

    def clear_content_area(self):
        # Eliminar todos los widgets excepto el vacío inicial
        while self.content_stack.count() > 1:
            widget = self.content_stack.widget(1)
            self.content_stack.removeWidget(widget)
            widget.deleteLater()
        
        self.content_stack.setCurrentWidget(self.empty_content)

    # ===================== CONSULTA DE ALUMNOS =====================
    def show_consulta_alumnos_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Consulta de Alumnos")
        dialog.setModal(True)
        dialog.setMinimumSize(800, 500)
        dialog_layout = QVBoxLayout(dialog)

        self.tabla_consulta = QTableWidget()
        self.tabla_consulta.setColumnCount(3)
        self.tabla_consulta.setHorizontalHeaderLabels(["Grupo", "Nombre", "Matrícula"])
        self.tabla_consulta.verticalHeader().setVisible(False)
        self.tabla_consulta.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        self.actualizar_tabla_todos_alumnos()

        dialog_layout.addWidget(self.tabla_consulta)
        dialog.exec()

    def actualizar_tabla_todos_alumnos(self):
        self.tabla_consulta.setRowCount(0)
        row = 0
        for grupo, alumnos in self.alumnos.items():
            for alumno in alumnos:
                self.tabla_consulta.insertRow(row)
                self.tabla_consulta.setItem(row, 0, QTableWidgetItem(grupo))
                self.tabla_consulta.setItem(row, 1, QTableWidgetItem(alumno['nombre']))
                self.tabla_consulta.setItem(row, 2, QTableWidgetItem(alumno['matricula']))
                row += 1

        self.tabla_consulta.resizeColumnsToContents()

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

    def iniciar_clase_desde_dialogo(self, dialog):
        materia = self.combo_materias_curso.currentText()
        grupo = self.combo_grupos_curso.currentText()
    
        items = self.lista_materias.findItems(materia, Qt.MatchFlag.MatchExactly)
        if items:
            self.lista_materias.setCurrentItem(items[0])
            self.combo_grupos.setCurrentText(grupo)
            self.iniciar_clase(dialog)  # Pasamos el diálogo como parámetro
        else:
            QMessageBox.warning(self, "Error", "No se pudo iniciar la clase")

    def iniciar_clase(self):
        """Método principal para iniciar una clase"""
        materia = self.lista_materias.currentItem().text()
        grupo = self.combo_grupos.currentText()
    
        self.clase_activa = True
        self.hora_inicio_clase = datetime.now().time()
        self.barra_clase_container.show()
        self.lbl_detalle_clase.setText(f"{materia} - {grupo} | Iniciada: {self.hora_inicio_clase.strftime('%H:%M')}")

        # Configurar tabla de asistencia
        alumnos = self.alumnos.get(grupo, [])
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

        # Eliminar botones existentes para evitar duplicados
        for i in reversed(range(self.barra_clase_layout.count())):
            widget = self.barra_clase_layout.itemAt(i).widget()
            if isinstance(widget, QPushButton):  # Solo eliminar botones
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

    #=====================================METODO DE EXPORTACION===========================================================
    def show_exportar_dialog(self):
        """Muestra el diálogo para exportar datos a PDF."""
        dialog = QDialog(self)
        dialog.setWindowTitle("Exportar a PDF")
        dialog.setModal(True)
        dialog_layout = QVBoxLayout(dialog)
    
    # Formulario para seleccionar qué exportar
        form = QFormLayout()
    
    # Combo para seleccionar el tipo de reporte
        self.combo_tipo_reporte = QComboBox()
        self.combo_tipo_reporte.addItems([
            "Lista de alumnos por grupo",
            "Asistencias por clase",
            "Historial completo de clases"
        ])
        form.addRow("Tipo de reporte:", self.combo_tipo_reporte)
    
    # Combo para filtrar por materia/grupo si es necesario
        self.combo_filtro = QComboBox()
        self.combo_filtro.addItems(sum([[f"{materia} - {grupo}" 
                                    for grupo in grupos] 
                                    for materia, grupos in self.materias.items()], []))
        form.addRow("Filtrar por:", self.combo_filtro)
    
        dialog_layout.addLayout(form)
    
    # Botones de acción
        btn_container = QWidget()
        btn_layout = QHBoxLayout(btn_container)
    
        btn_exportar_pdf = QPushButton("Exportar PDF")
        btn_exportar_pdf.setObjectName("success")
        btn_exportar_pdf.clicked.connect(lambda: self.exportar_a_pdf(dialog))
    
        btn_cancelar = QPushButton("Cancelar")
        btn_cancelar.clicked.connect(dialog.close)
    
        btn_layout.addWidget(btn_exportar_pdf)
        btn_layout.addWidget(btn_cancelar)
    
        dialog_layout.addWidget(btn_container)
        dialog.exec()

    def exportar_a_pdf(self, dialog):
        """Exporta los datos seleccionados a un archivo PDF."""
        tipo_reporte = self.combo_tipo_reporte.currentText()
        filtro = self.combo_filtro.currentText()
    
        QMessageBox.information(
            self, 
            "Exportación pendiente", 
            f"La función para exportar {tipo_reporte} a PDF será implementada próximamente.\n\n"
            f"Filtro seleccionado: {filtro}"
        )
    
    # Aquí irá el código que tu compañero desarrollará para la exportación a PDF
    
        dialog.close()

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

    # ===================== MÉTODOS ORIGINALES (COPIADOS SIN MODIFICAR) =====================
    # [Aquí van TODOS tus métodos originales exactamente como los tenías]
    # show_clases_dialog, show_registro_alumnos_dialog, show_consulta_alumnos_dialog,
    # iniciar_clase, finalizar_clase, etc. (todos los que estaban en tu código original)
    
    # Solo necesitamos modificar ligeramente finalizar_clase para guardar en el historial:
    def finalizar_clase(self):
        """Finaliza la clase actual y guarda en historial"""
        materia = self.lista_materias.currentItem().text()
        grupo = self.combo_grupos.currentText()
        
        # Calcular asistencia (ejemplo)
        total = self.tabla_asistencia.rowCount()
        presentes = sum(1 for row in range(total) 
                   if self.tabla_asistencia.item(row, 4).text() != "No registrado")
        
        # Guardar en historial
        self.historial_clases.append({
            "fecha": datetime.now().strftime("%d/%m/%Y"),
            "materia": f"{materia} - {grupo}",
            "aula": self.aulas.get(f"{materia} - {grupo}", "Sin aula"),
            "duracion": str(datetime.now() - datetime.combine(datetime.today(), self.hora_inicio_clase)),
            "asistencia": f"{presentes}/{total}",
        })
        
        self.clase_activa = False
        self.simulacion_timer.stop()
        self.barra_clase_container.hide()
        
        QMessageBox.information(self, "Clase Finalizada", 
                              f"La clase de {materia} - {grupo} ha finalizado.\n"
                              f"Duración: {datetime.now().strftime('%H:%M')}")

    # [El resto de tus métodos permanecen exactamente igual]

if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    ventana = Dashboard("admin")
    ventana.setWindowTitle("Sistema de Asistencia - Dashboard")
    ventana.resize(1200, 800)
    ventana.show()
    sys.exit(app.exec())