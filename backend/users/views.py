from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Usuario
from .serializers import UserSerializer, UserProfileSerializer

class UserCreateView(generics.CreateAPIView):
    """
    Vista para crear/registrar nuevos usuarios.
    """
    queryset = Usuario.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


@api_view(['GET', 'PUT', 'PATCH'])
@permission_classes([permissions.IsAuthenticated])
def user_profile(request):
    """
    Vista para ver y editar el perfil del usuario autenticado.
    
    GET: Obtiene la información del perfil
    PUT/PATCH: Actualiza el perfil
    """
    user = request.user
    
    if request.method == 'GET':
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)
    
    elif request.method in ['PUT', 'PATCH']:
        partial = request.method == 'PATCH'
        serializer = UserProfileSerializer(user, data=request.data, partial=partial)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def change_password(request):
    """
    Vista para cambiar la contraseña del usuario autenticado.
    
    Requiere:
    - old_password: Contraseña actual
    - new_password: Nueva contraseña
    """
    user = request.user
    old_password = request.data.get('old_password')
    new_password = request.data.get('new_password')
    
    if not old_password or not new_password:
        return Response(
            {'detail': 'Se requieren old_password y new_password'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Verificar que la contraseña actual sea correcta
    if not user.check_password(old_password):
        return Response(
            {'detail': 'La contraseña actual es incorrecta'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Validar la nueva contraseña
    if len(new_password) < 8:
        return Response(
            {'detail': 'La nueva contraseña debe tener al menos 8 caracteres'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Cambiar la contraseña
    user.set_password(new_password)
    user.save()
    
    return Response({'detail': 'Contraseña actualizada exitosamente'})
