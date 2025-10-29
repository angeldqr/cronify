import { defineStore } from 'pinia';
import { authService } from '../services/authService';
import { jwtDecode } from 'jwt-decode';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    accessToken: localStorage.getItem('access_token'),
    refreshToken: localStorage.getItem('refresh_token'),
    isAuthenticated: !!localStorage.getItem('access_token'),
  }),

  getters: {
    currentUser: (state) => state.user,
    isLoggedIn: (state) => state.isAuthenticated,
  },

  actions: {
    async register(userData) {
      const data = await authService.register(userData);
      return data;
    },

    async login(credentials) {
      const data = await authService.login(credentials);
      this.accessToken = data.access;
      this.refreshToken = data.refresh;
      this.isAuthenticated = true;

      const decoded = jwtDecode(data.access);
      this.user = {
        id: decoded.user_id,
        email: decoded.email,
      };

      await this.loadProfile();

      return data;
    },

    async loadProfile() {
      try {
        const profile = await authService.getProfile();
        this.user = profile;
      } catch (error) {
        console.error('Error loading profile:', error);
      }
    },

    async updateProfile(profileData) {
      const updatedProfile = await authService.updateProfile(profileData);
      this.user = updatedProfile;
      return updatedProfile;
    },

    async changePassword(passwordData) {
      const data = await authService.changePassword(passwordData);
      return data;
    },

    logout() {
      authService.logout();
      this.user = null;
      this.accessToken = null;
      this.refreshToken = null;
      this.isAuthenticated = false;
    },

    async checkAuth() {
      const token = localStorage.getItem('access_token');
      if (token) {
        try {
          const decoded = jwtDecode(token);
          const now = Date.now() / 1000;

          if (decoded.exp > now) {
            this.isAuthenticated = true;
            this.accessToken = token;
            this.refreshToken = localStorage.getItem('refresh_token');
            await this.loadProfile();
          } else {
            this.logout();
          }
        } catch {
          this.logout();
        }
      }
    },
  },
});
