# Guía de Pruebas Sin Credenciales de Azure

## Pruebas que puedes hacer sin configurar Azure

### 1. Verificar instalación del backend

```bash
cd backend
pip install -r requirements.txt
```

Deberías ver que se instalan las nuevas dependencias:
- msal
- django-allauth  
- requests

### 2. Verificar estructura de base de datos

```bash
python manage.py makemigrations
python manage.py migrate
```

Esto debería crear las migraciones para los nuevos campos:
- microsoft_id
- microsoft_access_token
- microsoft_refresh_token

### 3. Verificar el modelo de Usuario

```bash
python manage.py shell
```

Luego en la shell:
```python
from users.models import Usuario
print(Usuario._meta.get_fields())
# Deberías ver los campos microsoft_id, microsoft_access_token, microsoft_refresh_token
```

### 4. Verificar frontend

```bash
cd frontend
npm install
npm run dev
```

Ve a http://localhost:9000/auth/login

Deberías ver:
- El formulario de login tradicional
- Un separador "O"
- El botón "Iniciar sesión con Microsoft" (deshabilitado si no hay credenciales)

### 5. Verificar que el registro tradicional sigue funcionando

1. Ve a http://localhost:9000/auth/register
2. Crea un usuario con el formulario tradicional
3. Inicia sesión con ese usuario
4. Verifica que puedes acceder al sistema normalmente

### 6. Verificar endpoints de la API

Con el backend corriendo, verifica que existen los nuevos endpoints:

```bash
curl http://localhost:8000/api/auth/microsoft/login/
```

Debería devolver un error 500 (porque no hay credenciales), pero confirma que el endpoint existe.

## Lo que NO funcionará sin credenciales

- Login con Microsoft (necesita credenciales de Azure)
- Envío de correos con Microsoft Graph API (necesita credenciales)
- Callback de Microsoft OAuth (necesita App Registration en Azure)

## Lo que SÍ funcionará sin credenciales

- Login tradicional usuario/contraseña
- Registro de usuarios
- Creación y gestión de eventos
- Todas las funciones principales del sistema
- Envío de correos con SMTP (si configuras Gmail u otro)

## Configurar SMTP alternativo (Gmail)

Si quieres probar el envío de correos sin Microsoft:

1. Edita `.env`:
```env
USE_MICROSOFT_GRAPH=False
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu_email@gmail.com
EMAIL_HOST_PASSWORD=tu_contraseña_de_aplicación
DEFAULT_FROM_EMAIL=tu_email@gmail.com
```

2. Reinicia el servidor y Celery

3. Los correos se enviarán por Gmail en lugar de Microsoft Graph

## Verificar que no hay errores en el código

```bash
cd backend
python manage.py check
```

Debería mostrar "System check identified no issues"

## Próximos pasos cuando tengas credenciales

1. Obtener credenciales de Azure (ver CONFIGURACION_MICROSOFT.md)
2. Configurar variables en `.env`
3. Probar login con Microsoft
4. Probar envío de correos con Graph API
