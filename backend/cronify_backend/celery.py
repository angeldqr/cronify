import os
from celery import Celery

# Establece el módulo de settings de Django para el programa 'celery'.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cronify_backend.settings')

app = Celery('cronify_backend')

# Usando un string aquí significa que el worker no necesita serializar
# el objeto de configuración. El namespace 'CELERY' significa que
# todas las variables de configuración de Celery deben tener un prefijo `CELERY_`.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Carga automáticamente los módulos de tareas de todas las apps registradas en Django.
app.autodiscover_tasks()

