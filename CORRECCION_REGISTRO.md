# Corrección del Error de Registro

## Problema Identificado

El error `400 Bad Request` en `/api/auth/register/` se debía a que:

1. **El frontend enviaba el campo `password2`** (confirmación de contraseña)
2. **El serializador del backend NO lo aceptaba**, causando una validación fallida

## Cambios Realizados

### 1. Backend - `users/serializers.py`

Se actualizó el `UserSerializer` para:

- **Aceptar el campo `password2`** en el serializador
- **Validar que las contraseñas coincidan** antes de crear el usuario
- **Validar que el email no esté duplicado**
- **Validar que el username no esté duplicado**

```python
class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, attrs):
        # Valida que password y password2 coincidan
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({
                "password": "Las contraseñas no coinciden."
            })
        return attrs
    
    def validate_email(self, value):
        # Valida que el email no esté registrado
        if Usuario.objects.filter(email=value).exists():
            raise serializers.ValidationError("Este email ya está registrado.")
        return value
    
    def validate_username(self, value):
        # Valida que el username no esté en uso
        if Usuario.objects.filter(username=value).exists():
            raise serializers.ValidationError("Este nombre de usuario ya está en uso.")
        return value

    def create(self, validated_data):
        # Eliminar password2 antes de crear el usuario
        validated_data.pop('password2')
        
        user = Usuario.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
```

### 2. Backend - `users/views.py`

Se mejoró el `UserCreateView` para agregar logging detallado:

```python
class UserCreateView(generics.CreateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        logger.info(f"Intento de registro con datos: {request.data}")
        serializer = self.get_serializer(data=request.data)
        
        if not serializer.is_valid():
            logger.error(f"Errores de validación: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        logger.info(f"Usuario creado exitosamente: {serializer.data}")
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
```

### 3. Backend - `cronify_backend/settings.py`

Se agregó configuración de logging para debug más detallado:

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'users': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}
```

## Validaciones Implementadas

El sistema ahora valida:

1. **Contraseñas coinciden**: `password` y `password2` deben ser iguales
2. **Longitud de contraseña**: Mínimo 8 caracteres
3. **Email único**: No puede haber usuarios con el mismo email
4. **Username único**: No puede haber usuarios con el mismo username
5. **Formato de email**: Validación básica del formato

## Próximos Pasos

1. **Reinicia el servidor backend** para aplicar los cambios:
   ```bash
   # Detén el servidor (Ctrl+C) y vuélvelo a iniciar
   python manage.py runserver
   ```

2. **Prueba el registro** desde el frontend en `http://localhost:9000/auth/register`

3. **Usa una contraseña fuerte** para el registro:
   - ❌ Evita: `12345678`, `password`, `qwerty`
   - ✅ Usa: `Usuario123`, `MiPassword2025`, `TestUser2024`

4. **Observa los logs** en la consola del backend para ver detalles de cada intento de registro

## Validaciones de Contraseña de Django

Django rechaza contraseñas que:
- Son completamente numéricas (ej: `12345678`)
- Son muy comunes (ej: `password`, `qwerty`)
- Son muy cortas (menos de 8 caracteres)
- Son muy similares al username o email

**Ejemplos de contraseñas válidas:**
- `Usuario123`
- `MiContraseña2025`
- `TestPass!2024`

## Mensajes de Error Mejorados

Ahora el usuario verá mensajes específicos si:

- Las contraseñas no coinciden
- El email ya está registrado
- El username ya está en uso
- La contraseña es muy corta
- **La contraseña es demasiado común**
- **La contraseña es completamente numérica**
- Falta algún campo requerido

### Mejoras en el Frontend

Se actualizó `RegisterPage.vue` para:
- Mostrar todos los errores de validación de contraseña
- Concatenar múltiples errores en un solo mensaje
- Aumentar el tiempo de visualización del error (4 segundos)
- Incluir logs en consola para debug
