from django.core.mail import send_mail
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def send_email(subject, html_content, recipients):
    """
    Envía un correo electrónico usando Django Email (SMTP).
    
    Args:
        subject (str): Asunto del correo
        html_content (str): Contenido HTML del correo
        recipients (list): Lista de direcciones de correo destinatarias
    
    Returns:
        bool: True si se envió correctamente, False si hubo error
    """
    try:
        if not recipients:
            logger.warning("No se proporcionaron destinatarios para el correo")
            return False
        
        # Filtrar destinatarios válidos
        valid_recipients = [email for email in recipients if email]
        
        if not valid_recipients:
            logger.warning("No hay destinatarios válidos después de filtrar")
            return False
        
        send_mail(
            subject=subject,
            message='',  # Texto plano vacío
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=valid_recipients,
            html_message=html_content,
            fail_silently=False,
        )
        
        logger.info(f"Correo enviado exitosamente a: {', '.join(valid_recipients)}")
        return True
        
    except Exception as e:
        logger.error(f"Error al enviar correo: {str(e)}")
        return False
