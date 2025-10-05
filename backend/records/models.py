from django.db import models
from django.conf import settings

# Hacemos referencia al modelo de usuario personalizado desde settings
# para establecer las relaciones correctamente.
Usuario = settings.AUTH_USER_MODEL

class Evento(models.Model):

    class UnidadNotificacion(models.TextChoices):
        DIAS = 'días', 'Días'
        MESES = 'meses', 'Meses'

    creador = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='eventos_creados'
    )
    asunto = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_vencimiento = models.DateTimeField()
    notificacion_valor = models.PositiveIntegerField(default=7)
    notificacion_unidad = models.CharField(
        max_length=50,
        choices=UnidadNotificacion.choices,
        default=UnidadNotificacion.DIAS
    )
    es_publico = models.BooleanField(default=True)
    notificacion_enviada = models.BooleanField(default=False)
    fecha_notificacion = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    notificar_a = models.ManyToManyField(
        Usuario,
        related_name='eventos_a_notificar',
        blank=True,
        through='EventoUsuarioNotificacion'
    )

    def __str__(self):
        return f"{self.asunto} (Vence: {self.fecha_vencimiento.strftime('%d/%m/%Y')})"


class ArchivoAdjunto(models.Model):
    evento = models.ForeignKey(
        Evento,
        on_delete=models.CASCADE,
        related_name='archivos_adjuntos'
    )
    archivo = models.FileField(upload_to='eventos_adjuntos/')
    nombre_original = models.CharField(max_length=255)
    tipo_mime = models.CharField(max_length=100)
    tamaño_bytes = models.PositiveIntegerField()
    fecha_carga = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre_original


class EventoUsuarioNotificacion(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('evento', 'usuario')

    def __str__(self):
        return f"Notificación para {self.usuario} en evento {self.evento.id}"