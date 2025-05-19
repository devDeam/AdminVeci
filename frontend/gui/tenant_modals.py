import tkinter as tk
from tkinter import messagebox
import requests

def center_window(win, width=400, height=300):
    win.update_idletasks()
    x = win.winfo_screenwidth() // 2 - width // 2
    y = win.winfo_screenheight() // 2 - height // 2
    win.geometry(f"{width}x{height}+{x}+{y}")

def open_edit_tenant_modal(master, tenant_id, tenant_data, refresh_callback):
    uid, name, email, apt, _ = tenant_data

    win = tk.Toplevel(master)
    win.title(f"Editar inquilino {uid}")
    center_window(win, 300, 200)
    win.transient(master)
    win.grab_set()

    frame = tk.Frame(win)
    frame.pack(expand=True, fill="both", padx=20, pady=20)

    fields = {}
    for i, (label, value) in enumerate([
        ("name", name),
        ("email", email),
        ("apt", apt)
    ]):
        tk.Label(frame, text=label).grid(row=i, column=0, padx=10, pady=5, sticky="e")
        entry = tk.Entry(frame)
        entry.insert(0, value)
        entry.grid(row=i, column=1, padx=10, pady=5)
        fields[label.lower()] = entry

    def submit():
        updated_data = {
            "name": fields["name"].get(),
            "email": fields["email"].get(),
            "apt": fields["apt"].get()
        }

        try:
            response = requests.put(f"http://localhost:8000/tenants/{tenant_id}", json=updated_data)
            if response.status_code == 200:
                messagebox.showinfo("Éxito", "Inquilino actualizado correctamente.")
                win.destroy()
                refresh_callback()
            else:
                messagebox.showerror("Error", f"Error al actualizar: {response.json().get('detail')}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo conectar al servidor.\n{e}")

    tk.Button(frame, text="Guardar cambios", command=submit).grid(row=4, column=0, columnspan=2, pady=15)

def open_confirm_delete_modal(master, tenant_id, tenant_name, refresh_callback):
    if not messagebox.askyesno("Confirmar eliminación", f"¿Estás seguro de eliminar a {tenant_name}?"):
        return

    try:
        response = requests.delete(f"http://localhost:8000/tenants/{tenant_id}")
        if response.status_code == 200:
            messagebox.showinfo("Eliminado", "Inquilino eliminado correctamente.")
            refresh_callback()
        else:
            messagebox.showerror("Error", response.json().get("detail", "No se pudo eliminar."))
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo conectar al servidor.\n{e}")

def open_register_payment_modal(master, tenant_uid, tenant_name, current_debt, refresh_callback):
    win = tk.Toplevel(master)
    win.title(f"Registrar pago - {tenant_name}")
    center_window(win, 350, 270)
    win.transient(master)
    win.grab_set()

    frame = tk.Frame(win)
    frame.pack(expand=True, fill="both", padx=20, pady=20)

    # Etiquetas informativas
    tk.Label(frame, text=f"Inquilino: {tenant_name}").pack(pady=5)
    
    deuda_formateada = f"${current_debt:,.0f}".replace(",", ".")
    tk.Label(frame, text=f"Deuda actual: {deuda_formateada}").pack(pady=5)

    # Campo de monto
    tk.Label(frame, text="Monto del pago (COP):").pack(pady=5)
    amount_entry = tk.Entry(frame)
    amount_entry.pack(pady=5)

    def submit_payment():
        try:
            amount = float(amount_entry.get())
            if amount <= 0:
                raise ValueError("Monto inválido")

            if not messagebox.askyesno("Confirmar pago", f"¿Registrar pago de ${amount:,.0f}?"):
                return

            response = requests.post(
                f"http://localhost:8000/tenants/{tenant_uid}/pay",
                json={"amount": amount}
            )
            if response.status_code == 200:
                messagebox.showinfo("Éxito", "Pago registrado y factura generada.")
                win.destroy()
                refresh_callback()
            else:
                detail = response.json().get("detail", "Error desconocido.")
                messagebox.showerror("Error", f"No se pudo registrar el pago.\n{detail}")
        except ValueError:
            messagebox.showwarning("Monto inválido", "Ingrese un monto mayor a cero.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo conectar al servidor.\n{e}")

    tk.Button(frame, text="Registrar y enviar factura", command=submit_payment).pack(pady=20)


