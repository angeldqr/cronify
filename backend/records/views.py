from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from .models import Evento, ArchivoAdjunto
from .serializers import EventoSerializer, ArchivoAdjuntoSerializer
from .permissions import IsOwnerOrReadOnly

class EventoViewSet(viewsets.ModelViewSet):
    """
    API endpoint para Eventos, con una acción para subir archivos.
    """
    serializer_class = EventoSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        return Evento.objects.filter(
            Q(es_publico=True) | Q(creador=user) | Q(notificar_a=user),
            deleted_at__isnull=True
        ).distinct().order_by('fecha_vencimiento')

    def perform_create(self, serializer):
        serializer.save(creador=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[IsOwnerOrReadOnly])
    def upload_file(self, request, pk=None):
        """
        Acción personalizada para subir un archivo adjunto a un evento específico.
        URL: /api/eventos/{id}/upload_file/
        """
        evento = self.get_object()
        file = request.FILES.get('archivo')

        if not file:
            return Response(
                {'detail': 'No se proporcionó ningún archivo.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Crea la instancia del archivo adjunto en la base de datos
        adjunto = ArchivoAdjunto.objects.create(
            evento=evento,
            archivo=file,
            nombre_original=file.name,
            tipo_mime=file.content_type,
            tamaño_bytes=file.size
        )

        serializer = ArchivoAdjuntoSerializer(adjunto)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

