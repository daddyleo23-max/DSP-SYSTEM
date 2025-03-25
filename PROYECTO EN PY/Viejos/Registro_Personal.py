import tkinter as tk
from tkinter import Label, Entry, Button, messagebox, ttk
import time

class RegistroPersonal:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Registro de Personal")
        self.root.geometry("300x300")

        self.center_window()

        self.nombre_label = Label(self.root, text="Nombre:")
        self.nombre_label.place(x=50, y=50)
        self.nombre_entry = Entry(self.root)
        self.nombre_entry.place(x=150, y=50)

        self.apellidos_label = Label(self.root, text="Apellidos:")
        self.apellidos_label.place(x=50, y=90)
        self.apellidos_entry = Entry(self.root)
        self.apellidos_entry.place(x=150, y=90)

        self.telefono_label = Label(self.root, text="Teléfono:")
        self.telefono_label.place(x=50, y=130)
        self.telefono_entry = Entry(self.root)
        self.telefono_entry.place(x=150, y=130)

        self.correo_label = Label(self.root, text="Correo:")
        self.correo_label.place(x=50, y=170)
        self.correo_entry = Entry(self.root)
        self.correo_entry.place(x=150, y=170)

        self.rol_label = Label(self.root, text="Rol:")
        self.rol_label.place(x=50, y=210)
        self.rol_combobox = ttk.Combobox(self.root, values=["Director", "Administrador", "Docente"])
        self.rol_combobox.place(x=150, y=210)

        self.guardar_button = Button(self.root, text="Guardar", command=self.guardar)
        self.guardar_button.place(x=100, y=250)

    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def guardar(self):
        nombre = self.nombre_entry.get()
        apellidos = self.apellidos_entry.get()
        telefono = self.telefono_entry.get()
        correo = self.correo_entry.get()
        rol = self.rol_combobox.get()

        if not nombre or not apellidos or not telefono or not correo or not rol:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        id = self.generar_id()
        messagebox.showinfo("Éxito", f"Personal registrado con éxito. ID: {id}")
        self.limpiar_campos()

    def generar_id(self):
        return f"EMP-{int(time.time())}"

    def limpiar_campos(self):
        self.nombre_entry.delete(0, tk.END)
        self.apellidos_entry.delete(0, tk.END)
        self.telefono_entry.delete(0, tk.END)
        self.correo_entry.delete(0, tk.END)
        self.rol_combobox.set("")

    def show(self):
        self.root.mainloop()

if __name__ == "__main__":
    registro = RegistroPersonal()
    registro.show()