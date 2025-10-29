import axios from 'axios';

// Instancia de Axios con configuración base
const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Añade el token JWT a cada petición
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Maneja errores de autenticación y refresca el token si es necesario
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    // Error de red (sin conexión)
    if (!error.response) {
      console.error('Error de red: Sin conexión al servidor');
      // Puedes mostrar una notificación aquí si tienes acceso a Quasar
      return Promise.reject({
        message: 'No se pudo conectar al servidor. Verifica tu conexión a internet.',
        isNetworkError: true
      });
    }

    // Error 500 del servidor
    if (error.response?.status >= 500) {
      console.error('Error del servidor:', error.response.status);
      return Promise.reject({
        message: 'Error del servidor. Por favor intenta más tarde.',
        isServerError: true,
        status: error.response.status
      });
    }

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refreshToken = localStorage.getItem('refresh_token');
        if (refreshToken) {
          const response = await axios.post(
            `${import.meta.env.VITE_API_BASE_URL}/token/refresh/`,
            {
              refresh: refreshToken,
            }
          );

          const { access } = response.data;
          localStorage.setItem('access_token', access);

          originalRequest.headers.Authorization = `Bearer ${access}`;
          return api(originalRequest);
        }
      } catch (refreshError) {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        window.location.href = '/auth';
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

export default api;
