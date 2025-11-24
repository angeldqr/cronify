from django.core.management.base import BaseCommand
from users.models import Usuario
from django.utils.crypto import get_random_string
import random


class Command(BaseCommand):
    help = 'Crea múltiples usuarios de prueba para testing'

    def add_arguments(self, parser):
        parser.add_argument(
            'cantidad',
            type=int,
            help='Cantidad de usuarios a crear',
            default=100
        )

    def handle(self, *args, **options):
        cantidad = options['cantidad']
        
        nombres = [
            'Juan', 'María', 'Pedro', 'Ana', 'Luis', 'Carmen', 'José', 'Laura',
            'Carlos', 'Elena', 'Miguel', 'Sofia', 'Antonio', 'Isabel', 'Francisco',
            'Lucía', 'Manuel', 'Paula', 'David', 'Marta', 'Javier', 'Cristina',
            'Daniel', 'Andrea', 'Rafael', 'Beatriz', 'Sergio', 'Raquel', 'Alberto',
            'Patricia', 'Fernando', 'Silvia', 'Jorge', 'Natalia', 'Roberto', 'Mónica',
            'Alejandro', 'Rosa', 'Ángel', 'Teresa', 'Andrés', 'Pilar', 'Pablo',
            'Alicia', 'Raúl', 'Eva', 'Diego', 'Irene', 'Adrián', 'Clara'
        ]
        
        apellidos = [
            'García', 'Rodríguez', 'González', 'Fernández', 'López', 'Martínez',
            'Sánchez', 'Pérez', 'Gómez', 'Martín', 'Jiménez', 'Ruiz', 'Hernández',
            'Díaz', 'Moreno', 'Muñoz', 'Álvarez', 'Romero', 'Alonso', 'Gutiérrez',
            'Navarro', 'Torres', 'Domínguez', 'Vázquez', 'Ramos', 'Gil', 'Ramírez',
            'Serrano', 'Blanco', 'Suárez', 'Molina', 'Morales', 'Ortega', 'Delgado',
            'Castro', 'Ortiz', 'Rubio', 'Marín', 'Sanz', 'Iglesias', 'Medina',
            'Garrido', 'Santos', 'Cortés', 'Guerrero', 'Lozano', 'Cano', 'Prieto'
        ]
        
        dominios = ['gmail.com', 'hotmail.com', 'yahoo.com', 'outlook.com', 'icloud.com']
        
        usuarios_creados = 0
        usuarios_existentes = 0
        
        self.stdout.write(self.style.WARNING(f'Creando {cantidad} usuarios de prueba...'))
        
        for i in range(cantidad):
            nombre = random.choice(nombres)
            apellido1 = random.choice(apellidos)
            apellido2 = random.choice(apellidos)
            nombre_completo = f"{nombre} {apellido1} {apellido2}"
            
            # Generar username único
            username_base = f"{nombre.lower()}.{apellido1.lower()}{i+1}"
            username = username_base.replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u')
            
            # Generar email único
            dominio = random.choice(dominios)
            email = f"{username}@{dominio}"
            
            # Verificar si ya existe
            if Usuario.objects.filter(email=email).exists() or Usuario.objects.filter(username=username).exists():
                usuarios_existentes += 1
                continue
            
            # Crear usuario
            try:
                usuario = Usuario.objects.create_user(
                    username=username,
                    email=email,
                    password='password123',  # Contraseña por defecto
                    first_name=nombre,
                    last_name=f"{apellido1} {apellido2}",
                    nombre=nombre_completo
                )
                
                # Asignar aleatoriamente algunos como admins (5% de probabilidad)
                if random.random() < 0.05:
                    usuario.is_admin = True
                    usuario.save()
                
                usuarios_creados += 1
                
                # Mostrar progreso cada 10 usuarios
                if usuarios_creados % 10 == 0:
                    self.stdout.write(f'  Creados: {usuarios_creados}/{cantidad}...')
                    
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Error al crear usuario {username}: {str(e)}')
                )
        
        # Resumen
        self.stdout.write('\n' + '='*60)
        self.stdout.write(self.style.SUCCESS(f'✓ Usuarios creados exitosamente: {usuarios_creados}'))
        if usuarios_existentes > 0:
            self.stdout.write(self.style.WARNING(f'⚠ Usuarios ya existentes (omitidos): {usuarios_existentes}'))
        self.stdout.write('='*60)
        self.stdout.write(self.style.SUCCESS('\nCredenciales de acceso:'))
        self.stdout.write('  Username: [nombre.apellido + número]')
        self.stdout.write('  Password: password123')
        self.stdout.write('\nEjemplo: juan.garcia1 / password123')
