import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import requests
from gui.main_admin_view import AdminMainWindow
from gui.main_worker_view import WorkerMainWindow

class LoginView:
    def __init__(self, master):
        self.master = master
        master.title("Gestión de Usuarios")

        notebook = ttk.Notebook(master)
        notebook.pack(padx=10, pady=10, fill="both", expand=True)

        # Crear pestañas
        self.login_frame = tk.Frame(notebook)
        self.register_frame = tk.Frame(notebook)

        notebook.add(self.login_frame, text="Iniciar Sesión")
        notebook.add(self.register_frame, text="Registrar Usuario")

        self.build_login_tab()
        self.build_register_tab()

    def build_login_tab(self):
        # Configurar las columnas para que se expandan proporcionalmente
        self.login_frame.grid_columnconfigure(0, weight=1)
        self.login_frame.grid_columnconfigure(1, weight=1)

        # Etiqueta y campo de usuario
        tk.Label(self.login_frame, text="Usuario:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.login_username_entry = tk.Entry(self.login_frame)
        self.login_username_entry.grid(row=0, column=1, padx=5, pady=5)

        # Etiqueta y campo de contraseña
        tk.Label(self.login_frame, text="Contraseña:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.login_password_entry = tk.Entry(self.login_frame, show="*")
        self.login_password_entry.grid(row=1, column=1, padx=5, pady=5)

        # Botón de inicio de sesión, centrado pero con tamaño ajustado
        login_btn = tk.Button(self.login_frame, text="Iniciar sesión", command=self.login)
        login_btn.grid(row=2, column=0, columnspan=2, pady=10)  # Sin sticky para no estirar

    def build_register_tab(self):
        tk.Label(self.register_frame, text="Nombre:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.reg_name_entry = tk.Entry(self.register_frame)
        self.reg_name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.register_frame, text="Apellido:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.reg_lastname_entry = tk.Entry(self.register_frame)
        self.reg_lastname_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.register_frame, text="Número de documento:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.reg_uid_entry = tk.Entry(self.register_frame)
        self.reg_uid_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(self.register_frame, text="Usuario:").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        self.reg_username_entry = tk.Entry(self.register_frame)
        self.reg_username_entry.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(self.register_frame, text="Correo:").grid(row=4, column=0, sticky="e", padx=5, pady=5)
        self.reg_email_entry = tk.Entry(self.register_frame)
        self.reg_email_entry.grid(row=4, column=1, padx=5, pady=5)

        tk.Label(self.register_frame, text="Contraseña:").grid(row=5, column=0, sticky="e", padx=5, pady=5)
        self.reg_password_entry = tk.Entry(self.register_frame, show="*")
        self.reg_password_entry.grid(row=5, column=1, padx=5, pady=5)

        tk.Label(self.register_frame, text="Rol:").grid(row=6, column=0, sticky="e", padx=5, pady=5)
        self.reg_role_combo = ttk.Combobox(self.register_frame, values=["admin", "trabajador"], state="readonly")
        self.reg_role_combo.set("trabajador")  # valor por defecto
        self.reg_role_combo.grid(row=6, column=1, padx=5, pady=5)

        register_btn = tk.Button(self.register_frame, text="Registrar Usuario", command=self.register)
        register_btn.grid(row=7, column=0, columnspan=2, pady=10)

    def login(self):
        username = self.login_username_entry.get()
        password = self.login_password_entry.get()

        if not username or not password:
            messagebox.showwarning("Campos vacíos", "Completa todos los campos para iniciar sesión.")
            return

        try:
            response = requests.post("http://localhost:8000/auth/login", json={
                "username": username,
                "password": password
            })
            data = response.json()

            if response.status_code == 200 and data.get("success"):
                role = data.get("role")
                messagebox.showinfo(f"Bienvenido {username}", f"Inicio de sesión exitoso con funcionalidades {role}")

                self.master.destroy()  # Cerrar la ventana actual

                # Abrir la nueva ventana según el rol
                new_root = tk.Tk()
                if role == "admin":
                    AdminMainWindow(new_root, username, role)
                else:
                    WorkerMainWindow(new_root, username, role)
                new_root.mainloop()

            else:
                messagebox.showerror("Error", data.get("message", "Error al iniciar sesión."))
                self.clear_login_fields()

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo conectar al servidor.\n{e}")
            self.clear_login_fields()

    def register(self):
        name = self.reg_name_entry.get()
        lastName = self.reg_lastname_entry.get()
        uid = self.reg_uid_entry.get()
        username = self.reg_username_entry.get()
        email = self.reg_email_entry.get()
        password = self.reg_password_entry.get()
        role = self.reg_role_combo.get()
        role = self.reg_role_combo.get()
        if role == "trabajador":
            role = "basic"

        if not username or not email or not password or not role:
            messagebox.showwarning("Campos vacíos", "Completa todos los campos para registrar.")
            return

        try:
            response = requests.post("http://localhost:8000/auth/register", json={
                "name": name,
                "lastName": lastName,
                "uid": uid,
                "username": username,
                "email": email,
                "password": password,
                "role": role
            })
            data = response.json()

            if response.status_code == 200 and data.get("success"):
                messagebox.showinfo("Registro Exitoso", "Usuario registrado correctamente.")
                self.clear_register_fields()
            else:
                messagebox.showerror("Error", data.get("message", "No se pudo registrar."))
                self.clear_register_fields()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo conectar al servidor.\n{e}")
            self.clear_register_fields()

    def clear_login_fields(self):
        self.login_username_entry.delete(0, tk.END)
        self.login_password_entry.delete(0, tk.END)

    def clear_register_fields(self):
        self.reg_name_entry.delete(0, tk.END)
        self.reg_lastname_entry.delete(0, tk.END)
        self.reg_uid_entry.delete(0, tk.END)
        self.reg_username_entry.delete(0, tk.END)
        self.reg_email_entry.delete(0, tk.END)
        self.reg_password_entry.delete(0, tk.END)
        self.reg_role_combo.set("basic")
