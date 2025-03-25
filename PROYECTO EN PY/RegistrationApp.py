import tkinter as tk
from tkinter import messagebox, filedialog, ttk

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