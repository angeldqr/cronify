<template>
  <q-page class="q-pa-md page-background">
    <div class="page-header q-mb-lg">
      <h4 class="page-title">Configuración</h4>
      <p class="page-subtitle">Personaliza tu experiencia en Cronify</p>
    </div>

    <div class="row q-col-gutter-md">
      <!-- Preferencias de Notificación -->
      <div class="col-12 col-md-6">
        <q-card flat class="config-card">
          <q-card-section class="card-header">
            <div class="row items-center">
              <q-icon name="notifications_active" size="28px" color="primary" class="q-mr-sm" />
              <div class="text-h6">Notificaciones</div>
            </div>
          </q-card-section>

          <q-separator />

          <q-card-section>
            <div class="config-item">
              <div class="config-label">
                <q-icon name="email" class="q-mr-sm" color="grey-7" />
                <span>Notificaciones por Email</span>
              </div>
              <q-toggle
                v-model="config.emailNotifications"
                color="primary"
                @update:model-value="saveConfig"
              />
            </div>

            <div class="config-item">
              <div class="config-label">
                <q-icon name="notifications" class="q-mr-sm" color="grey-7" />
                <span>Notificaciones en la App</span>
              </div>
              <q-toggle
                v-model="config.appNotifications"
                color="primary"
                @update:model-value="saveConfig"
              />
            </div>

            <q-separator class="q-my-md" />

            <div class="q-mb-md">
              <label class="text-caption text-grey-7">Días de anticipación por defecto</label>
              <q-slider
                v-model="config.defaultDays"
                :min="1"
                :max="30"
                :step="1"
                label
                label-always
                color="primary"
                @change="saveConfig"
                class="q-mt-md"
              />
            </div>

            <div class="q-mb-md">
              <label class="text-caption text-grey-7">Unidad de tiempo por defecto</label>
              <q-select
                v-model="config.defaultUnit"
                :options="unitOptions"
                outlined
                dense
                emit-value
                map-options
                @update:model-value="saveConfig"
              />
            </div>
          </q-card-section>
        </q-card>
      </div>

      <!-- Preferencias de Calendario -->
      <div class="col-12 col-md-6">
        <q-card flat class="config-card">
          <q-card-section class="card-header">
            <div class="row items-center">
              <q-icon name="calendar_today" size="28px" color="primary" class="q-mr-sm" />
              <div class="text-h6">Calendario</div>
            </div>
          </q-card-section>

          <q-separator />

          <q-card-section>
            <div class="q-mb-md">
              <label class="text-caption text-grey-7">Primer día de la semana</label>
              <q-select
                v-model="config.weekStart"
                :options="weekStartOptions"
                outlined
                dense
                emit-value
                map-options
                @update:model-value="saveConfig"
              />
            </div>

            <div class="q-mb-md">
              <label class="text-caption text-grey-7">Formato de fecha</label>
              <q-select
                v-model="config.dateFormat"
                :options="dateFormatOptions"
                outlined
                dense
                emit-value
                map-options
                @update:model-value="saveConfig"
              />
            </div>

            <div class="q-mb-md">
              <label class="text-caption text-grey-7">Formato de hora</label>
              <q-select
                v-model="config.timeFormat"
                :options="timeFormatOptions"
                outlined
                dense
                emit-value
                map-options
                @update:model-value="saveConfig"
              />
            </div>

            <div class="config-item">
              <div class="config-label">
                <q-icon name="event" class="q-mr-sm" color="grey-7" />
                <span>Mostrar fines de semana</span>
              </div>
              <q-toggle
                v-model="config.showWeekends"
                color="primary"
                @update:model-value="saveConfig"
              />
            </div>
          </q-card-section>
        </q-card>
      </div>

      <!-- Privacidad -->
      <div class="col-12 col-md-6">
        <q-card flat class="config-card">
          <q-card-section class="card-header">
            <div class="row items-center">
              <q-icon name="lock" size="28px" color="primary" class="q-mr-sm" />
              <div class="text-h6">Privacidad</div>
            </div>
          </q-card-section>

          <q-separator />

          <q-card-section>
            <div class="config-item">
              <div class="config-label">
                <q-icon name="public" class="q-mr-sm" color="grey-7" />
                <span>Eventos públicos por defecto</span>
              </div>
              <q-toggle
                v-model="config.publicByDefault"
                color="primary"
                @update:model-value="saveConfig"
              />
            </div>

            <div class="config-item">
              <div class="config-label">
                <q-icon name="visibility" class="q-mr-sm" color="grey-7" />
                <span>Permitir que otros vean mis eventos</span>
              </div>
              <q-toggle
                v-model="config.allowOthersView"
                color="primary"
                @update:model-value="saveConfig"
              />
            </div>
          </q-card-section>
        </q-card>
      </div>

      <!-- Integración Email (Preparado para Azure) -->
      <div class="col-12 col-md-6">
        <q-card flat class="config-card">
          <q-card-section class="card-header">
            <div class="row items-center">
              <q-icon name="cloud" size="28px" color="primary" class="q-mr-sm" />
              <div class="text-h6">Integración de Email</div>
            </div>
          </q-card-section>

          <q-separator />

          <q-card-section>
            <div class="config-status">
              <q-icon name="info" color="blue-5" size="48px" />
              <div class="text-subtitle1 text-grey-8 q-mt-md">
                Microsoft Graph (Azure AD)
              </div>
              <div class="text-caption text-grey-6 q-mt-sm">
                La integración de email se configurará una vez que se proporcionen las credenciales de Azure Active Directory.
              </div>
              
              <q-btn
                outline
                color="primary"
                label="Configuración pendiente"
                icon="settings"
                class="q-mt-md"
                disabled
              />
            </div>
          </q-card-section>
        </q-card>
      </div>
    </div>

    <!-- Botón guardar -->
    <div class="row justify-end q-mt-md">
      <q-btn
        unelevated
        color="primary"
        label="Configuración guardada automáticamente"
        icon="check_circle"
        disable
        class="save-btn"
      />
    </div>
  </q-page>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useQuasar } from 'quasar';

const $q = useQuasar();

const config = ref({
  // Notificaciones
  emailNotifications: true,
  appNotifications: true,
  defaultDays: 7,
  defaultUnit: 'dias',
  
  // Calendario
  weekStart: 'sunday',
  dateFormat: 'DD/MM/YYYY',
  timeFormat: '24h',
  showWeekends: true,
  
  // Privacidad
  publicByDefault: true,
  allowOthersView: true,
});

const unitOptions = [
  { label: 'Minutos', value: 'minutos' },
  { label: 'Horas', value: 'horas' },
  { label: 'Días', value: 'dias' },
  { label: 'Semanas', value: 'semanas' },
];

const weekStartOptions = [
  { label: 'Domingo', value: 'sunday' },
  { label: 'Lunes', value: 'monday' },
];

const dateFormatOptions = [
  { label: 'DD/MM/YYYY', value: 'DD/MM/YYYY' },
  { label: 'MM/DD/YYYY', value: 'MM/DD/YYYY' },
  { label: 'YYYY-MM-DD', value: 'YYYY-MM-DD' },
];

const timeFormatOptions = [
  { label: '24 horas', value: '24h' },
  { label: '12 horas (AM/PM)', value: '12h' },
];

const loadConfig = () => {
  const saved = localStorage.getItem('cronify_config');
  if (saved) {
    config.value = JSON.parse(saved);
  }
};

const saveConfig = () => {
  localStorage.setItem('cronify_config', JSON.stringify(config.value));
  $q.notify({
    type: 'positive',
    message: 'Configuración guardada',
    position: 'top',
    timeout: 1000
  });
};

onMounted(() => {
  loadConfig();
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

  .page-subtitle {
    margin: 8px 0 0 0;
    color: #546e7a;
    font-size: 14px;
  }
}

.config-card {
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  height: 100%;
}

.card-header {
  background: linear-gradient(135deg, rgba(25, 118, 210, 0.05) 0%, rgba(21, 101, 192, 0.05) 100%);
}

.config-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 0;
}

.config-label {
  display: flex;
  align-items: center;
  font-size: 14px;
  color: #37474f;
}

.config-status {
  text-align: center;
  padding: 24px 0;
}

.save-btn {
  opacity: 0.7;
}
</style>
