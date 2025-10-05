from rest_framework import generics, permissions
from .models import Usuario
from .serializers import UserSerializer

class UserCreateView(generics.CreateAPIView):
    """
    Vista para crear/registrar nuevos usuarios.
    """
    queryset = Usuario.objects.all()
    serializer_class = UserSerializer
    # Permite que cualquier usuario (incluso no autenticado) acceda a esta vista.
    permission_classes = [permissions.AllowAny]
