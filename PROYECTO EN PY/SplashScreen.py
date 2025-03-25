import tkinter as tk
from tkinter import Label, ttk
import random
from MainMenu import MainMenu

class SplashScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("DetectSensePrism")
        self.root.geometry("600x350")
        self.root.configure(bg="#1F1F2E")
        self.root.overrideredirect(True)
        self.root.attributes("-alpha", 0.95)

        # Gradiente de fondo simulado (líneas suaves tipo prisma)
        self.canvas = tk.Canvas(self.root, width=600, height=350, highlightthickness=0, bg="#1F1F2E")
        self.canvas.place(x=0, y=0)
        for i in range(0, 600, 10):
            color = random.choice(["#81A1C1", "#88C0D0", "#A3BE8C", "#D08770", "#B48EAD"])
            self.canvas.create_line(i, 0, i - 100, 350, fill=color, stipple="gray50")

        # Fuentes modernas
        self.title_font = ("Helvetica", 64, "bold")
        self.subtitle_font = ("Helvetica", 28, "italic")

        # Etiquetas con resplandor simulado
        self.dsp_label = Label(root, text="DSP", font=self.title_font, fg="#ECEFF4", bg="#1F1F2E")
        self.dsp_label.place(relx=0.5, rely=0.35, anchor="center")

        self.system_label = Label(root, text="System", font=self.subtitle_font, fg="#ECEFF4", bg="#1F1F2E")
        self.system_label.place(relx=0.5, rely=0.60, anchor="center")

        # Barra de progreso moderna con estilo prisma
        style = ttk.Style()
        style.theme_use("default")
        style.configure("modern.Horizontal.TProgressbar",
                        troughcolor="#3B4252", 
                        bordercolor="#3B4252",
                        background="#88C0D0",
                        lightcolor="#81A1C1",
                        darkcolor="#5E81AC")

        self.progress = ttk.Progressbar(root, orient="horizontal", length=320, mode="determinate",
                                        style="modern.Horizontal.TProgressbar")
        self.progress.place(relx=0.5, rely=0.80, anchor="center")

        self.animate_text()
        self.update_progress()
        self.center_window()

    def animate_text(self):
        colors = ["#88C0D0", "#81A1C1", "#5E81AC", "#BF616A", "#D08770", "#EBCB8B", "#A3BE8C"]
        self.dsp_label.config(fg=random.choice(colors))
        self.system_label.config(fg=random.choice(colors))
        self.root.after(700, self.animate_text)

    def update_progress(self):
        if self.progress["value"] < 100:
            self.progress["value"] += 10
            self.root.after(400, self.update_progress)
        else:
            self.fade_out()

    def fade_out(self):
        alpha = self.root.attributes("-alpha")
        if alpha > 0:
            alpha -= 0.05
            self.root.attributes("-alpha", alpha)
            self.root.after(80, self.fade_out)
        else:
            self.root.destroy()
            root = tk.Tk()
            main_menu = MainMenu(root)
            root.mainloop()

    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

if __name__ == "__main__":
    root = tk.Tk()
    splash = SplashScreen(root)
    root.mainloop()
