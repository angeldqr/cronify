from django.urls import path
from .views import (
    UserCreateView, 
    user_profile, 
    change_password, 
    list_users,
    MicrosoftLoginView,
    MicrosoftCallbackView,
    refresh_microsoft_token
)

urlpatterns = [
    # Registro de usuarios
    path('register/', UserCreateView.as_view(), name='user_register'),
    
    # Listar usuarios
    path('list/', list_users, name='list_users'),
    
    # Perfil de usuario (ver y editar)
    path('profile/', user_profile, name='user_profile'),
    
    # Cambio de contraseña
    path('change-password/', change_password, name='change_password'),
    
    # Autenticación con Microsoft
    path('microsoft/login/', MicrosoftLoginView.as_view(), name='microsoft_login'),
    path('microsoft/callback/', MicrosoftCallbackView.as_view(), name='microsoft_callback'),
    path('microsoft/refresh-token/', refresh_microsoft_token, name='refresh_microsoft_token'),
]

