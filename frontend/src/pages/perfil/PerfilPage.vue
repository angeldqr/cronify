<template>
  <q-page class="q-pa-md page-background">
    <div class="row q-col-gutter-lg">
      <!-- Columna izquierda - Información personal -->
      <div class="col-12 col-md-8">
        <q-card flat class="profile-card">
          <q-card-section class="card-header">
            <div class="text-h6">Información Personal</div>
          </q-card-section>
          <q-separator />
          <q-card-section class="q-pa-lg">
            <q-form @submit="handleUpdateProfile" class="q-gutter-md">
              <div class="row q-col-gutter-md">
                <div class="col-12 col-sm-6">
                  <label class="field-label">Nombre</label>
                  <q-input
                    v-model="formData.first_name"
                    outlined
                    dense
                    placeholder="Tu nombre"
                  />
                </div>
                <div class="col-12 col-sm-6">
                  <label class="field-label">Apellido</label>
                  <q-input
                    v-model="formData.last_name"
                    outlined
                    dense
                    placeholder="Tu apellido"
                  />
                </div>
              </div>

              <div>
                <label class="field-label">Nombre de usuario</label>
                <q-input
                  v-model="formData.username"
                  outlined
                  dense
                  readonly
                  bg-color="grey-2"
                />
              </div>

              <div>
                <label class="field-label">Correo electrónico</label>
                <q-input
                  v-model="formData.email"
                  type="email"
                  outlined
                  dense
                  placeholder="tu@email.com"
                />
              </div>

              <div class="row justify-end q-mt-md">
                <q-btn
                  unelevated
                  label="Guardar Cambios"
                  color="primary"
                  type="submit"
                  :loading="loading"
                  padding="sm lg"
                />
              </div>
            </q-form>
          </q-card-section>
        </q-card>

        <!-- Cambiar contraseña -->
        <q-card flat class="profile-card q-mt-lg">
          <q-card-section class="card-header">
            <div class="text-h6">Cambiar Contraseña</div>
          </q-card-section>
          <q-separator />
          <q-card-section class="q-pa-lg">
            <q-form @submit="handleChangePassword" class="q-gutter-md">
              <div>
                <label class="field-label">Contraseña actual</label>
                <q-input
                  v-model="passwordData.old_password"
                  type="password"
                  outlined
                  dense
                  placeholder="••••••••"
                />
              </div>

              <div>
                <label class="field-label">Nueva contraseña</label>
                <q-input
                  v-model="passwordData.new_password"
                  type="password"
                  outlined
                  dense
                  placeholder="••••••••"
                />
              </div>

              <div>
                <label class="field-label">Confirmar nueva contraseña</label>
                <q-input
                  v-model="passwordData.confirm_password"
                  type="password"
                  outlined
                  dense
                  placeholder="••••••••"
                />
              </div>

              <div class="row justify-end q-mt-md">
                <q-btn
                  unelevated
                  label="Cambiar Contraseña"
                  color="primary"
                  type="submit"
                  :loading="loadingPassword"
                  padding="sm lg"
                />
              </div>
            </q-form>
          </q-card-section>
        </q-card>
      </div>

      <!-- Columna derecha - Estadísticas y Notificaciones -->
      <div class="col-12 col-md-4">
        <q-card flat class="profile-card">
          <q-card-section class="card-header">
            <div class="text-h6">Mi Actividad</div>
          </q-card-section>
          <q-separator />
          <q-card-section class="q-pa-lg">
            <div class="stats-grid">
              <div class="stat-item">
                <q-icon name="event" size="32px" color="primary" />
                <div class="stat-value">{{ user?.eventos_creados_count || 0 }}</div>
                <div class="stat-label">Eventos Creados</div>
              </div>
              <div class="stat-item">
                <q-icon name="person" size="32px" color="green-6" />
                <div class="stat-value">{{ user?.nombre || 'Usuario' }}</div>
                <div class="stat-label">Nombre Completo</div>
              </div>
              <div class="stat-item">
                <q-icon name="notifications_active" size="32px" color="orange" />
                <div class="stat-value">{{ user?.eventos_a_notificar?.length || 0 }}</div>
                <div class="stat-label">Eventos donde serás notificado</div>
              </div>
            </div>
          </q-card-section>
        </q-card>

        <q-card flat class="profile-card q-mt-lg" v-if="user?.eventos_a_notificar?.length">
          <q-card-section class="card-header">
            <div class="text-h6">Próximos eventos donde serás notificado</div>
          </q-card-section>
          <q-separator />
          <q-card-section class="q-pa-lg">
            <q-list>
              <q-item v-for="evento in user.eventos_a_notificar" :key="evento.id">
                <q-item-section>
                  <q-item-label><b>{{ evento.asunto }}</b></q-item-label>
                  <q-item-label caption>{{ formatFecha(evento.fecha_vencimiento) }}</q-item-label>
                </q-item-section>
              </q-item>
            </q-list>
          </q-card-section>
        </q-card>
      </div>
    </div>
  </q-page>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useQuasar } from 'quasar';
import { useAuthStore } from '../../stores/auth';


const $q = useQuasar();
const authStore = useAuthStore();

const loading = ref(false);
const loadingPassword = ref(false);
const user = ref(null);

const formData = ref({
  username: '',
  email: '',
  first_name: '',
  last_name: ''
});

const passwordData = ref({
  old_password: '',
  new_password: '',
  confirm_password: ''
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

const loadProfile = () => {
  user.value = authStore.user;
  if (user.value) {
    formData.value = {
      username: user.value.username || '',
      email: user.value.email || '',
      first_name: user.value.first_name || '',
      last_name: user.value.last_name || ''
    };
  }
};

const handleUpdateProfile = async () => {
  loading.value = true;
  try {
    await authStore.updateProfile({
      email: formData.value.email,
      first_name: formData.value.first_name,
      last_name: formData.value.last_name
    });

    $q.notify({
      type: 'positive',
      message: 'Perfil actualizado exitosamente',
      position: 'top'
    });
    
    loadProfile();
  } catch (error) {
    $q.notify({
      type: 'negative',
      message: error.response?.data?.detail || 'Error al actualizar el perfil',
      position: 'top'
    });
  } finally {
    loading.value = false;
  }
};

const handleChangePassword = async () => {
  if (passwordData.value.new_password !== passwordData.value.confirm_password) {
    $q.notify({
      type: 'negative',
      message: 'Las contraseñas no coinciden',
      position: 'top'
    });
    return;
  }

  if (passwordData.value.new_password.length < 8) {
    $q.notify({
      type: 'negative',
      message: 'La contraseña debe tener al menos 8 caracteres',
      position: 'top'
    });
    return;
  }

  loadingPassword.value = true;
  try {
    await authStore.changePassword({
      old_password: passwordData.value.old_password,
      new_password: passwordData.value.new_password
    });

    $q.notify({
      type: 'positive',
      message: 'Contraseña cambiada exitosamente',
      position: 'top'
    });

    passwordData.value = {
      old_password: '',
      new_password: '',
      confirm_password: ''
    };
  } catch (error) {
    $q.notify({
      type: 'negative',
      message: error.response?.data?.detail || 'Error al cambiar la contraseña',
      position: 'top'
    });
  } finally {
    loadingPassword.value = false;
  }
};

onMounted(() => {
  loadProfile();
});
</script>

<style scoped lang="scss">
.page-background {
  background: #f5f5f5;
}

.profile-card {
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.card-header {
  background: linear-gradient(135deg, #1976d2 0%, #1565c0 100%);
  color: white;
  padding: 20px 24px;
}

.field-label {
  display: block;
  font-size: 13px;
  font-weight: 600;
  color: #546e7a;
  margin-bottom: 6px;
}

.stats-grid {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.stat-item {
  text-align: center;
  padding: 20px;
  background: #f5f5f5;
  border-radius: 12px;

  .stat-value {
    font-size: 24px;
    font-weight: 700;
    color: #263238;
    margin: 12px 0 4px;
  }

  .stat-label {
    font-size: 13px;
    color: #78909c;
    font-weight: 500;
  }
}
</style>
