from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EventoViewSet, all_eventos_admin

# DefaultRouter crea automáticamente las URLs para las acciones estándar
# (listar, crear, recuperar, actualizar, eliminar).
router = DefaultRouter()
router.register(r'eventos', EventoViewSet, basename='evento')

# Las URLs de nuestra API para la app 'records'.
urlpatterns = [
    path('', include(router.urls)),
    # Endpoints de administración
    path('eventos/admin/all/', all_eventos_admin, name='all_eventos_admin'),
]
