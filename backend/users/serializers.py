from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import Usuario

class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, attrs):
        """
        Valida que las contraseñas coincidan.
        """
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({
                "password": "Las contraseñas no coinciden."
            })
        return attrs
    
    def validate_email(self, value):
        """
        Valida que el email no esté en uso.
        """
        if Usuario.objects.filter(email=value).exists():
            raise serializers.ValidationError("Este email ya está registrado.")
        return value
    
    def validate_username(self, value):
        """
        Valida que el username no esté en uso.
        """
        if Usuario.objects.filter(username=value).exists():
            raise serializers.ValidationError("Este nombre de usuario ya está en uso.")
        return value

    def validate_password(self, value):
        """
        Valida que la contraseña tenga al menos 8 caracteres.
        """
        if len(value) < 8:
            raise serializers.ValidationError(
                "La contraseña debe tener al menos 8 caracteres."
            )
        
        # Validación adicional de Django (opcional pero recomendado)
        validate_password(value)
        return value

    def create(self, validated_data):
        """
        Este método se ejecuta al crear un nuevo usuario.
        Usa 'create_user' para asegurar que la contraseña se hashee correctamente.
        """
        # Eliminar password2 antes de crear el usuario
        validated_data.pop('password2')
        
        user = Usuario.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializador para ver y editar el perfil del usuario.
    No permite cambiar la contraseña (usa el endpoint dedicado).
    """
    eventos_creados_count = serializers.IntegerField(
        source='eventos_creados.count',
        read_only=True
    )
    from records.serializers import EventoSerializer
    eventos_a_notificar = EventoSerializer(many=True, read_only=True)

    class Meta:
        model = Usuario
        fields = [
            'id',
            'username',
            'email',
            'nombre',
            'first_name',
            'last_name',
            'date_joined',
            'last_login',
            'eventos_creados_count',
            'eventos_a_notificar',
        ]
        read_only_fields = ['id', 'username', 'date_joined', 'last_login', 'eventos_creados_count', 'nombre', 'eventos_a_notificar']
    
    def validate_email(self, value):
        """
        Valida que el email no esté en uso por otro usuario.
        """
        # Si el email está vacío, mantener el actual
        if not value:
            return self.instance.email if self.instance else value
            
        user = self.context.get('request').user if self.context.get('request') else None
        if user and Usuario.objects.filter(email=value).exclude(pk=user.pk).exists():
            raise serializers.ValidationError("Este email ya está en uso.")
        return value
    
    def update(self, instance, validated_data):
        """
        Actualiza el usuario y sincroniza el campo nombre.
        """
        # Solo actualizar si se proporciona un valor
        if 'email' in validated_data and validated_data['email']:
            instance.email = validated_data['email']
        if 'first_name' in validated_data:
            instance.first_name = validated_data['first_name']
        if 'last_name' in validated_data:
            instance.last_name = validated_data['last_name']
        
        # El método save() del modelo se encargará de actualizar 'nombre'
        instance.save()
        return instance


