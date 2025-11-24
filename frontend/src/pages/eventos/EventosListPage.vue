<template>
  <q-page class="q-pa-sm q-pa-md-md page-background">
    <div class="page-header q-mb-md q-mb-md-lg">
      <div class="row justify-between items-center q-col-gutter-sm">
        <div class="col-12 col-sm-auto">
          <h4 class="page-title">
            Mis Eventos
            <q-badge v-if="viewMode === 'admin'" color="red" label="Vista Admin" class="q-ml-sm" />
          </h4>
          <p class="page-subtitle">
            {{ viewMode === 'admin' ? 'Visualizando TODOS los eventos del sistema' : 'Lista completa de todos tus eventos' }}
          </p>
        </div>
        <div class="col-12 col-sm-auto">
          <q-btn
            unelevated
            icon="add"
            :label="$q.screen.gt.xs ? 'Crear Evento' : 'Crear'"
            color="primary"
            class="create-event-btn full-width"
            @click="showCreateModal = true"
          />
        </div>
      </div>
    </div>

    <!-- Barra de búsqueda y filtros -->
    <div class="search-filters-bar q-mb-lg">
      <q-card flat class="search-card">
        <q-card-section class="q-pa-md">
          <div class="row q-col-gutter-md">
            <!-- Búsqueda -->
            <div class="col-12 col-md-6">
              <q-input
                v-model="searchQuery"
                outlined
                dense
                placeholder="Buscar eventos por asunto o descripción..."
                clearable
                @update:model-value="onSearchChange"
              >
                <template v-slot:prepend>
                  <q-icon name="search" color="primary" />
                </template>
              </q-input>
            </div>

            <!-- Filtro: Público/Privado -->
            <div class="col-6 col-md-2">
              <q-select
                v-model="filterPublico"
                outlined
                dense
                :options="opcionesPublico"
                label="Visibilidad"
                emit-value
                map-options
                clearable
                @update:model-value="onFilterChange"
              >
                <template v-slot:prepend>
                  <q-icon name="visibility" size="xs" />
                </template>
              </q-select>
            </div>

            <!-- Filtro: Notificados -->
            <div class="col-6 col-md-2">
              <q-select
                v-model="filterNotificado"
                outlined
                dense
                :options="opcionesNotificado"
                label="Notificación"
                emit-value
                map-options
                clearable
                @update:model-value="onFilterChange"
              >
                <template v-slot:prepend>
                  <q-icon name="notifications" size="xs" />
                </template>
              </q-select>
            </div>

            <!-- Bot�n limpiar filtros -->
            <div class="col-12 col-md-2">
              <q-btn
                unelevated
                outline
                color="grey-7"
                label="Limpiar Filtros"
                icon="clear"
                class="full-width"
                @click="clearFilters"
                :disable="!hasActiveFilters"
              />
            </div>
          </div>

          <!-- Indicador de resultados -->
          <div v-if="!loading && eventos.length > 0" class="q-mt-sm text-caption text-grey-7">
            <q-icon name="info" size="xs" class="q-mr-xs" />
            Mostrando {{ (currentPage - 1) * 20 + 1 }} - {{ Math.min(currentPage * 20, eventosStore.pagination.count) }} de {{ eventosStore.pagination.count }} eventos
            <span v-if="hasActiveFilters" class="text-primary"> (filtrados)</span>
          </div>
        </q-card-section>
      </q-card>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="text-center q-pa-xl">
      <q-spinner color="primary" size="50px" />
      <p class="text-grey-7 q-mt-md">Cargando eventos...</p>
    </div>

    <!-- Lista de eventos -->
    <div v-else-if="eventos.length > 0" class="events-grid">
      <q-card
        v-for="evento in eventos"
        :key="evento.id"
        flat
        class="event-card"
        @click="handleEventClick(evento)"
      >
        <q-card-section class="card-header">
          <div class="row items-center justify-between">
            <div class="event-title">{{ evento.asunto }}</div>
            <q-badge :color="evento.es_publico ? 'green' : 'orange'" rounded>
              {{ evento.es_publico ? 'Público' : 'Privado' }}
            </q-badge>
          </div>
        </q-card-section>

        <q-card-section>
          <div class="event-info">
            <div class="info-row">
              <q-icon name="schedule" color="primary" size="20px" />
              <span>{{ formatDate(evento.fecha_vencimiento) }}</span>
            </div>
            <div class="info-row" v-if="evento.descripcion">
              <q-icon name="description" color="grey-7" size="20px" />
              <span class="text-grey-7">{{ truncate(evento.descripcion, 100) }}</span>
            </div>
            <div class="info-row">
              <q-icon name="notifications" color="orange-7" size="20px" />
              <span>{{ evento.notificacion_valor }} {{ evento.notificacion_unidad }} antes</span>
            </div>
            <div class="info-row" v-if="evento.creador_nombre">
              <q-icon name="person" color="blue-7" size="20px" />
              <span>{{ evento.creador_nombre }}</span>
            </div>
          </div>
        </q-card-section>

        <q-card-actions v-if="isEventOwner(evento)" class="card-actions">
          <q-btn flat dense icon="edit" color="primary" @click.stop="handleEdit(evento)" />
          <q-btn flat dense icon="delete" color="negative" @click.stop="handleDelete(evento)" />
        </q-card-actions>
      </q-card>
    </div>

    <!-- Sin eventos -->
    <div v-else class="no-events">
      <q-card flat class="events-list-card">
        <q-card-section>
          <div class="text-center q-pa-xl">
            <q-icon name="event_note" size="64px" color="grey-5" />
            <p class="text-h6 text-grey-7 q-mt-md">No hay eventos</p>
            <p class="text-grey-6">Crea tu primer evento para comenzar</p>
            <q-btn
              unelevated
              icon="add"
              label="Crear Evento"
              color="primary"
              class="q-mt-md"
              @click="showCreateModal = true"
            />
          </div>
        </q-card-section>
      </q-card>
    </div>

    <!-- Paginaci�n -->
    <div v-if="eventos.length > 0 && eventosStore.pagination.count > 20" class="q-mt-lg">
      <div class="pagination-container">
        <q-pagination
          v-model="currentPage"
          :max="totalPages"
          :max-pages="7"
          direction-links
          boundary-links
          color="primary"
          @update:model-value="onPageChange"
        />
        <div class="pagination-info text-caption text-grey-7 q-mt-sm text-center">
          Mostrando {{ (currentPage - 1) * 20 + 1 }} - {{ Math.min(currentPage * 20, eventosStore.pagination.count) }} de {{ eventosStore.pagination.count}} eventos
        </div>
      </div>
    </div>

    <!-- Modal crear/editar evento -->
    <q-dialog v-model="showCreateModal" transition-show="scale" transition-hide="scale">
      <CreateEventModal
        :evento="eventoToEdit"
        @close="showCreateModal = false"
        @created="handleEventCreated"
        @updated="handleEventUpdated"
      />
    </q-dialog>

    <!-- Modal detalle evento -->
    <q-dialog v-model="showDetailModal" transition-show="scale" transition-hide="scale">
      <EventDetailModal
        v-if="selectedEvent"
        :event="selectedEvent"
        @close="showDetailModal = false"
        @edit="handleEditFromDetail"
        @updated="handleEventUpdated"
        @deleted="handleEventDeleted"
      />
    </q-dialog>
  </q-page>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useQuasar } from 'quasar';
import { useEventosStore } from '../../stores/eventos';
import { useAuthStore } from '../../stores/auth';
import adminService from '../../services/adminService';
import CreateEventModal from '../../components/eventos/CreateEventModal.vue';
import EventDetailModal from '../../components/eventos/EventDetailModal.vue';

const $q = useQuasar();
const eventosStore = useEventosStore();
const authStore = useAuthStore();

const loading = ref(false);
const showCreateModal = ref(false);
const showDetailModal = ref(false);
const selectedEvent = ref(null);
const eventoToEdit = ref(null);
const currentPage = ref(1);

const searchQuery = ref('');
const filterPublico = ref(null);
const filterNotificado = ref(null);
const viewMode = ref('normal'); // 'normal' o 'admin' - para vista de administrador
let searchTimeout = null;

// Opciones de filtro - se agregan condicionalmente basado en si es admin
const opcionesPublico = computed(() => {
  const opciones = [
    { label: 'Público', value: true },
    { label: 'Privado', value: false }
  ];
  
  // Si es admin, agregar opción de ver todos
  if (authStore.isAdmin) {
    opciones.push({ label: 'Todos (Admin)', value: 'admin' });
  }
  
  return opciones;
});

const opcionesNotificado = [
  { label: 'Notificados', value: true },
  { label: 'Pendientes', value: false }
];

const eventos = computed(() => eventosStore.eventos || []);
const currentUserId = computed(() => authStore.user?.id);
const totalPages = computed(() => Math.ceil(eventosStore.pagination.count / 20));

const hasActiveFilters = computed(() => {
  return searchQuery.value || filterPublico.value !== null || filterNotificado.value !== null;
});

const formatDate = (dateString) => {
  const date = new Date(dateString);
  const fechaFormato = date.toLocaleDateString('es-ES', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });
  const horaFormato = date.toLocaleTimeString('es-ES', {
    hour: 'numeric',
    minute: '2-digit',
    hour12: true
  });
  return `${fechaFormato}, ${horaFormato}`;
};

const truncate = (text, maxLength) => {
  if (!text) return '';
  // Eliminar etiquetas HTML y obtener solo el texto plano
  const tempDiv = document.createElement('div');
  tempDiv.innerHTML = text;
  const plainText = tempDiv.textContent || tempDiv.innerText || '';
  return plainText.length > maxLength ? plainText.substring(0, maxLength) + '...' : plainText;
};

const isEventOwner = (evento) => {
  return currentUserId.value && evento.creador === currentUserId.value;
};

const onSearchChange = () => {
  if (searchTimeout) {
    clearTimeout(searchTimeout);
  }
  searchTimeout = setTimeout(() => {
    currentPage.value = 1;
    applyFiltersAndLoad();
  }, 500);
};

const onFilterChange = () => {
  currentPage.value = 1;
  
  // Si se seleccionó "Todos (Admin)", cargar directamente con el servicio de admin
  if (filterPublico.value === 'admin') {
    loadEventos();
    return;
  }
  
  // Si no hay filtros activos, recargar sin filtros
  if (!hasActiveFilters.value) {
    eventosStore.clearFilters();
    loadEventos();
  } else {
    applyFiltersAndLoad();
  }
};

const clearFilters = () => {
  searchQuery.value = '';
  filterPublico.value = null;
  filterNotificado.value = null;
  currentPage.value = 1;
  eventosStore.clearFilters();
  loadEventos();
};

const applyFiltersAndLoad = async () => {
  const filters = {};
  if (searchQuery.value) {
    filters.search = searchQuery.value;
  }
  // Solo enviar filtro público si no es 'admin'
  if (filterPublico.value !== null && filterPublico.value !== undefined && filterPublico.value !== 'admin') {
    filters.es_publico = filterPublico.value;
  }
  if (filterNotificado.value !== null && filterNotificado.value !== undefined) {
    filters.notificacion_enviada = filterNotificado.value;
  }
  loading.value = true;
  try {
    await eventosStore.applyFilters(filters);
  } finally {
    loading.value = false;
  }
};

const handleEventClick = (evento) => {
  selectedEvent.value = evento;
  showDetailModal.value = true;
};

const handleEdit = (evento) => {
  eventoToEdit.value = evento;
  showCreateModal.value = true;
};

const handleEditFromDetail = (evento) => {
  showDetailModal.value = false;
  eventoToEdit.value = evento;
  showCreateModal.value = true;
};

const handleDelete = (evento) => {
  $q.dialog({
    title: 'Confirmar eliminación',
    message: `¿Estás seguro que deseas eliminar "${evento.asunto}"?`,
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
      await eventosStore.deleteEvento(evento.id);
      $q.notify({
        type: 'positive',
        message: 'Evento eliminado exitosamente',
        position: 'top',
        icon: 'check_circle',
        timeout: 2000
      });
      loadEventos();
    } catch {
      $q.notify({
        type: 'negative',
        message: 'Error al eliminar el evento',
        position: 'top',
        icon: 'error',
        timeout: 3000
      });
    }
  });
};

const handleEventCreated = () => {
  showCreateModal.value = false;
  eventoToEdit.value = null;
  currentPage.value = 1;
  loadEventos();
};

const handleEventUpdated = () => {
  showDetailModal.value = false;
  showCreateModal.value = false;
  eventoToEdit.value = null;
  loadEventos();
};

const handleEventDeleted = () => {
  showDetailModal.value = false;
  loadEventos();
};

const onPageChange = (page) => {
  currentPage.value = page;
  loadEventos();
  window.scrollTo({ top: 0, behavior: 'smooth' });
};

const loadEventos = async () => {
  loading.value = true;
  try {
    // Si se seleccionó "Todos (Admin)", usar el servicio de admin
    if (filterPublico.value === 'admin' && authStore.isAdmin) {
      viewMode.value = 'admin';
      const filters = {};
      if (searchQuery.value) filters.search = searchQuery.value;
      
      // Pasar la página actual al servicio de admin
      const response = await adminService.getAllEvents(filters, currentPage.value);
      
      // Actualizar el store manualmente con los datos de admin
      eventosStore.eventos = response.results || response.eventos || response;
      eventosStore.pagination.count = response.count || response.length;
      eventosStore.pagination.next = response.next || null;
      eventosStore.pagination.previous = response.previous || null;
    } else {
      viewMode.value = 'normal';
      await eventosStore.fetchEventos(currentPage.value);
    }
  } catch (error) {
    console.error('Error al cargar eventos:', error);
    $q.notify({
      type: 'negative',
      message: 'Error al cargar eventos',
      caption: error.message
    });
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  loadEventos();
  // Si hay un id de evento para abrir, abrir el modal automáticamente
  const openId = localStorage.getItem('open_evento_id');
  if (openId) {
    // Esperar a que los eventos se carguen
    setTimeout(() => {
      const evento = eventos.value.find(e => e.id == openId);
      if (evento) {
        handleEventClick(evento);
      }
      localStorage.removeItem('open_evento_id');
    }, 600);
  }
});
</script>

<style scoped lang="scss">
.page-background {
  background: #f5f5f5;
  min-height: calc(100vh - 100px);
}

.page-header {
  .page-title {
    margin: 0;
    font-size: 32px;
    font-weight: 700;
    color: #1976d2;
    letter-spacing: -0.5px;
    line-height: 1.2;
  }

  .page-subtitle {
    margin: 8px 0 0 0;
    color: #546e7a;
    font-size: 15px;
    font-weight: 500;
    opacity: 0.9;
  }
}

.search-filters-bar {
  .search-card {
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
    background: white;
    border-left: 4px solid #1976d2;
    transition: all 0.3s ease;

    &:hover {
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
    }
  }
}

.events-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 24px;
}

.event-card {
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  cursor: pointer;
  border-left: 4px solid #1976d2;
  position: relative;
  overflow: hidden;

  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(135deg, rgba(25, 118, 210, 0.03) 0%, rgba(21, 101, 192, 0.03) 100%);
    opacity: 0;
    transition: opacity 0.3s ease;
  }

  &:hover {
    box-shadow: 0 8px 24px rgba(25, 118, 210, 0.25);
    transform: translateY(-4px) scale(1.01);
    border-left-width: 6px;

    &::before {
      opacity: 1;
    }
  }

  &:active {
    transform: translateY(-2px) scale(1.005);
  }
}

.card-header {
  background: linear-gradient(135deg, rgba(25, 118, 210, 0.05) 0%, rgba(21, 101, 192, 0.05) 100%);
  padding: 20px;
}

.event-title {
  font-size: 19px;
  font-weight: 700;
  color: #1976d2;
  margin-right: 12px;
  letter-spacing: -0.3px;
  line-height: 1.4;
}

.event-info {
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding: 20px;
}

.info-row {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 14px;
  color: #546e7a;
  line-height: 1.6;
}

.card-actions {
  border-top: 1px solid #e0e0e0;
  padding: 8px 16px;
  justify-content: flex-end;
  background: rgba(0, 0, 0, 0.01);

  .q-btn {
    transition: all 0.2s ease;

    &:hover {
      transform: scale(1.1);
    }

    &:active {
      transform: scale(0.95);
    }
  }
}

.no-events {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 400px;
}

.events-list-card {
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  max-width: 500px;
  width: 100%;
}

.create-event-btn {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 16px rgba(25, 118, 210, 0.35);
  }
  
  &:active {
    transform: translateY(0);
  }
}

.pagination-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px 0;
}

.pagination-info {
  margin-top: 8px;
}
</style>
