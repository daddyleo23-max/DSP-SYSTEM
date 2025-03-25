import tkinter as tk
from tkinter import Label, Entry, Button, messagebox
from PantallaPrincipal import PantallaPrincipal

class LoginForm:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Login Form")
        self.root.geometry("800x600")
        self.root.configure(bg="black")

        self.center_window()

        self.id_label = Label(self.root, text="ID:", font=("Arial", 16, "bold"), fg="white", bg="black")
        self.id_label.place(x=50, y=50)

        self.id_entry = Entry(self.root, font=("Arial", 14))
        self.id_entry.place(x=150, y=50)

        self.password_label = Label(self.root, text="Contraseña:", font=("Arial", 16, "bold"), fg="white", bg="black")
        self.password_label.place(x=10, y=120)

        self.password_entry = Entry(self.root, font=("Arial", 14), show="*")
        self.password_entry.place(x=150, y=120)

        self.login_button = Button(self.root, text="Iniciar Sesión", font=("Arial", 16, "bold"), bg="white", fg="black", command=self.login)
        self.login_button.place(x=300, y=200)

    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def login(self):
        username = self.id_entry.get()
        password = self.password_entry.get()

        role = self.validate_credentials(username, password)

        if role:
            self.root.destroy()
            pantalla_principal = PantallaPrincipal(role)
            pantalla_principal.show()
        else:
            messagebox.showerror("Error", "Credenciales incorrectas. Inténtelo de nuevo.")

    def validate_credentials(self, username, password):
        # Simulación de validación de credenciales
        if username == "director" and password == "password":
            return "Director"
        elif username == "admin" and password == "password":
            return "Administrador"
        elif username == "docente" and password == "password":
            return "Docente"
        else:
            return None

    def show(self):
        self.root.mainloop()

if __name__ == "__main__":
    login = LoginForm()
    login.show()