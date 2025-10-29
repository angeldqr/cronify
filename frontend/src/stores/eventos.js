import { defineStore } from 'pinia';
import { eventosService } from '../services/eventosService';

export const useEventosStore = defineStore('eventos', {
  state: () => ({
    eventos: [],
    currentEvento: null,
    loading: false,
    filters: {
      search: '',
      fecha_desde: null,
      fecha_hasta: null,
      creador: null,
      notificacion_enviada: null,
      es_publico: null,
    },
    pagination: {
      page: 1,
      count: 0,
      next: null,
      previous: null,
    },
  }),

  getters: {
    totalEventos: (state) => state.pagination.count,
    hasMore: (state) => !!state.pagination.next,
  },

  actions: {
    async fetchEventos(page = 1) {
      this.loading = true;
      try {
        const params = {
          page,
          ...this.filters,
        };

        // Remover filtros vacíos
        Object.keys(params).forEach(
          (key) => params[key] == null && delete params[key]
        );

        const data = await eventosService.getEventos(params);

        this.eventos = data.results;
        this.pagination = {
          page,
          count: data.count,
          next: data.next,
          previous: data.previous,
        };
      } catch (error) {
        console.error('Error fetching eventos:', error);
        throw error;
      } finally {
        this.loading = false;
      }
    },

    async fetchEvento(id) {
      this.loading = true;
      try {
        const evento = await eventosService.getEvento(id);
        this.currentEvento = evento;
        return evento;
      } catch (error) {
        console.error('Error fetching evento:', error);
        throw error;
      } finally {
        this.loading = false;
      }
    },

    async createEvento(eventoData) {
      this.loading = true;
      try {
        const newEvento = await eventosService.createEvento(eventoData);
        this.eventos.unshift(newEvento);
        return newEvento;
      } catch (error) {
        console.error('Error creating evento:', error);
        throw error;
      } finally {
        this.loading = false;
      }
    },

    async updateEvento(id, eventoData) {
      this.loading = true;
      try {
        const updatedEvento = await eventosService.updateEvento(id, eventoData);

        const index = this.eventos.findIndex((e) => e.id === id);
        if (index !== -1) {
          this.eventos[index] = updatedEvento;
        }

        if (this.currentEvento?.id === id) {
          this.currentEvento = updatedEvento;
        }

        return updatedEvento;
      } catch (error) {
        console.error('Error updating evento:', error);
        throw error;
      } finally {
        this.loading = false;
      }
    },

    async deleteEvento(id) {
      this.loading = true;
      try {
        await eventosService.deleteEvento(id);

        // Remover de la lista local
        this.eventos = this.eventos.filter((e) => e.id !== id);

        if (this.currentEvento?.id === id) {
          this.currentEvento = null;
        }
      } catch (error) {
        console.error('Error deleting evento:', error);
        throw error;
      } finally {
        this.loading = false;
      }
    },

    async searchEventos(searchText) {
      this.filters.search = searchText;
      await this.fetchEventos(1);
    },

    async applyFilters(filters) {
      this.filters = { ...this.filters, ...filters };
      await this.fetchEventos(1);
    },

    clearFilters() {
      this.filters = {
        search: '',
        fecha_desde: null,
        fecha_hasta: null,
        creador: null,
        notificacion_enviada: null,
        es_publico: null,
      };
    },

    async uploadFile(eventoId, file) {
      try {
        const adjunto = await eventosService.uploadFile(eventoId, file);
        return adjunto;
      } catch (error) {
        console.error('Error uploading file:', error);
        throw error;
      }
    },
  },
});
