<!-- eslint-disable vue/multi-word-component-names -->
<template>
  <q-page class="flex flex-center page-background">
    <div class="text-center q-pa-xl">
      <q-icon name="error_outline" size="120px" color="red-5" class="q-mb-md" />
      
      <h1 class="text-h3 text-weight-bold text-grey-8 q-mb-md">
        500
      </h1>
      
      <div class="text-h5 text-grey-7 q-mb-md">
        Error del Servidor
      </div>
      
      <p class="text-body1 text-grey-6 q-mb-lg" style="max-width: 500px">
        Algo salió mal en el servidor. Nuestro equipo ha sido notificado y está trabajando en solucionarlo.
      </p>

      <div class="q-gutter-md">
        <q-btn
          unelevated
          color="primary"
          label="Volver al inicio"
          icon="home"
          @click="$router.push('/')"
          size="md"
        />
        <q-btn
          outline
          color="primary"
          label="Reintentar"
          icon="refresh"
          @click="$router.go(0)"
          size="md"
        />
      </div>
    </div>
  </q-page>
</template>

<script setup>
// Página de error 500 del servidor
</script>

<style scoped lang="scss">
.page-background {
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  min-height: 100vh;
}
</style>
