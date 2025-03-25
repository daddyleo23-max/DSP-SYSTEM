import tkinter as tk
from tkinter import Label, Entry, Button, messagebox, ttk

class RegistroEmpresa:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Registro de Empresa")
        self.root.geometry("600x600")
        self.root.configure(bg="black")

        self.center_window()

        self.nombre_empresa_label = Label(self.root, text="Nombre Empresa:", font=("Arial", 12, "bold"), fg="white", bg="black")
        self.nombre_empresa_label.place(x=50, y=30)
        self.nombre_empresa_entry = Entry(self.root, font=("Arial", 12))
        self.nombre_empresa_entry.place(x=200, y=30)

        self.tipo_empresa_label = Label(self.root, text="Tipo Empresa:", font=("Arial", 12, "bold"), fg="white", bg="black")
        self.tipo_empresa_label.place(x=50, y=70)
        self.tipo_empresa_combobox = ttk.Combobox(self.root, values=["Educación", "Tecnología", "Salud", "Finanzas", "Manufactura", "Otros"], font=("Arial", 12))
        self.tipo_empresa_combobox.place(x=200, y=70)

        self.registrar_button = Button(self.root, text="Registrar", font=("Arial", 14, "bold"), bg="white", fg="black", command=self.registrar)
        self.registrar_button.place(x=200, y=510)

    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def registrar(self):
        nombre_empresa = self.nombre_empresa_entry.get()
        tipo_empresa = self.tipo_empresa_combobox.get()

        if not nombre_empresa or not tipo_empresa:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        messagebox.showinfo("Éxito", "Empresa registrada con éxito.")
        self.root.destroy()

    def show(self):
        self.root.mainloop()

if __name__ == "__main__":
    registro = RegistroEmpresa()
    registro.show()