# 📅 Cronify - Sistema de Gestión de Vencimientos

> **Sistema web completo para gestión, seguimiento y notificación proactiva de vencimientos de eventos y actividades críticas.**

<div align="center">

![Estado](https://img.shields.io/badge/Estado-Producción%20Ready-success)
![Backend](https://img.shields.io/badge/Backend-Django%205.1-092E20?logo=django)
![Frontend](https://img.shields.io/badge/Frontend-Vue%203%20+%20Quasar-1976D2?logo=vue.js)
![Database](https://img.shields.io/badge/Database-PostgreSQL-316192?logo=postgresql)
![License](https://img.shields.io/badge/License-MIT-blue)

</div>

---


## 📋 Tabla de Contenidos

- [Características](#-características)
- [Capturas de Pantalla](#-capturas-de-pantalla)
- [Tecnologías](#-tecnologías)
- [Requisitos Previos](#-requisitos-previos)
- [Instalación](#-instalación)
  - [Backend (Django)](#1-backend-django)
  - [Frontend (Vue + Quasar)](#2-frontend-vue--quasar)
- [Configuración](#-configuración)
  - [Microsoft OAuth y Graph API](#configuración-de-microsoft-oauth-recomendado)
  -  - [Pruebas sin Azure](#pruebas-sin-azure)
- [Ejecución](#-ejecución)
- [API Endpoints](#-api-endpoints)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Características Técnicas](#-características-técnicas)
- [Validaciones](#validaciones)
- [Resumen de Cambios](#resumen-de-cambios)
- [Troubleshooting y Preguntas Frecuentes](#-troubleshooting-y-preguntas-frecuentes)
- [Roadmap](#-roadmap)
- [Contribuir](#-contribuir)
- [Licencia](#-licencia)

---

## ✨ Características

### 🎯 Funcionalidades Principales

- ✅ **Gestión Completa de Eventos**
  - Crear, editar, eliminar y visualizar eventos
  - Calendario interactivo con vista mensual
  - Lista de eventos con paginación (20 por página)
  - Vista de detalle completa de eventos

- 🔔 **Sistema de Notificaciones**
  - Notificaciones automáticas por email
  - Configuración personalizada (minutos, horas, días, semanas)
  - Notificaciones en tiempo real en el header
  - Programación automática con Celery Beat (8:00 AM diario)

- 🔍 **Búsqueda y Filtros Avanzados**
  - Búsqueda instantánea con debounce (500ms)
  - Filtros por fecha, creador, estado de notificación
  - Búsqueda en asunto y descripción

- Autenticación JWT (tokens de 24 horas)
  - Login con Microsoft OAuth (Outlook/Hotmail)
  - Registro tradicional (usuario/contraseña)
  - Perfil de usuario con estadísticas
  - Cambio de contraseña
  - Permisos granulares (solo el creador puede editar/eliminar)

- 📎 **Archivos Adjuntos**
  - Subida múltiple con drag & drop
  - Validación: 10MB por archivo, 50MB por evento
  - Soporte para PDF, imágenes, documentos
  - Descarga directa de archivos

- 🎨 **Interfaz Moderna**
  - Diseño Material Design (Quasar Framework)
  - Gradiente azul profesional (#1976d2 → #1565c0)
  - Transiciones suaves y animaciones
  - Responsive design (móvil, tablet, desktop)
  - Estados de hover interactivos

- 🔐 **Seguridad**
  - Soft delete (eliminación lógica)
  - Validaciones robustas en frontend y backend
  - Protección CSRF
  - Variables de entorno para secretos

---


## � Capturas de Pantalla

<div align="center">

<img src="screenshots/pantallageneral.png" alt="Pantalla General" width="600" />
<br/>
<img src="screenshots/pantallaeventos.png" alt="Lista de Eventos" width="600" />
<br/>
<img src="screenshots/pantallacrearevento.png" alt="Crear Evento" width="600" />
<br/>
<img src="screenshots/pantallaeditarevento.png" alt="Editar Evento" width="600" />
<br/>
<img src="screenshots/pantallaperfil.png" alt="Perfil de Usuario" width="600" />
<br/>
<img src="screenshots/sistemanotificaciones.png" alt="Sistema de Notificaciones" width="600" />

</div>

---



---

## 🛠️ Tecnologías

### Backend
- **Framework**: Django 5.1.1
- **API**: Django REST Framework 3.15.2
- **Base de Datos**: PostgreSQL 16
- **Autenticación**: JWT + Microsoft OAuth 2.0
- **Tareas Asíncronas**: Celery 5.4.0 + Redis 5.0.8
- **Email**: Microsoft Graph API (Outlook) / SMTP
- **OAuth**: MSAL + Django Allauth
- **Configuración**: python-decouple

### Frontend
- **Framework**: Vue 3 (Composition API)
- **UI Framework**: Quasar 2.18.5
- **Build Tool**: Vite
- **HTTP Client**: Axios
- **State Management**: Pinia
- **Router**: Vue Router 4
- **Date Handling**: date-fns

### DevOps & Tools
- **Control de Versiones**: Git
- **Package Managers**: pip (Python), npm (Node.js)
- **Linting**: ESLint
- **Code Quality**: Pylint, Black

---

## 📦 Requisitos Previos

Antes de comenzar, asegúrate de tener instalado:

### Backend
- ✅ Python 3.11 o superior
- ✅ PostgreSQL 14+ (corriendo en puerto 5432)
- ✅ Redis 5.0+ (para Celery)
- ✅ pip (gestor de paquetes de Python)

### Frontend
- ✅ Node.js 18+ (recomendado v18 LTS)
- ✅ npm 9+ o yarn 1.22+

### Opcional
- Git (para control de versiones)
- Cuenta de Microsoft Azure (para OAuth y Graph API)
- Cuenta de Outlook/Microsoft (para envío de correos)

---

## Instalación

> **NOTA**: El sistema incluye autenticación con Microsoft OAuth y envío de correos mediante Microsoft Graph API.  
> Ver [`CONFIGURACION_MICROSOFT.md`](CONFIGURACION_MICROSOFT.md) para configuración completa.

### 1. Backend (Django)

#### 1.1 Clonar el Repositorio
```bash
git clone https://github.com/tuusuario/cronify.git
cd cronify
```

#### 1.2 Crear Entorno Virtual
```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

#### 1.3 Instalar Dependencias
```bash
pip install -r requirements.txt
```

**Dependencias principales:**
- Django 5.1.1
- djangorestframework 3.15.2
- psycopg2-binary 2.9.9 (PostgreSQL)
- celery 5.4.0
- redis 5.0.8
- djangorestframework-simplejwt 5.3.1
- python-decouple 3.8
- Pillow 10.4.0 (imágenes)
- msal 1.28.0 (Microsoft Authentication)
- django-allauth 0.63.3 (OAuth Social)
- requests 2.31.0 (HTTP Client)

#### 1.4 Configurar Base de Datos PostgreSQL

**Opción A: Usar psql**
```bash
# Abrir terminal de PostgreSQL
psql -U postgres

# Crear base de datos
CREATE DATABASE cronify_db;

# Crear usuario (opcional)
CREATE USER cronify_user WITH PASSWORD 'tu_password';
GRANT ALL PRIVILEGES ON DATABASE cronify_db TO cronify_user;

# Salir
\q
```

**Opción B: Usar pgAdmin**
1. Abrir pgAdmin
2. Crear nueva base de datos: `cronify_db`
3. Configurar encoding: UTF8

#### 1.5 Configurar Variables de Entorno

Crea un archivo `.env` en la carpeta `backend/`:

```env
# Django
SECRET_KEY=tu-clave-secreta-super-segura-aqui
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_NAME=cronify_db
DB_USER=postgres
DB_PASSWORD=tu_password_postgres
DB_HOST=localhost
DB_PORT=5432

# Email Configuration (Gmail)
EMAIL_HOST_USER=tu_email@gmail.com
EMAIL_HOST_PASSWORD=tu_app_password_de_gmail
DEFAULT_FROM_EMAIL=tu_email@gmail.com

# Redis (para Celery)
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

**⚠️ IMPORTANTE - Contraseña de Aplicación de Gmail:**
1. Ve a tu cuenta de Google: https://myaccount.google.com/security
2. Habilita "Verificación en 2 pasos"
3. Ve a "Contraseñas de aplicaciones"
4. Genera una contraseña para "Correo"
5. Usa esa contraseña en `EMAIL_HOST_PASSWORD`

#### 1.6 Aplicar Migraciones
```bash
python manage.py migrate
```

Esto creará las siguientes tablas:
- `users_usuario` - Usuarios del sistema
- `records_evento` - Eventos
- `records_archivoadjunto` - Archivos adjuntos
- Tablas de autenticación de Django
- Tablas de Celery

#### 1.7 Crear Superusuario
```bash
python manage.py createsuperuser
```

Ingresa:
- Username: `admin`
- Email: `admin@cronify.com`
- Password: `tu_password_segura`
- Nombre: `Administrador`

#### 1.8 Cargar Datos de Prueba (Opcional)
```bash
python manage.py loaddata initial_data.json
```

---

### 2. Frontend (Vue + Quasar)

#### 2.1 Ir a la Carpeta Frontend
```bash
cd ../frontend
```

#### 2.2 Instalar Dependencias
```bash
npm install
```

**Dependencias principales:**
- vue 3.5.13
- quasar 2.18.5
- @quasar/extras 1.16.13
- axios 1.7.9
- pinia 2.3.0
- vue-router 4.5.0
- date-fns 4.1.0

#### 2.3 Configurar Variables de Entorno

Crea un archivo `.env` en la carpeta `frontend/`:

```env
# API Backend URL
VITE_API_BASE_URL=http://localhost:8000/api

# Otras configuraciones
VITE_APP_TITLE=Cronify
```

#### 2.4 Verificar Configuración de Quasar

El archivo `quasar.config.js` ya está configurado con:
- Puerto del dev server: `9000`
- Proxy para evitar CORS
- Material Icons
- Roboto Font

---


## Configuración

### Configuración de Microsoft OAuth (Recomendado)

Para habilitar login con Microsoft y envío de correos vía Outlook/Graph API:

1. Registra una app en Azure: https://portal.azure.com > Azure Active Directory > App registrations > New registration
2. Permisos requeridos: `User.Read`, `Mail.Send`, `offline_access` (delegados)
3. Obtén y coloca en `backend/.env`:

```env
# Microsoft OAuth
USE_MICROSOFT_GRAPH=True
MICROSOFT_CLIENT_ID=tu_application_client_id
MICROSOFT_CLIENT_SECRET=tu_client_secret
MICROSOFT_TENANT_ID=common
MICROSOFT_AUTHORITY=https://login.microsoftonline.com/common
MICROSOFT_REDIRECT_URI=http://localhost:8000/api/auth/microsoft/callback/
EMAIL_HOST_USER=tu_email@outlook.com
DEFAULT_FROM_EMAIL=tu_email@outlook.com
```

**Tips:**
- Otorga "Grant admin consent" a los permisos.
- El secret solo se muestra una vez, guárdalo seguro.
- Ejecuta `python verificar_configuracion_microsoft.py` para validar la integración.

---


### Pruebas sin Azure


Puedes probar el sistema sin configurar Microsoft OAuth:
- Login y registro tradicional funcionan normalmente.
- Todas las funciones principales están disponibles.
- Los endpoints de Microsoft devolverán error 500 si no hay credenciales, pero el sistema sigue operativo.

**Pruebas recomendadas:**
1. Instala dependencias y ejecuta migraciones.
2. Verifica el modelo de usuario en Django shell (`microsoft_id`, `microsoft_access_token`, `microsoft_refresh_token`).
3. Prueba el frontend: login, registro, CRUD de eventos.
4. Verifica endpoints `/api/auth/microsoft/login/` y `/api/auth/microsoft/callback/` existen.

---

## ▶️ Ejecución

### Opción 1: Ejecución Completa (Recomendada)

Abre **4 terminales diferentes**:

**Terminal 1: Backend Django**
```bash
cd backend
venv\Scripts\activate  # Windows
python manage.py runserver
```
✅ Servidor corriendo en: http://localhost:8000

**Terminal 2: Celery Worker**
```bash
cd backend
venv\Scripts\activate  # Windows
celery -A cronify_backend worker -l info
```
✅ Worker escuchando tareas asíncronas

**Terminal 3: Celery Beat (Scheduler)**
```bash
cd backend
venv\Scripts\activate  # Windows
celery -A cronify_backend beat -l info
```
✅ Scheduler programando tareas diarias

**Terminal 4: Frontend Quasar**
```bash
cd frontend
npm run dev
```
✅ App corriendo en: http://localhost:9000

### Opción 2: Solo Backend + Frontend (Sin Notificaciones)

**Terminal 1: Backend**
```bash
cd backend
venv\Scripts\activate
python manage.py runserver
```

**Terminal 2: Frontend**
```bash
cd frontend
npm run dev
```

---

## 📡 API Endpoints

### Base URL
```
http://localhost:8000/api
```

### Autenticación

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| POST | `/auth/register/` | Registrar nuevo usuario | No |
| POST | `/token/` | Login (obtener JWT) | No |
| POST | `/token/refresh/` | Refrescar token | No |
| GET | `/auth/profile/` | Ver perfil | Sí |
| PUT | `/auth/profile/` | Actualizar perfil | Sí |
| POST | `/auth/change-password/` | Cambiar contraseña | Sí |

### Eventos

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET | `/eventos/` | Listar eventos (con filtros) | Sí |
| POST | `/eventos/` | Crear evento | Sí |
| GET | `/eventos/{id}/` | Ver evento específico | Sí |
| PUT | `/eventos/{id}/` | Actualizar evento completo | Sí |
| PATCH | `/eventos/{id}/` | Actualizar evento parcial | Sí |
| DELETE | `/eventos/{id}/` | Eliminar evento (soft delete) | Sí |
| POST | `/eventos/{id}/upload_file/` | Subir archivo adjunto | Sí |

### Usuarios

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET | `/usuarios/` | Listar usuarios (para notificar) | Sí |

### Parámetros de Filtrado

**Búsqueda:**
```
GET /api/eventos/?search=reunión
```

**Filtros:**
```
GET /api/eventos/?fecha_desde=2025-10-01&fecha_hasta=2025-10-31
GET /api/eventos/?creador=1
GET /api/eventos/?notificacion_enviada=false
GET /api/eventos/?es_publico=true
```

**Paginación:**
```
GET /api/eventos/?page=2
```

**Ejemplo Completo:**
```
GET /api/eventos/?search=licencia&notificacion_enviada=false&page=1
```

### Formato de Respuesta

**Éxito (200 OK):**
```json
{
  "count": 25,
  "next": "http://localhost:8000/api/eventos/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "asunto": "Renovación de licencia",
      "descripcion": "Renovar licencia de conducir",
      "fecha_vencimiento": "2025-11-15T10:30:00Z",
      "notificacion_valor": 7,
      "notificacion_unidad": "dias",
      "es_publico": true,
      "creador": 1,
      "creador_nombre": "Juan Pérez",
      "archivos_adjuntos": [],
      "notificacion_enviada": false
    }
  ]
}
```

**Error (400 Bad Request):**
```json
{
  "asunto": ["Este campo es requerido."],
  "fecha_vencimiento": ["La fecha debe ser futura."]
}
```

---

## 📁 Estructura del Proyecto

```
Cronify/
│
├── backend/                          # Django Backend
│   ├── cronify_backend/              # Configuración principal
│   │   ├── __init__.py
│   │   ├── settings.py               # Configuración de Django
│   │   ├── urls.py                   # URLs principales
│   │   ├── celery.py                 # Configuración de Celery
│   │   ├── wsgi.py                   # WSGI para producción
│   │   └── asgi.py                   # ASGI para async
│   │
│   ├── users/                        # App de Usuarios
│   │   ├── models.py                 # Modelo Usuario
│   │   ├── serializers.py            # Serializadores
│   │   ├── views.py                  # Vistas API
│   │   ├── urls.py                   # URLs de usuarios
│   │   └── migrations/               # Migraciones
│   │
│   ├── records/                      # App de Eventos
│   │   ├── models.py                 # Modelos Evento y ArchivoAdjunto
│   │   ├── serializers.py            # Serializadores
│   │   ├── views.py                  # Vistas API
│   │   ├── permissions.py            # Permisos personalizados
│   │   ├── urls.py                   # URLs de eventos
│   │   └── migrations/               # Migraciones
│   │
│   ├── notifications/                # App de Notificaciones
│   │   ├── tasks.py                  # Tareas de Celery
│   │   ├── email_service.py          # Servicio de email SMTP
│   │   └── ms_graph_service.py       # Servicio Microsoft Graph (futuro)
│   │
│   ├── media/                        # Archivos subidos
│   │   └── eventos_adjuntos/
│   │
│   ├── docs/                         # Documentación
│   │   ├── API_ENDPOINTS.md
│   │   ├── CONFIGURACION_EMAIL.md
│   │   ├── ESTADO_PROYECTO.md
│   │   └── VALIDACIONES_IMPLEMENTADAS.md
│   │
│   ├── manage.py                     # CLI de Django
│   ├── requirements.txt              # Dependencias Python
│   ├── .env.example                  # Ejemplo de variables de entorno
│   └── .gitignore
│
├── frontend/                         # Vue + Quasar Frontend
│   ├── src/
│   │   ├── layouts/                  # Layouts de la app
│   │   │   ├── MainLayout.vue        # Layout principal con sidebar
│   │   │   └── AuthLayout.vue        # Layout de autenticación
│   │   │
│   │   ├── pages/                    # Páginas/Vistas
│   │   │   ├── IndexPage.vue         # Calendario principal
│   │   │   ├── auth/
│   │   │   │   └── AuthPage.vue      # Login/Registro
│   │   │   ├── eventos/
│   │   │   │   ├── EventosListPage.vue    # Lista de eventos
│   │   │   │   └── EventoDetailPage.vue   # Detalle de evento
│   │   │   ├── perfil/
│   │   │   │   └── PerfilPage.vue    # Perfil de usuario
│   │   │   └── ConfiguracionPage.vue # Configuración
│   │   │
│   │   ├── components/               # Componentes reutilizables
│   │   │   ├── eventos/
│   │   │   │   ├── CreateEventModal.vue   # Modal crear/editar
│   │   │   │   └── EventDetailModal.vue   # Modal detalle
│   │   │   └── GlobalLoader.vue      # Loader global
│   │   │
│   │   ├── stores/                   # Pinia Stores (Estado)
│   │   │   ├── auth.js               # Store de autenticación
│   │   │   └── eventos.js            # Store de eventos
│   │   │
│   │   ├── services/                 # Servicios API
│   │   │   ├── api.js                # Instancia de Axios
│   │   │   ├── authService.js        # Servicios de auth
│   │   │   └── eventosService.js     # Servicios de eventos
│   │   │
│   │   ├── router/                   # Vue Router
│   │   │   ├── index.js
│   │   │   └── routes.js             # Definición de rutas
│   │   │
│   │   ├── css/                      # Estilos globales
│   │   │   └── app.scss
│   │   │
│   │   ├── App.vue                   # Componente raíz
│   │   └── main.js                   # Entry point
│   │
│   ├── public/                       # Archivos públicos
│   ├── quasar.config.js              # Configuración de Quasar
│   ├── package.json                  # Dependencias Node
│   ├── .env.example                  # Ejemplo de variables
│   └── .gitignore
│
└── README.md                         # Este archivo
```

---


## 🔧 Características Técnicas

### Validaciones

#### Backend
- **Usuario:**
  - Username único
  - Email único y válido
  - Contraseña mínima 8 caracteres
  - Validación de duplicados en email y username
  - Confirmación de contraseña (`password2`)

- **Evento:**
  - Asunto: 5-200 caracteres
  - Fecha de vencimiento: Debe ser futura
  - Notificación valor: >= 1
  - Archivo individual: <= 10MB
  - Total archivos por evento: <= 50MB
  - Soft delete (eliminación lógica)

#### Frontend
- Validación en tiempo real de formularios
- Prevención de fechas pasadas
- Confirmación de cambios sin guardar
- Validación de archivos antes de subir

### Seguridad

- JWT con expiración de 24 horas
- Refresh tokens para renovación
- Protección CSRF
- Permisos granulares (IsOwnerOrReadOnly)
- Variables sensibles en `.env`
- Sanitización de inputs
- Soft delete (datos no se eliminan físicamente)

### Performance

- Paginación (20 eventos por página)
- Búsqueda con debounce (500ms)
- Lazy loading de componentes
- Queries optimizados con select_related
- Compresión de imágenes con Pillow
- Cache de Redis para Celery

### UX/UI

- Transiciones suaves (scale, fade)
- Estados de hover interactivos
- Loading states globales
- Notificaciones visuales (iconos + colores)
- Responsive design (móvil first)
- Formato de fecha inteligente (AM/PM)
- Drag & drop para archivos

---

## Resumen de Cambios

- Integración de Microsoft OAuth y Graph API para login y envío de correos.
- Dualidad de login: usuario/contraseña tradicional y Microsoft.
- Validaciones robustas en registro y eventos.
- Notificaciones automáticas por email (configurable por Microsoft o SMTP).
- Refactor de serializadores y vistas para exponer eventos donde el usuario será notificado.
- Sidebar "Notificados" con contador y navegación a eventos.
- Documentación unificada y profesional.

---

## ❓ Troubleshooting y Preguntas Frecuentes

### ¿Por qué falla el login con Microsoft?
- Verifica que las credenciales de Azure sean correctas y que los permisos estén otorgados.
- El redirect URI debe coincidir exactamente con el configurado en Azure.
- El secret de la app debe estar vigente.

### ¿No se envían correos?
- Si usas Microsoft, revisa que `USE_MICROSOFT_GRAPH=True` y las credenciales sean válidas.
- Verifica la conexión a internet.

### ¿Cómo probar sin credenciales de Azure?
- Usa el login tradicional. Los endpoints de Microsoft devolverán error, pero el sistema principal funciona.

### ¿Cómo restablecer la base de datos?
- Elimina el archivo `db.sqlite3` (si usas SQLite) o borra y recrea la base en PostgreSQL.
- Ejecuta `python manage.py migrate` y crea un superusuario.

### ¿Cómo reportar un bug?
- Abre un Issue en GitHub con pasos claros para reproducirlo.

---

---


## 🤝 Contribuir

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

### Guía de Estilo

**Backend (Python):**
- Seguir PEP 8
- Docstrings en todas las funciones
- Type hints cuando sea posible

**Frontend (JavaScript/Vue):**
- ESLint con configuración de Vue
- Composition API (no Options API)
- Componentes en PascalCase

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

---

## 👨‍💻 Autor

**Tu Nombre**
- GitHub: [@angeldqr](https://github.com/angeldqr)
- Email: angelquinteror102@gmail.com

---

## 🙏 Agradecimientos

- [Django](https://www.djangoproject.com/) - Framework web de Python
- [Vue.js](https://vuejs.org/) - Framework JavaScript progresivo
- [Quasar Framework](https://quasar.dev/) - UI Framework para Vue
- [PostgreSQL](https://www.postgresql.org/) - Base de datos relacional
- [Celery](https://docs.celeryq.dev/) - Distributed Task Queue
- [Redis](https://redis.io/) - In-memory data structure store

---

## 📞 Soporte

Si encuentras algún bug o tienes alguna pregunta:

1. Abre un [Issue](https://github.com/angeldqr/cronify/issues)
2. Revisa la [documentación](backend/docs/)
3. Contacta al autor

---

<div align="center">

**Hecho con ❤️ y ☕ por Ángel Quintero**

⭐ Si te gustó el proyecto, dale una estrella en GitHub ⭐

</div>
