import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
import random
import os

# Intento de importaciones con manejo de errores
try:
    import mysql.connector
    from reportlab.pdfgen import canvas
    import hashlib
except ImportError as e:
    messagebox.showerror("Error de Importación", 
                       f"Faltan dependencias: {str(e)}\n"
                       "Instale con: pip install mysql-connector-python reportlab")
    exit()

# ====================== CONFIGURACIÓN MYSQL ======================
def conectar_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="admin_dsp",
            password="DSP_2025",
            database="DetectSensePrism"
        )
        return conn
    except mysql.connector.Error as err:
        messagebox.showerror("Error MySQL", f"Código: {err.errno}\nMensaje: {err.msg}")
        return None

# Ventanas Dashboard (Director, Admin, Docente)
class DirectorDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Panel de Director")
        self.root.configure(bg="#3B4252")

        tk.Label(root, text="Panel de Director", font=("Helvetica", 24), bg="#3B4252", fg="#ECEFF4").pack(pady=20)
        
        button_frame = tk.Frame(root, bg="#3B4252")
        button_frame.pack(pady=20)

        RoundedButton(button_frame, text="Registrar Personal", bg="#81A1C1", fg="#ECEFF4", hover_bg="#5E81AC", command=self.registrar_personal).pack(pady=10)
        RoundedButton(button_frame, text="Registrar Alumnos", bg="#81A1C1", fg="#ECEFF4", hover_bg="#5E81AC", command=self.registrar_alumnos).pack(pady=10)
        RoundedButton(button_frame, text="Consulta", bg="#81A1C1", fg="#ECEFF4", hover_bg="#5E81AC", command=self.consulta).pack(pady=10)
        RoundedButton(button_frame, text="Estadísticas", bg="#81A1C1", fg="#ECEFF4", hover_bg="#5E81AC", command=self.estadisticas).pack(pady=10)
        RoundedButton(button_frame, text="Salir", bg="#BF616A", fg="#ECEFF4", hover_bg="#A9444E", command=root.quit).pack(pady=10)

        center_window(self.root)

    def registrar_personal(self):
        PersonalWindow(tk.Toplevel(self.root))

    def registrar_alumnos(self):
        AlumnosWindow(tk.Toplevel(self.root))

    def consulta(self):
        ConsultaWindow(tk.Toplevel(self.root))

    def estadisticas(self):
        messagebox.showinfo("Estadísticas", "Función para ver estadísticas.")

class AdminDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Panel de Administrador")
        self.root.configure(bg="#3B4252")

        tk.Label(root, text="Panel de Administrador", font=("Helvetica", 24), bg="#3B4252", fg="#ECEFF4").pack(pady=20)
        
        button_frame = tk.Frame(root, bg="#3B4252")
        button_frame.pack(pady=20)

        RoundedButton(button_frame, text="Registrar Personal", bg="#81A1C1", fg="#ECEFF4", hover_bg="#5E81AC", command=self.registrar_personal).pack(pady=10)
        RoundedButton(button_frame, text="Registrar Alumnos", bg="#81A1C1", fg="#ECEFF4", hover_bg="#5E81AC", command=self.registrar_alumnos).pack(pady=10)
        RoundedButton(button_frame, text="Consulta", bg="#81A1C1", fg="#ECEFF4", hover_bg="#5E81AC", command=self.consulta).pack(pady=10)
        RoundedButton(button_frame, text="Estadísticas", bg="#81A1C1", fg="#ECEFF4", hover_bg="#5E81AC", command=self.estadisticas).pack(pady=10)
        RoundedButton(button_frame, text="Salir", bg="#BF616A", fg="#ECEFF4", hover_bg="#A9444E", command=root.quit).pack(pady=10)

        center_window(self.root)

    def registrar_personal(self):
        PersonalWindow(tk.Toplevel(self.root))

    def registrar_alumnos(self):
        AlumnosWindow(tk.Toplevel(self.root))

    def consulta(self):
        ConsultaWindow(tk.Toplevel(self.root))

    def estadisticas(self):
        messagebox.showinfo("Estadísticas", "Función para ver estadísticas.")

# -----------------------------Dashboard Docente -----------------------------------------------------------------------------
class DocenteDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Panel de Docente")
        self.root.configure(bg="#3B4252")

        tk.Label(root, text="Panel de Docente", font=("Helvetica", 24), bg="#3B4252", fg="#ECEFF4").pack(pady=20)
        
        button_frame = tk.Frame(root, bg="#3B4252")
        button_frame.pack(pady=20)

        # Botones originales
        RoundedButton(button_frame, text="Clases", bg="#81A1C1", fg="#ECEFF4", hover_bg="#5E81AC", command=self.clases).pack(pady=10)
        
        # Nuevos botones añadidos
        RoundedButton(button_frame, text="Añadir Materia", bg="#81A1C1", fg="#ECEFF4", hover_bg="#5E81AC", command=self.agregar_materia).pack(pady=10)
        RoundedButton(button_frame, text="Crear Grupo", bg="#81A1C1", fg="#ECEFF4", hover_bg="#5E81AC", command=self.crear_grupo).pack(pady=10)
        
        RoundedButton(button_frame, text="Salir", bg="#BF616A", fg="#ECEFF4", hover_bg="#A9444E", command=root.quit).pack(pady=10)

        center_window(self.root)

    def clases(self):
        ClasesWindow(tk.Toplevel(self.root))

    def agregar_materia(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Añadir Nueva Materia")
        ventana.geometry("400x200")
        
        tk.Label(ventana, text="Nombre de la Materia:").pack(pady=5)
        self.nombre_materia = tk.Entry(ventana)
        self.nombre_materia.pack(pady=5)
        
        tk.Label(ventana, text="Clave:").pack(pady=5)
        self.clave_materia = tk.Entry(ventana)
        self.clave_materia.pack(pady=5)
        
        RoundedButton(ventana, text="Guardar", bg="#81A1C1", fg="#ECEFF4", command=self.guardar_materia).pack(pady=10)

    def guardar_materia(self):
        nombre = self.nombre_materia.get()
        clave = self.clave_materia.get()
        
        if nombre and clave:
            try:
                conn = conectar_db()
                cursor = conn.cursor()
                cursor.execute("INSERT INTO materias (nombre, clave, creado_por) VALUES (%s, %s, %s)", 
                             (nombre, clave, 1))  # 1 sería el ID del docente
                conn.commit()
                messagebox.showinfo("Éxito", "Materia añadida correctamente")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar: {str(e)}")
            finally:
                conn.close()

    def crear_grupo(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Crear Nuevo Grupo")
        ventana.geometry("400x300")
        
        tk.Label(ventana, text="Nombre del Grupo:").pack(pady=5)
        self.nombre_grupo = tk.Entry(ventana)
        self.nombre_grupo.pack(pady=5)
        
        tk.Label(ventana, text="Carrera:").pack(pady=5)
        self.combo_carrera = ttk.Combobox(ventana, values=["ISC", "II", "LA"])
        self.combo_carrera.pack(pady=5)
        
        tk.Label(ventana, text="Semestre:").pack(pady=5)
        self.spin_semestre = ttk.Spinbox(ventana, from_=1, to=12)
        self.spin_semestre.pack(pady=5)
        
        RoundedButton(ventana, text="Guardar Grupo", bg="#81A1C1", fg="#ECEFF4", command=self.guardar_grupo).pack(pady=10)

    def guardar_grupo(self):
        nombre = self.nombre_grupo.get()
        carrera = self.combo_carrera.get()
        semestre = self.spin_semestre.get()
        
        if nombre and carrera and semestre:
            try:
                conn = conectar_db()
                cursor = conn.cursor()
                
                # Obtener ID de carrera
                cursor.execute("SELECT id FROM carreras WHERE clave = %s", (carrera,))
                carrera_id = cursor.fetchone()[0]
                
                cursor.execute("""
                    INSERT INTO grupos (nombre, carrera_id, semestre, es_personalizado, creado_por)
                    VALUES (%s, %s, %s, TRUE, %s)
                """, (nombre, carrera_id, semestre, 1))  # 1 sería el ID del docente
                
                conn.commit()
                messagebox.showinfo("Éxito", "Grupo creado correctamente")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar: {str(e)}")
            finally:
                conn.close()
# Ventanas internas (Clases, Grupos, etc.)
class ClasesWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Clases del Semestre")
        self.root.configure(bg="#3B4252")

        tk.Label(root, text="Clases del Semestre", font=("Helvetica", 20), bg="#3B4252", fg="#ECEFF4").pack(pady=10)
        
        # Frame para botones de clases
        self.clases_frame = tk.Frame(root, bg="#3B4252")
        self.clases_frame.pack(padx=10, pady=10)

        # Obtener materias de la base de datos
        self.cargar_materias()

        RoundedButton(root, text="Cerrar", bg="#BF616A", fg="#ECEFF4", hover_bg="#A9444E", command=root.destroy).pack(pady=10)

        center_window(self.root)

    def cargar_materias(self):
        try:
            conn = conectar_db()
            cursor = conn.cursor()
            cursor.execute("SELECT nombre FROM materias")
            materias = [m[0] for m in cursor.fetchall()]
            
            # Crear botones para cada materia
            for i, clase in enumerate(materias):
                btn = RoundedButton(
                    self.clases_frame, 
                    text=clase, 
                    bg="#81A1C1", 
                    fg="#ECEFF4", 
                    hover_bg="#5E81AC", 
                    command=lambda c=clase: self.select_class(c)
                )
                btn.grid(row=i//2, column=i%2, padx=10, pady=10)
                
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar las materias: {str(e)}")
        finally:
            conn.close()

    def select_class(self, clase):
        GruposWindow(tk.Toplevel(self.root), clase)

class TomarAsistenciaWindow:
    def __init__(self, root, grupo, clase):
        self.root = root
        self.grupo = grupo
        self.clase = clase
        self.root.title(f"Tomar Asistencia - {grupo} - {clase}")
        self.root.configure(bg="#3B4252")

        # Frame principal
        main_frame = tk.Frame(root, bg="#3B4252")
        main_frame.pack(pady=20)

        # Lista de alumnos
        self.tree = ttk.Treeview(main_frame, columns=("Nombre", "Asistencia"), show="headings")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Asistencia", text="Asistencia")
        self.tree.pack()

        # Cargar alumnos del grupo
        self.cargar_alumnos()

        # Botones
        btn_frame = tk.Frame(main_frame, bg="#3B4252")
        btn_frame.pack(pady=10)

        RoundedButton(btn_frame, text="Registrar Huella", bg="#81A1C1", fg="#ECEFF4", 
                     command=self.registrar_huella).pack(side=tk.LEFT, padx=5)
        RoundedButton(btn_frame, text="Generar PDF", bg="#81A1C1", fg="#ECEFF4", 
                     command=self.generar_pdf).pack(side=tk.LEFT, padx=5)
        RoundedButton(btn_frame, text="Cerrar", bg="#BF616A", fg="#ECEFF4", 
                     command=root.destroy).pack(side=tk.LEFT, padx=5)

        center_window(self.root)

    def cargar_alumnos(self):
        try:
            conn = conectar_db()
            cursor = conn.cursor()
            
            # Obtener alumnos del grupo
            cursor.execute("""
                SELECT a.nombre 
                FROM alumnos a
                JOIN grupo_alumno ga ON a.id = ga.alumno_id
                JOIN grupos g ON ga.grupo_id = g.id
                WHERE g.nombre = %s
            """, (self.grupo,))
            
            for alumno in cursor.fetchall():
                self.tree.insert("", tk.END, values=(alumno[0], "No"))
                
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar alumnos: {str(e)}")
        finally:
            conn.close()

    def registrar_huella(self):
        # Simulación de captura de huella
        messagebox.showinfo("Instrucción", "Coloque su dedo en el lector")
        
        # En realidad aquí iría la integración con el SDK de Nitgen
        alumno_seleccionado = self.tree.focus()
        if alumno_seleccionado:
            self.tree.item(alumno_seleccionado, values=(self.tree.item(alumno_seleccionado)["values"][0], "Sí"))
            messagebox.showinfo("Éxito", "Asistencia registrada")

    def generar_pdf(self):
        try:
            filename = f"asistencia_{self.grupo}_{datetime.now().strftime('%Y%m%d')}.pdf"
            c = canvas.Canvas(filename)
            
            # Cabecera
            c.drawString(100, 800, f"Clase: {self.clase}")
            c.drawString(100, 780, f"Grupo: {self.grupo}")
            c.drawString(100, 760, f"Fecha: {datetime.now().strftime('%d/%m/%Y')}")
            
            # Lista de alumnos
            y = 700
            for item in self.tree.get_children():
                nombre, asistencia = self.tree.item(item)["values"]
                c.drawString(100, y, f"{nombre}: {asistencia}")
                y -= 20
                
            c.save()
            messagebox.showinfo("PDF Generado", f"Archivo guardado como {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar PDF: {str(e)}")


class GruposWindow:
    def __init__(self, root, clase):
        self.root = root
        self.clase = clase
        self.root.title(f"Grupos de {self.clase}")
        self.root.configure(bg="#3B4252")

        tk.Label(root, text=f"Grupos de {self.clase}", font=("Helvetica", 20), bg="#3B4252", fg="#ECEFF4").pack(pady=10)
        self.grupos_listbox = tk.Listbox(root, bg="#4C566A", fg="#ECEFF4")
        self.grupos_listbox.pack(padx=10, pady=10)

        # Simulación de grupos
        grupos = ["Grupo A", "Grupo B", "Grupo C"]
        for grupo in grupos:
            self.grupos_listbox.insert(tk.END, grupo)

        RoundedButton(root, text="Seleccionar Grupo", bg="#81A1C1", fg="#ECEFF4", hover_bg="#5E81AC", command=self.seleccionar_grupo).pack(pady=10)
        RoundedButton(root, text="Cerrar", bg="#BF616A", fg="#ECEFF4", hover_bg="#A9444E", command=root.destroy).pack(pady=10)

        center_window(self.root)

    def seleccionar_grupo(self):
        seleccion = self.grupos_listbox.curselection()
        if seleccion:
            grupo = self.grupos_listbox.get(seleccion)
            OpcionesGrupoWindow(tk.Toplevel(self.root), self.clase, grupo)
        else:
            messagebox.showerror("Error", "Por favor, selecciona un grupo.")

class OpcionesGrupoWindow:
    def __init__(self, root, clase, grupo):
        self.root = root
        self.clase = clase
        self.grupo = grupo
        self.root.title(f"Opciones para {self.grupo} en {self.clase}")
        self.root.configure(bg="#3B4252")

        tk.Label(root, text=f"Opciones para {self.grupo} en {self.clase}", font=("Helvetica", 20), bg="#3B4252", fg="#ECEFF4").pack(pady=10)
        RoundedButton(root, text="Tomar Asistencia", bg="#81A1C1", fg="#ECEFF4", hover_bg="#5E81AC", command=self.tomar_asistencia).pack(pady=10)
        RoundedButton(root, text="Registro de Inicio de Curso", bg="#81A1C1", fg="#ECEFF4", hover_bg="#5E81AC", command=self.registro_inicio_curso).pack(pady=10)
        RoundedButton(root, text="Cerrar", bg="#BF616A", fg="#ECEFF4", hover_bg="#A9444E", command=root.destroy).pack(pady=10)

        center_window(self.root)

    def tomar_asistencia(self):
        TomarAsistenciaWindow(tk.Toplevel(self.root), self.grupo, self.clase)
    
    def registro_inicio_curso(self):
        messagebox.showinfo("Registro de Inicio de Curso", "Función para registrar el inicio del curso.")

# Clase para botones redondeados
class RoundedButton(tk.Canvas):
    def __init__(self, master=None, text="", radius=25, bg="#81A1C1", fg="#ECEFF4", hover_bg="#5E81AC", hover_fg="#ECEFF4", command=None):
        super().__init__(master, bg=bg, bd=0, highlightthickness=0)
        self.config(width=200, height=50)
        self.radius = radius
        self.bg = bg
        self.fg = fg
        self.hover_bg = hover_bg
        self.hover_fg = hover_fg
        self.command = command
        self.text = text

        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Button-1>", self.on_click)

        self.draw_button()

    def draw_button(self):
        self.delete("all")
        self.create_rounded_rectangle(0, 0, 200, 50, radius=self.radius, fill=self.bg)
        self.create_text(100, 25, text=self.text, font=("Helvetica", 14), fill=self.fg)

    def create_rounded_rectangle(self, x1, y1, x2, y2, radius=25, **kwargs):
        points = [
            x1 + radius, y1,
            x2 - radius, y1,
            x2, y1,
            x2, y1 + radius,
            x2, y2 - radius,
            x2, y2,
            x2 - radius, y2,
            x1 + radius, y2,
            x1, y2,
            x1, y2 - radius,
            x1, y1 + radius,
            x1, y1
        ]
        return self.create_polygon(points, **kwargs, smooth=True)

    def on_enter(self, event):
        self.config(bg=self.hover_bg)
        self.draw_button()

    def on_leave(self, event):
        self.config(bg=self.bg)
        self.draw_button()

    def on_click(self, event):
        if self.command:
            self.command()

def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")
    window.deiconify()

class AlumnosWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Registrar Alumnos")
        self.root.geometry("800x700")
        self.root.configure(bg="#3B4252")  # Fondo oscuro moderno

        # Fuentes modernas
        self.title_font = ("Helvetica", 24, "bold")
        self.label_font = ("Helvetica", 14)
        self.button_font = ("Helvetica", 12)

        ttk.Label(root, text="Registrar Alumnos", font=self.title_font, foreground="#ECEFF4", background="#3B4252").pack(pady=20)

        self.form_frame = ttk.Frame(root)
        self.form_frame.pack(padx=20, pady=20)

        # Campos del formulario
        fields = [
            ("Nombre:", 0),
            ("Apellido Paterno:", 1),
            ("Apellido Materno:", 2),
            ("CURP:", 3),
            ("Fecha de Nacimiento:", 4),
            ("Localidad:", 5),
            ("NÃºmero de Control:", 6),
            ("Correo ElectrÃ³nico:", 7),
            ("Registrar Huella:", 8)
        ]

        self.entries = {}
        for field, row in fields:
            ttk.Label(self.form_frame, text=field, font=self.label_font, foreground="#ECEFF4", background="#3B4252").grid(row=row, column=0, padx=5, pady=5, sticky="e")
            if field == "Registrar Huella:":
                self.registrar_huella_button = RoundedButton(self.form_frame, text="Capturar Huella", bg="#81A1C1", fg="#ECEFF4", hover_bg="#5E81AC", command=self.registrar_huella)
                self.registrar_huella_button.grid(row=row, column=1, padx=5, pady=5)
            else:
                entry = ttk.Entry(self.form_frame, font=self.label_font)
                entry.grid(row=row, column=1, padx=5, pady=5)
                self.entries[field] = entry

        self.generar_numero_control()

        # Botones de acciÃ³n
        RoundedButton(root, text="Registrar", bg="#81A1C1", fg="#ECEFF4", hover_bg="#5E81AC", command=self.registrar_alumno).pack(pady=10)
        RoundedButton(root, text="Cerrar", bg="#BF616A", fg="#ECEFF4", hover_bg="#A9444E", command=root.destroy).pack(pady=10)

        center_window(self.root)

    def generar_numero_control(self):
        current_year = datetime.now().year
        year_suffix = str(current_year)[-2:]
        unique_number = f"{random.randint(0, 999999):06}"  # Genera un nÃºmero Ãºnico de 6 dÃ­gitos
        numero_control = f"{year_suffix}{unique_number}"
        self.entries["NÃºmero de Control:"].insert(0, numero_control)
        self.generar_correo(numero_control)

    def generar_correo(self, numero_control):
        correo = f"l{numero_control}@pachuca.tecnm.mx"
        self.entries["Correo ElectrÃ³nico:"].insert(0, correo)

    def registrar_huella(self):
        # SimulaciÃ³n de captura de huella
        messagebox.showinfo("Registrar Huella", "Coloque su dedo en el lector de huellas.")
        # AquÃ­ puedes integrar la lÃ³gica del lector de huellas mÃ¡s adelante.

    def registrar_alumno(self):
        nombre = self.entries["Nombre:"].get()
        apellido_paterno = self.entries["Apellido Paterno:"].get()
        apellido_materno = self.entries["Apellido Materno:"].get()
        curp = self.entries["CURP:"].get()
        fecha_nacimiento = self.entries["Fecha de Nacimiento:"].get()
        localidad = self.entries["Localidad:"].get()
        numero_control = self.entries["NÃºmero de Control:"].get()
        correo = self.entries["Correo ElectrÃ³nico:"].get()

        if not nombre or not apellido_paterno or not apellido_materno or not curp or not fecha_nacimiento or not localidad or not numero_control or not correo:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        # AquÃ­ puedes aÃ±adir la lÃ³gica para guardar los datos del alumno en una base de datos o archivo

        messagebox.showinfo("Registro Exitoso", "El alumno ha sido registrado con Ã©xito.")
        self.root.destroy()

class PersonalWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Registrar Personal")
        self.root.geometry("800x700")
        self.root.configure(bg="#3B4252")  # Fondo oscuro moderno

        # Fuentes modernas
        self.title_font = ("Helvetica", 24, "bold")
        self.label_font = ("Helvetica", 14)
        self.button_font = ("Helvetica", 12)

        ttk.Label(root, text="Registrar Personal", font=self.title_font, foreground="#ECEFF4", background="#3B4252").pack(pady=20)

        self.form_frame = ttk.Frame(root)
        self.form_frame.pack(padx=20, pady=20)

        # Campos del formulario
        fields = [
            ("Nombre:", 0),
            ("Apellido Paterno:", 1),
            ("Apellido Materno:", 2),
            ("CURP:", 3),
            ("Fecha de Nacimiento:", 4),
            ("Localidad:", 5),
            ("Ãrea de EspecializaciÃ³n:", 6),
            ("ID:", 7),
            ("ContraseÃ±a:", 8),
            ("Correo ElectrÃ³nico:", 9),
            ("Registrar Huella:", 10)
        ]

        self.entries = {}
        for field, row in fields:
            ttk.Label(self.form_frame, text=field, font=self.label_font, foreground="#ECEFF4", background="#3B4252").grid(row=row, column=0, padx=5, pady=5, sticky="e")
            if field == "Registrar Huella:":
                self.registrar_huella_button = RoundedButton(self.form_frame, text="Capturar Huella", bg="#81A1C1", fg="#ECEFF4", hover_bg="#5E81AC", command=self.registrar_huella)
                self.registrar_huella_button.grid(row=row, column=1, padx=5, pady=5)
            elif field == "Ãrea de EspecializaciÃ³n:":
                self.area_combobox = ttk.Combobox(self.form_frame, values=["Docente", "AdministraciÃ³n", "Limpieza", "Jardinero", "Otro"])
                self.area_combobox.grid(row=row, column=1, padx=5, pady=5)
                self.area_combobox.bind("<<ComboboxSelected>>", self.mostrar_seccion_id)
            elif field == "ContraseÃ±a:":
                entry = ttk.Entry(self.form_frame, font=self.label_font, show="*")
                entry.grid(row=row, column=1, padx=5, pady=5)
                self.entries[field] = entry
            else:
                entry = ttk.Entry(self.form_frame, font=self.label_font)
                entry.grid(row=row, column=1, padx=5, pady=5)
                self.entries[field] = entry

        # Botones de acciÃ³n
        RoundedButton(root, text="Registrar", bg="#81A1C1", fg="#ECEFF4", hover_bg="#5E81AC", command=self.registrar_personal).pack(pady=10)
        RoundedButton(root, text="Cerrar", bg="#BF616A", fg="#ECEFF4", hover_bg="#A9444E", command=root.destroy).pack(pady=10)

        center_window(self.root)

    def registrar_huella(self):
        # SimulaciÃ³n de captura de huella
        messagebox.showinfo("Registrar Huella", "Coloque su dedo en el lector de huellas.")
        # AquÃ­ puedes integrar la lÃ³gica del lector de huellas mÃ¡s adelante.

    def mostrar_seccion_id(self, event):
        area = self.area_combobox.get()
        current_year = datetime.now().year
        year_suffix = str(current_year)[-2:]
        unique_number = f"{random.randint(0, 999999):06}"

        if area == "Docente":
            self.entries["ID:"].grid_remove()
            if hasattr(self, 'area_docencia_combobox'):
                self.area_docencia_combobox.destroy()
            self.area_docencia_combobox = ttk.Combobox(self.form_frame, values=["IngenierÃ­a en Sistemas Computacionales", "IngenierÃ­a Civil", "IngenierÃ­a ElÃ©ctrica", "IngenierÃ­a QuÃ­mica"])
            self.area_docencia_combobox.grid(row=7, column=1, padx=5, pady=5)
            self.area_docencia_combobox.bind("<<ComboboxSelected>>", self.generar_id_docente)
        else:
            if hasattr(self, 'area_docencia_combobox'):
                self.area_docencia_combobox.destroy()
            self.entries["ID:"].grid(row=7, column=1, padx=5, pady=5)
            self.entries["ID:"].delete(0, tk.END)

            if area == "AdministraciÃ³n":
                id_personal = f"admin{year_suffix}{unique_number}"
            else:
                id_personal = f"{area[:3].upper()}{year_suffix}{unique_number}"

            self.entries["ID:"].insert(0, id_personal)
            self.generar_correo(id_personal)

    def generar_id_docente(self, event):
        area_docencia = self.area_docencia_combobox.get()
        current_year = datetime.now().year
        year_suffix = str(current_year)[-2:]
        unique_number = f"{random.randint(0, 999999):06}"
        area_code = "".join([word[0] for word in area_docencia.split()]).upper()
        id_personal = f"{area_code}{year_suffix}{unique_number}"
        self.entries["ID:"].grid(row=7, column=1, padx=5, pady=5)
        self.entries["ID:"].delete(0, tk.END)
        self.entries["ID:"].insert(0, id_personal)
        self.generar_correo(id_personal)

    def generar_correo(self, id_personal):
        correo = f"{id_personal.lower()}@pachuca.tecnm.mx"
        self.entries["Correo ElectrÃ³nico:"].delete(0, tk.END)
        self.entries["Correo ElectrÃ³nico:"].insert(0, correo)

    def registrar_personal(self):
        nombre = self.entries["Nombre:"].get()
        apellido_paterno = self.entries["Apellido Paterno:"].get()
        apellido_materno = self.entries["Apellido Materno:"].get()
        curp = self.entries["CURP:"].get()
        fecha_nacimiento = self.entries["Fecha de Nacimiento:"].get()
        localidad = self.entries["Localidad:"].get()
        area = self.area_combobox.get()
        id_personal = self.entries["ID:"].get()
        contrasena = self.entries["ContraseÃ±a:"].get()
        correo = self.entries["Correo ElectrÃ³nico:"].get()

        if not nombre or not apellido_paterno or not apellido_materno or not curp or not fecha_nacimiento or not localidad or not area or not id_personal or not contrasena or not correo:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        # AquÃ­ puedes aÃ±adir la lÃ³gica para guardar los datos del personal en una base de datos o archivo

        messagebox.showinfo("Registro Exitoso", "El personal ha sido registrado con Ã©xito.")
        self.root.destroy()



# Ventana de consulta
class ConsultaWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Consulta")

        tk.Label(root, text="Consulta", font=("Arial", 20)).pack(pady=10)

        self.form_frame = tk.Frame(root)
        self.form_frame.pack(padx=10, pady=10)

        tk.Label(self.form_frame, text="ID del Personal:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.id_entry = tk.Entry(self.form_frame)
        self.id_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Button(root, text="Buscar", command=self.buscar_personal).pack(pady=10)
        tk.Button(root, text="Cerrar", command=root.destroy).pack(pady=10)

        self.result_frame = tk.Frame(root)
        self.result_frame.pack(padx=10, pady=10)

        center_window(self.root)

    def buscar_personal(self):
        id_personal = self.id_entry.get()
        if not id_personal:
            messagebox.showerror("Error", "Por favor, ingrese el ID del personal.")
            return

        # Aquí puedes añadir la lógica para buscar los datos del personal en una base de datos o archivo
        # Simulación de resultados de búsqueda
        resultados = {
            "nombre": "Juan",
            "apellido_paterno": "Pérez",
            "apellido_materno": "García",
            "curp": "PEGA890123HDFRRL09",
            "fecha_nacimiento": "23/01/1989",
            "localidad": "Pachuca",
            "area": "Docente",
            "correo": "jperez@pachuca.tecnm.mx"
        }

        for widget in self.result_frame.winfo_children():
            widget.destroy()

        tk.Label(self.result_frame, text="Resultados de la Búsqueda", font=("Arial", 16)).pack(pady=10)
        for key, value in resultados.items():
            tk.Label(self.result_frame, text=f"{key.capitalize()}: {value}").pack(pady=2)


def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")
    window.deiconify()

if __name__ == "__main__":
    root = tk.Tk()
    app = DocenteDashboard(root)
    root.mainloop()
