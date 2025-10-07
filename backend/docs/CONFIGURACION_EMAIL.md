# Configuración de Email con Gmail - Instrucciones

## Paso 1: Activar Verificación en Dos Pasos

1. Ve a: https://myaccount.google.com/security
2. Inicia sesión con tu cuenta de Gmail
3. Busca "Verificación en dos pasos" y actívala si no la tienes
4. Sigue los pasos de configuración

## Paso 2: Generar Contraseña de Aplicación

1. Ve a: https://myaccount.google.com/apppasswords
2. En "Seleccionar app": Elige "Correo"
3. En "Seleccionar dispositivo": Elige "Otro (nombre personalizado)"
4. Escribe: "Cronify"
5. Haz clic en "Generar"
6. Copia la contraseña de 16 caracteres (sin espacios, ejemplo: "abcd efgh ijkl mnop")

## Paso 3: Configurar el archivo .env

Abre el archivo `.env` en la carpeta `backend` y modifica estas líneas:

```
EMAIL_HOST_USER=tu_email@gmail.com
EMAIL_HOST_PASSWORD=la_contraseña_de_aplicacion_sin_espacios
DEFAULT_FROM_EMAIL=tu_email@gmail.com
```

Ejemplo:
```
EMAIL_HOST_USER=miapp@gmail.com
EMAIL_HOST_PASSWORD=abcdefghijklmnop
DEFAULT_FROM_EMAIL=miapp@gmail.com
```

Importante: Elimina todos los espacios de la contraseña de aplicación.

## Paso 3: Verificar la configuración

Después de configurar el .env, puedes probar que funciona ejecutando:

```bash
cd backend
python manage.py shell
```

Luego en la consola de Python:

```python
from django.core.mail import send_mail

send_mail(
    'Prueba de Cronify',
    'Este es un correo de prueba',
    'tu_email@outlook.com',
    ['tu_email@outlook.com'],
    fail_silently=False,
)
```

Si no hay errores, el correo se envió correctamente.

## Solución de Problemas

### Error: SMTPAuthenticationError
- Verifica que la contraseña de aplicación esté correcta (sin espacios)
- Asegúrate de estar usando una contraseña de aplicación, no tu contraseña normal

### Error: SMTPConnectError
- Verifica tu conexión a internet
- Algunos firewalls bloquean el puerto 587

### No veo la opción de contraseñas de aplicación
- Activa primero la verificación en dos pasos en tu cuenta de Microsoft
- Espera unos minutos después de activar 2FA
