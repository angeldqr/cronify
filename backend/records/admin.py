from django.contrib import admin
from .models import Evento, ArchivoAdjunto, EventoUsuarioNotificacion

# Registramos los modelos para que aparezcan en el panel de administración.
admin.site.register(Evento)
admin.site.register(ArchivoAdjunto)
admin.site.register(EventoUsuarioNotificacion)
