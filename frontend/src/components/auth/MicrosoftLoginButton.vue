<template>
  <q-btn
    class="microsoft-btn"
    color="white"
    text-color="black"
    icon="img:https://upload.wikimedia.org/wikipedia/commons/4/44/Microsoft_logo.svg"
    :label="label"
    :loading="loading"
    :disable="loading"
    @click="handleMicrosoftLogin"
    unelevated
    no-caps
  >
    <template v-slot:loading>
      <q-spinner-dots size="20px" />
    </template>
  </q-btn>
</template>

<script>
import { ref } from 'vue';
import { authService } from 'src/services/authService';
import { useQuasar } from 'quasar';

export default {
  name: 'MicrosoftLoginButton',
  
  props: {
    label: {
      type: String,
      default: 'Iniciar sesión con Microsoft'
    }
  },

  setup() {
    const $q = useQuasar();
    const loading = ref(false);

    const handleMicrosoftLogin = async () => {
      loading.value = true;
      try {
        // Obtener la URL de autorización de Microsoft
        const authUrl = await authService.getMicrosoftLoginUrl();
        
        // Redirigir al usuario a Microsoft para autenticación
        window.location.href = authUrl;
        
      } catch (error) {
        loading.value = false;
        console.error('Error al iniciar sesión con Microsoft:', error);
        $q.notify({
          type: 'negative',
          message: 'No se pudo iniciar sesión con Microsoft',
          caption: error.response?.data?.error || 'Intenta nuevamente'
        });
      }
    };

    return {
      loading,
      handleMicrosoftLogin
    };
  }
};
</script>

<style scoped>
.microsoft-btn {
  border: 1px solid #8c8c8c;
  font-weight: 500;
  padding: 8px 16px;
}

.microsoft-btn:hover {
  background-color: #f3f3f3 !important;
}
</style>
