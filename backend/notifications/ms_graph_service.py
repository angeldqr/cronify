"""
Servicio de Microsoft Graph para envío de correos
Utiliza MSAL para autenticación y Microsoft Graph API
"""
import msal
import requests
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class MicrosoftGraphEmailService:
    """Servicio para enviar correos mediante Microsoft Graph API"""
    
    def __init__(self, access_token=None):
        """
        Inicializa el servicio
        Args:
            access_token: Token de acceso opcional. Si no se proporciona, se obtiene uno nuevo.
        """
        self.client_id = settings.MICROSOFT_CLIENT_ID
        self.client_secret = settings.MICROSOFT_CLIENT_SECRET
        self.authority = settings.MICROSOFT_AUTHORITY
        self.graph_endpoint = settings.MICROSOFT_GRAPH_API_ENDPOINT
        self.access_token = access_token
        
        if not self.access_token:
            self.access_token = self._get_access_token()
    
    def _get_access_token(self):
        """
        Obtiene un token de acceso usando credenciales de la aplicación
        Returns:
            str: Access token
        """
        app = msal.ConfidentialClientApplication(
            self.client_id,
            authority=self.authority,
            client_credential=self.client_secret,
        )
        
        # Usar flujo de credenciales del cliente para aplicación
        scopes = ["https://graph.microsoft.com/.default"]
        result = app.acquire_token_for_client(scopes=scopes)
        
        if "access_token" in result:
            return result["access_token"]
        else:
            error = result.get("error_description", "Error desconocido")
            logger.error(f"Error al obtener access token: {error}")
            raise Exception(f"No se pudo obtener el token de acceso: {error}")
    
    def send_email(self, subject, body, recipients, sender_email=None):
        """
        Envía un correo usando Microsoft Graph API
        Args:
            subject: Asunto del correo
            body: Cuerpo del correo (puede ser HTML)
            recipients: Lista de direcciones de correo electrónico
            sender_email: Email del remitente (si no se proporciona, usa el configurado)
        Returns:
            bool: True si se envió exitosamente, False en caso contrario
        """
        if not sender_email:
            sender_email = settings.EMAIL_HOST_USER
        
        if not sender_email:
            logger.error("No se ha configurado EMAIL_HOST_USER")
            return False
        
        # Preparar destinatarios
        to_recipients = [{"emailAddress": {"address": email}} for email in recipients]
        
        # Preparar el mensaje
        message = {
            "message": {
                "subject": subject,
                "body": {
                    "contentType": "HTML",
                    "content": body
                },
                "toRecipients": to_recipients
            },
            "saveToSentItems": "true"
        }
        
        # Headers para la solicitud
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
        
        # Endpoint para enviar correo
        endpoint = f'{self.graph_endpoint}/users/{sender_email}/sendMail'
        
        try:
            response = requests.post(endpoint, headers=headers, json=message)
            
            if response.status_code == 202:
                logger.info(f"Correo enviado exitosamente a: {recipients}")
                return True
            else:
                logger.error(f"Error al enviar correo: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"Excepción al enviar correo: {str(e)}")
            return False


def send_email(subject, body, recipients, sender_email=None):
    """
    Función auxiliar para enviar correos
    Compatible con la interfaz anterior para Celery
    Args:
        subject: Asunto del correo
        body: Cuerpo del correo (HTML)
        recipients: Lista de correos destinatarios
        sender_email: Email del remitente opcional
    Returns:
        bool: True si se envió, False en caso contrario
    """
    service = MicrosoftGraphEmailService()
    return service.send_email(subject, body, recipients, sender_email)
