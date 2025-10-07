# API Endpoints - Cronify Backend

## Autenticación

### Registro de Usuario
```http
POST /api/auth/register/
Content-Type: application/json

{
    "username": "usuario123",
    "email": "usuario@example.com",
    "password": "contraseña123"
}
```

### Login (Obtener Token JWT)
```http
POST /api/token/
Content-Type: application/json

{
    "username": "usuario123",
    "password": "contraseña123"
}

Response:
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Refrescar Token
```http
POST /api/token/refresh/
Content-Type: application/json

{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

## Perfil de Usuario

### Ver Perfil
```http
GET /api/auth/profile/
Authorization: Bearer {access_token}

Response:
{
    "id": 1,
    "username": "usuario123",
    "email": "usuario@example.com",
    "first_name": "Juan",
    "last_name": "Pérez",
    "date_joined": "2025-10-01T10:00:00Z",
    "last_login": "2025-10-06T15:30:00Z",
    "eventos_creados_count": 5
}
```

### Editar Perfil
```http
PUT /api/auth/profile/
Authorization: Bearer {access_token}
Content-Type: application/json

{
    "first_name": "Juan",
    "last_name": "Pérez",
    "email": "nuevo_email@example.com"
}
```

### Cambiar Contraseña
```http
POST /api/auth/change-password/
Authorization: Bearer {access_token}
Content-Type: application/json

{
    "old_password": "contraseña123",
    "new_password": "nuevaContraseña456"
}
```

## Eventos

### Listar Eventos (con paginación)
```http
GET /api/eventos/
Authorization: Bearer {access_token}

Response:
{
    "count": 45,
    "next": "http://localhost:8000/api/eventos/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "asunto": "Renovación Licencia Office",
            "descripcion": "Renovar licencia antes del vencimiento",
            "fecha_vencimiento": "2025-12-31T23:59:59Z",
            "notificacion_valor": 7,
            "notificacion_unidad": "días",
            "es_publico": true,
            "creador": 1,
            "creador_username": "usuario123",
            "fecha_creacion": "2025-10-01T10:00:00Z",
            "fecha_modificacion": "2025-10-05T14:30:00Z",
            "notificar_a": [2, 3],
            "archivos_adjuntos": [],
            "notificacion_enviada": false,
            "fecha_notificacion": null
        }
    ]
}
```

### Búsqueda por Texto
```http
GET /api/eventos/?search=licencia
Authorization: Bearer {access_token}
```

### Filtrar por Rango de Fechas
```http
GET /api/eventos/?fecha_inicio=2025-10-01T00:00:00Z&fecha_fin=2025-12-31T23:59:59Z
Authorization: Bearer {access_token}
```

### Filtrar por Creador
```http
GET /api/eventos/?creador=1
Authorization: Bearer {access_token}
```

### Filtrar por Estado de Notificación
```http
# Eventos ya notificados
GET /api/eventos/?notificado=true
Authorization: Bearer {access_token}

# Eventos pendientes de notificación
GET /api/eventos/?notificado=false
Authorization: Bearer {access_token}
```

### Filtros Combinados
```http
GET /api/eventos/?search=renovación&fecha_inicio=2025-11-01T00:00:00Z&notificado=false
Authorization: Bearer {access_token}
```

### Crear Evento
```http
POST /api/eventos/
Authorization: Bearer {access_token}
Content-Type: application/json

{
    "asunto": "Renovación de Contrato",
    "descripcion": "Renovar contrato de servicios antes del vencimiento",
    "fecha_vencimiento": "2025-12-31T23:59:59Z",
    "notificacion_valor": 15,
    "notificacion_unidad": "días",
    "es_publico": true,
    "notificar_a": [2, 3]
}
```

### Ver Evento Específico
```http
GET /api/eventos/1/
Authorization: Bearer {access_token}
```

### Actualizar Evento
```http
PUT /api/eventos/1/
Authorization: Bearer {access_token}
Content-Type: application/json

{
    "asunto": "Renovación de Contrato Actualizado",
    "descripcion": "Descripción actualizada",
    "fecha_vencimiento": "2025-12-31T23:59:59Z",
    "notificacion_valor": 30,
    "notificacion_unidad": "días",
    "es_publico": false,
    "notificar_a": [2]
}
```

### Eliminar Evento (Soft Delete)
```http
DELETE /api/eventos/1/
Authorization: Bearer {access_token}

# El evento se marca como eliminado (deleted_at = fecha actual)
# pero no se elimina físicamente de la base de datos
```

### Subir Archivo Adjunto
```http
POST /api/eventos/1/upload_file/
Authorization: Bearer {access_token}
Content-Type: multipart/form-data

archivo: [archivo binario]

# Límites:
# - Máximo 10MB por archivo
# - Máximo 50MB total por evento
```

## Validaciones

### Asunto
- Mínimo: 5 caracteres
- Máximo: 200 caracteres

### Fecha de Vencimiento
- Debe ser una fecha futura

### Notificación Valor
- Debe ser >= 1

### Contraseña
- Mínimo 8 caracteres

### Archivos
- Máximo 10MB por archivo individual
- Máximo 50MB total por evento

## Códigos de Estado HTTP

- `200 OK`: Solicitud exitosa
- `201 Created`: Recurso creado exitosamente
- `400 Bad Request`: Datos inválidos
- `401 Unauthorized`: Token inválido o no proporcionado
- `403 Forbidden`: Sin permisos para realizar la acción
- `404 Not Found`: Recurso no encontrado
- `500 Internal Server Error`: Error del servidor

## Notas

- Todos los endpoints (excepto registro y login) requieren autenticación JWT
- El token JWT tiene una duración de 24 horas
- La paginación devuelve 20 eventos por página
- Los eventos eliminados (soft delete) no aparecen en los listados
- Solo el creador puede editar o eliminar un evento
