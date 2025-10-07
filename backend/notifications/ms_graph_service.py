import asyncio
from django.conf import settings
from azure.identity.aio import ClientSecretCredential
from msgraph_core import APIVersion
from msgraph import GraphServiceClient
from msgraph.generated.users.item.send_mail.send_mail_post_request_body import SendMailPostRequestBody
from msgraph.generated.models.message import Message
from msgraph.generated.models.item_body import ItemBody
from msgraph.generated.models.body_type import BodyType
from msgraph.generated.models.recipient import Recipient
from msgraph.generated.models.email_address import EmailAddress

async def send_email_async(subject, body, recipients):
    """
    Función asíncrona para enviar un correo usando la API de Microsoft Graph.
    """
    config = settings.MS_GRAPH_CONFIG
    credential = ClientSecretCredential(
        tenant_id=config["TENANT_ID"],
        client_id=config["CLIENT_ID"],
        client_secret=config["CLIENT_SECRET"],
    )
    
    graph_client = GraphServiceClient(credentials=credential, api_version=APIVersion.V1)

    # Prepara la lista de destinatarios
    to_recipients = []
    for email_str in recipients:
        to_recipients.append(Recipient(email_address=EmailAddress(address=email_str)))

    request_body = SendMailPostRequestBody(
        message=Message(
            subject=subject,
            body=ItemBody(
                content_type=BodyType.Html,
                content=body,
            ),
            to_recipients=to_recipients,
        ),
        save_to_sent_items=True
    )
    
    try:
        # Envía el correo desde la cuenta de usuario especificada en settings.py
        await graph_client.users.by_user_id(config["USER_ID"]).send_mail.post(body=request_body)
        print(f"Correo enviado exitosamente a: {recipients}")
        return True
    except Exception as e:
        print(f"Error al enviar correo: {e}")
        return False

def send_email(subject, body, recipients):
    """
    Función síncrona que envuelve la función asíncrona.
    Celery funciona mejor con funciones síncronas.
    """
    return asyncio.run(send_email_async(subject, body, recipients))