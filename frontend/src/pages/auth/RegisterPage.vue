<template>
  <q-page class="flex flex-center bg-gradient">
    <q-card class="register-card q-pa-lg" style="width: 450px; max-width: 90vw">
      <q-card-section class="text-center">
        <div class="text-h4 text-weight-bold text-primary q-mb-md">Cronify</div>
        <div class="text-h6 q-mb-lg">Crear Cuenta</div>
      </q-card-section>

      <q-card-section>
        <q-form @submit="handleRegister" class="q-gutter-md">
          <q-input
            v-model="registerForm.username"
            label="Nombre de usuario"
            outlined
            :rules="[
              (val) => !!val || 'El nombre de usuario es requerido',
              (val) =>
                val.length >= 3 ||
                'Debe tener al menos 3 caracteres',
            ]"
            lazy-rules
          >
            <template v-slot:prepend>
              <q-icon name="person" />
            </template>
          </q-input>

          <q-input
            v-model="registerForm.email"
            type="email"
            label="Email"
            outlined
            :rules="[
              (val) => !!val || 'El email es requerido',
              (val) => isValidEmail(val) || 'Email inválido',
            ]"
            lazy-rules
          >
            <template v-slot:prepend>
              <q-icon name="email" />
            </template>
          </q-input>

          <q-input
            v-model="registerForm.password"
            :type="showPassword ? 'text' : 'password'"
            label="Contraseña"
            outlined
            :rules="[
              (val) => !!val || 'La contraseña es requerida',
              (val) =>
                val.length >= 8 ||
                'Debe tener al menos 8 caracteres',
            ]"
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

          <q-input
            v-model="registerForm.password2"
            :type="showConfirmPassword ? 'text' : 'password'"
            label="Confirmar contraseña"
            outlined
            :rules="[
              (val) => !!val || 'Confirma tu contraseña',
              (val) =>
                val === registerForm.password || 'Las contraseñas no coinciden',
            ]"
            lazy-rules
          >
            <template v-slot:prepend>
              <q-icon name="lock" />
            </template>
            <template v-slot:append>
              <q-icon
                :name="showConfirmPassword ? 'visibility_off' : 'visibility'"
                class="cursor-pointer"
                @click="showConfirmPassword = !showConfirmPassword"
              />
            </template>
          </q-input>

          <div class="q-mt-md">
            <q-btn
              type="submit"
              label="Registrarse"
              color="primary"
              class="full-width"
              :loading="loading"
              size="md"
            />
          </div>

          <div class="text-center q-mt-md">
            <router-link to="/auth/login" class="text-primary">
              ¿Ya tienes cuenta? Inicia sesión
            </router-link>
          </div>
        </q-form>
      </q-card-section>
    </q-card>
  </q-page>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useQuasar } from 'quasar';
import { useAuthStore } from '../../stores/auth';

const router = useRouter();
const $q = useQuasar();
const authStore = useAuthStore();

const registerForm = ref({
  username: '',
  email: '',
  password: '',
  password2: '',
});

const showPassword = ref(false);
const showConfirmPassword = ref(false);
const loading = ref(false);

const isValidEmail = (email) => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
};

const handleRegister = async () => {
  loading.value = true;
  try {
    await authStore.register(registerForm.value);
    $q.notify({
      type: 'positive',
      message: 'Registro exitoso. Por favor, inicia sesión.',
      position: 'top',
    });
    router.push('/auth/login');
  } catch (error) {
    const errorMessage =
      error.response?.data?.email?.[0] ||
      error.response?.data?.username?.[0] ||
      error.response?.data?.password?.[0] ||
      'Error al registrarse. Intenta de nuevo.';

    $q.notify({
      type: 'negative',
      message: errorMessage,
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

.register-card {
  border-radius: 12px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
}
</style>
