import tkinter as tk

class AdminMainWindow:
    def __init__(self, master, username):
        self.master = master
        master.title("Panel de Administración")
        tk.Label(master, text=f"Bienvenido administrador {username}", font=("Arial", 14)).pack(pady=20)
        # Aquí puedes agregar botones, menús y acciones para administrar usuarios, ver reportes, etc.
    