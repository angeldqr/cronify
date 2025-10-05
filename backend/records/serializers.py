from rest_framework import serializers
from .models import Evento

class EventoSerializer(serializers.ModelSerializer):
    """
    Traduce el modelo Evento a formato JSON y viceversa.
    """
    # Muestra el nombre de usuario del creador en lugar de solo su ID.
    # Es de solo lectura porque se establece automáticamente.
    creador_username = serializers.ReadOnlyField(source='creador.username')

    class Meta:
        model = Evento
        # Especifica los campos del modelo que se incluirán en la API.
        fields = [
            'id',
            'asunto',
            'descripcion',
            'fecha_vencimiento',
            'es_publico',
            'creador',
            'creador_username',
            'fecha_creacion',
            'notificar_a'
        ]
        # El campo 'creador' es de solo lectura en la API.
        read_only_fields = ['creador']