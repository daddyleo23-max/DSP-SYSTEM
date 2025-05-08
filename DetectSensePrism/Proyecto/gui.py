# gui/gui.py

import tkinter as tk
from tkinter import filedialog, messagebox
from database import insertar_datos_pdf

def seleccionar_pdf():
    ruta = filedialog.askopenfilename(
        title="Selecciona un archivo PDF",
        filetypes=[("Archivos PDF", "*.pdf")]
    )

    if not ruta:
        return

    try:
        insertar_datos_pdf(ruta)
        messagebox.showinfo("Éxito", "Datos insertados correctamente.")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error:\n{e}")

def iniciar_gui():
    ventana = tk.Tk()
    ventana.title("Registro de Asistencia")
    ventana.geometry("400x200")
    ventana.resizable(False, False)

    etiqueta = tk.Label(ventana, text="Selecciona un archivo PDF para procesar", font=("Arial", 12))
    etiqueta.pack(pady=20)

    boton = tk.Button(ventana, text="Subir PDF", command=seleccionar_pdf, width=20, height=2)
    boton.pack()

    ventana.mainloop()
