from rest_framework import serializers
from .models import Usuario

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        # Campos que se pedirán en el registro
        fields = ['id', 'username', 'email', 'password']
        # Configuraciones extra para el campo de contraseña
        extra_kwargs = {
            'password': {'write_only': True}
        }

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
