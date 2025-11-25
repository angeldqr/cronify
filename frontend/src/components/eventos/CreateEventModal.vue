<template>
  <q-card 
    :style="$q.screen.gt.md ? 'width: 750px; max-width: 90vw;' : $q.screen.gt.sm ? 'width: 650px; max-width: 90vw;' : 'width: 100%; max-width: 95vw;'" 
    class="event-modal shadow-10"
  >
    <!-- Header del modal -->
    <q-card-section :class="['modal-header', $q.screen.lt.sm ? 'q-pa-md' : 'q-pa-lg']">
      <div class="header-content">
        <div class="header-icon-wrapper">
          <q-icon :name="isEditMode ? 'edit_calendar' : 'add_box'" size="28px" color="white" />
        </div>
        <div class="header-text">
          <div :class="$q.screen.gt.xs ? 'text-h5' : 'text-h6'" class="text-weight-bold text-white header-title">
            {{ isEditMode ? 'Editar Evento' : 'Crear Nuevo Evento' }}
          </div>
          <div class="text-caption text-white header-subtitle" style="opacity: 0.9;">
            {{ isEditMode ? 'Actualiza los detalles de tu evento' : 'Configura todos los detalles del evento' }}
          </div>
        </div>
      </div>
      <q-btn icon="close" flat round dense color="white" size="md" @click="handleClose" class="close-btn" />
    </q-card-section>

    <!-- Formulario principal -->
    <q-card-section :class="['form-content', $q.screen.lt.sm ? 'q-pa-md' : 'q-pa-lg']">
      <q-form @submit="handleSubmit" class="q-gutter-md">
        <!-- Campo de asunto -->
        <div class="form-field">
          <label class="field-label">
            <q-icon name="title" size="18px" color="primary" class="q-mr-xs" />
            Asunto *
          </label>
          <q-input
            v-model="formData.asunto"
            outlined
            placeholder="Ej: Reunión con el equipo de desarrollo"
            :error="!!errors.asunto"
            :error-message="errors.asunto"
            class="custom-input"
          >
            <template v-slot:prepend>
              <q-icon name="event_note" color="grey-6" />
            </template>
          </q-input>
        </div>

        <!-- Campos de fecha y hora -->
        <div class="row q-col-gutter-md">
          <div :class="$q.screen.gt.xs ? 'col-6' : 'col-12'">
            <label class="field-label">
              <q-icon name="calendar_today" size="18px" color="primary" class="q-mr-xs" />
              Fecha de vencimiento *
            </label>
            <q-input
              v-model="formData.fecha"
              outlined
              placeholder="DD/MM/YYYY"
              mask="##/##/####"
              class="custom-input date-input"
              :error="!!errors.fecha"
              :error-message="errors.fecha"
              readonly
            >
              <template v-slot:append>
                <q-icon name="event" class="cursor-pointer" color="primary">
                  <q-popup-proxy cover transition-show="scale" transition-hide="scale">
                    <q-date
                      v-model="formData.fecha"
                      mask="DD/MM/YYYY"
                      first-day-of-week="0"
                      :options="dateOptions"
                      :navigation-min-year-month="currentYearMonth"
                      color="primary"
                    >
                      <div class="row items-center justify-end q-pa-sm">
                        <q-btn v-close-popup label="Cerrar" color="primary" flat />
                      </div>
                    </q-date>
                  </q-popup-proxy>
                </q-icon>
              </template>
            </q-input>
          </div>
          <div :class="$q.screen.gt.xs ? 'col-6' : 'col-12'">
            <label class="field-label">
              <q-icon name="schedule" size="18px" color="primary" class="q-mr-xs" />
              Hora *
            </label>
            <q-input
              v-model="formData.hora"
              type="time"
              outlined
              class="custom-input time-input"
              :error="!!errors.hora"
              :error-message="errors.hora"
            >
              <template v-slot:prepend>
                <q-icon name="access_time" color="grey-6" />
              </template>
            </q-input>
          </div>
        </div>

        <!-- Configuración de notificación -->
        <div class="notification-section">
          <div class="section-header">
            <q-icon name="notifications_active" color="primary" size="20px" />
            <span class="section-title">Configuración de Notificación</span>
          </div>
          <div class="section-description">
            Recibe un recordatorio antes del vencimiento del evento
          </div>
          <div class="notification-inputs">
            <div class="notification-label">Notificar con</div>
            <div class="notification-controls">
              <q-input
                v-model.number="formData.notificacion_cantidad"
                type="number"
                outlined
                dense
                min="1"
                placeholder="7"
                class="notification-input"
              >
                <template v-slot:prepend>
                  <q-icon name="tag" color="primary" size="18px" />
                </template>
              </q-input>
              <q-select
                v-model="formData.notificacion_unidad"
                :options="unidadesNotificacion"
                outlined
                dense
                emit-value
                map-options
                class="notification-select"
              >
                <template v-slot:prepend>
                  <q-icon name="timelapse" color="primary" size="18px" />
                </template>
              </q-select>
              <div class="notification-suffix">de anticipación</div>
            </div>
          </div>
        </div>

        <!-- Campo de descripción con editor enriquecido -->
        <div class="form-field">
          <label class="field-label">
            <q-icon name="description" size="18px" color="primary" class="q-mr-xs" />
            Descripción detallada
          </label>
          <q-editor
            v-model="formData.descripcion"
            min-height="6rem"
            max-height="16rem"
            :toolbar="editorToolbar"
            class="description-editor"
            placeholder="Escribe una descripción detallada del evento..."
          />
        </div>

        <!-- Selector de archivos adjuntos -->
        <div class="form-field">
          <label class="field-label">
            <q-icon name="attach_file" size="18px" color="primary" class="q-mr-xs" />
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
            <div class="dropzone-content">
              <q-icon name="cloud_upload" size="48px" color="primary" class="upload-icon" />
              <div class="upload-text-primary">
                Arrastra archivos aquí o <span class="text-primary text-weight-bold cursor-pointer">haz clic para seleccionar</span>
              </div>
              <div class="upload-text-secondary">
                Máximo 10MB por archivo • Imágenes, PDF, Word, Excel, ZIP
              </div>
              <div v-if="formData.archivos.length > 0" class="upload-badge-wrapper">
                <q-badge color="primary" :label="`${formData.archivos.length} archivo${formData.archivos.length !== 1 ? 's' : ''} seleccionado${formData.archivos.length !== 1 ? 's' : ''}`" class="upload-badge" />
              </div>
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
        <div class="form-field">
          <label class="field-label">
            <q-icon name="people" size="18px" color="primary" class="q-mr-xs" />
            Notificar a usuarios
          </label>
          <q-select
            v-model="formData.notificar_a"
            :options="usuariosFiltrados"
            multiple
            outlined
            use-input
            use-chips
            input-debounce="300"
            option-value="id"
            option-label="email"
            @filter="filterUsuarios"
            placeholder="Busca usuarios por correo electrónico..."
            :loading="loadingUsuarios"
            class="users-select custom-input"
          >
            <template v-slot:prepend>
              <q-icon name="mail_outline" color="grey-6" />
            </template>
            <template v-slot:selected-item="scope">
              <q-chip
                removable
                @remove="scope.removeAtIndex(scope.index)"
                :tabindex="scope.tabindex"
                color="primary"
                text-color="white"
                size="md"
                class="q-my-xs user-chip"
              >
                <q-avatar color="blue-9" text-color="white" size="26px" class="q-mr-xs">
                  {{ getInitials(scope.opt.nombre) }}
                </q-avatar>
                <span class="user-chip-email">{{ scope.opt.email }}</span>
              </q-chip>
            </template>
            <template v-slot:option="scope">
              <q-item v-bind="scope.itemProps" class="user-option">
                <q-item-section avatar>
                  <q-avatar color="primary" text-color="white" size="40px">
                    {{ getInitials(scope.opt.nombre) }}
                  </q-avatar>
                </q-item-section>
                <q-item-section>
                  <q-item-label class="text-weight-medium">{{ scope.opt.nombre }}</q-item-label>
                  <q-item-label caption class="text-grey-7">{{ scope.opt.email }}</q-item-label>
                </q-item-section>
              </q-item>
            </template>
            <template v-slot:no-option>
              <q-item>
                <q-item-section class="text-grey-6 text-center q-py-md">
                  <q-icon name="search_off" size="32px" color="grey-5" class="q-mb-sm" />
                  <q-item-label class="text-weight-medium">No se encontraron usuarios</q-item-label>
                  <q-item-label caption>Escribe un correo para buscar</q-item-label>
                </q-item-section>
              </q-item>
            </template>
          </q-select>
          <div class="field-hint">
            <q-icon name="info_outline" size="14px" color="grey-7" class="q-mr-xs" />
            Los usuarios seleccionados recibirán una notificación por correo antes del vencimiento
          </div>
        </div>

        <!-- Selector de visibilidad -->
        <div class="form-field">
          <label class="field-label">
            <q-icon name="security" size="18px" color="primary" class="q-mr-xs" />
            Visibilidad del evento *
          </label>
          <div class="visibility-info">
            <q-icon :name="formData.es_publico ? 'lock_open' : 'lock'" size="16px" :color="formData.es_publico ? 'positive' : 'warning'" />
            <div class="visibility-info-text">
              <strong>{{ formData.es_publico ? 'Evento Público' : 'Evento Privado' }}:</strong>
              <span v-if="formData.es_publico">
                Visible para ti, usuarios notificados y todos los demás usuarios
              </span>
              <span v-else>
                Solo visible para ti y los usuarios que notifiques
              </span>
            </div>
          </div>
          <div class="row q-col-gutter-md">
            <div class="col-6">
              <div
                :class="['visibility-card', formData.es_publico ? 'visibility-selected' : 'visibility-option']"
                @click="formData.es_publico = true"
              >
                <div class="visibility-icon-wrapper" :class="formData.es_publico ? 'selected' : ''">
                  <q-icon 
                    name="lock_open" 
                    size="28px" 
                    :color="formData.es_publico ? 'white' : 'grey-6'" 
                  />
                </div>
                <div class="visibility-title" :class="formData.es_publico ? 'text-white' : 'text-grey-8'">
                  Público
                </div>
                <div class="visibility-subtitle" :class="formData.es_publico ? 'text-white' : 'text-grey-6'">
                  Todos pueden verlo
                </div>
                <q-icon 
                  v-if="formData.es_publico" 
                  name="check_circle" 
                  size="20px" 
                  color="white" 
                  class="check-icon"
                />
              </div>
            </div>
            <div class="col-6">
              <div
                :class="['visibility-card', !formData.es_publico ? 'visibility-selected' : 'visibility-option']"
                @click="formData.es_publico = false"
              >
                <div class="visibility-icon-wrapper" :class="!formData.es_publico ? 'selected' : ''">
                  <q-icon 
                    name="lock" 
                    size="28px" 
                    :color="!formData.es_publico ? 'white' : 'grey-6'" 
                  />
                </div>
                <div class="visibility-title" :class="!formData.es_publico ? 'text-white' : 'text-grey-8'">
                  Privado
                </div>
                <div class="visibility-subtitle" :class="!formData.es_publico ? 'text-white' : 'text-grey-6'">
                  Solo tú y los notificados
                </div>
                <q-icon 
                  v-if="!formData.es_publico" 
                  name="check_circle" 
                  size="20px" 
                  color="white" 
                  class="check-icon"
                />
              </div>
            </div>
          </div>
        </div>
      </q-form>
    </q-card-section>

    <!-- Botones de acción -->
    <q-card-actions align="right" :class="['modal-actions', $q.screen.lt.sm ? 'q-pa-md' : 'q-pa-lg']">
      <q-btn 
        flat 
        label="Cancelar" 
        color="grey-8" 
        @click="handleClose" 
        padding="sm lg" 
        size="md"
        class="cancel-btn"
      />
      <q-btn
        unelevated
        :label="isEditMode ? 'Actualizar Evento' : 'Crear Evento'"
        color="primary"
        :loading="loading"
        @click="handleSubmit"
        padding="sm xl"
        size="md"
        class="submit-btn"
        :icon-right="isEditMode ? 'save' : 'add_circle'"
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
  },
  preselectedDate: {
    type: Date,
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
const archivosEliminados = ref([]); // IDs de archivos existentes que se eliminaron

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

const loadEventoData = async () => {
  if (props.evento) {
    const fechaVencimiento = new Date(props.evento.fecha_vencimiento);
    
    // Convertir a formato DD/MM/YYYY
    const dia = String(fechaVencimiento.getDate()).padStart(2, '0');
    const mes = String(fechaVencimiento.getMonth() + 1).padStart(2, '0');
    const anio = fechaVencimiento.getFullYear();
    const fecha = `${dia}/${mes}/${anio}`;
    
    const hora = fechaVencimiento.toTimeString().slice(0, 5);
    
    // Cargar archivos adjuntos existentes como objetos simulados para mostrar
    const archivosExistentes = (props.evento.archivos_adjuntos || []).map(archivo => ({
      name: archivo.nombre_original,
      size: archivo.tamaño_bytes || 0,
      type: archivo.tipo_mime || '',
      isExisting: true,
      id: archivo.id,
      url_descarga: archivo.url_descarga
    }));
    
    // Obtener los IDs de usuarios notificados
    const usuariosNotificadosIds = props.evento.notificar_a_ids || props.evento.notificar_a || [];
    
    // Cargar los usuarios completos desde los IDs
    // Primero asegurarse de que los usuarios disponibles están cargados
    if (usuariosDisponibles.value.length === 0) {
      await fetchUsuarios();
    }
    
    // Buscar los objetos completos de los usuarios notificados
    const usuariosNotificadosObjetos = usuariosDisponibles.value.filter(
      usuario => usuariosNotificadosIds.includes(usuario.id)
    );
    
    formData.value = {
      asunto: props.evento.asunto || '',
      fecha: fecha,
      hora: hora,
      descripcion: props.evento.descripcion || '',
      notificacion_cantidad: props.evento.notificacion_valor || 7,
      notificacion_unidad: props.evento.notificacion_unidad || 'días',
      es_publico: props.evento.es_publico ?? true,
      notificar_a: usuariosNotificadosObjetos,
      archivos: archivosExistentes
    };
    
    // Resetear la lista de archivos eliminados
    archivosEliminados.value = [];
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
  const archivo = formData.value.archivos[index];
  
  // Si es un archivo existente (del servidor), guardar su ID para eliminarlo después
  if (archivo.isExisting && archivo.id) {
    archivosEliminados.value.push(archivo.id);
  }
  
  formData.value.archivos.splice(index, 1);
};

const clearAllFiles = () => {
  // Guardar IDs de todos los archivos existentes para eliminarlos
  formData.value.archivos.forEach(archivo => {
    if (archivo.isExisting && archivo.id) {
      archivosEliminados.value.push(archivo.id);
    }
  });
  
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
  // Filtrar solo archivos nuevos (no los que ya están en el servidor)
  const archivosNuevos = formData.value.archivos.filter(file => !file.isExisting);
  
  if (archivosNuevos.length === 0) {
    return;
  }

  const uploadPromises = [];
  
  for (const file of archivosNuevos) {
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

const deleteFiles = async (eventoId) => {
  if (archivosEliminados.value.length === 0) {
    return;
  }

  const deletePromises = archivosEliminados.value.map(archivoId => 
    api.delete(`/eventos/${eventoId}/archivos/${archivoId}/`)
  );

  try {
    await Promise.all(deletePromises);
  } catch (error) {
    console.error('Error al eliminar archivos:', error);
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

    // Extraer solo los IDs de los usuarios notificados (pueden ser objetos o IDs)
    const notificarAIds = formData.value.notificar_a.map(usuario => 
      typeof usuario === 'object' ? usuario.id : usuario
    );

    const eventoData = {
      asunto: formData.value.asunto,
      descripcion: formData.value.descripcion,
      fecha_vencimiento: fechaHora,
      notificacion_valor: formData.value.notificacion_cantidad,
      notificacion_unidad: formData.value.notificacion_unidad,
      es_publico: formData.value.es_publico,
      notificar_a: notificarAIds
    };

    let evento;
    if (isEditMode.value) {
      evento = await eventosStore.updateEvento(props.evento.id, eventoData);
      
      // Eliminar archivos que fueron removidos
      if (archivosEliminados.value.length > 0) {
        try {
          await deleteFiles(props.evento.id);
        } catch {
          $q.notify({
            type: 'warning',
            message: 'Evento actualizado pero algunos archivos no se pudieron eliminar',
            icon: 'warning',
            position: 'top',
            timeout: 3000
          });
        }
      }
    } else {
      evento = await eventosStore.createEvento(eventoData);
    }

    // Subir solo archivos nuevos
    const archivosNuevos = formData.value.archivos.filter(file => !file.isExisting);
    if (archivosNuevos.length > 0) {
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

onMounted(async () => {
  await fetchUsuarios();
  if (isEditMode.value) {
    await loadEventoData();
  } else if (props.preselectedDate) {
    // Si hay una fecha pre-seleccionada (desde el calendario), usarla
    const dia = String(props.preselectedDate.getDate()).padStart(2, '0');
    const mes = String(props.preselectedDate.getMonth() + 1).padStart(2, '0');
    const anio = props.preselectedDate.getFullYear();
    formData.value.fecha = `${dia}/${mes}/${anio}`;
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
// Modal principal
.event-modal {
  border-radius: 20px !important;
  overflow: hidden;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
}

// Header del modal
.modal-header {
  background: linear-gradient(135deg, #1e88e5 0%, #1565c0 100%);
  position: relative;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  overflow: hidden;

  &::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -10%;
    width: 400px;
    height: 400px;
    background: radial-gradient(circle, rgba(255, 255, 255, 0.1) 0%, transparent 70%);
    border-radius: 50%;
  }

  .header-content {
    display: flex;
    align-items: center;
    gap: 16px;
    flex: 1;
    position: relative;
    z-index: 1;
  }

  .header-icon-wrapper {
    width: 56px;
    height: 56px;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.2);
    backdrop-filter: blur(10px);
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  }

  .header-text {
    flex: 1;
  }

  .header-title {
    line-height: 1.2;
    letter-spacing: 0.3px;
    margin-bottom: 4px;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }

  .header-subtitle {
    letter-spacing: 0.2px;
  }

  .close-btn {
    position: relative;
    z-index: 1;
    transition: all 0.2s ease;

    &:hover {
      background: rgba(255, 255, 255, 0.15);
      transform: rotate(90deg);
    }
  }
}

// Contenido del formulario
.form-content {
  overflow-y: auto;
  flex: 1;
  background: linear-gradient(to bottom, #ffffff 0%, #fafbfc 100%);

  &::-webkit-scrollbar {
    width: 8px;
  }
  
  &::-webkit-scrollbar-track {
    background: #f5f5f5;
    border-radius: 4px;
  }
  
  &::-webkit-scrollbar-thumb {
    background: #ccc;
    border-radius: 4px;
    
    &:hover {
      background: #aaa;
    }
  }
}

.form-field {
  margin-bottom: 24px;
}

// Labels de campos
.field-label {
  display: flex;
  align-items: center;
  font-size: 14px;
  font-weight: 700;
  color: #2c3e50;
  margin-bottom: 10px;
  letter-spacing: 0.3px;
}

.field-hint {
  display: flex;
  align-items: flex-start;
  margin-top: 8px;
  padding: 8px 12px;
  background: linear-gradient(to right, #f5f7fa 0%, #ffffff 100%);
  border-radius: 8px;
  border-left: 3px solid #1976d2;
  font-size: 12px;
  color: #616161;
  line-height: 1.5;
}

// Inputs personalizados
.custom-input {
  :deep(.q-field__control) {
    border-radius: 10px;
    min-height: 48px;
    background: white;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
    transition: all 0.3s ease;

    &:hover {
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    }
  }

  :deep(.q-field__control):before {
    border-color: #e0e0e0;
  }

  :deep(.q-field--focused) {
    .q-field__control {
      box-shadow: 0 4px 16px rgba(25, 118, 210, 0.15);
    }
  }

  :deep(input),
  :deep(textarea) {
    font-size: 14px;
    font-weight: 500;
    color: #2c3e50;
    padding: 12px 14px !important;
  }

  :deep(.q-field__prepend) {
    padding-left: 14px;
  }

  :deep(.q-field__append) {
    padding-right: 14px;
  }
}

// Sección de notificación
.notification-section {
  background: linear-gradient(135deg, #f8fbff 0%, #f0f7ff 100%);
  border-radius: 14px;
  padding: 18px 20px;
  border: 2px solid #e3f2fd;
  box-shadow: 0 2px 12px rgba(25, 118, 210, 0.08);

  .section-header {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 6px;
  }

  .section-title {
    font-size: 15px;
    font-weight: 700;
    color: #1565c0;
    letter-spacing: 0.3px;
  }

  .section-description {
    font-size: 12px;
    color: #616161;
    margin-bottom: 14px;
    line-height: 1.5;
  }

  .notification-inputs {
    display: flex;
    flex-direction: column;
    gap: 10px;
  }

  .notification-label {
    font-size: 13px;
    font-weight: 600;
    color: #424242;
  }

  .notification-controls {
    display: flex;
    align-items: center;
    gap: 10px;
    flex-wrap: wrap;
  }

  .notification-input {
    flex: 0 0 100px;
    min-width: 80px;

    :deep(.q-field__control) {
      border-radius: 8px;
      min-height: 40px;
      background: white;
    }

    :deep(input) {
      text-align: center;
      font-weight: 600;
      font-size: 16px;
      color: #1976d2;
    }
  }

  .notification-select {
    flex: 1 1 150px;
    min-width: 120px;

    :deep(.q-field__control) {
      border-radius: 8px;
      min-height: 40px;
      background: white;
    }

    :deep(.q-field__native) {
      font-weight: 600;
      color: #424242;
    }
  }

  .notification-suffix {
    font-size: 13px;
    font-weight: 500;
    color: #616161;
    white-space: nowrap;
  }
}

// Selector de usuarios
.users-select {
  :deep(.q-field__control) {
    min-height: 56px;
    padding-top: 8px;
    padding-bottom: 8px;
  }
  
  :deep(.q-chip) {
    margin: 3px;
  }
}

.user-chip {
  font-weight: 600;
  padding: 6px 12px;
  box-shadow: 0 2px 6px rgba(25, 118, 210, 0.2);

  .user-chip-email {
    font-size: 13px;
  }
}

.user-option {
  padding: 12px 16px;
  transition: all 0.2s ease;

  &:hover {
    background: linear-gradient(to right, #e3f2fd 0%, #ffffff 100%);
  }
}

// Dropzone de archivos
.file-dropzone {
  border: 3px dashed #b0bec5;
  border-radius: 14px;
  background: linear-gradient(135deg, #fafbfc 0%, #f5f7fa 100%);
  padding: 32px 24px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  cursor: pointer;
  text-align: center;
  min-height: 140px;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;

  &::before {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(135deg, transparent 0%, rgba(25, 118, 210, 0.03) 100%);
    opacity: 0;
    transition: opacity 0.3s ease;
  }
  
  &:hover {
    border-color: #1976d2;
    background: linear-gradient(135deg, #e3f2fd 0%, #f5f7fa 100%);
    box-shadow: 0 4px 20px rgba(25, 118, 210, 0.12);
    transform: scale(1.01);

    &::before {
      opacity: 1;
    }

    .upload-icon {
      transform: scale(1.1);
    }
  }
  
  &.file-dropzone-active {
    border-color: #1565c0;
    border-width: 3px;
    background: linear-gradient(135deg, #bbdefb 0%, #e3f2fd 100%);
    box-shadow: 0 8px 32px rgba(25, 118, 210, 0.25);
    transform: scale(1.02);

    .upload-icon {
      animation: bounce 0.6s ease infinite;
    }
  }
}

@keyframes bounce {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
}

.dropzone-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  position: relative;
  z-index: 1;
}

.upload-icon {
  margin-bottom: 8px;
  transition: transform 0.3s ease;
}

.upload-text-primary {
  font-size: 15px;
  color: #2c3e50;
  font-weight: 600;
  line-height: 1.5;
}

.upload-text-secondary {
  font-size: 12px;
  color: #757575;
  line-height: 1.4;
}

.upload-badge-wrapper {
  margin-top: 8px;

  .upload-badge {
    font-size: 12px;
    padding: 6px 14px;
    border-radius: 20px;
    font-weight: 700;
    box-shadow: 0 2px 8px rgba(25, 118, 210, 0.25);
  }
}

// Lista de archivos
.files-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  padding: 12px 16px;
  background: linear-gradient(to right, #f0f7ff 0%, #ffffff 100%);
  border-radius: 10px;
  border-left: 4px solid #1976d2;
  box-shadow: 0 2px 8px rgba(25, 118, 210, 0.08);
}

.files-preview-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 14px;
  max-height: 320px;
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
  border: 2px solid #e0e0e0;
  border-radius: 12px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  
  &:hover {
    border-color: #1976d2;
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.12);
    transform: translateY(-4px);
  }
}

.file-card-content {
  display: flex;
  align-items: center;
  padding: 14px;
  gap: 14px;
}

.file-icon-wrapper {
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 52px;
  height: 52px;
  background: linear-gradient(135deg, #f5f7fa 0%, #e8ecf1 100%);
  border-radius: 10px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.06);
}

.file-info {
  flex: 1;
  min-width: 0;
}

.file-name-text {
  font-size: 13px;
  font-weight: 700;
  color: #2c3e50;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  margin-bottom: 6px;
}

.file-size-text {
  font-size: 11px;
  color: #757575;
  font-weight: 500;
}

.file-remove-btn {
  flex-shrink: 0;
  opacity: 0.7;
  transition: all 0.2s ease;
  
  &:hover {
    opacity: 1;
    background: #ffebee !important;
    color: #d32f2f;
  }
}

// Animaciones
.slide-fade-enter-active {
  transition: all 0.3s ease;
}

.slide-fade-leave-active {
  transition: all 0.2s ease;
}

.slide-fade-enter-from {
  transform: translateY(-15px);
  opacity: 0;
}

.slide-fade-leave-to {
  transform: translateY(-15px);
  opacity: 0;
}

.file-item-enter-active,
.file-item-leave-active {
  transition: all 0.3s ease;
}

.file-item-enter-from {
  opacity: 0;
  transform: scale(0.8) rotate(-5deg);
}

.file-item-leave-to {
  opacity: 0;
  transform: scale(0.8) rotate(5deg);
}

.file-item-move {
  transition: transform 0.3s ease;
}

// Información de visibilidad
.visibility-info {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 14px 16px;
  background: linear-gradient(135deg, #f5f5f5 0%, #fafafa 100%);
  border-radius: 10px;
  border-left: 4px solid #1976d2;
  margin-bottom: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);

  .visibility-info-text {
    font-size: 13px;
    color: #424242;
    line-height: 1.6;

    strong {
      font-weight: 700;
      color: #2c3e50;
    }
  }
}

// Tarjetas de visibilidad
.visibility-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 24px 16px;
  border-radius: 14px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  min-height: 140px;
  position: relative;
  overflow: hidden;

  &::before {
    content: '';
    position: absolute;
    inset: 0;
    opacity: 0;
    transition: opacity 0.3s ease;
    z-index: 0;
  }
  
  &:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
  }
  
  &:active {
    transform: translateY(-2px);
  }

  > * {
    position: relative;
    z-index: 1;
  }
}

.visibility-option {
  border: 2px solid #e0e0e0;
  background: white;

  &::before {
    background: linear-gradient(135deg, #f5f5f5 0%, #fafafa 100%);
  }

  &:hover {
    border-color: #1976d2;

    &::before {
      opacity: 1;
    }
  }
}

.visibility-selected {
  background: linear-gradient(135deg, #1e88e5 0%, #1565c0 100%);
  border: 2px solid #1565c0;
  box-shadow: 0 6px 24px rgba(25, 118, 210, 0.35);

  &::before {
    background: linear-gradient(135deg, #2196f3 0%, #1976d2 100%);
  }
  
  &:hover {
    box-shadow: 0 8px 32px rgba(25, 118, 210, 0.45);

    &::before {
      opacity: 1;
    }
  }
}

.visibility-icon-wrapper {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background: rgba(0, 0, 0, 0.05);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 12px;
  transition: all 0.3s ease;

  &.selected {
    background: rgba(255, 255, 255, 0.2);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  }
}

.visibility-title {
  font-size: 16px;
  font-weight: 700;
  letter-spacing: 0.4px;
  margin-top: 4px;
  margin-bottom: 6px;
}

.visibility-subtitle {
  font-size: 12px;
  font-weight: 600;
  opacity: 0.9;
  text-align: center;
  line-height: 1.4;
}

.check-icon {
  position: absolute;
  top: 12px;
  right: 12px;
  animation: checkIn 0.4s ease;
}

@keyframes checkIn {
  0% {
    opacity: 0;
    transform: scale(0) rotate(-45deg);
  }
  50% {
    transform: scale(1.2) rotate(5deg);
  }
  100% {
    opacity: 1;
    transform: scale(1) rotate(0deg);
  }
}

// Editor de descripción
.description-editor {
  border: 2px solid #e0e0e0;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
  transition: all 0.3s ease;
  
  &:focus-within {
    border-color: #1976d2;
    box-shadow: 0 4px 16px rgba(25, 118, 210, 0.12);
  }

  :deep(.q-editor__toolbar) {
    background: linear-gradient(to bottom, #fafbfc 0%, #f5f6f8 100%);
    border-bottom: 2px solid #e4e7eb;
    padding: 8px;
  }
  
  :deep(.q-editor__content) {
    min-height: 6rem;
    max-height: 16rem;
    overflow-y: auto;
    padding: 14px;
    font-size: 14px;
    line-height: 1.7;
    
    p {
      margin-bottom: 0.8em;
    }
    
    ul, ol {
      padding-left: 1.8em;
      margin-bottom: 0.8em;
    }
    
    strong {
      font-weight: 700;
    }
  }
}

// Input de fecha y hora
.date-input,
.time-input {
  :deep(input) {
    cursor: pointer;
    
    &::-webkit-calendar-picker-indicator {
      cursor: pointer;
      padding: 4px;
      opacity: 0.6;
      transition: opacity 0.2s ease;
      
      &:hover {
        opacity: 1;
      }
    }
  }
}

// Botones de acción
.modal-actions {
  background: linear-gradient(to bottom, #fafbfc 0%, #f5f6f8 100%);
  border-top: 2px solid #e4e7eb;
  gap: 12px;
}

.cancel-btn {
  font-weight: 600;
  letter-spacing: 0.3px;
  transition: all 0.2s ease;

  &:hover {
    background: rgba(0, 0, 0, 0.05);
  }
}

.submit-btn {
  background: linear-gradient(135deg, #1e88e5 0%, #1565c0 100%);
  box-shadow: 0 4px 12px rgba(25, 118, 210, 0.3);
  font-weight: 700;
  letter-spacing: 0.5px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(25, 118, 210, 0.4);
  }

  &:active {
    transform: translateY(0px);
  }
}

// Responsive
@media (max-width: 599px) {
  .event-modal {
    border-radius: 16px !important;
  }

  .modal-header {
    .header-icon-wrapper {
      width: 48px;
      height: 48px;

      :deep(.q-icon) {
        font-size: 24px;
      }
    }
  }

  .field-label {
    font-size: 13px;
  }

  .custom-input {
    :deep(.q-field__control) {
      min-height: 44px;
    }

    :deep(input),
    :deep(textarea) {
      font-size: 13px;
    }
  }

  .notification-section {
    padding: 16px;

    .notification-controls {
      flex-direction: column;
      align-items: stretch;
    }

    .notification-input,
    .notification-select {
      flex: 1 1 100%;
    }

    .notification-suffix {
      text-align: center;
    }
  }

  .file-dropzone {
    padding: 24px 16px;
    min-height: 120px;
  }

  .files-preview-grid {
    grid-template-columns: 1fr;
  }

  .visibility-card {
    min-height: 120px;
    padding: 20px 12px;
  }

  .visibility-icon-wrapper {
    width: 52px;
    height: 52px;

    :deep(.q-icon) {
      font-size: 24px;
    }
  }

  .visibility-title {
    font-size: 15px;
  }

  .visibility-subtitle {
    font-size: 11px;
  }

  .modal-actions {
    flex-direction: column;

    .q-btn {
      width: 100%;
    }
  }
}
</style>


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
