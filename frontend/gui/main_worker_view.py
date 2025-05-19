import tkinter as tk
from tkinter import ttk, messagebox
import requests
from gui.tenant_modals import (
    open_edit_tenant_modal,
    open_confirm_delete_modal,
    open_register_payment_modal,
    center_window
)

class WorkerMainWindow:
    def __init__(self, master, username, benefits):
        self.master = master
        self.benefits = benefits
        master.title(f"Bienvenido {username}, actualmente sus funciones son: {benefits}")
        master.geometry("1040x500")

        self.build_ui()
        self.load_tenants()

    def build_ui(self):
        # Filtro de búsqueda
        search_frame = tk.Frame(self.master)
        search_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(search_frame, text="Buscar:").pack(side="left")
        self.search_entry = tk.Entry(search_frame)
        self.search_entry.pack(side="left", padx=5)
        tk.Button(search_frame, text="🔍", command=self.search_tenants).pack(side="left")

        # Tabla
        self.tree = ttk.Treeview(self.master, columns=("uid", "name", "email", "apt", "acct_status"), show="headings")
        self.tree.heading("uid", text="Número de identificación")
        self.tree.heading("name", text="Nombre")
        self.tree.heading("email", text="Correo")
        self.tree.heading("apt", text="Apartamento")
        self.tree.heading("acct_status", text="Deuda")
        self.tree.pack(fill="both", expand=True, padx=10, pady=5)

        # Columna de acciones (simulada)
        self.tree.bind("<Double-1>", self.on_double_click)

    def load_tenants(self, search_term=""):
        try:
            url = f"http://localhost:8000/tenants"
            if search_term:
                url += f"?search={search_term}"

            response = requests.get(url)
            data = response.json()

            self.tree.delete(*self.tree.get_children())
            for tenant in data:
                deuda = tenant.get("acct_status", 0)
                deuda_formateada = f"${deuda:,.0f}".replace(",", ".")  # Ej: 123456 → $123.456

                self.tree.insert("", "end", iid=tenant["_id"], values=(
                    tenant.get("uid", ""),
                    tenant.get("name", ""),
                    tenant.get("email", ""),
                    tenant.get("apt", ""),
                    deuda_formateada,
                ))

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo obtener la lista de inquilinos.\n{e}")

    def search_tenants(self):
        search_term = self.search_entry.get().strip()
        self.load_tenants(search_term)

    def on_double_click(self, event):
        selected = self.tree.selection()
        if not selected:
            return

        tenant_id = selected[0]
        tenant_values = self.tree.item(tenant_id, "values")
        uid, name, _, _, acct_status_str = tenant_values

        # Extraer el valor numérico de la deuda (ej: "$123.456" -> 123456)
        current_debt = int(acct_status_str.replace("$", "").replace(".", "").replace(",", ""))

        modal = tk.Toplevel(self.master)
        modal.title(f"Acciones para UID {uid}")
        center_window(modal, 400, 300)
        modal.transient(self.master)
        modal.grab_set()

        frame = tk.Frame(modal)
        frame.pack(expand=True, fill="both", padx=20, pady=20)

        tk.Label(frame, text=f"Seleccione una acción para {name}").pack(pady=10)

        tk.Button(frame, text="✏️ Editar", width=25,
                command=lambda: [modal.destroy(), open_edit_tenant_modal(self.master, tenant_id, tenant_values, self.search_tenants)]
                ).pack(pady=5)

        tk.Button(frame, text="🗑️ Eliminar", width=25,
                command=lambda: [modal.destroy(), open_confirm_delete_modal(self.master, tenant_id, name, self.search_tenants)]
                ).pack(pady=5)

        tk.Button(frame, text="💵 Registrar Pago", width=25,
                command=lambda: [modal.destroy(), open_register_payment_modal(self.master, uid, name, current_debt, self.search_tenants)]
                ).pack(pady=5)

        tk.Button(frame, text="Cancelar", width=25, command=modal.destroy).pack(pady=15)

#root = tk.Tk()
#login_view = WorkerMainWindow(root, 'prueba', 'basic')
#root.mainloop()