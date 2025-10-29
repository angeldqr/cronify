"""
Servicio de autenticación con Microsoft OAuth 2.0
Maneja el flujo de autenticación usando MSAL
"""
import msal
import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
import logging

logger = logging.getLogger(__name__)
Usuario = get_user_model()


class MicrosoftAuthService:
    """Servicio para manejar la autenticación OAuth con Microsoft"""
    
    def __init__(self):
        self.client_id = settings.MICROSOFT_CLIENT_ID
        self.client_secret = settings.MICROSOFT_CLIENT_SECRET
        self.authority = settings.MICROSOFT_AUTHORITY
        self.redirect_uri = settings.MICROSOFT_REDIRECT_URI
        self.scopes = ['User.Read', 'Mail.Send', 'offline_access']
    
    def get_msal_app(self):
        """Crea una instancia de MSAL ConfidentialClientApplication"""
        return msal.ConfidentialClientApplication(
            self.client_id,
            authority=self.authority,
            client_credential=self.client_secret,
        )
    
    def get_authorization_url(self):
        """
        Genera la URL de autorización de Microsoft
        Returns:
            tuple: (auth_url, state)
        """
        app = self.get_msal_app()
        auth_url = app.get_authorization_request_url(
            scopes=self.scopes,
            redirect_uri=self.redirect_uri,
        )
        return auth_url
    
    def get_token_from_code(self, code):
        """
        Intercambia el código de autorización por un token de acceso
        Args:
            code: Código de autorización recibido de Microsoft
        Returns:
            dict: Respuesta con access_token, refresh_token, etc.
        """
        app = self.get_msal_app()
        result = app.acquire_token_by_authorization_code(
            code,
            scopes=self.scopes,
            redirect_uri=self.redirect_uri,
        )
        
        if "error" in result:
            logger.error(f"Error al obtener token: {result.get('error_description')}")
            raise Exception(result.get("error_description"))
        
        return result
    
    def get_user_info(self, access_token):
        """
        Obtiene información del usuario desde Microsoft Graph API
        Args:
            access_token: Token de acceso de Microsoft
        Returns:
            dict: Información del usuario
        """
        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.get(
            f'{settings.MICROSOFT_GRAPH_API_ENDPOINT}/me',
            headers=headers
        )
        
        if response.status_code != 200:
            logger.error(f"Error al obtener info del usuario: {response.text}")
            raise Exception("No se pudo obtener la información del usuario")
        
        return response.json()
    
    def create_or_update_user(self, user_info, access_token, refresh_token):
        """
        Crea o actualiza un usuario basado en la información de Microsoft
        Args:
            user_info: Información del usuario de Microsoft Graph
            access_token: Token de acceso
            refresh_token: Token de actualización
        Returns:
            Usuario: Instancia del usuario
        """
        email = user_info.get('mail') or user_info.get('userPrincipalName')
        nombre = user_info.get('displayName', '')
        microsoft_id = user_info.get('id')
        
        # Buscar usuario por email o microsoft_id
        usuario = Usuario.objects.filter(email=email).first()
        
        if usuario:
            # Actualizar usuario existente
            usuario.nombre = nombre
            usuario.microsoft_id = microsoft_id
            usuario.microsoft_access_token = access_token
            usuario.microsoft_refresh_token = refresh_token
            usuario.save()
            logger.info(f"Usuario actualizado: {email}")
        else:
            # Crear nuevo usuario
            usuario = Usuario.objects.create(
                email=email,
                nombre=nombre,
                microsoft_id=microsoft_id,
                microsoft_access_token=access_token,
                microsoft_refresh_token=refresh_token,
                is_active=True
            )
            # No establecer contraseña para usuarios de OAuth
            logger.info(f"Usuario creado: {email}")
        
        return usuario
    
    def get_tokens_for_user(self, usuario):
        """
        Genera tokens JWT para el usuario
        Args:
            usuario: Instancia del modelo Usuario
        Returns:
            dict: access y refresh tokens
        """
        refresh = RefreshToken.for_user(usuario)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
    
    def refresh_access_token(self, refresh_token):
        """
        Refresca el access token usando el refresh token
        Args:
            refresh_token: Token de actualización de Microsoft
        Returns:
            dict: Nueva respuesta con tokens
        """
        app = self.get_msal_app()
        result = app.acquire_token_by_refresh_token(
            refresh_token,
            scopes=self.scopes
        )
        
        if "error" in result:
            logger.error(f"Error al refrescar token: {result.get('error_description')}")
            raise Exception(result.get("error_description"))
        
        return result
