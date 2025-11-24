<template>
  <q-page padding>
    <div class="q-pa-md">
      <!-- Header -->
      <div class="row items-center q-mb-lg">
        <div class="col">
          <h4 class="q-my-none text-h4 text-weight-bold">
            <q-icon name="admin_panel_settings" size="32px" class="q-mr-sm" color="primary" />
            Gestión de Administradores
          </h4>
          <p class="text-grey-7 q-mt-sm">
            Administra los usuarios con privilegios de administrador del sistema
          </p>
        </div>
        <div class="col-auto">
          <div class="row q-gutter-md">
            <q-card flat bordered class="stat-card">
              <q-card-section class="q-pa-md text-center">
                <div class="text-h5 text-primary text-weight-bold">{{ users.length }}</div>
                <div class="text-caption text-grey-7">Total Usuarios</div>
              </q-card-section>
            </q-card>
            <q-card flat bordered class="stat-card">
              <q-card-section class="q-pa-md text-center">
                <div class="text-h5 text-red text-weight-bold">{{ adminCount }}</div>
                <div class="text-caption text-grey-7">Administradores</div>
              </q-card-section>
            </q-card>
          </div>
        </div>
      </div>

      <!-- Búsqueda y filtros -->
      <q-card flat bordered class="q-mb-md">
        <q-card-section>
          <div class="row q-col-gutter-md">
            <div class="col-12 col-md-6">
              <q-input
                v-model="searchQuery"
                outlined
                dense
                placeholder="Buscar por nombre o email..."
                clearable
              >
                <template v-slot:prepend>
                  <q-icon name="search" />
                </template>
              </q-input>
            </div>
            <div class="col-12 col-md-6">
              <q-select
                v-model="filterType"
                outlined
                dense
                :options="filterOptions"
                option-value="value"
                option-label="label"
                emit-value
                map-options
              >
                <template v-slot:prepend>
                  <q-icon name="filter_list" />
                </template>
              </q-select>
            </div>
          </div>
        </q-card-section>
      </q-card>

      <!-- Tabla de usuarios -->
      <q-card flat bordered>
        <q-table
          :rows="paginatedUsers"
          :columns="columns"
          row-key="id"
          :loading="loading"
          v-model:pagination="pagination"
          :rows-per-page-options="[0]"
          flat
          class="admin-table"
          binary-state-sort
          hide-pagination
        >
          <!-- Columna de nombre -->
          <template v-slot:body-cell-nombre="props">
            <q-td :props="props">
              <div class="row items-center q-gutter-sm">
                <q-avatar color="primary" text-color="white" size="32px">
                  {{ props.row.nombre ? props.row.nombre.charAt(0).toUpperCase() : 'U' }}
                </q-avatar>
                <div>
                  <div class="text-weight-medium">{{ props.row.nombre || 'Sin nombre' }}</div>
                  <div class="text-caption text-grey-7">{{ props.row.username }}</div>
                </div>
              </div>
            </q-td>
          </template>

          <!-- Columna de estado admin -->
          <template v-slot:body-cell-is_admin="props">
            <q-td :props="props">
              <q-badge
                :color="props.row.is_admin ? 'red' : 'grey-5'"
                :label="props.row.is_admin ? 'Administrador' : 'Usuario'"
              >
                <q-icon
                  :name="props.row.is_admin ? 'verified' : 'person'"
                  size="14px"
                  class="q-ml-xs"
                />
              </q-badge>
            </q-td>
          </template>

          <!-- Columna de fecha de registro -->
          <template v-slot:body-cell-date_joined="props">
            <q-td :props="props">
              <div class="text-caption">{{ formatDate(props.row.date_joined) }}</div>
            </q-td>
          </template>

          <!-- Columna de acciones -->
          <template v-slot:body-cell-actions="props">
            <q-td :props="props">
              <div class="row q-gutter-xs no-wrap">
                <!-- Promover a admin -->
                <q-btn
                  v-if="!props.row.is_admin"
                  flat
                  dense
                  round
                  icon="upgrade"
                  color="primary"
                  size="sm"
                  @click="promoteUser(props.row)"
                >
                  <q-tooltip>Promover a Administrador</q-tooltip>
                </q-btn>

                <!-- Remover admin -->
                <q-btn
                  v-else
                  flat
                  dense
                  round
                  icon="remove_moderator"
                  color="negative"
                  size="sm"
                  @click="demoteUser(props.row)"
                  :disable="props.row.id === authStore.user?.id"
                >
                  <q-tooltip>
                    {{ props.row.id === authStore.user?.id ? 'No puedes remover tus propios privilegios' : 'Remover Administrador' }}
                  </q-tooltip>
                </q-btn>
              </div>
            </q-td>
          </template>

          <!-- Template para loading -->
          <template v-slot:loading>
            <q-inner-loading showing color="primary" />
          </template>

          <!-- Template para sin datos -->
          <template v-slot:no-data>
            <div class="full-width row flex-center q-gutter-sm q-pa-lg">
              <q-icon name="people_outline" size="48px" color="grey-5" />
              <span class="text-grey-7">No se encontraron usuarios</span>
            </div>
          </template>

          <!-- Footer con información de paginación -->
          <template v-slot:bottom>
            <div class="full-width row items-center justify-between q-pa-sm">
              <div class="text-caption text-grey-7">
                Mostrando {{ ((pagination.page - 1) * pagination.rowsPerPage) + 1 }} 
                - {{ Math.min(pagination.page * pagination.rowsPerPage, filteredUsers.length) }} 
                de {{ filteredUsers.length }} usuarios
                <span v-if="searchQuery || filterType !== 'all'" class="text-primary"> (filtrados)</span>
              </div>
              <q-pagination
                v-model="pagination.page"
                :max="Math.ceil(filteredUsers.length / pagination.rowsPerPage)"
                :max-pages="7"
                direction-links
                boundary-links
                color="primary"
                :disable="loading"
              />
              <div>
                <span class="text-caption text-grey-7 q-mr-sm">Filas por página:</span>
                <q-select
                  v-model="pagination.rowsPerPage"
                  :options="[10, 25, 50, 100]"
                  dense
                  options-dense
                  borderless
                  style="width: 70px"
                />
              </div>
            </div>
          </template>
        </q-table>
      </q-card>
    </div>
  </q-page>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { useQuasar } from 'quasar';
import { useAuthStore } from 'src/stores/auth';
import adminService from 'src/services/adminService';

const $q = useQuasar();
const authStore = useAuthStore();

// Estado
const loading = ref(false);
const users = ref([]);
const searchQuery = ref('');
const filterType = ref('all');

const filterOptions = [
  { label: 'Todos los usuarios', value: 'all' },
  { label: 'Solo administradores', value: 'admins' },
  { label: 'Solo usuarios', value: 'users' },
];

const pagination = ref({
  page: 1,
  rowsPerPage: 10,
  rowsNumber: 0,
});

// Columnas de la tabla
const columns = [
  {
    name: 'nombre',
    label: 'Usuario',
    field: 'nombre',
    align: 'left',
    sortable: true,
  },
  {
    name: 'email',
    label: 'Email',
    field: 'email',
    align: 'left',
    sortable: true,
  },
  {
    name: 'is_admin',
    label: 'Rol',
    field: 'is_admin',
    align: 'center',
    sortable: true,
  },
  {
    name: 'date_joined',
    label: 'Fecha de Registro',
    field: 'date_joined',
    align: 'center',
    sortable: true,
  },
  {
    name: 'actions',
    label: 'Acciones',
    field: 'actions',
    align: 'center',
  },
];

// Computed
const filteredUsers = computed(() => {
  let result = users.value;

  // Filtrar por búsqueda
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase();
    result = result.filter(
      (user) =>
        user.nombre?.toLowerCase().includes(query) ||
        user.email?.toLowerCase().includes(query) ||
        user.username?.toLowerCase().includes(query)
    );
  }

  // Filtrar por tipo
  if (filterType.value === 'admins') {
    result = result.filter((user) => user.is_admin);
  } else if (filterType.value === 'users') {
    result = result.filter((user) => !user.is_admin);
  }

  return result;
});

const paginatedUsers = computed(() => {
  const start = (pagination.value.page - 1) * pagination.value.rowsPerPage;
  const end = start + pagination.value.rowsPerPage;
  return filteredUsers.value.slice(start, end);
});

const adminCount = computed(() => {
  return users.value.filter(user => user.is_admin).length;
});

// Métodos
async function loadUsers() {
  loading.value = true;
  try {
    const data = await adminService.listAllUsers();
    users.value = data;
    pagination.value.rowsNumber = data.length;
  } catch (error) {
    $q.notify({
      type: 'negative',
      message: 'Error al cargar usuarios',
      caption: error.response?.data?.error || error.message,
    });
  } finally {
    loading.value = false;
  }
}

function promoteUser(user) {
  $q.dialog({
    title: 'Promover a Administrador',
    message: `¿Estás seguro de que deseas promover a <strong>${user.nombre}</strong> a administrador?`,
    html: true,
    cancel: true,
    persistent: true,
  }).onOk(async () => {
    try {
      await adminService.promoteToAdmin(user.id);
      $q.notify({
        type: 'positive',
        message: `${user.nombre} ahora es administrador`,
        icon: 'check_circle',
      });
      await loadUsers();
    } catch (error) {
      $q.notify({
        type: 'negative',
        message: 'Error al promover usuario',
        caption: error.response?.data?.error || error.message,
      });
    }
  });
}

function demoteUser(user) {
  $q.dialog({
    title: 'Remover Administrador',
    message: `¿Estás seguro de que deseas remover los privilegios de administrador de <strong>${user.nombre}</strong>?`,
    html: true,
    cancel: true,
    persistent: true,
    color: 'negative',
  }).onOk(async () => {
    try {
      await adminService.removeAdmin(user.id);
      $q.notify({
        type: 'positive',
        message: `Privilegios de ${user.nombre} removidos`,
        icon: 'check_circle',
      });
      await loadUsers();
    } catch (error) {
      $q.notify({
        type: 'negative',
        message: 'Error al remover administrador',
        caption: error.response?.data?.error || error.message,
      });
    }
  });
}

function formatDate(dateString) {
  if (!dateString) return '';
  const date = new Date(dateString);
  return date.toLocaleDateString('es-ES', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  });
}

// Watchers - Resetear página cuando cambien filtros
watch([searchQuery, filterType], () => {
  pagination.value.page = 1;
});

// Lifecycle
onMounted(() => {
  loadUsers();
});
</script>

<style scoped>
.admin-table {
  box-shadow: none;
}

.ellipsis-2-lines {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.stat-card {
  min-width: 120px;
  transition: all 0.3s ease;
}

.stat-card:hover {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}
</style>
