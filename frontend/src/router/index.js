import { defineRouter } from '#q-app/wrappers';
import {
  createRouter,
  createMemoryHistory,
  createWebHistory,
  createWebHashHistory,
} from 'vue-router';
import routes from './routes';
import { useAuthStore } from 'src/stores/auth';

export default defineRouter(function (/* { store, ssrContext } */) {
  const createHistory = process.env.SERVER
    ? createMemoryHistory
    : process.env.VUE_ROUTER_MODE === 'history'
      ? createWebHistory
      : createWebHashHistory;

  const Router = createRouter({
    scrollBehavior: () => ({ left: 0, top: 0 }),
    routes,
    history: createHistory(process.env.VUE_ROUTER_BASE),
  });

  // Protege las rutas que requieren autenticación y permisos de admin
  Router.beforeEach((to, from, next) => {
    const token = localStorage.getItem('access_token');
    const isAuthenticated = !!token;

    const publicPages = ['auth'];
    const isPublicPage = publicPages.includes(to.name);

    // Verificar autenticación
    if (isAuthenticated && isPublicPage) {
      next({ name: 'home' });
      return;
    }

    if (!isAuthenticated && !isPublicPage) {
      next({ name: 'auth' });
      return;
    }

    // Protección de rutas de administrador
    if (to.meta.requiresAdmin) {
      const authStore = useAuthStore();
      
      if (!authStore.isAdmin) {
        // Redirigir si no es admin
        next({ name: 'home' });
        return;
      }
    }

    next();
  });

  return Router;
});
