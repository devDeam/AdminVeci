# AdminVeci

AdminVeci es una aplicación de escritorio desarrollada en Python para la gestión de propiedad horizontal. Ofrece una interfaz gráfica para la administración y operación de inquilinos, pagos, facturación y autenticación de usuarios, conectándose con un backend construido en FastAPI y una base de datos MongoDB.

## Características

- 🧑‍💼 Interfaz diferenciada para administradores y trabajadores
- 🏠 Gestión de inquilinos (crear, editar, eliminar, buscar)
- 💸 Registro y control de pagos de administración
- 📄 Generación y envío de facturas por correo electrónico
- 🔐 Inicio de sesión con validación de credenciales
- ☁️ Conexión a MongoDB Atlas desde el backend

## Estructura del Proyecto

```
AdminVeci/
├── backend/
│   ├── main.py              # Punto de entrada de FastAPI
│   └── db/
│       ├── database.py      # Conexión a MongoDB
│       ├── init_db.py       # Inicialización de la DB
│       └── models/          # Modelos Pydantic
│           ├── tenant.py
│           ├── user.py
│           └── payments.py
├── frontend/
│   ├── main.py              # Inicia la GUI
│   ├── api_client/
│   │   └── tenant_client.py # Cliente HTTP para consumir la API
│   └── gui/                 # Interfaz gráfica con Tkinter
│       ├── login_view.py
│       ├── main_admin_view.py
│       ├── main_worker_view.py
│       ├── tenant_form.py
│       ├── tenant_modals.py
├── requirements.txt
├── .env                     # Variables de entorno
└── .gitignore
```

## Instalación

1. Clona el repositorio:
```bash
git clone https://github.com/tuusuario/AdminVeci.git
cd AdminVeci
```

2. Crea y activa un entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instala las dependencias:
```bash
pip install -r requirements.txt
```

4. Crea un archivo `.env` con tus variables de conexión a MongoDB y configuración SMTP (correo electrónico).
```MONGO_URI="mongodb+srv://<db_username>:<db_password>@proyectofinal-6315.87hywsi.mongodb.net/?retryWrites=true&w=majority&appName=ProyectoFinal-6315"
DB_NAME="ProyectoFinal"
SMTP_SERVER="smtp.gmail.com"
SMTP_PORT=587
SENDER_EMAIL=
SENDER_PASSWORD = "
```
  Configurar envío de correos con Gmail
  
  Para poder enviar correos desde tu cuenta de Gmail usando `smtplib`, necesitas generar una contraseña de aplicación. Sigue estos pasos:
  
  1. Accede a tu cuenta de Google y entra a [https://myaccount.google.com/security](https://myaccount.google.com/security).
  2. En la sección **"Inicio de sesión en Google"**, asegúrate de tener activada la **verificación en dos pasos**.
  3. Una vez activada, vuelve a la sección de seguridad y haz clic en **"Contraseñas de aplicaciones"**.
  4. Selecciona **"Correo"** como la aplicación y **"Otro"** para poner un nombre personalizado (por ejemplo: `AdminVeciApp`).
  5. Google te dará una contraseña de 16 caracteres. Guarda esta contraseña, la necesitarás para enviar correos.
  
  Uso en tu archivo `.env`
  
  Agrega esta contraseña y tu correo remitente al archivo `.env` del proyecto.
   

## Uso
Para usar la aplicación en simultaneo, puedes dividir la terminal de tu editor de código y seguir los pasos para la ejecución del proyecto:

1. Ejecuta el backend:
```bash
cd backend
uvicorn main:app --reload
```

2. Ejecuta la interfaz gráfica:
```bash
cd ../frontend
python main.py
```

## Tecnologías

- 🐍 Python
- ⚡ FastAPI
- 🍃 MongoDB (Atlas)
- 🖼️ Tkinter o PyQt (según GUI)
- 📧 smtplib/email (para facturas)

## Contribuciones

¡Contribuciones son bienvenidas! Abre un issue o haz un pull request.

## Licencia

Este proyecto está licenciado bajo la Licencia MIT. Consulta el archivo [LICENSE](./LICENSE) para más información.
