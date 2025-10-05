from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

# Registramos nuestro modelo Usuario personalizado.
# Usamos UserAdmin para que la interfaz de administración
# tenga todas las opciones avanzadas para gestionar usuarios.
admin.site.register(Usuario, UserAdmin)
