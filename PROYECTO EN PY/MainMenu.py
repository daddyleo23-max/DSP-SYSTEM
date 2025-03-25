import tkinter as tk
from tkinter import Label, messagebox
import random
from tkinter import ttk, filedialog

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

# Clase para el menú principal
class MainMenu:
    def __init__(self, root):
        self.root = root
        self.root.title("Menú Principal")
        self.root.geometry("600x400")
        self.root.configure(bg="#3B4252")  # Fondo oscuro moderno

        # Fuentes modernas
        self.title_font = ("Helvetica", 24, "bold")
        self.button_font = ("Helvetica", 14)

        # Título con animación
        Label(root, text="Bienvenido a", font=("Helvetica", 14), fg="#ECEFF4", bg="#3B4252").pack(pady=(20, 5))
        self.title_label = Label(root, text="DetectSensePrism", font=self.title_font, fg="#88C0D0", bg="#3B4252")
        self.title_label.pack(pady=(5, 20))
        self.animate_title()

        # Botones modernos
        self.register_button = RoundedButton(root, text="Registrar Empresa", bg="#81A1C1", fg="#ECEFF4", hover_bg="#5E81AC", command=self.registrar_empresa)
        self.register_button.pack(pady=10)

        self.login_button = RoundedButton(root, text="Ingresar", bg="#81A1C1", fg="#ECEFF4", hover_bg="#5E81AC", command=self.ingresar) 
        self.login_button.pack(pady=10)

        self.exit_button = RoundedButton(root, text="Salir", bg="#BF616A", fg="#ECEFF4", hover_bg="#A9444E", command=root.quit)
        self.exit_button.pack(pady=10)

        # Centrar ventana
        self.center_window()

    def animate_title(self):
        colors = ["#88C0D0", "#81A1C1", "#5E81AC", "#BF616A", "#D08770", "#EBCB8B", "#A3BE8C"]
        current_color = self.title_label.cget("fg")
        new_color = random.choice(colors)
        self.title_label.config(fg=new_color)
        self.root.after(1000, self.animate_title)
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def registrar_empresa(self):
        # Ocultar la ventana principal
        self.root.withdraw()
        # Abrir la ventana de registro
        registration_window = tk.Toplevel(self.root)
        registration_window.title("Registro de Empresa")
        registration_window.geometry("800x600")
        registration_window.configure(bg="#3B4252")
        app = RegistrationApp(registration_window)
        # Centrar la ventana de registro
        self.center_window(registration_window)
        # Manejar el cierre de la ventana de registro
        registration_window.protocol("WM_DELETE_WINDOW", lambda: self.on_registration_close(registration_window))

    def on_registration_close(self, registration_window):
        # Cerrar la ventana de registro y mostrar la ventana principal nuevamente
        registration_window.destroy()
        self.root.deiconify()
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def ingresar(self):
        login_window = tk.Toplevel(self.root)
        login_window.title("Ingreso")
        login_window.geometry("400x300")
        login_window.configure(bg="#3B4252")

        Label(login_window, text="ID de Usuario", font=self.button_font, fg="#ECEFF4", bg="#3B4252").pack(pady=10)
        self.id_entry = tk.Entry(login_window, font=self.button_font, bg="#4C566A", fg="#ECEFF4", bd=0)
        self.id_entry.pack(pady=5)

        Label(login_window, text="Contraseña", font=self.button_font, fg="#ECEFF4", bg="#3B4252").pack(pady=10)
        self.password_entry = tk.Entry(login_window, show="*", font=self.button_font, bg="#4C566A", fg="#ECEFF4", bd=0)
        self.password_entry.pack(pady=5)

        # Botón de ingreso con RoundedButton
        RoundedButton(login_window, text="Ingresar", bg="#81A1C1", fg="#ECEFF4", hover_bg="#5E81AC", command=self.validate_login).pack(pady=10)

        self.center_window(login_window)

    def validate_login(self):
        user_id = self.id_entry.get()
        password = self.password_entry.get()
        if user_id == "director" and password == "director":
            self.open_director_dashboard()
        elif user_id == "admin" and password == "admin":
            self.open_admin_dashboard()
        elif user_id == "docente" and password == "docente":
            self.open_docente_dashboard()
        else:
            messagebox.showerror("Error", "ID de Usuario o Contraseña incorrectos")

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def open_director_dashboard(self):
        self.root.destroy()
        root = tk.Tk()
        director_dashboard = DirectorDashboard(root)
        root.attributes('-fullscreen', True)
        root.mainloop()

    def open_admin_dashboard(self):
        self.root.destroy()
        root = tk.Tk()
        admin_dashboard = AdminDashboard(root)
        root.attributes('-fullscreen', True)
        root.mainloop()

    def open_docente_dashboard(self):
        self.root.destroy()
        root = tk.Tk()
        docente_dashboard = DocenteDashboard(root)
        root.attributes('-fullscreen', True)
        root.mainloop()

    def center_window(self, window=None):
        if window is None:
            window = self.root
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry(f'{width}x{height}+{x}+{y}')
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Clases simuladas para los paneles (puedes reemplazarlas con tus implementaciones reales)
class DirectorDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Panel de Director")
        Label(root, text="Panel de Director", font=("Helvetica", 24), fg="#ECEFF4", bg="#3B4252").pack(pady=20)

class AdminDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Panel de Administrador")
        Label(root, text="Panel de Administrador", font=("Helvetica", 24), fg="#ECEFF4", bg="#3B4252").pack(pady=20)

class DocenteDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Panel de Docente")
        Label(root, text="Panel de Docente", font=("Helvetica", 24), fg="#ECEFF4", bg="#3B4252").pack(pady=20)

# Clase para el registro de empresas
class RegistrationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Registro de Empresa")
        self.frames = {}

        # Data storage
        self.data = {
            "empresa": {},
            "propietarios": [],
            "licencias": [],
            "dueno": {}
        }

        self.create_frames()
        self.show_frame("GeneralInfo")

        self.center_window()

    def create_frames(self):
        for F in (GeneralInfo, ContactInfo, LegalInfo, Propietarios, Licencias, Dueno, Review):
            page_name = F.__name__
            frame = F(parent=self.root, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

class GeneralInfo(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        tk.Label(self, text="Información General", font=("Arial", 18)).pack(pady=10)

        tk.Label(self, text="Nombre de la Empresa").pack()
        self.nombre_entry = tk.Entry(self)
        self.nombre_entry.pack()

        tk.Label(self, text="Tipo de Empresa").pack()
        self.tipo_combobox = ttk.Combobox(self, values=["Institución", "Comercial", "Industrial", "Servicios"])
        self.tipo_combobox.pack()

        tk.Label(self, text="Objetivos Sociales").pack()
        self.objetivos_entry = tk.Entry(self)
        self.objetivos_entry.pack()
        self.sugerencias_listbox = tk.Listbox(self)
        self.sugerencias_listbox.pack(pady=5)
        self.objetivos_entry.bind("<KeyRelease>", self.sugerir_objetivos)

        tk.Button(self, text="Continuar", command=self.save_data).pack(pady=10)

    def sugerir_objetivos(self, event):
        sugerencias = ["Educación", "Salud", "Desarrollo", "Innovación", "Sostenibilidad", "Tecnología"]
        typed_text = self.objetivos_entry.get()
        self.sugerencias_listbox.delete(0, tk.END)
        for item in sugerencias:
            if typed_text.lower() in item.lower():
                self.sugerencias_listbox.insert(tk.END, item)
        self.sugerencias_listbox.bind("<<ListboxSelect>>", self.seleccionar_sugerencia)

    def seleccionar_sugerencia(self, event):
        selected = self.sugerencias_listbox.get(tk.ACTIVE)
        current_text = self.objetivos_entry.get()
        if selected not in current_text:
            if len(current_text.split(',')) < 10:
                self.objetivos_entry.insert(tk.END, f", {selected}" if current_text else selected)

    def save_data(self):
        self.controller.data["empresa"]["nombre"] = self.nombre_entry.get()
        self.controller.data["empresa"]["tipo"] = self.tipo_combobox.get()
        self.controller.data["empresa"]["objetivos"] = self.objetivos_entry.get()
        self.controller.show_frame("ContactInfo")

class ContactInfo(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        tk.Label(self, text="Datos de Contacto", font=("Arial", 18)).pack(pady=10)

        tk.Label(self, text="Dirección").pack()
        self.direccion_entry = tk.Entry(self)
        self.direccion_entry.pack()

        tk.Label(self, text="Teléfono").pack()
        self.telefono_entry = tk.Entry(self)
        self.telefono_entry.pack()

        tk.Label(self, text="Correo Electrónico").pack()
        self.correo_entry = tk.Entry(self)
        self.correo_entry.pack()

        tk.Button(self, text="Regresar", command=lambda: controller.show_frame("GeneralInfo")).pack(side="left", padx=10, pady=10)
        tk.Button(self, text="Continuar", command=self.save_data).pack(side="right", padx=10, pady=10)

    def save_data(self):
        direccion = self.direccion_entry.get()
        telefono = self.telefono_entry.get()
        correo = self.correo_entry.get()

        if not direccion:
            messagebox.showerror("Error", "La dirección no puede estar vacía.")
            return
        if not telefono.isdigit() or len(telefono) < 10:
            messagebox.showerror("Error", "El teléfono debe ser un número válido de al menos 10 dígitos.")
            return
        if "@" not in correo or "." not in correo:
            messagebox.showerror("Error", "El correo electrónico no es válido.")
            return

        self.controller.data["empresa"]["direccion"] = direccion
        self.controller.data["empresa"]["telefono"] = telefono
        self.controller.data["empresa"]["correo"] = correo
        self.controller.show_frame("LegalInfo")

class LegalInfo(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        tk.Label(self, text="Datos Legales", font=("Arial", 18)).pack(pady=10)

        tk.Label(self, text="NIF").pack()
        self.nif_entry = tk.Entry(self)
        self.nif_entry.pack()

        tk.Label(self, text="IVA").pack()
        self.iva_entry = tk.Entry(self)
        self.iva_entry.pack()

        tk.Label(self, text="Capital").pack()
        self.capital_entry = tk.Entry(self)
        self.capital_entry.pack()

        tk.Label(self, text="Estatus").pack()
        self.estatus_entry = tk.Entry(self)
        self.estatus_entry.pack()

        tk.Button(self, text="Regresar", command=lambda: controller.show_frame("ContactInfo")).pack(side="left", padx=10, pady=10)
        tk.Button(self, text="Continuar", command=self.save_data).pack(side="right", padx=10, pady=10)

    def save_data(self):
        self.controller.data["empresa"]["nif"] = self.nif_entry.get()
        self.controller.data["empresa"]["iva"] = self.iva_entry.get()
        self.controller.data["empresa"]["capital"] = self.capital_entry.get()
        self.controller.data["empresa"]["estatus"] = self.estatus_entry.get()
        self.controller.show_frame("Propietarios")

class Propietarios(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        tk.Label(self, text="Propietarios", font=("Arial", 18)).pack(pady=10)

        self.propietarios_frame = tk.Frame(self)
        self.propietarios_frame.pack()

        self.add_propietario()

        tk.Button(self, text="Agregar Propietario", command=self.add_propietario).pack(pady=10)
        tk.Button(self, text="Regresar", command=lambda: controller.show_frame("LegalInfo")).pack(side="left", padx=10, pady=10)
        tk.Button(self, text="Continuar", command=self.save_data).pack(side="right", padx=10, pady=10)

    def add_propietario(self):
        row = len(self.propietarios_frame.winfo_children()) // 3
        tk.Entry(self.propietarios_frame).grid(row=row, column=0, padx=5, pady=5)
        tk.Entry(self.propietarios_frame).grid(row=row, column=1, padx=5, pady=5)
        tk.Entry(self.propietarios_frame).grid(row=row, column=2, padx=5, pady=5)

    def save_data(self):
        self.controller.data["propietarios"] = [
            {
                "nombre": self.propietarios_frame.grid_slaves(row=i, column=0)[0].get(),
                "curp": self.propietarios_frame.grid_slaves(row=i, column=1)[0].get(),
                "participacion": self.propietarios_frame.grid_slaves(row=i, column=2)[0].get()
            }
            for i in range(len(self.propietarios_frame.winfo_children()) // 3)
        ]
        self.controller.show_frame("Licencias")

class Licencias(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        tk.Label(self, text="Licencias y Permisos", font=("Arial", 18)).pack(pady=10)

        self.files_frame = tk.Frame(self)
        self.files_frame.pack()

        tk.Button(self, text="Agregar Archivo", command=self.add_file).pack(pady=10)
        tk.Button(self, text="Regresar", command=lambda: controller.show_frame("Propietarios")).pack(side="left", padx=10, pady=10)
        tk.Button(self, text="Continuar", command=self.save_data).pack(side="right", padx=10, pady=10)

    def add_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if file_path:
            tk.Label(self.files_frame, text=file_path).pack()

    def save_data(self):
        self.controller.data["licencias"] = [label.cget("text") for label in self.files_frame.winfo_children()]
        self.controller.show_frame("Dueno")

class Dueno(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        tk.Label(self, text="Registro Propietario Principal", font=("Arial", 18)).pack(pady=10)

        tk.Label(self, text="CURP").pack()
        self.curp_entry = tk.Entry(self)
        self.curp_entry.pack()

        tk.Label(self, text="Nombre").pack()
        self.nombre_entry = tk.Entry(self)
        self.nombre_entry.pack()

        tk.Label(self, text="Apellido Paterno").pack()
        self.paterno_entry = tk.Entry(self)
        self.paterno_entry.pack()

        tk.Label(self, text="Apellido Materno").pack()
        self.materno_entry = tk.Entry(self)
        self.materno_entry.pack()

        tk.Label(self, text="Dirección").pack()
        self.direccion_entry = tk.Entry(self)
        self.direccion_entry.pack()

        tk.Label(self, text="Teléfono").pack()
        self.telefono_entry = tk.Entry(self)
        self.telefono_entry.pack()

        tk.Label(self, text="Correo Electrónico").pack()
        self.correo_entry = tk.Entry(self)
        self.correo_entry.pack()

        tk.Button(self, text="Regresar", command=lambda: controller.show_frame("Licencias")).pack(side="left", padx=10, pady=10)
        tk.Button(self, text="Continuar", command=self.save_data).pack(side="right", padx=10, pady=10)

    def save_data(self):
        self.controller.data["dueno"] = {
            "curp": self.curp_entry.get(),
            "nombre": self.nombre_entry.get(),
            "paterno": self.paterno_entry.get(),
            "materno": self.materno_entry.get(),
            "direccion": self.direccion_entry.get(),
            "telefono": self.telefono_entry.get(),
            "correo": self.correo_entry.get()
        }
        self.controller.show_frame("Review")

class Review(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        tk.Label(self, text="Revisión y Confirmación", font=("Arial", 18)).pack(pady=10)

        self.text = tk.Text(self, height=15, width=50)
        self.text.pack()

        tk.Button(self, text="Regresar", command=lambda: controller.show_frame("Dueno")).pack(side="left", padx=10, pady=10)
        tk.Button(self, text="Confirmar", command=self.confirm).pack(side="right", padx=10, pady=10)

    def tkraise(self):
        super().tkraise()
        self.update_text()

    def update_text(self):
        self.text.delete(1.0, tk.END)
        data = self.controller.data
        self.text.insert(tk.END, "Datos de la Empresa:\n")
        for key, value in data["empresa"].items():
            self.text.insert(tk.END, f"{key.capitalize()}: {value}\n")
        self.text.insert(tk.END, "\nPropietarios:\n")
        for propietario in data["propietarios"]:
            self.text.insert(tk.END, f"Nombre: {propietario['nombre']}, CURP: {propietario['curp']}, Participación: {propietario['participacion']}\n")
        self.text.insert(tk.END, "\nLicencias y Permisos:\n")
        for file in data["licencias"]:
            self.text.insert(tk.END, f"{file}\n")
        self.text.insert(tk.END, "\nDatos del Dueño Principal:\n")
        for key, value in data["dueno"].items():
            self.text.insert(tk.END, f"{key.capitalize()}: {value}\n")

    def confirm(self):
        messagebox.showinfo("Confirmación", "Todos los datos han sido registrados correctamente.")
        self.controller.root.quit()

# Ejecutar la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    main_menu = MainMenu(root)
    root.mainloop()