<template>
  <q-card :style="$q.screen.gt.md ? 'min-width: 750px; max-width: 850px; max-height: 90vh; border-radius: 16px; display: flex; flex-direction: column;' : 'width: 100%; max-width: 95vw; max-height: 90vh; border-radius: 8px; display: flex; flex-direction: column;'" class="event-detail-modal">
    <div class="modal-header">
      <div class="header-content">
        <div class="header-title">
          <h5 :class="$q.screen.gt.xs ? 'event-title' : 'event-title-mobile'">{{ event.asunto }}</h5>
          <div class="badges-row">
            <span class="badge" :class="event.es_publico ? 'badge-public' : 'badge-private'">
              <q-icon :name="event.es_publico ? 'lock_open' : 'lock'" size="14px" class="q-mr-xs" />
              {{ event.es_publico ? 'Público' : 'Privado' }}
            </span>
            <span v-if="event.notificacion_enviada" class="badge badge-success">
              <q-icon name="check_circle" size="14px" class="q-mr-xs" />
              Notificado
            </span>
          </div>
        </div>
        <q-btn icon="close" flat round dense color="white" v-close-popup class="close-btn" />
      </div>
      <div class="header-meta">
        Creado por {{ event.creador_nombre || event.creador_username || 'Usuario' }}
      </div>
    </div>

    <q-card-section class="modal-body scroll q-pa-sm q-pa-md-md" style="flex: 1; overflow-y: auto;">
      <div :class="$q.screen.gt.sm ? 'info-grid' : 'info-grid-mobile'">
        <div class="info-item">
          <div class="info-icon-wrapper blue">
            <q-icon name="schedule" size="24px" />
          </div>
          <div class="info-content">
            <div class="info-label">Fecha y Hora</div>
            <div class="info-value">{{ formatDateTime(event.fecha_vencimiento) }}</div>
          </div>
        </div>

        <div class="info-item">
          <div class="info-icon-wrapper orange">
            <q-icon name="notifications" size="24px" />
          </div>
          <div class="info-content">
            <div class="info-label">Notificación</div>
            <div class="info-value">{{ event.notificacion_valor }} {{ event.notificacion_unidad }} antes del vencimiento</div>
          </div>
        </div>

        <div v-if="event.descripcion" class="info-item full-width">
          <div class="info-icon-wrapper gray">
            <q-icon name="description" size="24px" />
          </div>
          <div class="info-content">
            <div class="info-label">Descripción</div>
            <div class="info-value description-text" v-html="event.descripcion"></div>
          </div>
        </div>

        <div v-if="archivosAdjuntos.length > 0" class="info-item full-width">
          <div class="info-icon-wrapper purple">
            <q-icon name="attach_file" size="24px" />
          </div>
          <div class="info-content">
            <div class="info-label">Archivos Adjuntos ({{ archivosAdjuntos.length }})</div>
            <div class="files-grid">
              <div
                v-for="file in archivosAdjuntos"
                :key="file.id"
                class="file-card"
                @click="downloadFile(file)"
              >
                <q-icon :name="getFileIcon(file.nombre_original)" :color="getFileColor(file.nombre_original)" size="28px" />
                <div class="file-name">{{ file.nombre_original }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </q-card-section>

    <template v-if="isEventOwner">
      <q-separator />
      <q-card-actions class="modal-actions">
        <q-btn
          flat
          label="EDITAR"
          icon="edit"
          color="primary"
          @click="handleEdit"
          class="action-btn"
        />
        <q-btn
          flat
          label="ELIMINAR"
          icon="delete"
          color="negative"
          @click="handleDelete"
          class="action-btn"
        />
      </q-card-actions>
    </template>
  </q-card>
</template>

<script setup>
import { useQuasar } from 'quasar';
import { computed } from 'vue';
import { useEventosStore } from '../../stores/eventos';
import { useAuthStore } from '../../stores/auth';

const props = defineProps({
  event: {
    type: Object,
    required: true
  }
});

const emit = defineEmits(['close', 'updated', 'deleted', 'edit']);

const $q = useQuasar();
const eventosStore = useEventosStore();
const authStore = useAuthStore();

// Verificar si el usuario actual es el dueño del evento
const isEventOwner = computed(() => {
  return authStore.user?.id === props.event.creador;
});

const archivosAdjuntos = computed(() => {
  return props.event.archivos_adjuntos || [];
});

const formatDateTime = (dateString) => {
  const date = new Date(dateString);
  
  // Obtener fecha formateada
  const fechaFormato = date.toLocaleDateString('es-ES', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });
  
  // Obtener hora en formato 12 horas con AM/PM
  const horaFormato = date.toLocaleTimeString('es-ES', {
    hour: 'numeric',
    minute: '2-digit',
    hour12: true
  });
  
  return `${fechaFormato}, ${horaFormato}`;
};

const getFileIcon = (filename) => {
  const ext = filename.split('.').pop().toLowerCase();
  const iconMap = {
    pdf: 'picture_as_pdf',
    doc: 'description',
    docx: 'description',
    xls: 'table_chart',
    xlsx: 'table_chart',
    ppt: 'slideshow',
    pptx: 'slideshow',
    jpg: 'image',
    jpeg: 'image',
    png: 'image',
    gif: 'image',
    zip: 'folder_zip',
    rar: 'folder_zip'
  };
  return iconMap[ext] || 'insert_drive_file';
};

const getFileColor = (filename) => {
  const ext = filename.split('.').pop().toLowerCase();
  const colorMap = {
    pdf: 'red-6',
    doc: 'blue-6',
    docx: 'blue-6',
    xls: 'green-6',
    xlsx: 'green-6',
    ppt: 'orange-6',
    pptx: 'orange-6',
    jpg: 'purple-6',
    jpeg: 'purple-6',
    png: 'purple-6',
    gif: 'purple-6',
    zip: 'amber-7',
    rar: 'amber-7'
  };
  return colorMap[ext] || 'grey-6';
};

const downloadFile = (file) => {
  if (file.url_descarga) {
    window.open(file.url_descarga, '_blank');
  } else {
    $q.notify({
      type: 'warning',
      message: 'No se puede descargar este archivo',
      position: 'top'
    });
  }
};

const handleEdit = () => {
  emit('edit', props.event);
};

const handleDelete = () => {
  $q.dialog({
    title: 'Confirmar eliminación',
    message: '¿Estás seguro que deseas eliminar este evento?',
    cancel: {
      label: 'Cancelar',
      flat: true,
      color: 'grey-7'
    },
    ok: {
      label: 'Eliminar',
      flat: true,
      color: 'negative'
    },
    persistent: true
  }).onOk(async () => {
    try {
      await eventosStore.deleteEvento(props.event.id);
      $q.notify({
        type: 'positive',
        message: 'Evento eliminado exitosamente',
        position: 'top'
      });
      emit('deleted');
    } catch {
      $q.notify({
        type: 'negative',
        message: 'Error al eliminar el evento',
        position: 'top'
      });
    }
  });
};
</script>

<style scoped lang="scss">
.event-detail-modal {
  overflow: hidden;
}

.modal-header {
  background: linear-gradient(135deg, #1976d2 0%, #1565c0 100%);
  padding: 28px 32px 24px;
  position: relative;

  .header-content {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 12px;

    .header-title {
      flex: 1;

      .event-title {
        margin: 0 0 12px 0;
        font-size: 22px;
        font-weight: 600;
        color: white;
        line-height: 1.3;
      }

      .badges-row {
        display: flex;
        gap: 8px;
        flex-wrap: wrap;
      }
    }

    .close-btn {
      margin-top: -4px;
    }
  }

  .header-meta {
    font-size: 13px;
    color: rgba(255, 255, 255, 0.85);
    font-weight: 500;
  }
}

.badge {
  display: inline-flex;
  align-items: center;
  padding: 5px 12px;
  border-radius: 16px;
  font-size: 12px;
  font-weight: 600;
  color: white;
  
  &.badge-public {
    background: linear-gradient(135deg, #4caf50 0%, #388e3c 100%);
  }
  
  &.badge-private {
    background: linear-gradient(135deg, #ff9800 0%, #f57c00 100%);
  }
  
  &.badge-success {
    background: linear-gradient(135deg, #2196f3 0%, #1976d2 100%);
  }
}

.modal-body {
  padding: 32px;
  background: #fafafa;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;

  .full-width {
    grid-column: 1 / -1;
  }
}

.info-item {
  background: white;
  border-radius: 12px;
  padding: 20px;
  display: flex;
  gap: 16px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
  transition: all 0.2s ease;

  &:hover {
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
    transform: translateY(-2px);
  }
}

.info-icon-wrapper {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  color: white;

  &.blue {
    background: linear-gradient(135deg, #2196f3 0%, #1976d2 100%);
  }

  &.orange {
    background: linear-gradient(135deg, #ff9800 0%, #f57c00 100%);
  }

  &.gray {
    background: linear-gradient(135deg, #78909c 0%, #546e7a 100%);
  }

  &.purple {
    background: linear-gradient(135deg, #ab47bc 0%, #8e24aa 100%);
  }
}

.info-content {
  flex: 1;
  min-width: 0;

  .info-label {
    font-size: 12px;
    font-weight: 600;
    color: #78909c;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 6px;
  }

  .info-value {
    font-size: 15px;
    color: #263238;
    font-weight: 500;
    line-height: 1.5;
    word-wrap: break-word;

    &.description-text {
      white-space: normal;
      font-weight: 400;
      color: #546e7a;
      
      // Estilos para contenido HTML del editor
      :deep(p) {
        margin-bottom: 0.5em;
      }
      
      :deep(ul), :deep(ol) {
        padding-left: 1.5em;
        margin-bottom: 0.5em;
      }
      
      :deep(strong) {
        font-weight: 600;
        color: #263238;
      }
      
      :deep(em) {
        font-style: italic;
      }
      
      :deep(u) {
        text-decoration: underline;
      }
      
      :deep(h1), :deep(h2), :deep(h3), :deep(h4), :deep(h5), :deep(h6) {
        font-weight: 600;
        margin-bottom: 0.5em;
        color: #263238;
      }
    }
  }
}

.files-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
  gap: 12px;
  margin-top: 12px;
}

.file-card {
  background: #f5f5f5;
  border: 2px solid #e0e0e0;
  border-radius: 10px;
  padding: 16px 12px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  transition: all 0.2s ease;

  &:hover {
    background: white;
    border-color: #1976d2;
    box-shadow: 0 4px 12px rgba(25, 118, 210, 0.15);
    transform: translateY(-2px);
  }

  .file-name {
    font-size: 12px;
    font-weight: 500;
    color: #546e7a;
    text-align: center;
    word-break: break-word;
    line-height: 1.3;
  }
}

.modal-actions {
  padding: 16px 24px;
  background: white;
  display: flex;
  justify-content: flex-end;
  gap: 8px;

  .action-btn {
    font-weight: 600;
    padding: 8px 24px;
    border-radius: 8px;
    transition: all 0.2s ease;

    &:hover {
      transform: translateY(-1px);
    }
  }
}

/* Estilos Responsive */
@media (max-width: 600px) {
  .event-title-mobile {
    font-size: 18px !important;
    margin: 0 0 10px 0;
    font-weight: 600;
    color: white;
    line-height: 1.3;
  }

  .modal-header {
    padding: 20px 16px 18px;
  }

  .info-grid-mobile {
    display: flex;
    flex-direction: column;
    gap: 16px;
  }

  .info-item {
    padding: 16px;
  }

  .files-grid {
    grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
  }

  .modal-actions {
    padding: 12px 16px;
    flex-direction: column;

    .action-btn {
      width: 100%;
    }
  }
}
</style>