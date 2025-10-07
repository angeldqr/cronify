from django.urls import path
from .views import UserCreateView, user_profile, change_password

urlpatterns = [
    # Registro de usuarios
    path('register/', UserCreateView.as_view(), name='user_register'),
    
    # Perfil de usuario (ver y editar)
    path('profile/', user_profile, name='user_profile'),
    
    # Cambio de contraseña
    path('change-password/', change_password, name='change_password'),
]

