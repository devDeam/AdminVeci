import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import os

load_dotenv()

SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")

def send_invoice_email(invoice: dict):
    recipient = invoice["tenant_email"]
    subject = f"Factura de pago - {invoice['invoice_id']}"

    # Ruta absoluta desde el archivo actual hacia la plantilla
    current_dir = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(current_dir, "..", "templates", "invoice_template.html")

    with open(template_path, "r", encoding="utf-8") as f:
        html_template = f.read()

    # Reemplazar variables en plantilla
    html_body = html_template.replace("{{tenant_name}}", invoice["tenant_name"])\
                             .replace("{{invoice_id}}", invoice["invoice_id"])\
                             .replace("{{tenant_apt}}", invoice["tenant_apt"])\
                             .replace("{{tenant_document}}", invoice["tenant_document"])\
                             .replace("{{previous_balance}}", f"{invoice['previous_balance']:,.0f}".replace(",", "."))\
                             .replace("{{payment_amount}}", f"{invoice['payment_amount']:,.0f}".replace(",", "."))\
                             .replace("{{new_balance}}", f"{invoice['new_balance']:,.0f}".replace(",", "."))\
                             .replace("{{date}}", invoice["date"].strftime("%Y-%m-%d %H:%M:%S"))

    message = EmailMessage()
    message["From"] = SENDER_EMAIL
    message["To"] = recipient
    message["Subject"] = subject
    message.set_content("Este correo contiene una factura en formato HTML. Por favor, visualízalo en un cliente compatible.")  # Texto plano por si no carga HTML
    message.add_alternative(html_body, subtype="html")

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
            smtp.starttls()
            smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
            smtp.send_message(message)
        return True
    except Exception as e:
        print("Error al enviar el correo:", e)
        return False
