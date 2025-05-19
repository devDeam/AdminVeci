from datetime import datetime
from uuid import uuid4
from db.database import db
from services.email_service import send_invoice_email

def register_payment(tenant_uid: str, amount: float):
    timestamp = datetime.now()
    invoice_id = f"FACT-{uuid4().hex[:8].upper()}"

    # Obtener los datos del inquilino
    tenant = db["tenants"].find_one({"uid": tenant_uid})
    if not tenant:
        raise ValueError("Inquilino no encontrado")

    # Deuda anterior y nueva deuda
    deuda_anterior = tenant.get("acct_status", 0)
    nueva_deuda = deuda_anterior - amount

    # Actualizar deuda del inquilino
    db["tenants"].update_one(
        {"uid": tenant_uid},
        {"$set": {"acct_status": nueva_deuda}}
    )
    
    # Prepara el diccionario con toda la info de la factura
    invoice = {
        "invoice_id": invoice_id,
        "tenant_uid": tenant_uid,
        "tenant_name": tenant.get("name", ""),
        "tenant_email": tenant.get("email", ""),
        "tenant_apt": tenant.get("apt", ""),
        "tenant_document": tenant.get("uid", ""),
        "previous_balance": deuda_anterior,
        "payment_amount": amount,
        "new_balance": nueva_deuda,
        "date": timestamp,
        "status": "pending_email",
        "description": "Pago registrado para generación y envío de factura"
    }

    # Inserta la factura en la BD
    db["invoices"].insert_one(invoice)

    # Enviar correo con el diccionario completo
    correo_enviado = send_invoice_email(invoice)

    # Actualizar estado
    nuevo_estado = "sent" if correo_enviado else "email_failed"
    db["invoices"].update_one({"invoice_id": invoice_id}, {"$set": {"status": nuevo_estado}})

    return {
        "message": "Pago registrado correctamente.",
        "invoice_id": invoice_id,
        "timestamp": timestamp,
        "previous_balance": deuda_anterior,
        "new_balance": nueva_deuda
    }
