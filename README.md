# Cronify - Sistema de Gestión de Vencimientos

Aplicación web para gestión, seguimiento y notificación proactiva de vencimientos de registros, eventos y actividades críticas.

## Características Principales

- Gestión completa de eventos con fechas de vencimiento
- Notificaciones automáticas por correo electrónico
- Sistema de búsqueda y filtrado avanzado
- Gestión de usuarios y perfiles
- Archivos adjuntos con límites de tamaño
- Soft delete (eliminación lógica)
- API RESTful completa
- Autenticación JWT (24 horas)

## Instalación

### 1. Crear entorno virtual

```bash
cd backend
python -m venv venv
venv\Scripts\activate  # En Windows
source venv/bin/activate  # En Linux/Mac
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Configurar variables de entorno

Copia `.env.example` a `.env` y edita con tus credenciales:

```env
# Email Configuration
EMAIL_HOST_USER=tu_email@gmail.com
EMAIL_HOST_PASSWORD=tu_contraseña_de_aplicacion
DEFAULT_FROM_EMAIL=tu_email@gmail.com
```

Ver instrucciones detalladas en: `backend/docs/CONFIGURACION_EMAIL.md`

### 4. Configurar base de datos

Asegúrate de tener PostgreSQL instalado y corriendo.

```bash
python manage.py migrate
```

### 5. Crear superusuario

```bash
python manage.py createsuperuser
```

## Ejecutar el Proyecto

### Servidor de desarrollo

```bash
python manage.py runserver
```

El servidor estará disponible en: http://localhost:8000

### Celery Worker y Beat (para notificaciones automáticas)

En terminales separadas:

```bash
# Terminal 1: Worker
celery -A cronify_backend worker -l info

# Terminal 2: Beat (scheduler)
celery -A cronify_backend beat -l info
```

## API Endpoints

### Autenticación

- `POST /api/auth/register/` - Registro de usuarios
- `POST /api/token/` - Login (obtener JWT)
- `POST /api/token/refresh/` - Refrescar token
- `GET /api/auth/profile/` - Ver perfil
- `PUT /api/auth/profile/` - Editar perfil
- `POST /api/auth/change-password/` - Cambiar contraseña

### Eventos

- `GET /api/eventos/` - Listar eventos (con búsqueda y filtros)
- `POST /api/eventos/` - Crear evento
- `GET /api/eventos/{id}/` - Ver evento específico
- `PUT /api/eventos/{id}/` - Actualizar evento
- `DELETE /api/eventos/{id}/` - Eliminar evento (soft delete)
- `POST /api/eventos/{id}/upload_file/` - Subir archivo adjunto

### Parámetros de Búsqueda y Filtrado

- `?search=texto` - Busca en asunto y descripción
- `?fecha_inicio=YYYY-MM-DDTHH:MM:SSZ` - Filtrar desde fecha
- `?fecha_fin=YYYY-MM-DDTHH:MM:SSZ` - Filtrar hasta fecha
- `?creador=ID` - Filtrar por creador
- `?notificado=true/false` - Filtrar por estado de notificación

Ejemplo:
```
GET /api/eventos/?search=licencia&notificado=false&fecha_inicio=2025-11-01T00:00:00Z
```

Ver documentación completa en: `backend/docs/API_ENDPOINTS.md`

## Validaciones

### Usuario
- Contraseña: Mínimo 8 caracteres
- Email: Único en el sistema

### Evento
- Asunto: 5-200 caracteres
- Fecha de vencimiento: Debe ser futura
- Notificación valor: >= 1
- Archivo individual: Máximo 10MB
- Total archivos por evento: Máximo 50MB

## Estructura del Proyecto

```
backend/
├── cronify_backend/     # Configuración principal
│   ├── settings.py      # Configuración de Django
│   ├── urls.py          # URLs principales
│   ├── celery.py        # Configuración de Celery
│   └── wsgi.py
├── users/               # Gestión de usuarios
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
├── records/             # Gestión de eventos
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── permissions.py
│   └── urls.py
├── notifications/       # Sistema de notificaciones
│   ├── tasks.py         # Tareas de Celery
│   └── email_service.py
├── docs/                # Documentación
│   ├── API_ENDPOINTS.md
│   ├── CONFIGURACION_EMAIL.md
│   ├── ESTADO_PROYECTO.md
│   └── VALIDACIONES_IMPLEMENTADAS.md
├── media/               # Archivos subidos
├── .env                 # Variables de entorno
├── .env.example
├── .gitignore
├── manage.py
└── requirements.txt
```

## Tecnologías

- **Backend**: Django 5.1.1
- **API**: Django REST Framework 3.15.2
- **Base de Datos**: PostgreSQL
- **Autenticación**: JWT (djangorestframework-simplejwt)
- **Tareas Asíncronas**: Celery 5.4.0
- **Cola de Mensajes**: Redis 5.0.8
- **Email**: SMTP (Gmail)
- **Gestión de Configuración**: python-decouple

## Documentación Adicional

- `backend/docs/API_ENDPOINTS.md` - Documentación completa de la API
- `backend/docs/VALIDACIONES_IMPLEMENTADAS.md` - Lista de validaciones
- `backend/docs/CONFIGURACION_EMAIL.md` - Configuración de email
- `backend/docs/ESTADO_PROYECTO.md` - Estado actual del desarrollo

## Características Implementadas

- Autenticación y autorización completa
- CRUD completo de eventos
- Sistema de notificaciones automáticas
- Búsqueda y filtrado avanzado
- Gestión de archivos adjuntos
- Soft delete
- Paginación
- Validaciones robustas
- Gestión de perfil de usuario

## Estado del Proyecto

**Progreso: 85-90% completo**

Ver detalles en: `backend/docs/ESTADO_PROYECTO.md`

## Licencia

Proyecto académico/personal
