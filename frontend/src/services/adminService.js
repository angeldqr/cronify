import api from './api';

/**
 * Servicio para gestión de administradores
 * Solo disponible para usuarios con rol de administrador
 */
const adminService = {
  /**
   * Obtiene TODOS los eventos del sistema (públicos, privados, de cualquier usuario)
   * Solo accesible para administradores
   * @param {object} filters - Filtros opcionales (search, fecha_inicio, fecha_fin, creador)
   * @param {number} page - Número de página (por defecto 1)
   */
  async getAllEvents(filters = {}, page = 1) {
    try {
      const params = new URLSearchParams();
      
      // Agregar paginación
      params.append('page', page);
      
      // Agregar filtros opcionales
      if (filters.search) params.append('search', filters.search);
      if (filters.fecha_inicio) params.append('fecha_inicio', filters.fecha_inicio);
      if (filters.fecha_fin) params.append('fecha_fin', filters.fecha_fin);
      if (filters.creador) params.append('creador', filters.creador);
      
      const response = await api.get(`/eventos/admin/all/?${params.toString()}`);
      return response.data;
    } catch (error) {
      console.error('Error al obtener todos los eventos (admin):', error);
      throw error;
    }
  },

  /**
   * Obtiene la lista de todos los usuarios del sistema
   * Incluye información sobre quién es administrador
   */
  async listAllUsers() {
    try {
      const response = await api.get('/auth/admins/');
      return response.data;
    } catch (error) {
      console.error('Error al listar usuarios:', error);
      throw error;
    }
  },

  /**
   * Promueve un usuario a administrador
   * @param {number} userId - ID del usuario a promover
   */
  async promoteToAdmin(userId) {
    try {
      const response = await api.post(`/auth/admins/${userId}/promote/`);
      return response.data;
    } catch (error) {
      console.error('Error al promover usuario a admin:', error);
      throw error;
    }
  },

  /**
   * Remueve privilegios de administrador de un usuario
   * @param {number} userId - ID del usuario a remover como admin
   */
  async removeAdmin(userId) {
    try {
      const response = await api.delete(`/auth/admins/${userId}/demote/`);
      return response.data;
    } catch (error) {
      console.error('Error al remover admin:', error);
      throw error;
    }
  },

  /**
   * Obtiene estadísticas generales del sistema (opcional)
   * Puede incluir: total de usuarios, eventos, admins, etc.
   */
  async getSystemStats() {
    try {
      // Este endpoint se puede implementar después si se necesita
      const [users, events] = await Promise.all([
        this.listAllUsers(),
        this.getAllEvents()
      ]);
      
      return {
        totalUsers: users.length,
        totalAdmins: users.filter(u => u.is_admin).length,
        totalEvents: events.count || events.eventos?.length || 0
      };
    } catch (error) {
      console.error('Error al obtener estadísticas:', error);
      throw error;
    }
  }
};

export default adminService;
