from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import Usuario

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

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
    
    class Meta:
        model = Usuario
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'date_joined',
            'last_login',
            'eventos_creados_count'
        ]
        read_only_fields = ['id', 'date_joined', 'last_login', 'eventos_creados_count']
    
    def validate_email(self, value):
        """
        Valida que el email no esté en uso por otro usuario.
        """
        user = self.context['request'].user if 'request' in self.context else None
        if Usuario.objects.filter(email=value).exclude(pk=user.pk).exists():
            raise serializers.ValidationError("Este email ya está en uso.")
        return value


