# Configuración de Microsoft OAuth para Cronify

## Resumen

El sistema ahora soporta autenticación con Microsoft OAuth y envío de correos mediante Microsoft Graph API.

## Requisitos

### Credenciales de Azure

Necesitas crear una aplicación en Azure Active Directory y obtener:

1. **Application (Client) ID**
2. **Directory (Tenant) ID**
3. **Client Secret**
4. **Email de Outlook/Microsoft** (para envío de correos)

### Cómo obtener las credenciales

1. Ve a https://portal.azure.com
2. Navega a "Azure Active Directory" > "App registrations"
3. Click en "New registration"
4. Configuración:
   - Nombre: `Cronify`
   - Tipos de cuenta: "Accounts in any organizational directory and personal Microsoft accounts"
   - Redirect URI: `http://localhost:8000/api/auth/microsoft/callback/`
5. Copia el **Application (client) ID** y **Directory (tenant) ID**
6. Ve a "Certificates & secrets" > "New client secret"
7. Copia el valor del secret (solo se muestra una vez)
8. Ve a "API permissions" > "Add a permission" > "Microsoft Graph" > "Delegated permissions"
9. Agrega: `User.Read`, `Mail.Send`, `offline_access`
10. Click en "Grant admin consent"

## Instalación

### 1. Instalar dependencias

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configurar variables de entorno

Edita el archivo `backend/.env` y agrega:

```env
# Microsoft OAuth
MICROSOFT_CLIENT_ID=tu_application_client_id
MICROSOFT_CLIENT_SECRET=tu_client_secret
MICROSOFT_TENANT_ID=common
MICROSOFT_AUTHORITY=https://login.microsoftonline.com/common
MICROSOFT_REDIRECT_URI=http://localhost:8000/api/auth/microsoft/callback/

# Email
EMAIL_HOST_USER=tu_email@outlook.com
DEFAULT_FROM_EMAIL=tu_email@outlook.com
USE_MICROSOFT_GRAPH=True
```

### 3. Ejecutar migraciones

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Verificar configuración

```bash
python verificar_configuracion_microsoft.py
```

### 5. Iniciar el sistema

Terminal 1 - Backend:
```bash
python manage.py runserver
```

Terminal 2 - Celery Worker:
```bash
celery -A cronify_backend worker -l info
```

Terminal 3 - Celery Beat:
```bash
celery -A cronify_backend beat -l info
```

Terminal 4 - Frontend:
```bash
cd ../frontend
npm run dev
```

## Uso

### Login con Microsoft

1. Ve a http://localhost:9000/auth/login
2. Verás dos opciones:
   - Login tradicional (usuario/contraseña)
   - Botón "Iniciar sesión con Microsoft"
3. Click en el botón de Microsoft
4. Serás redirigido a Microsoft para autenticarte
5. Después de autenticarte, volverás a la aplicación ya logueado

### Envío de correos

Los correos se envían automáticamente usando Microsoft Graph API desde la cuenta configurada en `EMAIL_HOST_USER`.

## Producción

Para producción, actualiza en Azure:

1. Agrega la URI de producción: `https://tudominio.com/api/auth/microsoft/callback/`
2. Actualiza `.env` con la nueva URI
3. Configura HTTPS

## Solución de problemas

### Error: redirect_uri_mismatch
Verifica que la URI en Azure coincida exactamente con `MICROSOFT_REDIRECT_URI` en `.env`

### Error: invalid_client
Verifica que `MICROSOFT_CLIENT_ID` y `MICROSOFT_CLIENT_SECRET` sean correctos

### Los correos no se envían
- Verifica que `USE_MICROSOFT_GRAPH=True`
- Verifica que `EMAIL_HOST_USER` sea una cuenta válida de Microsoft
- Verifica que los permisos estén otorgados en Azure

## Arquitectura técnica

### Backend
- `users/microsoft_auth.py` - Servicio de autenticación OAuth
- `users/views.py` - Endpoints de login y callback
- `users/urls.py` - Rutas de autenticación
- `notifications/ms_graph_service.py` - Servicio de envío de correos
- `users/models.py` - Campos para almacenar tokens

### Frontend
- `components/auth/MicrosoftLoginButton.vue` - Botón de login
- `pages/auth/LoginPage.vue` - Página de login con ambas opciones
- `services/authService.js` - Servicios de autenticación
- `router/routes.js` - Ruta de callback

### Flujo de autenticación

1. Usuario click en "Iniciar con Microsoft"
2. Frontend solicita URL de autorización al backend
3. Usuario es redirigido a Microsoft
4. Microsoft redirige de vuelta con código de autorización
5. Backend intercambia código por tokens
6. Backend crea/actualiza usuario con tokens
7. Backend genera JWT para la API
8. Usuario queda autenticado

### Flujo de envío de correos

1. Celery Beat ejecuta tarea diaria (8:00 AM)
2. Busca eventos próximos a vencer
3. Para cada recordatorio:
   - Obtiene token de acceso de Microsoft
   - Llama a Microsoft Graph API
   - Envía correo desde la cuenta configurada
