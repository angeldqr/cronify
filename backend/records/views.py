from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q, Sum
from django.utils import timezone
from datetime import datetime
from .models import Evento, ArchivoAdjunto
from .serializers import EventoSerializer, ArchivoAdjuntoSerializer
from .permissions import IsOwnerOrReadOnly
from users.permissions import IsAdmin

class EventoViewSet(viewsets.ModelViewSet):
    """
    API endpoint para Eventos con búsqueda y filtrado.
    
    Parámetros de búsqueda/filtrado:
    - search: Busca en asunto y descripción
    - fecha_inicio: Filtra eventos desde esta fecha
    - fecha_fin: Filtra eventos hasta esta fecha
    - creador: Filtra por ID del creador
    - notificado: true/false para filtrar por estado de notificación
    """
    serializer_class = EventoSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        queryset = Evento.objects.filter(
            Q(es_publico=True) | Q(creador=user) | Q(notificar_a=user),
            deleted_at__isnull=True
        ).distinct()

        # Búsqueda por texto en asunto y descripción
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(asunto__icontains=search) | Q(descripcion__icontains=search)
            )

        # Filtrado por rango de fechas
        fecha_inicio = self.request.query_params.get('fecha_inicio', None)
        fecha_fin = self.request.query_params.get('fecha_fin', None)
        
        if fecha_inicio:
            try:
                fecha_inicio_dt = datetime.fromisoformat(fecha_inicio.replace('Z', '+00:00'))
                queryset = queryset.filter(fecha_vencimiento__gte=fecha_inicio_dt)
            except ValueError:
                pass  # Ignora fechas inválidas
        
        if fecha_fin:
            try:
                fecha_fin_dt = datetime.fromisoformat(fecha_fin.replace('Z', '+00:00'))
                queryset = queryset.filter(fecha_vencimiento__lte=fecha_fin_dt)
            except ValueError:
                pass  # Ignora fechas inválidas

        # Filtrado por creador
        creador_id = self.request.query_params.get('creador', None)
        if creador_id:
            queryset = queryset.filter(creador__id=creador_id)

        # Filtrado por estado de notificación
        notificacion_enviada = self.request.query_params.get('notificacion_enviada', None)
        if notificacion_enviada is not None:
            if notificacion_enviada.lower() == 'true':
                queryset = queryset.filter(notificacion_enviada=True)
            elif notificacion_enviada.lower() == 'false':
                queryset = queryset.filter(notificacion_enviada=False)

        # Filtrado por visibilidad (público/privado)
        es_publico = self.request.query_params.get('es_publico', None)
        if es_publico is not None:
            if es_publico.lower() == 'true':
                queryset = queryset.filter(es_publico=True)
            elif es_publico.lower() == 'false':
                queryset = queryset.filter(es_publico=False)

        # Ordenar por fecha de vencimiento (más próximos primero)
        return queryset.order_by('fecha_vencimiento')

    def perform_create(self, serializer):
        serializer.save(creador=self.request.user)

    def perform_destroy(self, instance):
        """
        Implementa eliminación lógica (soft delete).
        En lugar de eliminar el registro, marca deleted_at con la fecha actual.
        """
        instance.deleted_at = timezone.now()
        instance.save()

    @action(detail=True, methods=['post'], permission_classes=[IsOwnerOrReadOnly])
    def upload_file(self, request, pk=None):
        """
        Acción personalizada para subir un archivo adjunto a un evento específico.
        URL: /api/eventos/{id}/upload_file/
        
        Límites:
        - Máximo 10MB por archivo
        - Máximo 50MB total por evento
        """
        evento = self.get_object()
        file = request.FILES.get('archivo')

        if not file:
            return Response(
                {'detail': 'No se proporcionó ningún archivo.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validar tamaño del archivo individual (10MB)
        MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB en bytes
        if file.size > MAX_FILE_SIZE:
            return Response(
                {'detail': f'El archivo excede el tamaño máximo permitido de 10MB. Tamaño actual: {file.size / (1024*1024):.2f}MB'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validar tamaño total de archivos del evento (50MB)
        MAX_TOTAL_SIZE = 50 * 1024 * 1024  # 50MB en bytes
        total_size = evento.archivos_adjuntos.aggregate(
            total=Sum('tamaño_bytes')
        )['total'] or 0
        
        if total_size + file.size > MAX_TOTAL_SIZE:
            return Response(
                {'detail': f'El evento ya tiene {total_size / (1024*1024):.2f}MB de archivos. El límite total es 50MB.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Crear la instancia del archivo adjunto en la base de datos
        adjunto = ArchivoAdjunto.objects.create(
            evento=evento,
            archivo=file,
            nombre_original=file.name,
            tipo_mime=file.content_type,
            tamaño_bytes=file.size
        )

        serializer = ArchivoAdjuntoSerializer(adjunto)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['delete'], url_path='archivos/(?P<archivo_id>[^/.]+)', permission_classes=[IsOwnerOrReadOnly])
    def delete_archivo(self, request, pk=None, archivo_id=None):
        """
        Acción personalizada para eliminar un archivo adjunto de un evento.
        URL: /api/eventos/{id}/archivos/{archivo_id}/
        """
        evento = self.get_object()
        
        try:
            archivo = ArchivoAdjunto.objects.get(id=archivo_id, evento=evento)
            archivo.delete()
            return Response(
                {'detail': 'Archivo eliminado exitosamente.'},
                status=status.HTTP_204_NO_CONTENT
            )
        except ArchivoAdjunto.DoesNotExist:
            return Response(
                {'detail': 'Archivo no encontrado.'},
                status=status.HTTP_404_NOT_FOUND
            )


# ==================== VISTAS DE ADMINISTRACIÓN ====================

@api_view(['GET'])
@permission_classes([IsAdmin])
def all_eventos_admin(request):
    """
    Vista para que los administradores vean TODOS los eventos del sistema.
    
    Incluye eventos públicos, privados y de cualquier usuario.
    Solo accesible por administradores.
    
    Parámetros de búsqueda opcionales:
    - search: Busca en asunto y descripción
    - fecha_inicio: Filtra eventos desde esta fecha
    - fecha_fin: Filtra eventos hasta esta fecha
    - creador: Filtra por ID del creador
    - page: Número de página (paginación de 20 eventos)
    """
    # Obtener TODOS los eventos no eliminados
    queryset = Evento.objects.filter(deleted_at__isnull=True).order_by('-fecha_creacion')
    
    # Búsqueda por texto
    search = request.query_params.get('search', None)
    if search:
        queryset = queryset.filter(
            Q(asunto__icontains=search) | Q(descripcion__icontains=search)
        )
    
    # Filtrado por rango de fechas
    fecha_inicio = request.query_params.get('fecha_inicio', None)
    fecha_fin = request.query_params.get('fecha_fin', None)
    
    if fecha_inicio:
        try:
            fecha_inicio_dt = datetime.fromisoformat(fecha_inicio.replace('Z', '+00:00'))
            queryset = queryset.filter(fecha_vencimiento__gte=fecha_inicio_dt)
        except ValueError:
            pass
    
    if fecha_fin:
        try:
            fecha_fin_dt = datetime.fromisoformat(fecha_fin.replace('Z', '+00:00'))
            queryset = queryset.filter(fecha_vencimiento__lte=fecha_fin_dt)
        except ValueError:
            pass
    
    # Filtrado por creador
    creador = request.query_params.get('creador', None)
    if creador:
        queryset = queryset.filter(creador_id=creador)
    
    # Aplicar paginación
    paginator = PageNumberPagination()
    paginator.page_size = 20
    paginated_queryset = paginator.paginate_queryset(queryset, request)
    
    serializer = EventoSerializer(paginated_queryset, many=True, context={'request': request})
    
    return paginator.get_paginated_response(serializer.data)







