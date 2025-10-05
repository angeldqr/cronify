from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    # Heredamos todos los campos de AbstractUser (username, email, etc.)
    # y podemos añadir más en el futuro si es necesario.
    pass

    def __str__(self):
        return self.username