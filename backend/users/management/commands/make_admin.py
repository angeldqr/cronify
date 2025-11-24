from django.core.management.base import BaseCommand
from users.models import Usuario


class Command(BaseCommand):
    help = 'Convierte un usuario en administrador'

    def add_arguments(self, parser):
        parser.add_argument('email', type=str, help='Email del usuario')

    def handle(self, *args, **options):
        email = options['email']
        
        try:
            usuario = Usuario.objects.get(email=email)
            usuario.is_admin = True
            usuario.save()
            self.stdout.write(
                self.style.SUCCESS(f'✓ Usuario "{usuario.nombre}" ({email}) es ahora administrador')
            )
        except Usuario.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'✗ No existe un usuario con el email: {email}')
            )
