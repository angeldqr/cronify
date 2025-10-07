from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from records.models import Evento
from .email_service import send_email

@shared_task
def verificar_vencimientos():
    """
    Tarea de Celery que revisa vencimientos y envía correos.
    """
    print("--- Iniciando verificación de vencimientos ---")
    now = timezone.now()

    eventos_pendientes = Evento.objects.filter(
        notificacion_enviada=False,
        deleted_at__isnull=True
    )

    eventos_notificados_count = 0
    for evento in eventos_pendientes:
        if evento.notificacion_unidad == 'días':
            fecha_notificacion = evento.fecha_vencimiento - timedelta(days=evento.notificacion_valor)
        elif evento.notificacion_unidad == 'meses':
            fecha_notificacion = evento.fecha_vencimiento - timedelta(days=evento.notificacion_valor * 30)
        else:
            continue

        if fecha_notificacion.date() <= now.date():
            print(f"Evento ID {evento.id} ('{evento.asunto}') cumple la condición. Enviando notificación...")

            # Prepara los datos para el correo
            asunto_correo = f"Recordatorio de Vencimiento: {evento.asunto}"
            cuerpo_correo = f"""
            <h1>Recordatorio de Vencimiento</h1>
            <p>Hola,</p>
            <p>Este es un recordatorio para el evento: <strong>{evento.asunto}</strong>.</p>
            <p><strong>Fecha de Vencimiento:</strong> {evento.fecha_vencimiento.strftime('%d/%m/%Y a las %H:%M')}</p>
            <p><strong>Descripción:</strong></p>
            <p>{evento.descripcion or 'No hay descripción.'}</p>
            <p>Gracias,<br>Sistema de Notificaciones Cronify</p>
            """
            
            # Recopila las direcciones de correo de los destinatarios
            destinatarios = [evento.creador.email]
            for usuario in evento.notificar_a.all():
                if usuario.email:
                    destinatarios.append(usuario.email)
            
            # Elimina duplicados
            destinatarios_unicos = list(set(destinatarios))
            
            # Llama a la función para enviar el correo
            email_enviado = send_email(asunto_correo, cuerpo_correo, destinatarios_unicos)

            if email_enviado:
                evento.notificacion_enviada = True
                evento.fecha_notificacion = now
                evento.save()
                eventos_notificados_count += 1
            else:
                print(f"Fallo al enviar notificación para el evento ID {evento.id}")

    mensaje_final = f"--- Verificación de vencimientos completada. {eventos_notificados_count} correos enviados. ---"
    print(mensaje_final)
    return mensaje_final