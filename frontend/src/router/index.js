import { defineRouter } from '#q-app/wrappers';
import {
  createRouter,
  createMemoryHistory,
  createWebHistory,
  createWebHashHistory,
} from 'vue-router';
import routes from './routes';

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

  // Protege las rutas que requieren autenticación
  Router.beforeEach((to, from, next) => {
    const token = localStorage.getItem('access_token');
    const isAuthenticated = !!token;

    const publicPages = ['auth'];
    const isPublicPage = publicPages.includes(to.name);

    if (isAuthenticated && isPublicPage) {
      next({ name: 'home' });
      return;
    }

    if (!isAuthenticated && !isPublicPage) {
      next({ name: 'auth' });
      return;
    }

    next();
  });

  return Router;
});
