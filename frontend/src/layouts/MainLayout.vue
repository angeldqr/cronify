<template>
  <q-layout view="lHh Lpr lFf">
    <!-- Header principal -->
    <q-header elevated class="header-gradient">
      <q-toolbar class="q-py-sm">
        <q-btn
          flat
          dense
          round
          icon="menu"
          aria-label="Menu"
          @click="toggleLeftDrawer"
          color="white"
        />

        <q-toolbar-title class="row items-center q-gutter-sm">
          <div class="logo-container">
            <q-icon name="schedule" size="28px" color="white" />
          </div>
          <div>
            <div class="text-weight-bold text-h6 text-white">Cronify</div>
            <div class="text-caption" style="color: rgba(255, 255, 255, 0.9);">Sistema de Gestión de Vencimientos</div>
          </div>
        </q-toolbar-title>

        <q-space />

        <!-- Notificaciones -->
        <q-btn flat round dense icon="notifications" color="white" class="q-mr-sm">
          <q-badge color="red" floating rounded v-if="stats.upcoming > 0">
            {{ stats.upcoming }}
          </q-badge>
          <q-tooltip>Próximos vencimientos</q-tooltip>
          
          <q-menu transition-show="scale" transition-hide="scale" :offset="[0, 8]">
            <q-card style="width: 400px; max-width: 90vw;" class="notifications-card">
              <q-card-section class="notification-header">
                <div class="text-h6 text-white">Próximos Vencimientos</div>
                <div class="text-caption" style="color: rgba(255,255,255,0.9);">
                  Eventos en los próximos 7 días
                </div>
              </q-card-section>

              <q-separator />

              <q-card-section class="q-pa-none" style="max-height: 400px; overflow-y: auto;">
                <q-list v-if="upcomingEvents.length > 0" separator>
                  <q-item
                    v-for="event in upcomingEvents"
                    :key="event.id"
                    clickable
                    v-ripple
                    @click="viewEventFromNotification(event)"
                    class="notification-item"
                  >
                    <q-item-section avatar>
                      <q-avatar :color="getEventColor(event)" text-color="white" size="40px">
                        <q-icon name="event" />
                      </q-avatar>
                    </q-item-section>

                    <q-item-section>
                      <q-item-label class="text-weight-medium">
                        {{ event.asunto }}
                      </q-item-label>
                      <q-item-label caption>
                        <q-icon name="schedule" size="14px" class="q-mr-xs" />
                        {{ formatNotificationDate(event.fecha_vencimiento) }}
                      </q-item-label>
                      <q-item-label caption v-if="event.descripcion" class="text-grey-7 q-mt-xs ellipsis-2-lines">
                        {{ event.descripcion }}
                      </q-item-label>
                    </q-item-section>

                    <q-item-section side>
                      <q-badge :color="getEventColor(event)" :label="getDaysRemaining(event.fecha_vencimiento)" />
                    </q-item-section>
                  </q-item>
                </q-list>

                <div v-else class="q-pa-lg text-center">
                  <q-icon name="check_circle" size="48px" color="green-5" />
                  <div class="text-subtitle1 text-grey-7 q-mt-md">
                    No hay vencimientos próximos
                  </div>
                  <div class="text-caption text-grey-6">
                    Estás al día con tus eventos
                  </div>
                </div>
              </q-card-section>

              <q-separator />

              <q-card-actions align="right" class="q-pa-md">
                <q-btn
                  flat
                  label="Ver todos"
                  color="primary"
                  icon-right="arrow_forward"
                  @click="goToEvents"
                  size="sm"
                />
              </q-card-actions>
            </q-card>
          </q-menu>
        </q-btn>

        <!-- Usuario -->
        <q-btn-dropdown flat dense no-caps>
          <template v-slot:label>
            <div class="row items-center no-wrap">
              <q-avatar size="32px" class="user-avatar">
                {{ userInitials }}
              </q-avatar>
              <div class="text-left q-ml-sm text-white">
                <div class="text-weight-medium text-body2">{{ userName }}</div>
              </div>
            </div>
          </template>

          <q-list>
            <q-item clickable v-close-popup @click="goToProfile">
              <q-item-section avatar>
                <q-icon name="person" color="primary" />
              </q-item-section>
              <q-item-section>
                <q-item-label>Mi Perfil</q-item-label>
              </q-item-section>
            </q-item>

            <q-item clickable v-close-popup @click="goToSettings">
              <q-item-section avatar>
                <q-icon name="settings" color="grey-7" />
              </q-item-section>
              <q-item-section>
                <q-item-label>Configuración</q-item-label>
              </q-item-section>
            </q-item>

            <q-separator />

            <q-item clickable v-close-popup @click="handleLogout">
              <q-item-section avatar>
                <q-icon name="logout" color="negative" />
              </q-item-section>
              <q-item-section>
                <q-item-label class="text-negative">Cerrar Sesión</q-item-label>
              </q-item-section>
            </q-item>
          </q-list>
        </q-btn-dropdown>
      </q-toolbar>
    </q-header>

    <!-- Sidebar lateral -->
    <q-drawer
      v-model="leftDrawerOpen"
      show-if-above
      bordered
      :width="260"
      class="bg-grey-1"
    >
      <q-scroll-area class="fit">
        <div class="q-pa-md">
          <!-- Navegación -->
          <div class="q-mb-lg">
            <div class="text-overline text-grey-7 q-mb-sm q-ml-xs">NAVEGACIÓN</div>
            <q-list>
              <q-item
                clickable
                v-ripple
                :active="$route.name === 'home'"
                @click="$router.push('/')"
                active-class="nav-item-active"
                class="rounded-borders q-mb-xs nav-item"
              >
                <q-item-section avatar>
                  <q-icon name="home" />
                </q-item-section>
                <q-item-section>
                  <q-item-label class="text-weight-medium">Calendario</q-item-label>
                </q-item-section>
              </q-item>

              <q-item
                clickable
                v-ripple
                :active="$route.name === 'eventos'"
                @click="$router.push('/eventos')"
                active-class="nav-item-active"
                class="rounded-borders q-mb-xs nav-item"
              >
                <q-item-section avatar>
                  <q-icon name="event_note" />
                </q-item-section>
                <q-item-section>
                  <q-item-label class="text-weight-medium">Eventos</q-item-label>
                </q-item-section>
              </q-item>

              <q-item
                clickable
                v-ripple
                :active="$route.name === 'configuracion'"
                @click="$router.push('/configuracion')"
                active-class="nav-item-active"
                class="rounded-borders nav-item"
              >
                <q-item-section avatar>
                  <q-icon name="settings" />
                </q-item-section>
                <q-item-section>
                  <q-item-label class="text-weight-medium">Configuración</q-item-label>
                </q-item-section>
              </q-item>

              <!-- Sección de Administrador (solo visible para admins) -->
              <q-item
                v-if="authStore.isAdmin"
                clickable
                v-ripple
                :active="$route.name === 'administradores'"
                @click="$router.push('/administradores')"
                active-class="nav-item-active"
                class="rounded-borders nav-item q-mt-md"
              >
                <q-item-section avatar>
                  <q-icon name="admin_panel_settings" />
                </q-item-section>
                <q-item-section>
                  <q-item-label class="text-weight-medium">Administradores</q-item-label>
                </q-item-section>
                <q-item-section side>
                  <q-badge color="red" label="Admin" />
                </q-item-section>
              </q-item>
            </q-list>
          </div>

          <!-- Estadísticas -->
          <div>
            <div class="text-overline text-grey-7 q-mb-sm q-ml-xs">ESTADÍSTICAS</div>
            <q-card flat bordered class="stats-card">
              <q-card-section class="q-pa-md">
                <div class="stat-row">
                  <span class="text-grey-7 text-body2">Total</span>
                  <q-chip dense color="primary" text-color="white">
                    {{ stats.total }}
                  </q-chip>
                </div>
                <q-separator class="q-my-sm" />
                <div class="stat-row">
                  <span class="text-grey-7 text-body2">Próximos 7 días</span>
                  <q-chip dense color="orange" text-color="white">
                    {{ stats.upcoming }}
                  </q-chip>
                </div>
                <q-separator class="q-my-sm" />
                <div class="stat-row">
                  <span class="text-grey-7 text-body2">Notificados</span>
                  <q-chip dense color="green" text-color="white" clickable @click.stop="showNotificadosMenu = true">
                    {{ stats.notified }}
                  </q-chip>
                  <q-menu v-model="showNotificadosMenu" anchor="bottom right" self="top right" :offset="[0, 8]">
                    <q-list style="min-width: 250px; max-width: 350px; max-height: 300px; overflow-y: auto;">
                      <q-item v-if="!userNotificados.length" dense>
                        <q-item-section>No tienes eventos asignados para notificación.</q-item-section>
                      </q-item>
                      <q-item v-for="evento in userNotificados" :key="evento.id" clickable @click="goToEvento(evento.id)" dense>
                        <q-item-section>
                          <q-item-label><b>{{ evento.asunto }}</b></q-item-label>
                          <q-item-label caption>{{ formatFecha(evento.fecha_vencimiento) }}</q-item-label>
                        </q-item-section>
                      </q-item>
                    </q-list>
                  </q-menu>
                </div>
              </q-card-section>
            </q-card>
          </div>
        </div>
      </q-scroll-area>
    </q-drawer>

    <!-- Contenido principal -->
    <q-page-container>
      <router-view />
    </q-page-container>

    <!-- Modal detalle evento desde notificación -->
    <q-dialog v-model="showDetailModal" transition-show="scale" transition-hide="scale">
      <EventDetailModal
        v-if="selectedEvent"
        :event="selectedEvent"
        @close="showDetailModal = false"
        @updated="handleEventUpdated"
        @deleted="handleEventDeleted"
      />
    </q-dialog>

    <!-- Loading Global -->
    <GlobalLoader />
  </q-layout>
</template>

<script setup>
const showNotificadosMenu = ref(false);
const userNotificados = computed(() => {
  const user = authStore.user;
  return user && user.eventos_a_notificar ? user.eventos_a_notificar : [];
});

function formatFecha(fechaIso) {
  if (!fechaIso) return '';
  const fecha = new Date(fechaIso);
  return fecha.toLocaleString('es-ES', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });
}

function goToEvento(id) {
  // Guardar el id en localStorage para que la página de eventos lo lea y abra el modal
  localStorage.setItem('open_evento_id', id);
  router.push('/eventos');
  showNotificadosMenu.value = false;
}
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useQuasar } from 'quasar';
import { useAuthStore } from '../stores/auth';
import { useEventosStore } from '../stores/eventos';
import EventDetailModal from '../components/eventos/EventDetailModal.vue';
import GlobalLoader from '../components/GlobalLoader.vue';

const router = useRouter();
const $q = useQuasar();
const authStore = useAuthStore();
const eventosStore = useEventosStore();

const leftDrawerOpen = ref(false);
const showDetailModal = ref(false);
const selectedEvent = ref(null);

// Obtiene nombre de usuario y sus iniciales
const userName = computed(() => authStore.user?.nombre || authStore.user?.username || 'Usuario');
const userInitials = computed(() => {
  const name = authStore.user?.nombre || authStore.user?.username || 'U';
  const parts = name.trim().split(' ');
  if (parts.length >= 2) {
    return (parts[0][0] + parts[1][0]).toUpperCase();
  }
  return name.substring(0, 2).toUpperCase();
});

// Calcula estadísticas de eventos
const stats = computed(() => {
  const now = new Date();
  const sevenDaysLater = new Date(now.getTime() + 7 * 24 * 60 * 60 * 1000);
  const eventos = eventosStore.eventos || [];
  const user = authStore.user;
  return {
    total: eventos.length,
    upcoming: eventos.filter(e => {
      const eventDate = new Date(e.fecha_vencimiento);
      return eventDate >= now && eventDate <= sevenDaysLater;
    }).length,
    notified: user && user.eventos_a_notificar ? user.eventos_a_notificar.length : 0
  };
});

// Eventos próximos (7 días)
const upcomingEvents = computed(() => {
  const now = new Date();
  const sevenDaysLater = new Date(now.getTime() + 7 * 24 * 60 * 60 * 1000);
  
  return eventosStore.eventos
    .filter(e => {
      const eventDate = new Date(e.fecha_vencimiento);
      return eventDate >= now && eventDate <= sevenDaysLater;
    })
    .sort((a, b) => new Date(a.fecha_vencimiento) - new Date(b.fecha_vencimiento));
});

const toggleLeftDrawer = () => {
  leftDrawerOpen.value = !leftDrawerOpen.value;
};

const goToProfile = () => {
  router.push('/perfil');
};

const goToSettings = () => {
  router.push('/configuracion');
};

const goToEvents = () => {
  router.push('/eventos');
};

const viewEventFromNotification = (event) => {
  selectedEvent.value = event;
  showDetailModal.value = true;
};

const formatNotificationDate = (dateString) => {
  const date = new Date(dateString);
  
  // Obtener fecha formateada corta
  const fechaFormato = date.toLocaleDateString('es-ES', {
    weekday: 'short',
    day: 'numeric',
    month: 'short'
  });
  
  // Obtener hora en formato 12 horas con AM/PM
  const horaFormato = date.toLocaleTimeString('es-ES', {
    hour: 'numeric',
    minute: '2-digit',
    hour12: true
  });
  
  return `${fechaFormato}, ${horaFormato}`;
};

const getDaysRemaining = (dateString) => {
  const now = new Date();
  const eventDate = new Date(dateString);
  const diff = eventDate - now;
  const days = Math.ceil(diff / (1000 * 60 * 60 * 24));
  
  if (days === 0) return 'Hoy';
  if (days === 1) return 'Mañana';
  return `${days} días`;
};

const getEventColor = (event) => {
  const now = new Date();
  const eventDate = new Date(event.fecha_vencimiento);
  const diff = eventDate - now;
  const days = Math.ceil(diff / (1000 * 60 * 60 * 24));
  
  if (days <= 1) return 'red';
  if (days <= 3) return 'orange';
  return 'primary';
};

const handleEventUpdated = () => {
  showDetailModal.value = false;
  eventosStore.fetchEventos();
};

const handleEventDeleted = () => {
  showDetailModal.value = false;
  eventosStore.fetchEventos();
};

// Maneja cierre de sesión
const handleLogout = () => {
  $q.dialog({
    title: 'Cerrar Sesión',
    message: '¿Estás seguro que deseas cerrar sesión?',
    cancel: true,
    persistent: true
  }).onOk(() => {
    authStore.logout();
    router.push('/auth');
  });
};

// Carga eventos al iniciar
onMounted(async () => {
  try {
    await authStore.checkAuth();
    await eventosStore.fetchEventos();
  } catch (error) {
    console.error('Error cargando datos:', error);
  }
});
</script>

<style scoped lang="scss">
// Header con gradiente azul
.header-gradient {
  background: linear-gradient(135deg, #1976d2 0%, #1565c0 100%);
  box-shadow: 0 2px 8px rgba(25, 118, 210, 0.3);
}

// Logo con fondo semitransparente
.logo-container {
  width: 40px;
  height: 40px;
  background: rgba(255, 255, 255, 0.15);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
}

// Avatar del usuario
.user-avatar {
  background: linear-gradient(135deg, #42a5f5 0%, #1e88e5 100%);
  color: white;
  font-weight: 600;
}

// Bordes redondeados
.rounded-borders {
  border-radius: 8px;
}

// Items de navegación
.nav-item {
  transition: all 0.2s ease;

  &:hover:not(.nav-item-active) {
    background-color: #e3f2fd;
  }
}

// Item activo con gradiente azul
.nav-item-active {
  background: linear-gradient(135deg, #1976d2 0%, #1565c0 100%);
  color: white;
  
  :deep(.q-icon) {
    color: white;
  }
}

// Tarjeta de estadísticas
.stats-card {
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

// Fila de estadística
.stat-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

// Notificaciones
.notifications-card {
  border-radius: 12px;
  overflow: hidden;
}

.notification-header {
  background: linear-gradient(135deg, #1976d2 0%, #1565c0 100%);
  padding: 20px;
}

.notification-item {
  transition: background-color 0.2s;

  &:hover {
    background-color: rgba(25, 118, 210, 0.05);
  }
}

.ellipsis-2-lines {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
