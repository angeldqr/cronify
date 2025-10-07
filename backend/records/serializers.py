from rest_framework import serializers
from django.utils import timezone
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
    archivos_adjuntos = ArchivoAdjuntoSerializer(many=True, read_only=True)

    class Meta:
        model = Evento
        fields = [
            'id',
            'asunto',
            'descripcion',
            'fecha_vencimiento',
            'notificacion_valor',
            'notificacion_unidad',
            'es_publico',
            'creador',
            'creador_username',
            'fecha_creacion',
            'fecha_modificacion',
            'notificar_a',
            'archivos_adjuntos',
            'notificacion_enviada',
            'fecha_notificacion',
        ]
        read_only_fields = ['creador', 'fecha_creacion', 'fecha_modificacion', 'notificacion_enviada', 'fecha_notificacion']

    def validate_asunto(self, value):
        """
        Valida que el asunto tenga entre 5 y 200 caracteres.
        """
        if len(value) < 5:
            raise serializers.ValidationError(
                "El asunto debe tener al menos 5 caracteres."
            )
        if len(value) > 200:
            raise serializers.ValidationError(
                "El asunto no puede exceder los 200 caracteres."
            )
        return value

    def validate_fecha_vencimiento(self, value):
        """
        Valida que la fecha de vencimiento sea futura.
        """
        if value <= timezone.now():
            raise serializers.ValidationError(
                "La fecha de vencimiento debe ser una fecha futura."
            )
        return value

    def validate_notificacion_valor(self, value):
        """
        Valida que el valor de notificación sea al menos 1.
        """
        if value < 1:
            raise serializers.ValidationError(
                "El tiempo de notificación debe ser al menos 1."
            )
        return value


