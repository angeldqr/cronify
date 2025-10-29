<template>
  <q-page class="q-pa-md page-background">
    <!-- Barra de acciones -->
    <div class="row justify-between items-center q-mb-md">
      <div class="row q-gutter-sm">
        <q-input
          v-model="searchText"
          outlined
          dense
          placeholder="Buscar eventos..."
          class="search-input"
          style="width: 300px"
          @update:model-value="debouncedSearch"
        >
          <template v-slot:prepend>
            <q-icon name="search" />
          </template>
          <template v-slot:append v-if="searchText">
            <q-icon name="close" class="cursor-pointer" @click="clearSearch" />
          </template>
        </q-input>
        <q-btn
          outline
          icon="filter_list"
          label="Filtros"
          color="primary"
          @click="showFilters = !showFilters"
        />
      </div>

      <q-btn
        unelevated
        icon="add"
        label="Crear Evento"
        color="primary"
        class="create-btn"
        @click="openCreateModal"
      />
    </div>

    <!-- Panel de filtros -->
    <q-slide-transition>
      <div v-show="showFilters" class="filters-panel q-mb-md">
        <q-card flat class="q-pa-md">
          <div class="row q-col-gutter-md">
            <div class="col-12 col-md-4">
              <label class="text-caption text-grey-7">Estado de notificación</label>
              <q-select
                v-model="filters.notificado"
                :options="notificacionOptions"
                outlined
                dense
                emit-value
                map-options
                clearable
              />
            </div>
            <div class="col-12 col-md-4">
              <label class="text-caption text-grey-7">Visibilidad</label>
              <q-select
                v-model="filters.esPublico"
                :options="visibilidadOptions"
                outlined
                dense
                emit-value
                map-options
                clearable
              />
            </div>
            <div class="col-12 col-md-4 flex items-end">
              <q-btn
                flat
                label="Limpiar filtros"
                color="grey-7"
                icon="clear"
                @click="clearFilters"
                size="sm"
              />
              <q-btn
                unelevated
                label="Aplicar"
                color="primary"
                icon="check"
                @click="applyFilters"
                size="sm"
                class="q-ml-sm"
              />
            </div>
          </div>
        </q-card>
      </div>
    </q-slide-transition>

    <!-- Calendario -->
    <q-card flat class="calendar-card">
      <!-- Header del calendario -->
      <q-card-section class="calendar-header">
        <div class="row justify-between items-center">
          <h2 class="text-h6 text-weight-medium text-capitalize q-ma-none text-white">
            {{ currentMonthYear }}
          </h2>
          <div class="row q-gutter-sm">
            <q-btn
              flat
              dense
              label="Hoy"
              color="white"
              size="sm"
              @click="goToToday"
            />
            <q-btn
              flat
              round
              dense
              icon="chevron_left"
              color="white"
              @click="previousMonth"
            />
            <q-btn
              flat
              round
              dense
              icon="chevron_right"
              color="white"
              @click="nextMonth"
            />
          </div>
        </div>
      </q-card-section>

      <!-- Días de la semana -->
      <q-separator />
      <div class="weekdays-header row">
        <div
          v-for="day in weekDays"
          :key="day"
          class="col text-center text-weight-medium q-pa-sm text-grey-7"
        >
          {{ day }}
        </div>
      </div>

      <!-- Grilla de días -->
      <div class="calendar-grid">
        <div
          v-for="(day, index) in calendarDays"
          :key="index"
          :class="[
            'calendar-day',
            { 'is-today': day.isToday },
            { 'other-month': !day.isCurrentMonth }
          ]"
        >
          <div class="day-number">
            {{ day.date }}
            <span v-if="day.isToday" class="today-badge">Hoy</span>
          </div>

          <!-- Eventos del día -->
          <div class="day-events" v-if="day.events && day.events.length > 0">
            <div
              v-for="event in day.events.slice(0, 3)"
              :key="event.id"
              :class="['event-chip', event.es_publico ? 'event-public' : 'event-private']"
              @click="viewEvent(event)"
            >
              <q-icon
                v-if="event.notificacion_enviada"
                name="check_circle"
                size="12px"
              />
              <span class="event-title">{{ event.asunto }}</span>
            </div>
            <div v-if="day.events.length > 3" class="more-events">
              +{{ day.events.length - 3 }} más
            </div>
          </div>
        </div>
      </div>
    </q-card>

    <!-- Modal crear evento -->
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
        @edit="handleEdit"
        @updated="handleEventUpdated"
        @deleted="handleEventDeleted"
      />
    </q-dialog>
  </q-page>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useEventosStore } from '../stores/eventos';
import CreateEventModal from '../components/eventos/CreateEventModal.vue';
import EventDetailModal from '../components/eventos/EventDetailModal.vue';
import { format, startOfMonth, endOfMonth, startOfWeek, endOfWeek, eachDayOfInterval, isSameMonth, isToday, isSameDay, addMonths, subMonths } from 'date-fns';
import { es } from 'date-fns/locale';

const eventosStore = useEventosStore();

// Estado del componente
const currentDate = ref(new Date());
const showCreateModal = ref(false);
const showDetailModal = ref(false);
const selectedEvent = ref(null);
const eventoToEdit = ref(null);
const showFilters = ref(false);
const searchText = ref('');
const searchTimeout = ref(null);
const filters = ref({
  notificado: null,
  esPublico: null
});

const notificacionOptions = [
  { label: 'Notificados', value: true },
  { label: 'Sin notificar', value: false }
];

const visibilidadOptions = [
  { label: 'Públicos', value: true },
  { label: 'Privados', value: false }
];

// Días de la semana
const weekDays = ['Dom', 'Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb'];

// Título del mes y año actual
const currentMonthYear = computed(() => {
  return format(currentDate.value, 'MMMM yyyy', { locale: es });
});

// Genera los días para mostrar en el calendario
const calendarDays = computed(() => {
  const start = startOfWeek(startOfMonth(currentDate.value));
  const end = endOfWeek(endOfMonth(currentDate.value));
  const days = eachDayOfInterval({ start, end });

  return days.map(day => {
    const dayEvents = eventosStore.eventos.filter(evento => {
      const eventoDate = new Date(evento.fecha_vencimiento);
      return isSameDay(eventoDate, day);
    });

    return {
      date: format(day, 'd'),
      fullDate: day,
      isCurrentMonth: isSameMonth(day, currentDate.value),
      isToday: isToday(day),
      events: dayEvents
    };
  });
});

// Navegación del calendario
const previousMonth = () => {
  currentDate.value = subMonths(currentDate.value, 1);
};

const nextMonth = () => {
  currentDate.value = addMonths(currentDate.value, 1);
};

const goToToday = () => {
  currentDate.value = new Date();
};

// Manejo de eventos
const viewEvent = (event) => {
  selectedEvent.value = event;
  showDetailModal.value = true;
};

const handleEventCreated = () => {
  showCreateModal.value = false;
  eventoToEdit.value = null;
  eventosStore.fetchEventos();
};

const handleEdit = (evento) => {
  showDetailModal.value = false;
  eventoToEdit.value = evento;
  showCreateModal.value = true;
};

const handleEventUpdated = () => {
  showDetailModal.value = false;
  showCreateModal.value = false;
  eventoToEdit.value = null;
  eventosStore.fetchEventos();
};

const handleEventDeleted = () => {
  showDetailModal.value = false;
  eventosStore.fetchEventos();
};

const openCreateModal = () => {
  eventoToEdit.value = null;
  showCreateModal.value = true;
};

// Búsqueda instantánea con debounce (500ms)
const debouncedSearch = (value) => {
  if (searchTimeout.value) {
    clearTimeout(searchTimeout.value);
  }
  
  searchTimeout.value = setTimeout(() => {
    eventosStore.applyFilters({ search: value });
  }, 500);
};

const clearSearch = () => {
  searchText.value = '';
  if (searchTimeout.value) {
    clearTimeout(searchTimeout.value);
  }
  eventosStore.applyFilters({ search: '' });
};

const applyFilters = () => {
  const filterParams = { search: searchText.value };
  if (filters.value.notificado !== null) {
    filterParams.notificacion_enviada = filters.value.notificado;
  }
  if (filters.value.esPublico !== null) {
    filterParams.es_publico = filters.value.esPublico;
  }
  eventosStore.applyFilters(filterParams);
};

const clearFilters = () => {
  filters.value = {
    notificado: null,
    esPublico: null
  };
  searchText.value = '';
  eventosStore.clearFilters();
  eventosStore.fetchEventos();
};

// Cargar eventos al montar el componente
onMounted(() => {
  eventosStore.fetchEventos();
});
</script>

<style scoped lang="scss">
.page-background {
  background: linear-gradient(135deg, #f5f7fa 0%, #e8ecf1 100%);
  min-height: calc(100vh - 50px);
}

.create-btn {
  background: linear-gradient(135deg, #1976d2 0%, #1565c0 100%);
  box-shadow: 0 2px 8px rgba(21, 101, 192, 0.3);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);

  &:hover {
    transform: translateY(-3px);
    box-shadow: 0 6px 20px rgba(21, 101, 192, 0.5);
  }

  &:active {
    transform: translateY(-1px);
    box-shadow: 0 3px 12px rgba(21, 101, 192, 0.4);
  }
}

.calendar-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

.calendar-header {
  background: linear-gradient(135deg, #1976d2 0%, #1565c0 100%);
  padding: 24px;
}

.weekdays-header {
  background: linear-gradient(to bottom, #f8f9fa, #e9ecef);
  border-bottom: 1px solid #dee2e6;
}

.calendar-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 1px;
  background-color: #e0e0e0;
  border: 1px solid #e0e0e0;
}

.calendar-day {
  min-height: 120px;
  padding: 12px;
  background: white;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  cursor: pointer;
  position: relative;

  &:hover {
    background: #f8fbff;
    box-shadow: inset 0 0 0 2px #1976d2, 0 2px 8px rgba(25, 118, 210, 0.15);
    transform: scale(1.02);
    z-index: 1;
  }

  &:active {
    transform: scale(0.98);
  }

  &.is-today {
    background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
    box-shadow: inset 0 0 0 2px #1976d2;
    
    &:hover {
      background: linear-gradient(135deg, #bbdefb 0%, #90caf9 100%);
      box-shadow: inset 0 0 0 2px #1565c0, 0 4px 12px rgba(25, 118, 210, 0.25);
    }
  }

  &.other-month {
    background: #fafafa;
    opacity: 0.5;
    
    .day-number {
      color: #bdbdbd;
    }

    &:hover {
      opacity: 0.7;
      transform: scale(1);
    }
  }
}

.day-number {
  font-size: 15px;
  font-weight: 700;
  color: #424242;
  margin-bottom: 8px;
  display: flex;
  align-items: center;
  gap: 6px;
  letter-spacing: -0.2px;
}

.today-badge {
  font-size: 10px;
  background: linear-gradient(135deg, #1976d2 0%, #1565c0 100%);
  color: white;
  padding: 2px 8px;
  border-radius: 10px;
  font-weight: 600;
  text-transform: uppercase;
}

.day-events {
  display: flex;
  flex-direction: column;
  gap: 4px;
  margin-top: 4px;
}

.event-chip {
  font-size: 12px;
  padding: 6px 8px;
  border-radius: 6px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 4px;
  transition: all 0.2s ease;
  font-weight: 500;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;

  &:hover {
    transform: translateX(2px);
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.15);
  }

  &.event-public {
    background: linear-gradient(135deg, #4caf50 0%, #388e3c 100%);
    color: white;
  }

  &.event-private {
    background: linear-gradient(135deg, #ff9800 0%, #f57c00 100%);
    color: white;
  }
}

.event-title {
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.more-events {
  font-size: 11px;
  color: #1976d2;
  font-weight: 600;
  padding: 4px 8px;
  background: #e3f2fd;
  border-radius: 4px;
  text-align: center;
  margin-top: 2px;
}

.search-input {
  background: white;
  border-radius: 8px;
}

.filters-panel {
  .q-card {
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  }
}
</style>


