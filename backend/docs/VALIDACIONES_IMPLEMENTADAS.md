# Validaciones Implementadas en Cronify Backend

## RF-001: Gestión de Usuarios y Autenticación

### Implementado:
- **Token JWT**: Configurado a 24 horas (ACCESS_TOKEN_LIFETIME)
- **Refresh Token**: 7 días (REFRESH_TOKEN_LIFETIME)
- **Validación de contraseña**: Mínimo 8 caracteres
- **Email único**: Validado por Django automáticamente
- **Contraseñas hasheadas**: bcrypt por defecto en Django

### Ejemplo de Prueba:
```bash
# Registro con contraseña corta (debe fallar)
POST /api/auth/register/
{
    "username": "testuser",
    "email": "test@example.com",
    "password": "1234567"  # Solo 7 caracteres - ERROR
}

# Registro válido
POST /api/auth/register/
{
    "username": "testuser",
    "email": "test@example.com",
    "password": "12345678"  # 8 caracteres - OK
}
```

## RF-002: Creación y Gestión de Eventos

### Validaciones del Asunto:
- **Mínimo**: 5 caracteres
- **Máximo**: 200 caracteres

```bash
# Asunto muy corto (debe fallar)
POST /api/eventos/
{
    "asunto": "Hola",  # Solo 4 caracteres - ERROR
    "fecha_vencimiento": "2025-12-31T10:00:00Z"
}

# Asunto válido
POST /api/eventos/
{
    "asunto": "Reunión importante",  # 18 caracteres - OK
    "fecha_vencimiento": "2025-12-31T10:00:00Z"
}
```

### Validaciones de Fecha de Vencimiento:
- **Debe ser futura**: No se permiten fechas pasadas o actuales

```bash
# Fecha pasada (debe fallar)
POST /api/eventos/
{
    "asunto": "Evento pasado",
    "fecha_vencimiento": "2024-01-01T10:00:00Z"  # ERROR
}

# Fecha futura (válido)
POST /api/eventos/
{
    "asunto": "Evento futuro",
    "fecha_vencimiento": "2025-12-31T10:00:00Z"  # OK
}
```

### Validaciones de Notificación:
- **notificacion_valor**: Debe ser >= 1

```bash
# Valor inválido (debe fallar)
POST /api/eventos/
{
    "asunto": "Evento test",
    "fecha_vencimiento": "2025-12-31T10:00:00Z",
    "notificacion_valor": 0  # ERROR
}

# Valor válido
POST /api/eventos/
{
    "asunto": "Evento test",
    "fecha_vencimiento": "2025-12-31T10:00:00Z",
    "notificacion_valor": 7,  # OK
    "notificacion_unidad": "días"
}
```

### Validaciones de Archivos Adjuntos:
- **Archivo individual**: Máximo 10MB
- **Total por evento**: Máximo 50MB

```bash
# Subir archivo que excede 10MB (debe fallar)
POST /api/eventos/{id}/upload_file/
Content-Type: multipart/form-data
archivo: [archivo de 15MB]  # ERROR

# Subir archivo válido
POST /api/eventos/{id}/upload_file/
Content-Type: multipart/form-data
archivo: [archivo de 5MB]  # OK
```

### Soft Delete:
- **DELETE** en eventos ahora usa eliminación lógica
- El evento se marca con `deleted_at` pero no se elimina de la BD

```bash
# Eliminar evento (soft delete)
DELETE /api/eventos/{id}/
# El evento se marca como deleted_at = fecha_actual
# Ya no aparecerá en los listados
```

## Campos Expuestos en el Serializer

El EventoSerializer ahora incluye:
- `id`
- `asunto`
- `descripcion`
- `fecha_vencimiento`
- `notificacion_valor` (NUEVO)
- `notificacion_unidad` (NUEVO)
- `es_publico`
- `creador`
- `creador_username`
- `fecha_creacion`
- `notificar_a`
- `archivos_adjuntos`
- `notificacion_enviada` (NUEVO)
- `fecha_notificacion` (NUEVO)

## Resumen de Cambios

### settings.py
- JWT ACCESS_TOKEN_LIFETIME: 60 min → 24 horas
- JWT REFRESH_TOKEN_LIFETIME: 1 día → 7 días

### users/serializers.py
- Agregada validación de contraseña mínima (8 caracteres)
- Agregada validación completa de Django para contraseñas

### records/serializers.py
- Agregada validación de asunto (5-200 caracteres)
- Agregada validación de fecha futura
- Agregada validación de notificacion_valor (>= 1)
- Expuestos campos: notificacion_valor, notificacion_unidad, notificacion_enviada, fecha_notificacion

### records/views.py
- Implementado soft delete en perform_destroy()
- Agregada validación de tamaño de archivo (10MB máx)
- Agregada validación de tamaño total por evento (50MB máx)

## Cómo Probar

1. Ejecutar el servidor:
```bash
python manage.py runserver
```

2. Usar Postman/Thunder Client/curl para probar cada endpoint

3. Verificar que las validaciones funcionen correctamente con datos inválidos
