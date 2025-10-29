<template>
  <q-dialog v-model="show" persistent seamless position="top">
    <q-card flat class="loading-card">
      <q-card-section class="row items-center q-pa-md">
        <q-spinner-dots color="primary" size="40px" class="q-mr-md" />
        <div>
          <div class="text-subtitle1 text-weight-medium">{{ message }}</div>
          <div class="text-caption text-grey-7">Por favor espera...</div>
        </div>
      </q-card-section>
      <q-linear-progress indeterminate color="primary" />
    </q-card>
  </q-dialog>
</template>

<script setup>
import { computed } from 'vue';
import { useEventosStore } from '../stores/eventos';

const eventosStore = useEventosStore();

const show = computed(() => eventosStore.loading);

const message = computed(() => {
  return 'Procesando';
});
</script>

<style scoped lang="scss">
.loading-card {
  min-width: 300px;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  background: white;
}
</style>
