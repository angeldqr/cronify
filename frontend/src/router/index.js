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

  // Demo mode: Sin autenticación para Vercel
  Router.beforeEach((to, from, next) => {
    // Redirigir de auth a home siempre
    if (to.path.startsWith('/auth')) {
      next({ name: 'home' });
      return;
    }
    next();
  });

  return Router;
});
