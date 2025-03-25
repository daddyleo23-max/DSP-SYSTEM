import tkinter as tk
from tkinter import Label, Entry, Button, messagebox

class RegistroDueño:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Registro de Dueño")
        self.root.geometry("600x300")
        self.root.configure(bg="black")

        self.center_window()

        self.curp_label = Label(self.root, text="CURP:", font=("Arial", 12, "bold"), fg="white", bg="black")
        self.curp_label.place(x=50, y=30)
        self.curp_entry = Entry(self.root, font=("Arial", 12))
        self.curp_entry.place(x=200, y=30)

        self.nombre_label = Label(self.root, text="Nombre:", font=("Arial", 12, "bold"), fg="white", bg="black")
        self.nombre_label.place(x=50, y=70)
        self.nombre_entry = Entry(self.root, font=("Arial", 12))
        self.nombre_entry.place(x=200, y=70)

        self.registrar_button = Button(self.root, text="Registrar", font=("Arial", 14, "bold"), bg="white", fg="black", command=self.registrar)
        self.registrar_button.place(x=200, y=230)

    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def registrar(self):
        curp = self.curp_entry.get()
        nombre = self.nombre_entry.get()

        if not curp or not nombre:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        messagebox.showinfo("Éxito", "Dueño registrado con éxito.")
        self.root.destroy()

    def show(self):
        self.root.mainloop()

if __name__ == "__main__":
    registro = RegistroDueño()
    registro.show()