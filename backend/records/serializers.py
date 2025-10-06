from rest_framework import serializers
from .models import Evento, ArchivoAdjunto

class ArchivoAdjuntoSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo ArchivoAdjunto.
    """
    class Meta:
        model = ArchivoAdjunto
        fields = [
            'id',
            'evento',
            'archivo',
            'nombre_original',
            'tipo_mime',
            'tamaño_bytes',
            'fecha_carga'
        ]
        read_only_fields = [
            'evento',
            'nombre_original',
            'tipo_mime',
            'tamaño_bytes',
            'fecha_carga'
        ]


class EventoSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Evento.
    """
    creador_username = serializers.ReadOnlyField(source='creador.username')
    # Muestra los archivos adjuntos relacionados con cada evento.
    archivos_adjuntos = ArchivoAdjuntoSerializer(many=True, read_only=True)

    class Meta:
        model = Evento
        fields = [
            'id',
            'asunto',
            'descripcion',
            'fecha_vencimiento',
            'es_publico',
            'creador',
            'creador_username',
            'fecha_creacion',
            'notificar_a',
            'archivos_adjuntos'
        ]
        read_only_fields = ['creador']

