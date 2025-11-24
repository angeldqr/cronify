<template>
  <q-page :class="['q-pa-xs q-pa-sm-sm q-pa-md-md', 'page-background']">
    <!-- Barra de acciones -->
    <div class="row justify-between items-center q-mb-sm q-mb-md-md action-bar">
      <div class="row q-gutter-sm items-center">
        <q-input
          v-model="searchText"
          outlined
          dense
          :placeholder="$q.screen.gt.xs ? 'Buscar eventos...' : 'Buscar...'"
          class="search-input"
          :style="$q.screen.gt.sm ? 'width: 300px' : 'width: 150px'"
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
          :label="$q.screen.gt.xs ? 'Filtros' : ''"
          color="primary"
          @click="showFilters = !showFilters"
        />
      </div>

      <q-btn
        unelevated
        icon="add"
        :label="$q.screen.gt.xs ? 'Crear Evento' : 'Crear'"
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
      <q-card-section :class="['calendar-header', $q.screen.lt.sm ? 'q-pa-md' : 'q-pa-lg']">
        <div class="row justify-between items-center">
          <div class="header-date-section">
            <div :class="[$q.screen.gt.xs ? 'text-h5' : 'text-h6', 'text-weight-bold text-capitalize text-white month-title']">
              {{ format(currentDate, 'MMMM', { locale: es }) }}
            </div>
            <div :class="[$q.screen.gt.xs ? 'text-h6' : 'text-subtitle1', 'text-weight-light text-white year-title']">
              {{ format(currentDate, 'yyyy') }}
            </div>
          </div>
          <div class="row q-gutter-xs items-center">
            <q-btn
              flat
              dense
              :label="$q.screen.gt.xs ? 'Hoy' : ''"
              :icon="$q.screen.lt.sm ? 'today' : undefined"
              color="white"
              :size="$q.screen.gt.xs ? 'md' : 'sm'"
              class="today-btn"
              @click="goToToday"
            />
            <q-separator vertical color="white" class="q-mx-xs" style="opacity: 0.3" />
            <q-btn
              flat
              round
              dense
              icon="chevron_left"
              color="white"
              class="nav-btn"
              @click="previousMonth"
            />
            <q-btn
              flat
              round
              dense
              icon="chevron_right"
              color="white"
              class="nav-btn"
              @click="nextMonth"
            />
          </div>
        </div>
      </q-card-section>

      <!-- Días de la semana -->
      <div class="weekdays-header row">
        <div
          v-for="day in weekDays"
          :key="day"
          :class="['col text-center text-weight-bold q-py-md text-grey-8', $q.screen.lt.sm ? 'text-caption q-py-sm' : 'text-body2']"
        >
          {{ $q.screen.gt.xs ? day : day.charAt(0) }}
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
            { 'other-month': !day.isCurrentMonth },
            { 'has-events': day.events && day.events.length > 0 },
            { 'mobile': $q.screen.lt.sm }
          ]"
          @click="day.events && day.events.length > 0 && viewEvent(day.events[0])"
        >
          <div class="day-header">
            <div class="day-number">
              {{ day.date }}
            </div>
            <div v-if="day.isToday" class="today-indicator">
              <q-icon name="fiber_manual_record" size="8px" color="primary" />
            </div>
          </div>

          <!-- Eventos del día -->
          <div class="day-events" v-if="day.events && day.events.length > 0">
            <div
              v-for="event in day.events.slice(0, $q.screen.gt.md ? 4 : $q.screen.gt.sm ? 3 : 2)"
              :key="event.id"
              :class="[
                'event-chip',
                event.es_publico ? 'event-public' : 'event-private',
                { 'has-notification': event.notificacion_enviada }
              ]"
              @click.stop="viewEvent(event)"
            >
              <div class="event-content">
                <div class="event-indicator" :class="event.es_publico ? 'indicator-public' : 'indicator-private'"></div>
                <span class="event-title">{{ event.asunto }}</span>
                <q-icon
                  v-if="event.notificacion_enviada"
                  name="notifications_active"
                  size="14px"
                  class="event-notification-icon"
                />
              </div>
            </div>
            <div 
              v-if="day.events.length > ($q.screen.gt.md ? 4 : $q.screen.gt.sm ? 3 : 2)" 
              class="more-events"
              @click.stop="showDayEvents(day)"
            >
              <q-icon name="more_horiz" size="14px" />
              <span>{{ day.events.length - ($q.screen.gt.md ? 4 : $q.screen.gt.sm ? 3 : 2) }} más</span>
            </div>
          </div>

          <!-- Empty state para días sin eventos -->
          <div v-else class="empty-day">
            <q-icon 
              v-if="!day.isCurrentMonth || $q.screen.gt.sm" 
              name="event_available" 
              size="20px" 
              color="grey-4" 
              class="empty-icon"
            />
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

const showDayEvents = (day) => {
  // Por ahora muestra el primer evento, pero podría expandirse a mostrar todos
  if (day.events && day.events.length > 0) {
    viewEvent(day.events[0]);
  }
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
  background: #f0f2f5;
  min-height: calc(100vh - 50px);
}

.action-bar {
  flex-wrap: wrap;
  gap: 8px;
  
  @media (max-width: 599px) {
    gap: 6px;
  }
}

.create-btn {
  background: linear-gradient(135deg, #1976d2 0%, #1565c0 100%);
  box-shadow: 0 2px 8px rgba(25, 118, 210, 0.25);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  white-space: nowrap;
  font-weight: 600;
  letter-spacing: 0.3px;

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(25, 118, 210, 0.35);
  }

  &:active {
    transform: translateY(0px);
  }
}

.calendar-card {
  background: white;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
  border: 1px solid rgba(0, 0, 0, 0.05);
}

.calendar-header {
  background: linear-gradient(135deg, #1e88e5 0%, #1565c0 100%);
  position: relative;
  overflow: hidden;

  &::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -10%;
    width: 300px;
    height: 300px;
    background: radial-gradient(circle, rgba(255, 255, 255, 0.1) 0%, transparent 70%);
    border-radius: 50%;
  }

  .header-date-section {
    position: relative;
    z-index: 1;
  }

  .month-title {
    line-height: 1.2;
    letter-spacing: 0.5px;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }

  .year-title {
    opacity: 0.9;
    letter-spacing: 1px;
  }
}

.today-btn {
  font-weight: 600;
  letter-spacing: 0.5px;
  transition: all 0.2s ease;
  
  &:hover {
    background: rgba(255, 255, 255, 0.15);
  }
}

.nav-btn {
  transition: all 0.2s ease;
  
  &:hover {
    background: rgba(255, 255, 255, 0.15);
    transform: scale(1.1);
  }
}

.weekdays-header {
  background: linear-gradient(to bottom, #fafbfc, #f5f6f8);
  border-bottom: 2px solid #e4e7eb;
  position: sticky;
  top: 0;
  z-index: 2;
  padding: 6px 0;
}

.calendar-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 0;
  background-color: #e4e7eb;
  border: 1px solid #e4e7eb;
}

.calendar-day {
  min-height: 110px;
  padding: 8px;
  background: white;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  cursor: pointer;
  position: relative;
  border: 1px solid #e4e7eb;
  display: flex;
  flex-direction: column;

  &:hover:not(.other-month) {
    background: linear-gradient(135deg, #f8fbff 0%, #f0f7ff 100%);
    box-shadow: inset 0 0 0 2px #1976d2;
    transform: translateY(-2px);
    z-index: 1;
    border-color: #1976d2;
  }

  &.is-today {
    background: linear-gradient(135deg, #e3f2fd 0%, #d1e9ff 100%);
    border: 2px solid #1976d2;
    box-shadow: 0 4px 12px rgba(25, 118, 210, 0.15);
    
    .day-number {
      color: #1565c0;
      font-weight: 800;
      font-size: 18px;
    }

    &:hover {
      background: linear-gradient(135deg, #bbdefb 0%, #90caf9 100%);
      box-shadow: 0 6px 20px rgba(25, 118, 210, 0.25);
      transform: translateY(-3px);
    }
  }

  &.other-month {
    background: #fafafa;
    opacity: 0.4;
    
    .day-number {
      color: #bdbdbd;
    }

    &:hover {
      opacity: 0.5;
      transform: none;
      box-shadow: none;
      border-color: #e4e7eb;
    }
  }

  &.has-events:not(.other-month) {
    background: linear-gradient(to bottom, white 0%, #fafbfc 100%);
  }

  &.mobile {
    min-height: 90px;
    padding: 8px;

    &:hover {
      transform: none;
      box-shadow: none;
      background: white;
      
      &.is-today {
        background: linear-gradient(135deg, #e3f2fd 0%, #d1e9ff 100%);
        box-shadow: 0 4px 12px rgba(25, 118, 210, 0.15);
      }
    }
  }
}

.day-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 6px;
}

.day-number {
  font-size: 15px;
  font-weight: 700;
  color: #2c3e50;
  letter-spacing: -0.3px;
  transition: all 0.2s ease;
}

.today-indicator {
  display: flex;
  align-items: center;
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
    transform: scale(1);
  }
  50% {
    opacity: 0.7;
    transform: scale(1.2);
  }
}

.day-events {
  display: flex;
  flex-direction: column;
  gap: 4px;
  flex: 1;
}

.event-chip {
  font-size: 10.5px;
  padding: 6px 8px;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  font-weight: 600;
  position: relative;
  overflow: hidden;
  border: 1px solid transparent;
  backdrop-filter: blur(10px);

  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    opacity: 0;
    transition: opacity 0.3s ease;
    z-index: 0;
  }

  &:hover {
    transform: translateX(4px) translateY(-2px);
    box-shadow: 0 6px 16px rgba(0, 0, 0, 0.15);
    
    &::before {
      opacity: 1;
    }
  }

  &:active {
    transform: translateX(2px) translateY(-1px);
  }

  &.event-public {
    background: linear-gradient(135deg, #4caf50 0%, #2e7d32 100%);
    color: white;
    border-color: rgba(255, 255, 255, 0.2);

    &::before {
      background: linear-gradient(135deg, #66bb6a 0%, #4caf50 100%);
    }

    &:hover {
      box-shadow: 0 6px 16px rgba(76, 175, 80, 0.35);
    }
  }

  &.event-private {
    background: linear-gradient(135deg, #ff9800 0%, #e65100 100%);
    color: white;
    border-color: rgba(255, 255, 255, 0.2);

    &::before {
      background: linear-gradient(135deg, #ffa726 0%, #ff9800 100%);
    }

    &:hover {
      box-shadow: 0 6px 16px rgba(255, 152, 0, 0.35);
    }
  }
}

.event-content {
  display: flex;
  align-items: center;
  gap: 6px;
  width: 100%;
  position: relative;
  z-index: 1;
}

.event-indicator {
  width: 3px;
  height: 16px;
  border-radius: 2px;
  flex-shrink: 0;
  
  &.indicator-public {
    background: rgba(255, 255, 255, 0.9);
  }
  
  &.indicator-private {
    background: rgba(255, 255, 255, 0.9);
  }
}

.event-title {
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  line-height: 1.3;
}

.event-notification-icon {
  flex-shrink: 0;
  opacity: 0.9;
}

.more-events {
  font-size: 10px;
  color: #1976d2;
  font-weight: 700;
  padding: 6px 10px;
  background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
  border-radius: 8px;
  text-align: center;
  cursor: pointer;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
  border: 1px solid rgba(25, 118, 210, 0.2);
  margin-top: auto;

  &:hover {
    background: linear-gradient(135deg, #bbdefb 0%, #90caf9 100%);
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(25, 118, 210, 0.25);
    border-color: #1976d2;
  }

  &:active {
    transform: translateY(0px);
  }
}

.empty-day {
  display: flex;
  align-items: center;
  justify-content: center;
  flex: 1;
  opacity: 0.3;
  transition: opacity 0.2s ease;

  .calendar-day:hover & {
    opacity: 0.5;
  }
}

.empty-icon {
  transition: all 0.3s ease;
  
  .calendar-day:hover & {
    transform: scale(1.2);
  }
}

.search-input {
  background: white;
  border-radius: 10px;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);

  &:focus-within {
    box-shadow: 0 4px 16px rgba(25, 118, 210, 0.15);
  }

  :deep(.q-field__control) {
    border-radius: 10px;
  }
}

.filters-panel {
  .q-card {
    border-radius: 16px;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
    border: 1px solid rgba(0, 0, 0, 0.05);
  }
}

// Responsive styles
@media (max-width: 599px) {
  .calendar-card {
    border-radius: 16px;
  }

  .calendar-header {
    padding: 16px !important;
  }

  .weekdays-header {
    padding: 8px 0;
    font-size: 11px;
  }

  .calendar-day {
    min-height: 85px;
    padding: 6px;

    &:hover {
      background: white;
      box-shadow: none;
      transform: none;
      border-color: #e4e7eb;
    }

    &.is-today:hover {
      background: linear-gradient(135deg, #e3f2fd 0%, #d1e9ff 100%);
    }
  }

  .day-header {
    margin-bottom: 6px;
  }

  .day-number {
    font-size: 14px;
  }

  .event-chip {
    font-size: 10px;
    padding: 6px 8px;
    border-radius: 8px;

    &:hover {
      transform: none;
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }
  }

  .event-indicator {
    width: 2px;
    height: 14px;
  }

  .more-events {
    font-size: 9px;
    padding: 4px 8px;
    margin-top: 4px;

    &:hover {
      transform: none;
      box-shadow: 0 2px 6px rgba(25, 118, 210, 0.15);
    }
  }

  .empty-icon {
    display: none;
  }
}

@media (min-width: 600px) and (max-width: 1023px) {
  .calendar-day {
    min-height: 95px;
    padding: 8px;
  }

  .day-number {
    font-size: 14px;
  }

  .event-chip {
    font-size: 10px;
  }
}

@media (min-width: 1024px) and (max-width: 1439px) {
  .calendar-day {
    min-height: 105px;
    padding: 10px;
  }

  .day-number {
    font-size: 15px;
  }
}

@media (min-width: 1440px) {
  .calendar-day {
    min-height: 120px;
    padding: 11px;
  }

  .day-number {
    font-size: 16px;
  }

  .event-chip {
    font-size: 11px;
    padding: 7px 9px;
  }

  .more-events {
    font-size: 10px;
  }
}
</style>

