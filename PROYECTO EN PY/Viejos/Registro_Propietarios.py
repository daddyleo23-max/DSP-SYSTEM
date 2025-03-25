import tkinter as tk
from tkinter import Label, Entry, Button, messagebox

class RegistroPropietarios:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Registro de Propietarios")
        self.root.geometry("600x250")
        self.root.configure(bg="black")

        self.center_window()

        self.nombre_label = Label(self.root, text="Nombre:", font=("Arial", 12, "bold"), fg="white", bg="black")
        self.nombre_label.place(x=50, y=30)
        self.nombre_entry = Entry(self.root, font=("Arial", 12))
        self.nombre_entry.place(x=200, y=30)

        self.curp_label = Label(self.root, text="CURP:", font=("Arial", 12, "bold"), fg="white", bg="black")
        self.curp_label.place(x=50, y=70)
        self.curp_entry = Entry(self.root, font=("Arial", 12))
        self.curp_entry.place(x=200, y=70)

        self.registrar_button = Button(self.root, text="Registrar", font=("Arial", 14, "bold"), bg="white", fg="black", command=self.registrar)
        self.registrar_button.place(x=200, y=190)

    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def registrar(self):
        nombre = self.nombre_entry.get()
        curp = self.curp_entry.get()

        if not nombre or not curp:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        messagebox.showinfo("Éxito", "Propietario registrado con éxito.")
        self.root.destroy()

    def show(self):
        self.root.mainloop()

if __name__ == "__main__":
    registro = RegistroPropietarios()
    registro.show()