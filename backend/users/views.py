from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import redirect
from django.conf import settings
from .models import Usuario
from .serializers import UserSerializer, UserProfileSerializer, AdminUserSerializer
from .permissions import IsAdmin
from .microsoft_auth import MicrosoftAuthService
import logging

logger = logging.getLogger(__name__)


class UserCreateView(generics.CreateAPIView):
    """
    Vista para crear/registrar nuevos usuarios.
    """
    queryset = Usuario.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        logger.info(f"Intento de registro con datos: {request.data}")
        serializer = self.get_serializer(data=request.data)
        
        if not serializer.is_valid():
            logger.error(f"Errores de validación: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        logger.info(f"Usuario creado exitosamente: {serializer.data}")
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def list_users(request):
    """
    Vista para listar todos los usuarios registrados.
    Retorna id, nombre completo y email de cada usuario.
    """
    users = Usuario.objects.filter(is_active=True).exclude(id=request.user.id)
    users_data = [
        {
            'id': user.id,
            'nombre': user.get_full_name() or user.username,
            'email': user.email
        }
        for user in users
    ]
    return Response(users_data)


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
        print(f"Datos recibidos: {request.data}")  # Debug
        serializer = UserProfileSerializer(
            user, 
            data=request.data, 
            partial=partial,
            context={'request': request}
        )
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        print(f"Errores de validación: {serializer.errors}")  # Debug
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


class MicrosoftLoginView(APIView):
    """
    Vista para iniciar el proceso de autenticación con Microsoft OAuth
    """
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        """Redirige al usuario a la página de autorización de Microsoft"""
        try:
            auth_service = MicrosoftAuthService()
            auth_url = auth_service.get_authorization_url()
            return Response({'auth_url': auth_url})
        except Exception as e:
            logger.error(f"Error al obtener URL de autorización: {str(e)}")
            return Response(
                {'error': 'No se pudo iniciar el proceso de autenticación'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class MicrosoftCallbackView(APIView):
    """
    Vista de callback para manejar la respuesta de Microsoft OAuth
    """
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        """Procesa el código de autorización y crea/actualiza el usuario"""
        code = request.GET.get('code')
        error = request.GET.get('error')
        
        if error:
            logger.error(f"Error en OAuth: {error}")
            # Redirigir al frontend con error
            frontend_url = settings.CORS_ALLOWED_ORIGINS[0] if settings.CORS_ALLOWED_ORIGINS else 'http://localhost:9000'
            return redirect(f'{frontend_url}/auth/login?error=auth_failed')
        
        if not code:
            return Response(
                {'error': 'Código de autorización no proporcionado'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            auth_service = MicrosoftAuthService()
            
            # Intercambiar código por tokens
            token_response = auth_service.get_token_from_code(code)
            access_token = token_response.get('access_token')
            refresh_token = token_response.get('refresh_token')
            
            # Obtener información del usuario
            user_info = auth_service.get_user_info(access_token)
            
            # Crear o actualizar usuario
            usuario = auth_service.create_or_update_user(
                user_info, 
                access_token, 
                refresh_token
            )
            
            # Generar tokens JWT
            tokens = auth_service.get_tokens_for_user(usuario)
            
            # Redirigir al frontend con los tokens
            frontend_url = settings.CORS_ALLOWED_ORIGINS[0] if settings.CORS_ALLOWED_ORIGINS else 'http://localhost:9000'
            redirect_url = f"{frontend_url}/auth/callback?access={tokens['access']}&refresh={tokens['refresh']}"
            
            return redirect(redirect_url)
            
        except Exception as e:
            logger.error(f"Error en callback de Microsoft: {str(e)}")
            frontend_url = settings.CORS_ALLOWED_ORIGINS[0] if settings.CORS_ALLOWED_ORIGINS else 'http://localhost:9000'
            return redirect(f'{frontend_url}/auth/login?error=auth_process_failed')


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def refresh_microsoft_token(request):
    """
    Refresca el token de acceso de Microsoft del usuario autenticado
    """
    user = request.user
    
    if not user.microsoft_refresh_token:
        return Response(
            {'error': 'No hay refresh token disponible'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        auth_service = MicrosoftAuthService()
        token_response = auth_service.refresh_access_token(user.microsoft_refresh_token)
        
        # Actualizar tokens del usuario
        user.microsoft_access_token = token_response.get('access_token')
        if token_response.get('refresh_token'):
            user.microsoft_refresh_token = token_response.get('refresh_token')
        user.save()
        
        return Response({'detail': 'Token refrescado exitosamente'})
        
    except Exception as e:
        logger.error(f"Error al refrescar token: {str(e)}")
        return Response(
            {'error': 'No se pudo refrescar el token'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# ==================== VISTAS DE ADMINISTRACIÓN ====================

@api_view(['GET'])
@permission_classes([IsAdmin])
def list_all_users(request):
    """
    Vista para que los administradores listen todos los usuarios.
    Incluye información sobre quién es admin.
    
    Solo accesible por administradores.
    """
    users = Usuario.objects.filter(is_active=True).order_by('-date_joined')
    serializer = AdminUserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAdmin])
def promote_to_admin(request, user_id):
    """
    Vista para promover un usuario a administrador.
    
    Solo accesible por administradores.
    """
    try:
        user = Usuario.objects.get(id=user_id, is_active=True)
        
        if user.is_admin:
            return Response(
                {'detail': 'El usuario ya es administrador'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user.is_admin = True
        user.save()
        
        logger.info(f"Usuario {user.email} promovido a admin por {request.user.email}")
        
        return Response({
            'detail': f'Usuario {user.nombre} promovido a administrador exitosamente',
            'user': AdminUserSerializer(user).data
        })
        
    except Usuario.DoesNotExist:
        return Response(
            {'error': 'Usuario no encontrado'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['DELETE'])
@permission_classes([IsAdmin])
def remove_admin(request, user_id):
    """
    Vista para remover privilegios de administrador de un usuario.
    
    Previene que el último admin se remueva a sí mismo.
    Solo accesible por administradores.
    """
    try:
        user = Usuario.objects.get(id=user_id, is_active=True)
        
        if not user.is_admin:
            return Response(
                {'detail': 'El usuario no es administrador'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Prevenir que se quite el último admin
        admin_count = Usuario.objects.filter(is_admin=True, is_active=True).count()
        if admin_count <= 1:
            return Response(
                {'error': 'No se puede remover el último administrador del sistema'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Prevenir que un admin se remueva a sí mismo
        if user.id == request.user.id:
            return Response(
                {'error': 'No puedes remover tus propios privilegios de administrador'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user.is_admin = False
        user.save()
        
        logger.info(f"Privilegios de admin removidos de {user.email} por {request.user.email}")
        
        return Response({
            'detail': f'Privilegios de administrador removidos de {user.nombre} exitosamente',
            'user': AdminUserSerializer(user).data
        })
        
    except Usuario.DoesNotExist:
        return Response(
            {'error': 'Usuario no encontrado'},
            status=status.HTTP_404_NOT_FOUND
        )


