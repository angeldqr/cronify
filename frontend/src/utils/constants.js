// Constantes de configuración

export const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';

export const APP_NAME = import.meta.env.VITE_APP_NAME || 'Cronify';

// Unidades de tiempo para notificaciones
export const NOTIFICACION_UNIDADES = [
  { value: 'minutos', label: 'Minutos' },
  { value: 'horas', label: 'Horas' },
  { value: 'dias', label: 'Días' },
  { value: 'semanas', label: 'Semanas' },
];

// Límites para archivos adjuntos
export const MAX_FILE_SIZE = 10 * 1024 * 1024; // 10MB por archivo
export const MAX_TOTAL_SIZE = 50 * 1024 * 1024; // 50MB total por evento

// Paginación
export const DEFAULT_PAGE_SIZE = 20;

// Mensajes del sistema
export const MESSAGES = {
  SUCCESS: {
    EVENTO_CREATED: 'Evento creado correctamente',
    EVENTO_UPDATED: 'Evento actualizado correctamente',
    EVENTO_DELETED: 'Evento eliminado correctamente',
    PROFILE_UPDATED: 'Perfil actualizado correctamente',
    PASSWORD_CHANGED: 'Contraseña cambiada correctamente',
    FILE_UPLOADED: 'Archivo subido correctamente',
  },
  ERROR: {
    GENERIC: 'Ha ocurrido un error. Por favor, intenta de nuevo.',
    NETWORK: 'Error de conexión. Verifica tu conexión a internet.',
    UNAUTHORIZED: 'No tienes autorización para realizar esta acción.',
    EVENTO_NOT_FOUND: 'Evento no encontrado',
    FILE_TOO_LARGE: 'El archivo excede el tamaño máximo permitido',
    INVALID_CREDENTIALS: 'Credenciales inválidas',
  },
  WARNING: {
    UNSAVED_CHANGES: 'Tienes cambios sin guardar. ¿Estás seguro de salir?',
    DELETE_CONFIRM: '¿Estás seguro de eliminar este evento?',
  },
};

// Estados posibles de eventos
export const EVENTO_ESTADOS = {
  PENDIENTE: 'pendiente',
  VENCIDO: 'vencido',
  NOTIFICADO: 'notificado',
};
