from django.core.management.base import BaseCommand
from users.models import Usuario
from records.models import Evento
from django.utils import timezone
from datetime import timedelta
import random


class Command(BaseCommand):
    help = 'Crea múltiples eventos de prueba para diferentes usuarios'

    def add_arguments(self, parser):
        parser.add_argument(
            'cantidad',
            type=int,
            help='Cantidad de eventos a crear',
            default=100
        )

    def handle(self, *args, **options):
        cantidad = options['cantidad']
        
        # Obtener usuarios (excluyendo superusuarios)
        usuarios = list(Usuario.objects.filter(is_active=True, is_superuser=False)[:30])
        
        if not usuarios:
            self.stdout.write(self.style.ERROR('No hay usuarios disponibles'))
            return
        
        asuntos = [
            'Renovación de contrato', 'Pago de factura', 'Entrega de proyecto',
            'Vencimiento de licencia', 'Renovación de seguro', 'Pago de impuestos',
            'Presentación de informe', 'Revisión de documentos', 'Actualización de sistema',
            'Mantenimiento preventivo', 'Auditoría interna', 'Capacitación obligatoria',
            'Reunión con cliente', 'Entrega de propuesta', 'Firma de convenio',
            'Evaluación de desempeño', 'Renovación de certificado', 'Pago de nómina',
            'Revisión de inventario', 'Actualización de software', 'Backup de datos',
            'Renovación de dominio', 'Pago de servicios', 'Inspección de seguridad',
            'Envío de reportes', 'Actualización de permisos', 'Revisión legal',
            'Pago de proveedores', 'Cierre de mes', 'Presentación de resultados',
            'Vencimiento de garantía', 'Renovación de membresía', 'Actualización de licencias',
            'Revisión de presupuesto', 'Entrega de materiales', 'Firma de acta',
            'Renovación de póliza', 'Pago de alquiler', 'Inspección técnica',
            'Actualización de contratos', 'Entrega de equipos', 'Revisión de calidad'
        ]
        
        descripciones = [
            'Recordatorio importante para no olvidar esta tarea',
            'Evento crítico que requiere atención inmediata',
            'Seguimiento necesario para cumplir con los plazos',
            'Actividad programada para el periodo establecido',
            'Compromiso adquirido que debe ser cumplido',
            'Tarea pendiente de alta prioridad',
            'Actividad recurrente del proceso estándar',
            'Evento importante para el cumplimiento de objetivos',
            'Tarea administrativa de rutina',
            'Compromiso contractual que debe ser atendido',
            'Actividad programada según calendario',
            'Evento que requiere coordinación con otras áreas',
            'Tarea de seguimiento y control',
            'Actividad de cumplimiento regulatorio',
            'Evento crítico para la operación'
        ]
        
        eventos_creados = 0
        
        self.stdout.write(self.style.WARNING(f'Creando {cantidad} eventos de prueba...'))
        
        for i in range(cantidad):
            # Seleccionar usuario aleatorio como creador
            creador = random.choice(usuarios)
            
            # Fecha de vencimiento aleatoria (entre ayer y 60 días en el futuro)
            dias_adelante = random.randint(-1, 60)
            fecha_vencimiento = timezone.now() + timedelta(days=dias_adelante)
            
            # 70% públicos, 30% privados
            es_publico = random.random() < 0.7
            
            # Asunto y descripción aleatorios
            asunto = random.choice(asuntos)
            descripcion = random.choice(descripciones)
            
            try:
                evento = Evento.objects.create(
                    asunto=asunto,
                    descripcion=descripcion,
                    fecha_vencimiento=fecha_vencimiento,
                    es_publico=es_publico,
                    creador=creador
                )
                
                # 40% de probabilidad de notificar a otros usuarios (1-3 usuarios)
                if random.random() < 0.4:
                    # Seleccionar 1-3 usuarios aleatorios (sin incluir al creador)
                    otros_usuarios = [u for u in usuarios if u.id != creador.id]
                    cantidad_notificar = random.randint(1, min(3, len(otros_usuarios)))
                    usuarios_notificar = random.sample(otros_usuarios, cantidad_notificar)
                    evento.notificar_a.set(usuarios_notificar)
                
                eventos_creados += 1
                
                # Mostrar progreso cada 10 eventos
                if eventos_creados % 10 == 0:
                    self.stdout.write(f'  Creados: {eventos_creados}/{cantidad}...')
                    
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Error al crear evento {i+1}: {str(e)}')
                )
        
        # Resumen
        self.stdout.write('\n' + '='*60)
        self.stdout.write(self.style.SUCCESS(f'✓ Eventos creados exitosamente: {eventos_creados}'))
        self.stdout.write('='*60)
        
        # Estadísticas
        total_eventos = Evento.objects.filter(deleted_at__isnull=True).count()
        eventos_publicos = Evento.objects.filter(es_publico=True, deleted_at__isnull=True).count()
        eventos_privados = Evento.objects.filter(es_publico=False, deleted_at__isnull=True).count()
        eventos_con_notificaciones = Evento.objects.filter(notificar_a__isnull=False, deleted_at__isnull=True).distinct().count()
        
        self.stdout.write('\n' + self.style.SUCCESS('Estadísticas del sistema:'))
        self.stdout.write(f'  Total de eventos: {total_eventos}')
        self.stdout.write(f'  Eventos públicos: {eventos_publicos}')
        self.stdout.write(f'  Eventos privados: {eventos_privados}')
        self.stdout.write(f'  Eventos con notificaciones: {eventos_con_notificaciones}')
        self.stdout.write(f'  Usuarios con eventos: {len(usuarios)}')
