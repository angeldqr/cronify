import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cronify_backend.settings')
django.setup()

from users.models import Usuario

usuarios = Usuario.objects.all()
for usuario in usuarios:
    usuario.save()
    print(f"Actualizado: {usuario.username} -> {usuario.nombre}")

print(f"\n✓ Se actualizaron {usuarios.count()} usuarios")
