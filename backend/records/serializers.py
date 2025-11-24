from rest_framework import serializers
from django.utils import timezone
from .models import Evento, ArchivoAdjunto
from users.models import Usuario


class ArchivoAdjuntoSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo ArchivoAdjunto.
    """
    url_descarga = serializers.SerializerMethodField()
    
    class Meta:
        model = ArchivoAdjunto
        fields = [
            'id',
            'evento',
            'archivo',
            'nombre_original',
            'tipo_mime',
            'tamaño_bytes',
            'fecha_carga',
            'url_descarga'
        ]
        read_only_fields = [
            'evento',
            'nombre_original',
            'tipo_mime',
            'tamaño_bytes',
            'fecha_carga'
        ]
    
    def get_url_descarga(self, obj):
        """
        Retorna la URL completa para descargar el archivo.
        """
        request = self.context.get('request')
        if obj.archivo and request:
            return request.build_absolute_uri(obj.archivo.url)
        return None


class EventoSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Evento.
    """
    creador_username = serializers.ReadOnlyField(source='creador.username')
    creador_nombre = serializers.ReadOnlyField(source='creador.nombre')
    archivos_adjuntos = ArchivoAdjuntoSerializer(many=True, read_only=True)
    notificar_a = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Usuario.objects.filter(is_active=True),
        required=False
    )
    # Campo adicional para asegurar que los IDs se devuelven correctamente en la respuesta
    notificar_a_ids = serializers.SerializerMethodField()

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
            'creador_nombre',
            'fecha_creacion',
            'fecha_modificacion',
            'notificar_a',
            'notificar_a_ids',
            'archivos_adjuntos',
            'notificacion_enviada',
            'fecha_notificacion',
        ]
        read_only_fields = ['creador', 'fecha_creacion', 'fecha_modificacion', 'notificacion_enviada', 'fecha_notificacion']
    
    def get_notificar_a_ids(self, obj):
        """
        Devuelve los IDs de los usuarios notificados.
        """
        return list(obj.notificar_a.values_list('id', flat=True))

    def create(self, validated_data):
        notificar_a_ids = validated_data.pop('notificar_a', [])
        evento = Evento.objects.create(**validated_data)
        
        if notificar_a_ids:
            evento.notificar_a.set(notificar_a_ids)
        
        return evento

    def update(self, instance, validated_data):
        notificar_a_ids = validated_data.pop('notificar_a', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        if notificar_a_ids is not None:
            instance.notificar_a.set(notificar_a_ids)
        
        return instance

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


