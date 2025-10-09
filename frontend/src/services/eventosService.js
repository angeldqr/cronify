import api from './api';

export const eventosService = {
  // Obtiene la lista de eventos con filtros opcionales
  async getEventos(params = {}) {
    const response = await api.get('/eventos/', { params });
    return response.data;
  },

  // Obtiene un evento específico por ID
  async getEvento(id) {
    const response = await api.get(`/eventos/${id}/`);
    return response.data;
  },

  // Crea un nuevo evento
  async createEvento(eventoData) {
    const response = await api.post('/eventos/', eventoData);
    return response.data;
  },

  // Actualiza un evento completo
  async updateEvento(id, eventoData) {
    const response = await api.put(`/eventos/${id}/`, eventoData);
    return response.data;
  },

  // Actualiza campos específicos de un evento
  async patchEvento(id, eventoData) {
    const response = await api.patch(`/eventos/${id}/`, eventoData);
    return response.data;
  },

  // Elimina un evento (soft delete)
  async deleteEvento(id) {
    const response = await api.delete(`/eventos/${id}/`);
    return response.data;
  },

  // Busca eventos con parámetros de búsqueda
  async searchEventos(searchParams) {
    const response = await api.get('/eventos/', { params: searchParams });
    return response.data;
  },

  // Sube un archivo adjunto a un evento
  async uploadFile(eventoId, file) {
    const formData = new FormData();
    formData.append('archivo', file);
    formData.append('evento', eventoId);

    const response = await api.post('/eventos/adjuntos/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  // Obtiene los adjuntos de un evento
  async getAdjuntos(eventoId) {
    const response = await api.get(`/eventos/${eventoId}/adjuntos/`);
    return response.data;
  },

  // Elimina un archivo adjunto
  async deleteAdjunto(adjuntoId) {
    const response = await api.delete(`/eventos/adjuntos/${adjuntoId}/`);
    return response.data;
  },
};
