<template>
  <q-page class="q-pa-md page-background">
    <div v-if="loading" class="flex flex-center" style="min-height: 400px;">
      <q-spinner color="primary" size="50px" />
    </div>

    <div v-else-if="evento">
      <!-- Header con botón volver -->
      <div class="page-header q-mb-lg">
        <q-btn
          flat
          icon="arrow_back"
          label="Volver"
          color="primary"
          @click="$router.back()"
          class="q-mb-md"
        />
        <h4 class="page-title">{{ evento.asunto }}</h4>
        <div class="badges-row q-mt-sm">
          <q-badge
            :color="evento.es_publico ? 'green' : 'orange'"
            :label="evento.es_publico ? 'Público' : 'Privado'"
            class="q-mr-sm"
          />
          <q-badge
            v-if="evento.notificacion_enviada"
            color="blue"
            label="Notificado"
          />
        </div>
      </div>

      <!-- Contenido del evento -->
      <div class="row q-col-gutter-md">
        <!-- Información principal -->
        <div class="col-12 col-md-8">
          <q-card flat class="detail-card q-mb-md">
            <q-card-section>
              <div class="text-overline text-grey-7">Información del Evento</div>
              <q-separator class="q-my-md" />

              <div class="info-row">
                <div class="info-icon">
                  <q-icon name="schedule" color="primary" size="24px" />
                </div>
                <div class="info-content">
                  <div class="info-label">Fecha y Hora de Vencimiento</div>
                  <div class="info-value">{{ formatDateTime(evento.fecha_vencimiento) }}</div>
                </div>
              </div>

              <div class="info-row">
                <div class="info-icon">
                  <q-icon name="person" color="primary" size="24px" />
                </div>
                <div class="info-content">
                  <div class="info-label">Creado por</div>
                  <div class="info-value">{{ evento.creador_nombre || evento.creador_username || 'Usuario' }}</div>
                </div>
              </div>

              <div class="info-row">
                <div class="info-icon">
                  <q-icon name="notifications" color="orange" size="24px" />
                </div>
                <div class="info-content">
                  <div class="info-label">Notificación</div>
                  <div class="info-value">
                    {{ evento.notificacion_valor }} {{ evento.notificacion_unidad }} antes del vencimiento
                  </div>
                </div>
              </div>

              <div v-if="evento.descripcion" class="info-row">
                <div class="info-icon">
                  <q-icon name="description" color="grey-7" size="24px" />
                </div>
                <div class="info-content">
                  <div class="info-label">Descripción</div>
                  <div class="info-value description-text">{{ evento.descripcion }}</div>
                </div>
              </div>
            </q-card-section>
          </q-card>

          <!-- Archivos adjuntos -->
          <q-card v-if="evento.archivos_adjuntos && evento.archivos_adjuntos.length > 0" flat class="detail-card">
            <q-card-section>
              <div class="text-overline text-grey-7">
                Archivos Adjuntos ({{ evento.archivos_adjuntos.length }})
              </div>
              <q-separator class="q-my-md" />

              <div class="files-grid">
                <div
                  v-for="file in evento.archivos_adjuntos"
                  :key="file.id"
                  class="file-card"
                  @click="downloadFile(file)"
                >
                  <q-icon
                    :name="getFileIcon(file.nombre_original)"
                    :color="getFileColor(file.nombre_original)"
                    size="40px"
                  />
                  <div class="file-name">{{ file.nombre_original }}</div>
                  <div class="file-action">
                    <q-icon name="download" size="20px" />
                  </div>
                </div>
              </div>
            </q-card-section>
          </q-card>
        </div>

        <!-- Sidebar con acciones -->
        <div class="col-12 col-md-4">
          <q-card v-if="isEventOwner" flat class="detail-card q-mb-md">
            <q-card-section>
              <div class="text-overline text-grey-7">Acciones</div>
              <q-separator class="q-my-md" />

              <q-btn
                unelevated
                color="primary"
                icon="edit"
                label="Editar Evento"
                class="full-width q-mb-sm"
                @click="editEvento"
              />
              <q-btn
                outline
                color="negative"
                icon="delete"
                label="Eliminar Evento"
                class="full-width"
                @click="deleteEvento"
              />
            </q-card-section>
          </q-card>

          <q-card flat class="detail-card">
            <q-card-section>
              <div class="text-overline text-grey-7">Metadatos</div>
              <q-separator class="q-my-md" />

              <div class="meta-item">
                <span class="meta-label">ID del Evento:</span>
                <span class="meta-value">{{ evento.id }}</span>
              </div>
              <div class="meta-item">
                <span class="meta-label">Creado el:</span>
                <span class="meta-value">{{ formatDate(evento.created_at) }}</span>
              </div>
              <div class="meta-item">
                <span class="meta-label">Última actualización:</span>
                <span class="meta-value">{{ formatDate(evento.updated_at) }}</span>
              </div>
            </q-card-section>
          </q-card>
        </div>
      </div>
    </div>

    <div v-else class="flex flex-center" style="min-height: 400px;">
      <div class="text-center">
        <q-icon name="error_outline" size="64px" color="grey-5" />
        <p class="text-h6 text-grey-7 q-mt-md">Evento no encontrado</p>
        <q-btn flat label="Volver" color="primary" @click="$router.back()" />
      </div>
    </div>

    <!-- Modal editar -->
    <q-dialog v-model="showEditModal">
      <CreateEventModal
        :evento="evento"
        @close="showEditModal = false"
        @updated="handleEventUpdated"
      />
    </q-dialog>
  </q-page>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useQuasar } from 'quasar';
import { useEventosStore } from '../../stores/eventos';
import { useAuthStore } from '../../stores/auth';
import CreateEventModal from '../../components/eventos/CreateEventModal.vue';

const route = useRoute();
const router = useRouter();
const $q = useQuasar();
const eventosStore = useEventosStore();
const authStore = useAuthStore();

const evento = ref(null);
const loading = ref(true);
const showEditModal = ref(false);

const isEventOwner = computed(() => {
  return authStore.user?.id === evento.value?.creador;
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

const formatDate = (dateString) => {
  if (!dateString) return 'N/A';
  const date = new Date(dateString);
  return date.toLocaleDateString('es-ES', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });
};

const getFileIcon = (filename) => {
  const ext = filename.split('.').pop().toLowerCase();
  const iconMap = {
    pdf: 'picture_as_pdf',
    doc: 'description',
    docx: 'description',
    xls: 'table_chart',
    xlsx: 'table_chart',
    jpg: 'image',
    jpeg: 'image',
    png: 'image',
    zip: 'folder_zip',
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
    jpg: 'purple-6',
    jpeg: 'purple-6',
    png: 'purple-6',
    zip: 'amber-7',
  };
  return colorMap[ext] || 'grey-6';
};

const downloadFile = (file) => {
  if (file.url_descarga) {
    window.open(file.url_descarga, '_blank');
  }
};

const editEvento = () => {
  showEditModal.value = true;
};

const deleteEvento = () => {
  $q.dialog({
    title: 'Confirmar eliminación',
    message: '¿Estás seguro que deseas eliminar este evento?',
    cancel: true,
    persistent: true,
    ok: {
      label: 'Eliminar',
      color: 'negative'
    }
  }).onOk(async () => {
    try {
      await eventosStore.deleteEvento(evento.value.id);
      $q.notify({
        type: 'positive',
        message: 'Evento eliminado exitosamente',
        position: 'top'
      });
      router.push('/eventos');
    } catch {
      $q.notify({
        type: 'negative',
        message: 'Error al eliminar el evento',
        position: 'top'
      });
    }
  });
};

const handleEventUpdated = async () => {
  showEditModal.value = false;
  await loadEvento();
  $q.notify({
    type: 'positive',
    message: 'Evento actualizado exitosamente',
    position: 'top'
  });
};

const loadEvento = async () => {
  loading.value = true;
  try {
    const id = route.params.id;
    evento.value = await eventosStore.fetchEvento(id);
  } catch (error) {
    console.error('Error cargando evento:', error);
    evento.value = null;
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  loadEvento();
});
</script>

<style scoped lang="scss">
.page-background {
  background: #f5f5f5;
}

.page-header {
  .page-title {
    margin: 0;
    font-size: 28px;
    font-weight: 600;
    color: #1976d2;
  }
}

.badges-row {
  display: flex;
  gap: 8px;
}

.detail-card {
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.info-row {
  display: flex;
  gap: 16px;
  padding: 16px 0;
  border-bottom: 1px solid #e0e0e0;

  &:last-child {
    border-bottom: none;
  }
}

.info-icon {
  flex-shrink: 0;
}

.info-content {
  flex: 1;
}

.info-label {
  font-size: 12px;
  color: #78909c;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 4px;
}

.info-value {
  font-size: 15px;
  color: #37474f;
  font-weight: 500;
}

.description-text {
  line-height: 1.6;
}

.files-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 12px;
}

.file-card {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 16px;
  text-align: center;
  cursor: pointer;
  transition: all 0.2s;

  &:hover {
    border-color: #1976d2;
    background: rgba(25, 118, 210, 0.05);
    transform: translateY(-2px);
  }
}

.file-name {
  font-size: 12px;
  margin-top: 8px;
  word-break: break-word;
  color: #546e7a;
}

.file-action {
  margin-top: 8px;
  color: #1976d2;
}

.meta-item {
  display: flex;
  justify-content: space-between;
  padding: 8px 0;
  font-size: 13px;
}

.meta-label {
  color: #78909c;
}

.meta-value {
  color: #37474f;
  font-weight: 500;
}
</style>
