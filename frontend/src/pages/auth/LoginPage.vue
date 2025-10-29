<template>
  <q-page class="flex flex-center bg-gradient">
    <q-card class="login-card q-pa-lg" style="width: 400px; max-width: 90vw">
      <q-card-section class="text-center">
        <div class="text-h4 text-weight-bold text-primary q-mb-md">Cronify</div>
        <div class="text-h6 q-mb-lg">Iniciar Sesión</div>
      </q-card-section>

      <q-card-section>
        <q-form @submit="handleLogin" class="q-gutter-md">
          <q-input
            v-model="loginForm.username"
            type="text"
            label="Nombre de usuario"
            outlined
            :rules="[(val) => !!val || 'El nombre de usuario es requerido']"
            lazy-rules
          >
            <template v-slot:prepend>
              <q-icon name="person" />
            </template>
          </q-input>

          <q-input
            v-model="loginForm.password"
            :type="showPassword ? 'text' : 'password'"
            label="Contraseña"
            outlined
            :rules="[(val) => !!val || 'La contraseña es requerida']"
            lazy-rules
          >
            <template v-slot:prepend>
              <q-icon name="lock" />
            </template>
            <template v-slot:append>
              <q-icon
                :name="showPassword ? 'visibility_off' : 'visibility'"
                class="cursor-pointer"
                @click="showPassword = !showPassword"
              />
            </template>
          </q-input>

          <div class="q-mt-md">
            <q-btn
              type="submit"
              label="Iniciar Sesión"
              color="primary"
              class="full-width"
              :loading="loading"
              size="md"
            />
          </div>

          <!-- Divider -->
          <div class="row items-center q-my-md">
            <div class="col">
              <q-separator />
            </div>
            <div class="col-auto q-px-md text-grey-6">O</div>
            <div class="col">
              <q-separator />
            </div>
          </div>

          <!-- Botón de Microsoft -->
          <div class="q-mt-md">
            <MicrosoftLoginButton class="full-width" />
          </div>

          <div class="text-center q-mt-md">
            <router-link to="/auth/register" class="text-primary">
              ¿No tienes cuenta? Regístrate
            </router-link>
          </div>
        </q-form>
      </q-card-section>
    </q-card>
  </q-page>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useQuasar } from 'quasar';
import { useAuthStore } from '../../stores/auth';
import MicrosoftLoginButton from '../../components/auth/MicrosoftLoginButton.vue';
import { authService } from '../../services/authService';

const router = useRouter();
const route = useRoute();
const $q = useQuasar();
const authStore = useAuthStore();

const loginForm = ref({
  username: '',
  password: '',
});

const showPassword = ref(false);
const loading = ref(false);

// Manejar callback de Microsoft OAuth
onMounted(() => {
  const { access, refresh, error } = route.query;
  
  if (error) {
    $q.notify({
      type: 'negative',
      message: 'Error al autenticarse con Microsoft',
      caption: 'Por favor, intenta nuevamente'
    });
    // Limpiar la URL
    router.replace('/auth/login');
  } else if (access && refresh) {
    // Guardar tokens y redirigir
    authService.loginWithMicrosoft(access, refresh);
    authStore.fetchUser().then(() => {
      $q.notify({
        type: 'positive',
        message: 'Inicio de sesión exitoso con Microsoft',
        position: 'top',
      });
      router.push('/');
    });
  }
});

const handleLogin = async () => {
  loading.value = true;
  try {
    await authStore.login(loginForm.value);
    $q.notify({
      type: 'positive',
      message: 'Inicio de sesión exitoso',
      position: 'top',
    });
    router.push('/');
  } catch (error) {
    $q.notify({
      type: 'negative',
      message:
        error.response?.data?.detail ||
        'Error al iniciar sesión. Verifica tus credenciales.',
      position: 'top',
    });
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.bg-gradient {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.login-card {
  border-radius: 12px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
}
</style>
