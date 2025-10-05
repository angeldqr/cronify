from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EventoViewSet

# DefaultRouter crea automáticamente las URLs para las acciones estándar
# (listar, crear, recuperar, actualizar, eliminar).
router = DefaultRouter()
router.register(r'eventos', EventoViewSet, basename='evento')

# Las URLs de nuestra API para la app 'records'.
urlpatterns = [
    path('', include(router.urls)),
]
