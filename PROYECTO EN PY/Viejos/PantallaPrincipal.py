import tkinter as tk
from tkinter import Button, messagebox
from Registro_Personal import RegistroPersonal
from Buscar_Personal import BuscarPersonal

class PantallaPrincipal:
    def __init__(self, role):
        self.role = role
        self.root = tk.Tk()
        self.root.title("Pantalla Principal")
        self.root.geometry("800x450")
        self.root.configure(bg="white")

        self.center_window()
        self.configure_ui_based_on_role()

    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def configure_ui_based_on_role(self):
        if self.role == "Director" or self.role == "Administrador":
            self.btn_registrar_personal = Button(self.root, text="Registrar Personal", command=self.open_registro_personal)
            self.btn_registrar_personal.place(x=50, y=50)

            self.btn_buscar_personal = Button(self.root, text="Buscar Personal", command=self.open_buscar_personal)
            self.btn_buscar_personal.place(x=50, y=120)

            # Agregar más botones según sea necesario

        elif self.role == "Docente":
            self.btn_opciones_docente = Button(self.root, text="Opciones Docente", command=self.open_opciones_docente)
            self.btn_opciones_docente.place(x=50, y=50)

    def open_registro_personal(self):
        registro_personal = RegistroPersonal()
        registro_personal.show()

    def open_buscar_personal(self):
        buscar_personal = BuscarPersonal()
        buscar_personal.show()

    def open_opciones_docente(self):
        messagebox.showinfo("Opciones Docente", "Funcionalidad no implementada aún.")

    def show(self):
        self.root.mainloop()

if __name__ == "__main__":
    pantalla = PantallaPrincipal("Director")
    pantalla.show()