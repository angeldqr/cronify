// Validadores para formularios

export const isValidEmail = (email) => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
};

export const minLength = (value, min) => {
  return value && value.length >= min;
};

export const maxLength = (value, max) => {
  return value && value.length <= max;
};

export const required = (value) => {
  if (typeof value === 'string') {
    return value.trim().length > 0;
  }
  return value !== null && value !== undefined;
};

export const isFutureDate = (date) => {
  if (!date) return false;
  const selectedDate = new Date(date);
  const now = new Date();
  return selectedDate > now;
};

export const isPositiveNumber = (value) => {
  const num = Number(value);
  return !isNaN(num) && num > 0;
};

export const validateFileSize = (file, maxSizeInMB) => {
  const maxSizeInBytes = maxSizeInMB * 1024 * 1024;
  return file.size <= maxSizeInBytes;
};

export const passwordsMatch = (password, confirmPassword) => {
  return password === confirmPassword;
};

// Reglas de validación para eventos
export const eventoRules = {
  asunto: [
    (v) => required(v) || 'El asunto es requerido',
    (v) => minLength(v, 5) || 'El asunto debe tener al menos 5 caracteres',
    (v) => maxLength(v, 200) || 'El asunto no puede exceder 200 caracteres',
  ],
  fecha_vencimiento: [
    (v) => required(v) || 'La fecha de vencimiento es requerida',
    (v) => isFutureDate(v) || 'La fecha debe ser futura',
  ],
  notificacion_valor: [
    (v) =>
      !v || isPositiveNumber(v) || 'El valor debe ser un número positivo',
  ],
};

// Reglas de validación para registro
export const registerRules = {
  email: [
    (v) => required(v) || 'El email es requerido',
    (v) => isValidEmail(v) || 'Email inválido',
  ],
  username: [
    (v) => required(v) || 'El nombre de usuario es requerido',
    (v) =>
      minLength(v, 3) ||
      'El nombre de usuario debe tener al menos 3 caracteres',
  ],
  password: [
    (v) => required(v) || 'La contraseña es requerida',
    (v) => minLength(v, 8) || 'La contraseña debe tener al menos 8 caracteres',
  ],
};
