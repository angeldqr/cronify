import api from './api';

export const authService = {
  // Registra un nuevo usuario
  async register(userData) {
    const response = await api.post('/auth/register/', userData);
    return response.data;
  },

  // Autentica al usuario y guarda los tokens
  async login(credentials) {
    const response = await api.post('/token/', credentials);
    const { access, refresh } = response.data;

    localStorage.setItem('access_token', access);
    localStorage.setItem('refresh_token', refresh);

    return response.data;
  },

  // Cierra sesión eliminando los tokens
  logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  },

  // Verifica si hay una sesión activa
  isAuthenticated() {
    return !!localStorage.getItem('access_token');
  },

  // Obtiene el perfil del usuario autenticado
  async getProfile() {
    const response = await api.get('/auth/profile/');
    return response.data;
  },

  // Actualiza el perfil del usuario
  async updateProfile(profileData) {
    const response = await api.put('/auth/profile/', profileData);
    return response.data;
  },

  // Cambia la contraseña del usuario
  async changePassword(passwordData) {
    const response = await api.post('/auth/change-password/', passwordData);
    return response.data;
  },
};
