<template>
  <q-card style="width: 650px; max-width: 90vw; border-radius: 12px;" class="shadow-2">
    <!-- Header del modal -->
    <q-card-section class="modal-header">
      <div class="text-h6 text-weight-medium text-white">{{ isEditMode ? 'Editar Evento' : 'Crear Nuevo Evento' }}</div>
      <q-space />
      <q-btn icon="close" flat round dense color="white" @click="handleClose" />
    </q-card-section>

    <q-separator />

    <!-- Formulario principal -->
    <q-card-section class="q-pa-lg form-content">
      <q-form @submit="handleSubmit" class="q-gutter-md">
        <!-- Campo de asunto -->
        <div>
          <label class="field-label">Asunto *</label>
          <q-input
            v-model="formData.asunto"
            outlined
            dense
            placeholder="Ej: Reunión con el equipo"
            :error="!!errors.asunto"
            :error-message="errors.asunto"
          />
        </div>

        <!-- Campos de fecha y hora -->
        <div class="row q-col-gutter-md">
          <div class="col-6">
            <label class="field-label">Fecha *</label>
            <q-input
              v-model="formData.fecha"
              outlined
              dense
              placeholder="DD/MM/YYYY"
              mask="##/##/####"
              class="date-input"
              :error="!!errors.fecha"
              :error-message="errors.fecha"
              readonly
            >
              <template v-slot:append>
                <q-icon name="event" class="cursor-pointer">
                  <q-popup-proxy cover transition-show="scale" transition-hide="scale">
                    <q-date
                      v-model="formData.fecha"
                      mask="DD/MM/YYYY"
                      first-day-of-week="0"
                      :options="dateOptions"
                      :navigation-min-year-month="currentYearMonth"
                    >
                      <div class="row items-center justify-end">
                        <q-btn v-close-popup label="Cerrar" color="primary" flat />
                      </div>
                    </q-date>
                  </q-popup-proxy>
                </q-icon>
              </template>
            </q-input>
          </div>
          <div class="col-6">
            <label class="field-label">Hora *</label>
            <q-input
              v-model="formData.hora"
              type="time"
              outlined
              dense
              class="time-input"
              :error="!!errors.hora"
              :error-message="errors.hora"
            />
          </div>
        </div>

        <!-- Configuración de notificación -->
        <div class="notification-section q-pa-md">
          <div class="field-label row items-center">
            <q-icon name="notifications" color="primary" size="18px" class="q-mr-xs" />
            <span>Configuración de Notificación</span>
          </div>
          <div class="row q-col-gutter-md q-mt-sm">
            <div class="col-6">
              <q-input
                v-model.number="formData.notificacion_cantidad"
                type="number"
                outlined
                dense
                min="1"
                placeholder="7"
              />
            </div>
            <div class="col-6">
              <q-select
                v-model="formData.notificacion_unidad"
                :options="unidadesNotificacion"
                outlined
                dense
                emit-value
                map-options
              />
            </div>
          </div>
        </div>

        <!-- Campo de descripción con editor enriquecido -->
        <div>
          <label class="field-label">Descripción</label>
          <q-editor
            v-model="formData.descripcion"
            min-height="5rem"
            max-height="15rem"
            :toolbar="editorToolbar"
            class="description-editor"
          />
        </div>

        <!-- Selector de archivos adjuntos -->
        <div>
          <label class="field-label">
            <q-icon name="attach_file" size="16px" color="primary" class="q-mr-xs" />
            Archivos Adjuntos
          </label>
          
          <!-- Zona de drag & drop -->
          <div 
            class="file-dropzone"
            :class="{ 'file-dropzone-active': isDragging }"
            @dragover.prevent="isDragging = true"
            @dragleave.prevent="isDragging = false"
            @drop.prevent="handleDrop"
            @click="triggerFileInput"
          >
            <q-icon name="cloud_upload" size="40px" color="primary" class="upload-icon" />
            <div class="upload-text-primary">
              Arrastra archivos aquí o <span class="text-primary text-weight-bold cursor-pointer">haz clic para seleccionar</span>
            </div>
            <div class="upload-text-secondary">
              Máximo 10MB por archivo • Imágenes, PDF, Word, Excel, ZIP
            </div>
            <div v-if="formData.archivos.length > 0" class="upload-badge">
              <q-badge color="primary" :label="`${formData.archivos.length} archivo${formData.archivos.length !== 1 ? 's' : ''}`" />
            </div>
          </div>
          
          <!-- Input file oculto -->
          <input
            ref="fileInputRef"
            type="file"
            multiple
            accept="image/*,.pdf,.doc,.docx,.xls,.xlsx,.txt,.zip,.rar"
            @change="handleFileSelect"
            style="display: none"
          />

          <!-- Vista previa de archivos seleccionados -->
          <transition name="slide-fade">
            <div v-if="formData.archivos.length > 0" class="q-mt-md">
              <div class="files-header">
                <span class="text-weight-medium text-grey-8">
                  Archivos adjuntos ({{ formData.archivos.length }}/10)
                </span>
                <q-btn
                  flat
                  dense
                  size="sm"
                  color="negative"
                  icon="delete_sweep"
                  label="Eliminar todos"
                  @click="clearAllFiles"
                />
              </div>
              <div class="files-preview-grid">
                <transition-group name="file-item">
                  <div
                    v-for="(file, index) in formData.archivos"
                    :key="`${file.name}-${index}`"
                    class="file-card"
                  >
                    <div class="file-card-content">
                      <div class="file-icon-wrapper">
                        <q-icon 
                          :name="getFileIcon(file)" 
                          size="32px"
                          :color="getFileColor(file)"
                        />
                      </div>
                      <div class="file-info">
                        <div class="file-name-text" :title="file.name">
                          {{ file.name }}
                        </div>
                        <div class="file-size-text">
                          {{ formatFileSize(file.size) }}
                        </div>
                      </div>
                      <q-btn
                        flat
                        round
                        dense
                        size="sm"
                        icon="close"
                        color="grey-7"
                        class="file-remove-btn"
                        @click="removeFile(index)"
                      >
                        <q-tooltip>Eliminar</q-tooltip>
                      </q-btn>
                    </div>
                  </div>
                </transition-group>
              </div>
            </div>
          </transition>
        </div>

        <!-- Selector de usuarios para notificar -->
        <div>
          <label class="field-label">
            <q-icon name="mail" size="16px" color="primary" class="q-mr-xs" />
            Notificar a
          </label>
          <q-select
            v-model="formData.notificar_a"
            :options="usuariosFiltrados"
            multiple
            outlined
            dense
            use-input
            use-chips
            input-debounce="300"
            option-value="id"
            option-label="email"
            emit-value
            map-options
            @filter="filterUsuarios"
            placeholder="Escribe el correo electrónico del usuario"
            :loading="loadingUsuarios"
            class="users-select"
          >
            <template v-slot:selected-item="scope">
              <q-chip
                removable
                @remove="scope.removeAtIndex(scope.index)"
                :tabindex="scope.tabindex"
                color="primary"
                text-color="white"
                size="sm"
                dense
                class="q-ma-xs"
              >
                <q-avatar color="blue-7" text-color="white" size="24px">
                  {{ getInitials(scope.opt.nombre) }}
                </q-avatar>
                {{ scope.opt.email }}
              </q-chip>
            </template>
            <template v-slot:option="scope">
              <q-item v-bind="scope.itemProps">
                <q-item-section avatar>
                  <q-avatar color="primary" text-color="white" size="36px">
                    {{ getInitials(scope.opt.nombre) }}
                  </q-avatar>
                </q-item-section>
                <q-item-section>
                  <q-item-label>{{ scope.opt.nombre }}</q-item-label>
                  <q-item-label caption class="text-grey-7">{{ scope.opt.email }}</q-item-label>
                </q-item-section>
              </q-item>
            </template>
            <template v-slot:no-option>
              <q-item>
                <q-item-section class="text-grey-6 text-center">
                  <q-item-label>No se encontraron usuarios</q-item-label>
                  <q-item-label caption>Escribe un correo para buscar</q-item-label>
                </q-item-section>
              </q-item>
            </template>
          </q-select>
          <div class="text-caption text-grey-7 q-mt-xs q-pl-xs">
            Los usuarios seleccionados recibirán una notificación por correo antes del vencimiento
          </div>
        </div>

        <!-- Selector de visibilidad -->
        <div>
          <label class="field-label">
            <q-icon name="visibility" size="16px" color="primary" class="q-mr-xs" />
            Visibilidad *
          </label>
          <div class="visibility-info q-mb-sm q-pa-sm">
            <div class="text-caption text-grey-8">
              <strong v-if="formData.es_publico">Público:</strong>
              <strong v-else>Privado:</strong>
              <span v-if="formData.es_publico">
                Visible para ti, usuarios notificados y todos los demás
              </span>
              <span v-else>
                Solo visible para ti y los usuarios notificados
              </span>
            </div>
          </div>
          <div class="row q-col-gutter-sm">
            <div class="col-6">
              <div
                :class="['visibility-card', formData.es_publico ? 'visibility-selected' : 'visibility-option']"
                @click="formData.es_publico = true"
              >
                <q-icon 
                  name="lock_open" 
                  :size="'20px'" 
                  :color="formData.es_publico ? 'white' : 'grey-6'" 
                />
                <div class="visibility-title" :class="formData.es_publico ? 'text-white' : 'text-grey-8'">
                  Público
                </div>
                <div class="visibility-subtitle" :class="formData.es_publico ? 'text-white' : 'text-grey-6'">
                  Visible para todos
                </div>
              </div>
            </div>
            <div class="col-6">
              <div
                :class="['visibility-card', !formData.es_publico ? 'visibility-selected' : 'visibility-option']"
                @click="formData.es_publico = false"
              >
                <q-icon 
                  name="lock" 
                  :size="'20px'" 
                  :color="!formData.es_publico ? 'white' : 'grey-6'" 
                />
                <div class="visibility-title" :class="!formData.es_publico ? 'text-white' : 'text-grey-8'">
                  Privado
                </div>
                <div class="visibility-subtitle" :class="!formData.es_publico ? 'text-white' : 'text-grey-6'">
                  Solo tú puedes verlo
                </div>
              </div>
            </div>
          </div>
        </div>
      </q-form>
    </q-card-section>

    <!-- Botones de acción -->
    <q-separator />
    <q-card-actions align="right" class="q-pa-md bg-grey-1">
      <q-btn flat label="Cancelar" color="grey-8" @click="handleClose" padding="sm lg" />
      <q-btn
        unelevated
        :label="isEditMode ? 'Actualizar Evento' : 'Crear Evento'"
        color="primary"
        :loading="loading"
        @click="handleSubmit"
        padding="sm lg"
      />
    </q-card-actions>
  </q-card>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue';
import { useQuasar } from 'quasar';
import { useEventosStore } from '../../stores/eventos';
import api from '../../services/api';

const props = defineProps({
  evento: {
    type: Object,
    default: null
  }
});

const emit = defineEmits(['close', 'created', 'updated']);

const $q = useQuasar();
const eventosStore = useEventosStore();

const isEditMode = computed(() => !!props.evento);

const loading = ref(false);
const loadingUsuarios = ref(false);
const errors = ref({});
const usuariosDisponibles = ref([]);
const usuariosFiltrados = ref([]);
const isDragging = ref(false);
const fileInputRef = ref(null);
const hasUnsavedChanges = ref(false);

const formData = ref({
  asunto: '',
  fecha: '',
  hora: '',
  descripcion: '',
  notificacion_cantidad: 7,
  notificacion_unidad: 'días',
  es_publico: true,
  notificar_a: [],
  archivos: []
});

const unidadesNotificacion = [
  { label: 'Días', value: 'días' },
  { label: 'Meses', value: 'meses' }
];

// Configuración del editor de texto enriquecido
const editorToolbar = [
  ['bold', 'italic', 'underline', 'strike'],
  ['left', 'center', 'right', 'justify'],
  [
    {
      label: 'Tamaño',
      icon: 'format_size',
      fixedLabel: true,
      fixedIcon: true,
      list: 'no-icons',
      options: ['size-1', 'size-2', 'size-3', 'size-4', 'size-5', 'size-6', 'size-7']
    }
  ],
  ['unordered', 'ordered'],
  ['undo', 'redo'],
  ['removeFormat']
];

// Fecha mínima: hoy
const currentYearMonth = computed(() => {
  const now = new Date();
  const year = now.getFullYear();
  const month = String(now.getMonth() + 1).padStart(2, '0');
  return `${year}/${month}`;
});

// Validación de fechas: solo fechas futuras
const dateOptions = (date) => {
  const [year, month, day] = date.split('/');
  const selectedDate = new Date(year, month - 1, day);
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  return selectedDate >= today;
};

const loadEventoData = () => {
  if (props.evento) {
    const fechaVencimiento = new Date(props.evento.fecha_vencimiento);
    
    // Convertir a formato DD/MM/YYYY
    const dia = String(fechaVencimiento.getDate()).padStart(2, '0');
    const mes = String(fechaVencimiento.getMonth() + 1).padStart(2, '0');
    const anio = fechaVencimiento.getFullYear();
    const fecha = `${dia}/${mes}/${anio}`;
    
    const hora = fechaVencimiento.toTimeString().slice(0, 5);
    
    formData.value = {
      asunto: props.evento.asunto || '',
      fecha: fecha,
      hora: hora,
      descripcion: props.evento.descripcion || '',
      notificacion_cantidad: props.evento.notificacion_valor || 7,
      notificacion_unidad: props.evento.notificacion_unidad || 'días',
      es_publico: props.evento.es_publico ?? true,
      notificar_a: props.evento.notificar_a || [],
      archivos: []
    };
  }
};

const fetchUsuarios = async () => {
  loadingUsuarios.value = true;
  try {
    const response = await api.get('/auth/list/');
    usuariosDisponibles.value = response.data;
    usuariosFiltrados.value = [];
  } catch (error) {
    console.error('Error al cargar usuarios:', error);
    $q.notify({
      type: 'negative',
      message: 'Error al cargar la lista de usuarios',
      icon: 'error',
      position: 'top',
      timeout: 2500
    });
  } finally {
    loadingUsuarios.value = false;
  }
};

const filterUsuarios = (val, update) => {
  update(() => {
    if (val === '') {
      usuariosFiltrados.value = [];
    } else {
      const needle = val.toLowerCase();
      usuariosFiltrados.value = usuariosDisponibles.value.filter(
        user => 
          user.email.toLowerCase().includes(needle) ||
          user.nombre.toLowerCase().includes(needle)
      );
    }
  });
};

const getInitials = (nombre) => {
  if (!nombre) return '?';
  const words = nombre.trim().split(' ');
  if (words.length === 1) {
    return words[0].charAt(0).toUpperCase();
  }
  return (words[0].charAt(0) + words[words.length - 1].charAt(0)).toUpperCase();
};

const getFileIcon = (file) => {
  const name = file.name.toLowerCase();
  const type = file.type.toLowerCase();
  
  if (type.startsWith('image/')) return 'image';
  if (name.endsWith('.pdf')) return 'picture_as_pdf';
  if (name.endsWith('.doc') || name.endsWith('.docx')) return 'description';
  if (name.endsWith('.xls') || name.endsWith('.xlsx')) return 'table_chart';
  if (name.endsWith('.zip') || name.endsWith('.rar')) return 'folder_zip';
  if (name.endsWith('.txt')) return 'article';
  return 'insert_drive_file';
};

const getFileColor = (file) => {
  const name = file.name.toLowerCase();
  const type = file.type.toLowerCase();
  
  if (type.startsWith('image/')) return 'purple';
  if (name.endsWith('.pdf')) return 'red';
  if (name.endsWith('.doc') || name.endsWith('.docx')) return 'blue';
  if (name.endsWith('.xls') || name.endsWith('.xlsx')) return 'green';
  if (name.endsWith('.zip') || name.endsWith('.rar')) return 'orange';
  if (name.endsWith('.txt')) return 'grey-7';
  return 'grey';
};

const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 Bytes';
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
};

const removeFile = (index) => {
  formData.value.archivos.splice(index, 1);
};

const clearAllFiles = () => {
  formData.value.archivos = [];
};

const handleDrop = (event) => {
  isDragging.value = false;
  const files = Array.from(event.dataTransfer.files);
  processFiles(files);
};

const triggerFileInput = () => {
  fileInputRef.value?.click();
};

const handleFileSelect = (event) => {
  const files = Array.from(event.target.files || []);
  processFiles(files);
  event.target.value = '';
};

const processFiles = (files) => {
  files.forEach(file => {
    if (file.size > 10485760) {
      $q.notify({
        type: 'negative',
        message: `"${file.name}" excede 10MB`,
        icon: 'error',
        position: 'top',
        timeout: 2500
      });
      return;
    }
    
    if (formData.value.archivos.length >= 10) {
      $q.notify({
        type: 'warning',
        message: 'Máximo 10 archivos permitidos',
        icon: 'warning',
        position: 'top',
        timeout: 2000
      });
      return;
    }
    
    const isDuplicate = formData.value.archivos.some(
      existingFile => existingFile.name === file.name && existingFile.size === file.size
    );
    
    if (!isDuplicate) {
      formData.value.archivos.push(file);
    } else {
      $q.notify({
        type: 'info',
        message: `"${file.name}" ya está agregado`,
        position: 'top'
      });
    }
  });
};

const uploadFiles = async (eventoId) => {
  if (formData.value.archivos.length === 0) {
    return;
  }

  const uploadPromises = [];
  
  for (const file of formData.value.archivos) {
    const formDataFile = new FormData();
    formDataFile.append('archivo', file);
    
    const uploadPromise = api.post(`/eventos/${eventoId}/upload_file/`, formDataFile, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
    
    uploadPromises.push(uploadPromise);
  }

  try {
    await Promise.all(uploadPromises);
  } catch (error) {
    console.error('Error al subir archivos:', error);
    throw error;
  }
};

const validateForm = () => {
  const newErrors = {};

  if (!formData.value.asunto.trim()) {
    newErrors.asunto = 'El asunto es requerido';
  } else if (formData.value.asunto.length < 5) {
    newErrors.asunto = 'Mínimo 5 caracteres';
  }

  if (!formData.value.fecha) {
    newErrors.fecha = 'La fecha es requerida';
  } else {
    // Validar que la fecha no sea pasada
    const [dia, mes, anio] = formData.value.fecha.split('/');
    const fechaSeleccionada = new Date(anio, mes - 1, dia);
    const hoy = new Date();
    hoy.setHours(0, 0, 0, 0);
    
    if (fechaSeleccionada < hoy) {
      newErrors.fecha = 'La fecha no puede ser en el pasado';
    }
  }

  if (!formData.value.hora) {
    newErrors.hora = 'La hora es requerida';
  }

  errors.value = newErrors;
  return Object.keys(newErrors).length === 0;
};

const handleSubmit = async () => {
  if (!validateForm()) return;

  loading.value = true;
  try {
    // Convertir DD/MM/YYYY a YYYY-MM-DD
    const [dia, mes, anio] = formData.value.fecha.split('/');
    const fechaISO = `${anio}-${mes}-${dia}`;
    const fechaHora = `${fechaISO}T${formData.value.hora}:00`;

    const eventoData = {
      asunto: formData.value.asunto,
      descripcion: formData.value.descripcion,
      fecha_vencimiento: fechaHora,
      notificacion_valor: formData.value.notificacion_cantidad,
      notificacion_unidad: formData.value.notificacion_unidad,
      es_publico: formData.value.es_publico,
      notificar_a: formData.value.notificar_a
    };

    let evento;
    if (isEditMode.value) {
      evento = await eventosStore.updateEvento(props.evento.id, eventoData);
    } else {
      evento = await eventosStore.createEvento(eventoData);
    }

    if (formData.value.archivos.length > 0) {
      try {
        await uploadFiles(evento.id);
      } catch {
        $q.notify({
          type: 'warning',
          message: `Evento ${isEditMode.value ? 'actualizado' : 'creado'} pero algunos archivos no se pudieron subir`,
          icon: 'warning',
          position: 'top',
          timeout: 3000
        });
      }
    }

    $q.notify({
      type: 'positive',
      message: isEditMode.value ? 'Evento actualizado exitosamente' : 'Evento creado exitosamente',
      icon: 'check_circle',
      position: 'top',
      timeout: 2000
    });

    hasUnsavedChanges.value = false;
    emit(isEditMode.value ? 'updated' : 'created');
  } catch (error) {
    $q.notify({
      type: 'negative',
      message: error.response?.data?.detail || `Error al ${isEditMode.value ? 'actualizar' : 'crear'} el evento`,
      icon: 'error',
      position: 'top',
      timeout: 2500
    });
  } finally {
    loading.value = false;
  }
};

// Detectar cambios en el formulario
const trackChanges = () => {
  hasUnsavedChanges.value = true;
};

// Cerrar con confirmación si hay cambios
const handleClose = () => {
  if (hasUnsavedChanges.value) {
    $q.dialog({
      title: 'Cambios sin guardar',
      message: '¿Estás seguro que deseas salir? Los cambios no guardados se perderán.',
      cancel: {
        label: 'Cancelar',
        flat: true,
        color: 'grey-7'
      },
      ok: {
        label: 'Salir sin guardar',
        flat: true,
        color: 'negative'
      },
      persistent: true
    }).onOk(() => {
      hasUnsavedChanges.value = false;
      emit('close');
    });
  } else {
    emit('close');
  }
};

onMounted(() => {
  fetchUsuarios();
  if (isEditMode.value) {
    loadEventoData();
  }
  

  // Watch para detectar cambios en el formulario
  watch(() => formData.value.asunto, trackChanges);
  watch(() => formData.value.fecha, trackChanges);
  watch(() => formData.value.hora, trackChanges);
  watch(() => formData.value.descripcion, trackChanges);
  // Es más eficiente observar el objeto formData en profundidad
  // para detectar cualquier cambio en sus propiedades.
  watch(formData, trackChanges, { deep: true });
});
</script>

<style scoped lang="scss">
.modal-header {
  background: linear-gradient(135deg, #1976d2 0%, #1565c0 100%);
  padding: 18px 24px;
  display: flex;
  align-items: center;
}

.form-content {
  max-height: calc(90vh - 140px);
  overflow-y: auto;
  
  &::-webkit-scrollbar {
    width: 6px;
  }
  
  &::-webkit-scrollbar-track {
    background: #f5f5f5;
    border-radius: 3px;
  }
  
  &::-webkit-scrollbar-thumb {
    background: #ccc;
    border-radius: 3px;
    
    &:hover {
      background: #aaa;
    }
  }
}

.field-label {
  display: block;
  font-size: 13px;
  font-weight: 600;
  color: #424242;
  margin-bottom: 6px;
  letter-spacing: 0.2px;
}

.notification-section {
  background: linear-gradient(to right, #f8f9fa 0%, #ffffff 100%);
  border-radius: 8px;
  border: 1px solid #e3e8ee;
}

.users-select {
  :deep(.q-field__control) {
    min-height: 42px;
  }
  
  :deep(.q-chip) {
    margin: 2px;
  }
}

.file-dropzone {
  border: 2px dashed #b0bec5;
  border-radius: 10px;
  background: linear-gradient(to bottom, #fafbfc 0%, #f5f7fa 100%);
  padding: 20px;
  transition: all 0.3s ease;
  cursor: pointer;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  min-height: 120px;
  justify-content: center;
  
  &:hover {
    border-color: #1976d2;
    background: linear-gradient(to bottom, #e3f2fd 0%, #f5f7fa 100%);
    box-shadow: 0 2px 8px rgba(25, 118, 210, 0.15);
  }
  
  &.file-dropzone-active {
    border-color: #1976d2;
    border-width: 3px;
    background: linear-gradient(to bottom, #e3f2fd 0%, #bbdefb 100%);
    box-shadow: 0 4px 16px rgba(25, 118, 210, 0.25);
    transform: scale(1.01);
  }
}

.upload-icon {
  margin-bottom: 4px;
}

.upload-text-primary {
  font-size: 14px;
  color: #424242;
  font-weight: 500;
  line-height: 1.4;
}

.upload-text-secondary {
  font-size: 11px;
  color: #757575;
  line-height: 1.3;
}

.upload-badge {
  margin-top: 4px;
}

.files-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
  padding: 8px 12px;
  background: linear-gradient(to right, #f5f7fa 0%, #ffffff 100%);
  border-radius: 8px;
  border-left: 3px solid #1976d2;
}

.files-preview-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 12px;
  max-height: 300px;
  overflow-y: auto;
  padding: 4px;
  
  &::-webkit-scrollbar {
    width: 6px;
  }
  
  &::-webkit-scrollbar-track {
    background: #f5f5f5;
    border-radius: 3px;
  }
  
  &::-webkit-scrollbar-thumb {
    background: #ccc;
    border-radius: 3px;
    
    &:hover {
      background: #aaa;
    }
  }
}

.file-card {
  background: white;
  border: 1px solid #e0e0e0;
  border-radius: 10px;
  transition: all 0.2s ease;
  
  &:hover {
    border-color: #1976d2;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    transform: translateY(-2px);
  }
}

.file-card-content {
  display: flex;
  align-items: center;
  padding: 12px;
  gap: 12px;
}

.file-icon-wrapper {
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
  background: linear-gradient(135deg, #f5f7fa 0%, #e8ecf1 100%);
  border-radius: 8px;
}

.file-info {
  flex: 1;
  min-width: 0;
}

.file-name-text {
  font-size: 13px;
  font-weight: 600;
  color: #424242;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  margin-bottom: 4px;
}

.file-size-text {
  font-size: 11px;
  color: #757575;
}

.file-remove-btn {
  flex-shrink: 0;
  opacity: 0.6;
  transition: all 0.2s ease;
  
  &:hover {
    opacity: 1;
    background: #ffebee;
  }
}

.slide-fade-enter-active {
  transition: all 0.3s ease;
}

.slide-fade-leave-active {
  transition: all 0.2s ease;
}

.slide-fade-enter-from {
  transform: translateY(-10px);
  opacity: 0;
}

.slide-fade-leave-to {
  transform: translateY(-10px);
  opacity: 0;
}

.file-item-enter-active,
.file-item-leave-active {
  transition: all 0.3s ease;
}

.file-item-enter-from {
  opacity: 0;
  transform: scale(0.8);
}

.file-item-leave-to {
  opacity: 0;
  transform: scale(0.8);
}

.file-item-move {
  transition: transform 0.3s ease;
}

.visibility-info {
  background: linear-gradient(to right, #e3f2fd 0%, #f5f5f5 100%);
  border-left: 3px solid #1976d2;
  border-radius: 6px;
}

.date-input,
.time-input {
  :deep(.q-field__control) {
    min-height: 38px;
    padding: 0;
    
    input {
      font-size: 13px;
      padding: 8px 12px !important;
      text-align: left;
    }
  }
  
  :deep(.q-field__native) {
    padding: 0 !important;
  }
  
  :deep(input[type="date"]),
  :deep(input[type="time"]) {
    cursor: pointer;
    padding-left: 12px !important;
    padding-right: 8px !important;
    
    &::-webkit-calendar-picker-indicator {
      cursor: pointer;
      padding: 2px;
      margin-right: 4px;
      opacity: 0.5;
      
      &:hover {
        opacity: 0.8;
      }
    }
    
    &::-webkit-datetime-edit {
      padding-left: 0;
    }
    
    &::-webkit-datetime-edit-fields-wrapper {
      padding: 0;
    }
  }
}

.visibility-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 16px 12px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.25s ease;
  min-height: 100px;
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
  }
  
  &:active {
    transform: translateY(0);
  }
}

.visibility-option {
  border: 2px solid #e0e0e0;
  background: #fafafa;

  &:hover {
    border-color: #1976d2;
    background: #f5f5f5;
  }
}

.visibility-selected {
  background: linear-gradient(135deg, #1976d2 0%, #1565c0 100%);
  border: 2px solid #1565c0;
  box-shadow: 0 4px 16px rgba(21, 101, 192, 0.35);
  
  &:hover {
    box-shadow: 0 6px 20px rgba(21, 101, 192, 0.45);
  }
}

.visibility-title {
  font-size: 14px;
  font-weight: 600;
  letter-spacing: 0.3px;
  margin-top: 8px;
}

.visibility-subtitle {
  font-size: 11px;
  font-weight: 500;
  margin-top: 4px;
  opacity: 0.9;
}

// Estilos para el editor de texto enriquecido
.description-editor {
  border: 1px solid rgba(0, 0, 0, 0.24);
  border-radius: 4px;
  
  :deep(.q-editor__toolbar) {
    background: #f5f5f5;
    border-bottom: 1px solid rgba(0, 0, 0, 0.12);
  }
  
  :deep(.q-editor__content) {
    min-height: 5rem;
    max-height: 15rem;
    overflow-y: auto;
    
    // Estilos para el contenido HTML del editor
    p {
      margin-bottom: 0.5em;
    }
    
    ul, ol {
      padding-left: 1.5em;
      margin-bottom: 0.5em;
    }
    
    strong {
      font-weight: 600;
    }
  }
}
</style>

