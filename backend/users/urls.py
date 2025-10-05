from django.urls import path
from .views import UserCreateView

urlpatterns = [
    # URL para el registro de usuarios
    path('register/', UserCreateView.as_view(), name='user_register'),
]
