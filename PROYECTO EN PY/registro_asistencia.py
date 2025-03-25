import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
from reportlab.pdfgen import canvas
import sqlite3
import os

# Configuración inicial de la BD
def inicializar_bd():
    conn = sqlite3.connect('asistencia.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS alumnos (
        id INTEGER PRIMARY KEY,
        nombre TEXT NOT NULL,
        numero_control TEXT UNIQUE,
        huella BLOB  # Template de la huella (se llena con el SDK de Nitgen)
    )''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS registros (
        id INTEGER PRIMARY KEY,
        alumno_id INTEGER,
        clase TEXT,
        grupo TEXT,
        fecha TEXT,
        FOREIGN KEY (alumno_id) REFERENCES alumnos (id)
    )''')
    
    conn.commit()
    conn.close()

# Clase principal para el registro de asistencia
class RegistroAsistenciaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Asistencia con Huella")
        self.root.geometry("800x600")
        
        # Inicializar BD y UI
        inicializar_bd()
        self.crear_interfaz()
        
    def crear_interfaz(self):
        # Frame principal
        main_frame = ttk.Frame(self.root)
        main_frame.pack(pady=20)
        
        # Selección de clase y grupo
        ttk.Label(main_frame, text="Clase:").grid(row=0, column=0, padx=5, pady=5)
        self.clase_combobox = ttk.Combobox(main_frame, values=["Programación Lógica", "Base de Datos", "Redes"])
        self.clase_combobox.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(main_frame, text="Grupo:").grid(row=1, column=0, padx=5, pady=5)
        self.grupo_combobox = ttk.Combobox(main_frame, values=["A", "B", "C"])
        self.grupo_combobox.grid(row=1, column=1, padx=5, pady=5)
        
        # Botón para iniciar registro
        ttk.Button(main_frame, text="Iniciar Registro", command=self.iniciar_registro).grid(row=2, columnspan=2, pady=10)
        
        # Lista de alumnos registrados
        self.lista_alumnos = ttk.Treeview(main_frame, columns=("Nombre", "Control"), show="headings")
        self.lista_alumnos.heading("Nombre", text="Nombre")
        self.lista_alumnos.heading("Control", text="Núm. Control")
        self.lista_alumnos.grid(row=3, columnspan=2, pady=10)
        
        # Botón para generar PDF
        ttk.Button(main_frame, text="Generar PDF", command=self.generar_pdf).grid(row=4, columnspan=2, pady=10)
    
    def iniciar_registro(self):
        # Simulación de captura de huella (reemplazar con SDK de Nitgen)
        alumno = self.capturar_huella()
        if alumno:
            self.registrar_asistencia(alumno)
    
    def capturar_huella(self):
        # Aquí integrarías el SDK de Nitgen Hamster II
        messagebox.showinfo("Instrucción", "Coloque su dedo en el lector")
        
        # Simulación: Devuelve un alumno de prueba (en realidad se buscaría en la BD)
        return {"nombre": "Juan Pérez", "numero_control": "21200999"}
    
    def registrar_asistencia(self, alumno):
        # Añadir a la lista visual
        self.lista_alumnos.insert("", "end", values=(alumno["nombre"], alumno["numero_control"]))
        
        # Guardar en BD
        conn = sqlite3.connect('asistencia.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO registros (alumno_id, clase, grupo, fecha)
            VALUES (?, ?, ?, ?)
        ''', (1, self.clase_combobox.get(), self.grupo_combobox.get(), datetime.now().strftime("%Y-%m-%d")))
        conn.commit()
        conn.close()
        
        messagebox.showinfo("Éxito", f"{alumno['nombre']} registrado/a")
    
    def generar_pdf(self):
        # Crear PDF idéntico al formato del Instituto
        pdf_path = f"asistencia_{datetime.now().strftime('%Y%m%d')}.pdf"
        c = canvas.Canvas(pdf_path)
        
        # Cabecera
        c.drawString(100, 800, "INSTITUTO TECNOLÓGICO DE PACHUCA")
        c.drawString(100, 780, "SUBDIRECCIÓN ACADÉMICA")
        c.drawString(100, 760, f"FECHA: {datetime.now().strftime('%d/%m/%Y')}")
        c.drawString(100, 740, f"MATERIA: {self.clase_combobox.get()}")
        c.drawString(100, 720, f"GRUPO: {self.grupo_combobox.get()}")
        
        # Tabla de alumnos
        y_position = 680
        c.drawString(100, y_position, "No. | No. de Control | Nombre del Alumno")
        y_position -= 20
        
        for i, item in enumerate(self.lista_alumnos.get_children()):
            alumno = self.lista_alumnos.item(item)["values"]
            c.drawString(100, y_position, f"{i+1} | {alumno[1]} | {alumno[0]}")
            y_position -= 20
        
        c.save()
        messagebox.showinfo("PDF Generado", f"Archivo guardado como: {os.path.abspath(pdf_path)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = RegistroAsistenciaApp(root)
    root.mainloop()