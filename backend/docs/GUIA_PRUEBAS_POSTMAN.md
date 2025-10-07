# Guía de Pruebas con Postman - Cronify Backend

## Prerrequisitos

1. **Descargar e instalar Postman**: https://www.postman.com/downloads/
2. **Tener el servidor corriendo**:
   ```bash
   python manage.py runserver
   ```
3. **Importar la colección**: `Cronify_Postman_Collection.json`

## Paso 1: Importar la Colección

1. Abre Postman
2. Click en "Import" (botón superior izquierdo)
3. Arrastra el archivo `Cronify_Postman_Collection.json` o selecciónalo
4. Click en "Import"

La colección aparecerá en tu sidebar con todas las peticiones organizadas.

## Paso 2: Verificar Variables de Entorno

La colección ya tiene configuradas estas variables:
- `base_url`: http://localhost:8000
- `access_token`: (se llenará automáticamente al hacer login)
- `refresh_token`: (se llenará automáticamente al hacer login)
- `evento_id`: (se llenará automáticamente al crear un evento)

## Paso 3: Secuencia de Pruebas

### Prueba 1: Registro de Usuario

1. En la carpeta "1. Autenticación", ejecuta "Registrar Usuario"
2. Deberías recibir:
   - **Status**: 201 Created
   - **Respuesta**: Datos del usuario creado (id, username, email)

**Si fallas**: Verifica que el email no esté duplicado o la contraseña tenga mínimo 8 caracteres.

### Prueba 2: Login

1. Ejecuta "Login (Obtener Token)"
2. Deberías recibir:
   - **Status**: 200 OK
   - **Respuesta**: `access` y `refresh` tokens
3. **IMPORTANTE**: El token se guarda automáticamente en las variables

**Verificar**: En la pestaña "Console" (abajo) deberías ver "Token guardado: ..."

### Prueba 3: Ver Perfil

1. Ejecuta "Ver Perfil" en la carpeta "2. Perfil de Usuario"
2. Deberías recibir:
   - **Status**: 200 OK
   - **Respuesta**: Datos completos del perfil

**Si fallas**: Verifica que el token se guardó correctamente. Puedes verlo en:
   - Click en el ícono del ojo (arriba derecha)
   - Busca `access_token`

### Prueba 4: Crear Evento

1. En "3. Eventos - CRUD", ejecuta "Crear Evento"
2. Deberías recibir:
   - **Status**: 201 Created
   - **Respuesta**: Evento creado con todos los campos
3. El `evento_id` se guarda automáticamente

**Verificar campos importantes**:
- `fecha_creacion`: Debe ser la fecha actual
- `fecha_modificacion`: Debe ser la fecha actual
- `notificacion_enviada`: Debe ser `false`

### Prueba 5: Listar Eventos

1. Ejecuta "Listar Eventos"
2. Deberías recibir:
   - **Status**: 200 OK
   - **Respuesta**: Lista paginada con el evento que creaste

**Verificar paginación**:
- `count`: Número total de eventos
- `next`: URL de la siguiente página (si hay)
- `results`: Array de eventos (máximo 20)

### Prueba 6: Actualizar Evento

1. Ejecuta "Actualizar Evento"
2. Deberías recibir:
   - **Status**: 200 OK
   - **Respuesta**: Evento actualizado

**Verificar**: `fecha_modificacion` debe ser diferente a `fecha_creacion`

### Prueba 7: Búsqueda y Filtrado

Ejecuta todas las peticiones en "4. Búsqueda y Filtrado":

1. **Buscar por Texto**: Encuentra eventos con "licencia" en asunto o descripción
2. **Filtrar por Rango de Fechas**: Eventos entre nov-dic 2025
3. **Filtrar No Notificados**: Solo eventos sin notificar
4. **Búsqueda Combinada**: Combina múltiples filtros

**Todas deberían**: Status 200 OK con resultados filtrados

### Prueba 8: Subir Archivo

1. En "5. Archivos Adjuntos", ejecuta "Subir Archivo"
2. En el Body:
   - Click en "archivo"
   - Click en "Select Files"
   - Elige un archivo (< 10MB)
3. Ejecuta

**Deberías recibir**:
- **Status**: 201 Created
- **Respuesta**: Datos del archivo (nombre, tamaño, tipo, URL)

**Probar validación**:
- Intenta subir un archivo > 10MB → Error 400
- Sube varios archivos hasta pasar 50MB total → Error 400

### Prueba 9: Validaciones (Casos de Error)

En "6. Validaciones", ejecuta todas las peticiones:

1. **Contraseña Corta**: 
   - **Esperado**: 400 Bad Request
   - **Mensaje**: "La contraseña debe tener al menos 8 caracteres"

2. **Asunto Corto**:
   - **Esperado**: 400 Bad Request
   - **Mensaje**: "El asunto debe tener al menos 5 caracteres"

3. **Fecha Pasada**:
   - **Esperado**: 400 Bad Request
   - **Mensaje**: "La fecha de vencimiento debe ser una fecha futura"

**IMPORTANTE**: Estas peticiones DEBEN fallar. Si reciben 200/201, algo está mal.

### Prueba 10: Soft Delete

1. Ejecuta "Eliminar Evento (Soft Delete)"
2. Deberías recibir:
   - **Status**: 204 No Content

3. Ejecuta "Listar Eventos" nuevamente
4. El evento eliminado NO debe aparecer

**Verificar en BD** (opcional):
```sql
SELECT id, asunto, deleted_at FROM records_evento WHERE id = X;
```
- `deleted_at` debe tener una fecha, no NULL

### Prueba 11: Cambiar Contraseña

1. Ejecuta "Cambiar Contraseña"
2. Deberías recibir:
   - **Status**: 200 OK
   - **Mensaje**: "Contraseña actualizada exitosamente"

3. Intenta hacer login con la contraseña antigua → Debe fallar
4. Login con la nueva contraseña → Debe funcionar

### Prueba 12: Token Expirado (Opcional)

1. Espera 24 horas O modifica settings.py temporalmente a 1 minuto
2. Intenta "Ver Perfil"
3. Deberías recibir:
   - **Status**: 401 Unauthorized
   - **Mensaje**: Token inválido o expirado

4. Ejecuta "Refrescar Token"
5. Intenta "Ver Perfil" nuevamente → Debe funcionar

## Checklist de Verificación

- [ ] Registro de usuario funciona
- [ ] Login genera tokens correctamente
- [ ] Ver/editar perfil funciona
- [ ] Crear evento con validaciones
- [ ] Listar eventos con paginación
- [ ] Actualizar evento (fecha_modificacion cambia)
- [ ] Búsqueda por texto funciona
- [ ] Filtros de fecha funcionan
- [ ] Filtro por estado de notificación funciona
- [ ] Subir archivos funciona
- [ ] Validaciones de tamaño de archivo funcionan
- [ ] Soft delete funciona (evento no aparece pero existe en BD)
- [ ] Validaciones de contraseña funcionan
- [ ] Validaciones de asunto funcionan
- [ ] Validaciones de fecha funcionan
- [ ] Cambio de contraseña funciona
- [ ] Permisos (solo creador puede editar/eliminar)

## Problemas Comunes

### Error 401: Unauthorized
- El token no está configurado
- El token expiró
- **Solución**: Ejecuta "Login" nuevamente

### Error 403: Forbidden
- Intentas editar/eliminar un evento que no creaste
- **Solución**: Solo puedes modificar eventos que tú creaste

### Error 400: Fecha de vencimiento debe ser futura
- La fecha que pusiste ya pasó
- **Solución**: Usa una fecha futura, ej: 2025-12-31T23:59:59Z

### Error 500: Internal Server Error
- Problema en el servidor
- **Solución**: Revisa la consola del servidor (terminal) para ver el error detallado

## Pruebas Adicionales (Opcional)

### Probar Notificaciones

1. Crea un evento con fecha de vencimiento mañana
2. Configura notificación para "1 día"
3. Ejecuta manualmente la tarea de Celery:
   ```bash
   python manage.py shell
   >>> from notifications.tasks import verificar_vencimientos
   >>> verificar_vencimientos()
   ```
4. Revisa tu email (el configurado en .env)

### Probar Paginación

1. Crea 25 eventos
2. Lista eventos
3. Verifica que solo muestra 20
4. Usa la URL en `next` para ver los siguientes 5

## Resultado Esperado

Si todas las pruebas pasan:
- El backend está 100% funcional
- Todas las validaciones funcionan
- La seguridad (JWT) funciona
- Las búsquedas y filtros funcionan
- El sistema de archivos funciona
- El soft delete funciona

Estás listo para integrar el frontend.
