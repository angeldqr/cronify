<template>
  <q-page class="auth-page flex flex-center">
    <div class="auth-container">
      <!-- Logo de la app -->
      <div class="text-center q-mb-lg">
        <div class="logo-wrapper">
          <q-icon name="schedule" size="32px" color="white" />
        </div>
        <h1 class="app-title">Cronify</h1>
        <p class="app-subtitle">Gestiona tus fechas importantes</p>
      </div>

      <q-card class="auth-card">
        <!-- Tabs para cambiar entre login y registro -->
        <div class="toggle-tabs q-mb-lg">
          <button
            @click="isLogin || handleToggle()"
            :class="['toggle-btn', { active: isLogin }]"
          >
            Iniciar Sesión
          </button>
          <button
            @click="!isLogin || handleToggle()"
            :class="['toggle-btn', { active: !isLogin }]"
          >
            Registrarse
          </button>
        </div>

        <q-form @submit="handleSubmit" class="form-container">
          <!-- Campo de usuario (siempre visible) -->
          <div class="form-field">
            <label class="field-label">{{ isLogin ? 'Usuario' : 'Nombre de usuario' }}</label>
            <div class="input-wrapper">
              <q-icon name="person" class="input-icon" />
              <input
                v-model="formData.username"
                type="text"
                :placeholder="isLogin ? 'Tu usuario' : 'Elige un nombre de usuario'"
                :class="['custom-input', { error: errors.username }]"
                @input="clearError('username')"
              />
            </div>
            <p v-if="errors.username" class="error-message">{{ errors.username }}</p>
          </div>

          <!-- Email solo aparece en el registro -->
          <div v-if="!isLogin" class="form-field">
            <label class="field-label">Correo electrónico</label>
            <div class="input-wrapper">
              <q-icon name="email" class="input-icon" />
              <input
                v-model="formData.email"
                type="email"
                placeholder="tu@email.com"
                :class="['custom-input', { error: errors.email }]"
                @input="clearError('email')"
              />
            </div>
            <p v-if="errors.email" class="error-message">{{ errors.email }}</p>
          </div>

          <!-- Campo de contraseña -->
          <div class="form-field">
            <label class="field-label">Contraseña</label>
            <div class="input-wrapper">
              <q-icon name="lock" class="input-icon" />
              <input
                v-model="formData.password"
                :type="showPassword ? 'text' : 'password'"
                placeholder="••••••••"
                :class="['custom-input', { error: errors.password }]"
                @input="clearError('password')"
              />
              <q-icon
                :name="showPassword ? 'visibility_off' : 'visibility'"
                class="input-icon-right cursor-pointer"
                @click="showPassword = !showPassword"
              />
            </div>
            <p v-if="errors.password" class="error-message">{{ errors.password }}</p>
          </div>

          <!-- Confirmar contraseña solo en registro -->
          <div v-if="!isLogin" class="form-field">
            <label class="field-label">Confirmar contraseña</label>
            <div class="input-wrapper">
              <q-icon name="lock" class="input-icon" />
              <input
                v-model="formData.password2"
                :type="showConfirmPassword ? 'text' : 'password'"
                placeholder="••••••••"
                :class="['custom-input', { error: errors.password2 }]"
                @input="clearError('password2')"
              />
              <q-icon
                :name="showConfirmPassword ? 'visibility_off' : 'visibility'"
                class="input-icon-right cursor-pointer"
                @click="showConfirmPassword = !showConfirmPassword"
              />
            </div>
            <p v-if="errors.password2" class="error-message">{{ errors.password2 }}</p>
          </div>

          <!-- Link de contraseña olvidada solo en login -->
          <div v-if="isLogin" class="text-right">
            <a href="#" class="forgot-password">¿Olvidaste tu contraseña?</a>
          </div>

          <q-btn
            type="submit"
            :loading="loading"
            class="submit-btn"
            unelevated
            no-caps
          >
            <span>{{ isLogin ? 'Iniciar Sesión' : 'Crear Cuenta' }}</span>
            <q-icon name="arrow_forward" right />
          </q-btn>
        </q-form>
      </q-card>

      <p class="footer-text q-mt-md">© 2025 Cronify</p>
    </div>
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

// Estado del formulario
const isLogin = ref(true);
const loading = ref(false);
const showPassword = ref(false);
const showConfirmPassword = ref(false);

const formData = ref({
  username: '',
  email: '',
  password: '',
  password2: '',
});

const errors = ref({});

// Cambia entre login y registro
const handleToggle = () => {
  isLogin.value = !isLogin.value;
  formData.value = {
    username: '',
    email: '',
    password: '',
    password2: '',
  };
  errors.value = {};
};

// Limpia el error de un campo específico
const clearError = (field) => {
  if (errors.value[field]) {
    delete errors.value[field];
  }
};

// Valida los campos del formulario
const validateForm = () => {
  const newErrors = {};

  // Validar username (siempre requerido)
  if (!formData.value.username.trim()) {
    newErrors.username = isLogin.value ? 'El usuario es requerido' : 'El nombre de usuario es requerido';
  } else if (formData.value.username.length < 3) {
    newErrors.username = 'Mínimo 3 caracteres';
  }

  // Validar email (solo en registro)
  if (!isLogin.value) {
    if (!formData.value.email.trim()) {
      newErrors.email = 'El email es requerido';
    } else if (!/\S+@\S+\.\S+/.test(formData.value.email)) {
      newErrors.email = 'Email inválido';
    }
  }

  if (!formData.value.password) {
    newErrors.password = 'La contraseña es requerida';
  } else if (!isLogin.value && formData.value.password.length < 8) {
    newErrors.password = 'Mínimo 8 caracteres';
  } else if (isLogin.value && formData.value.password.length < 6) {
    newErrors.password = 'Mínimo 6 caracteres';
  }

  if (!isLogin.value && formData.value.password !== formData.value.password2) {
    newErrors.password2 = 'Las contraseñas no coinciden';
  }

  errors.value = newErrors;
  return Object.keys(newErrors).length === 0;
};

// Procesa el envío del formulario
const handleSubmit = async () => {
  if (!validateForm()) return;

  loading.value = true;
  try {
    if (isLogin.value) {
      await authStore.login({
        username: formData.value.username,
        password: formData.value.password,
      });
      $q.notify({
        type: 'positive',
        message: '¡Inicio de sesión exitoso!',
        position: 'top',
      });
      router.push('/');
    } else {
      await authStore.register(formData.value);
      $q.notify({
        type: 'positive',
        message: '¡Registro exitoso! Por favor, inicia sesión.',
        position: 'top',
      });
      handleToggle();
    }
  } catch (error) {
    $q.notify({
      type: 'negative',
      message:
        error.response?.data?.detail ||
        error.response?.data?.email?.[0] ||
        error.response?.data?.username?.[0] ||
        'Error en la operación. Intenta de nuevo.',
      position: 'top',
    });
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped lang="scss">
.auth-page {
  min-height: 100vh;
  background: #f9fafb;
}

.auth-container {
  width: 100%;
  max-width: 450px;
  padding: 16px;
}

.logo-wrapper {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 64px;
  height: 64px;
  background: #2563eb;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(37, 99, 235, 0.2);
  margin-bottom: 16px;
}

.app-title {
  font-size: 32px;
  font-weight: 700;
  color: #111827;
  margin-bottom: 4px;
}

.app-subtitle {
  color: #6b7280;
  font-size: 14px;
}

.auth-card {
  border-radius: 8px;
  padding: 32px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.toggle-tabs {
  display: flex;
  border-bottom: 1px solid #e5e7eb;
  margin-bottom: 24px;
}

.toggle-btn {
  flex: 1;
  padding: 12px;
  background: none;
  border: none;
  font-weight: 500;
  color: #6b7280;
  cursor: pointer;
  transition: color 0.2s;
  position: relative;

  &:hover {
    color: #374151;
  }

  &.active {
    color: #2563eb;

    &::after {
      content: '';
      position: absolute;
      bottom: -1px;
      left: 0;
      right: 0;
      height: 2px;
      background: #2563eb;
    }
  }
}

.form-container {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.form-field {
  display: flex;
  flex-direction: column;
}

.field-label {
  display: block;
  font-size: 14px;
  font-weight: 500;
  color: #374151;
  margin-bottom: 4px;
}

.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.input-icon {
  position: absolute;
  left: 12px;
  color: #9ca3af;
  font-size: 20px;
}

.input-icon-right {
  position: absolute;
  right: 12px;
  color: #9ca3af;
  font-size: 20px;
}

.custom-input {
  width: 100%;
  padding: 10px 12px 10px 40px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 14px;
  transition: border-color 0.2s, box-shadow 0.2s;

  &:focus {
    outline: none;
    border-color: #2563eb;
    box-shadow: 0 0 0 1px #2563eb;
  }

  &.error {
    border-color: #fca5a5;
  }

  &::placeholder {
    color: #9ca3af;
  }
}

.error-message {
  color: #ef4444;
  font-size: 12px;
  margin-top: 4px;
}

.forgot-password {
  font-size: 14px;
  color: #2563eb;
  text-decoration: none;
  font-weight: 500;

  &:hover {
    color: #1d4ed8;
  }
}

.submit-btn {
  width: 100%;
  background: #2563eb;
  color: white;
  font-weight: 500;
  padding: 10px;
  border-radius: 8px;
  margin-top: 8px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
  transition: all 0.2s;

  &:hover {
    background: #1d4ed8;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }
}

.footer-text {
  text-align: center;
  color: #6b7280;
  font-size: 14px;
}
</style>
