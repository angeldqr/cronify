from rest_framework import viewsets, permissions
from django.db.models import Q
from .models import Evento
from .serializers import EventoSerializer

class EventoViewSet(viewsets.ModelViewSet):
    """
    API endpoint que permite ver o editar eventos.
    """
    serializer_class = EventoSerializer
    # Solo los usuarios autenticados pueden interactuar con esta API.
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Este método personaliza la consulta a la base de datos.
        Asegura que un usuario solo pueda ver los eventos que le corresponden:
        1. Todos los eventos públicos.
        2. Los eventos privados que él mismo creó.
        3. Los eventos privados en los que fue añadido para ser notificado.
        """
        user = self.request.user
        return Evento.objects.filter(
            Q(es_publico=True) | Q(creador=user) | Q(notificar_a=user)
        ).distinct().order_by('fecha_vencimiento')

    def perform_create(self, serializer):
        """
        Este método se ejecuta al crear un nuevo evento.
        Asigna automáticamente al usuario autenticado como el creador del evento.
        """
        serializer.save(creador=self.request.user)
