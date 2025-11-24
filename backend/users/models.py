from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    nombre = models.CharField(max_length=200, blank=True, default='')
    
    # Campos para autenticación Microsoft OAuth
    microsoft_id = models.CharField(max_length=255, blank=True, null=True, unique=True)
    microsoft_access_token = models.TextField(blank=True, null=True)
    microsoft_refresh_token = models.TextField(blank=True, null=True)
    
    # Campo para rol de administrador
    is_admin = models.BooleanField(default=False, help_text='Designa si el usuario tiene privilegios de administrador')

    def save(self, *args, **kwargs):
        if not self.nombre and (self.first_name or self.last_name):
            self.nombre = f"{self.first_name} {self.last_name}".strip()
        elif not self.nombre:
            self.nombre = self.username
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre if self.nombre else self.username
    
    def get_full_name(self):
        """Retorna el nombre completo del usuario"""
        return self.nombre if self.nombre else super().get_full_name()
