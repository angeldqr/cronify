const routes = [
  // Rutas públicas
  {
    path: '/auth',
    component: () => import('layouts/AuthLayout.vue'),
    children: [
      {
        path: '',
        name: 'auth',
        component: () => import('pages/auth/AuthPage.vue'),
        meta: { requiresAuth: false },
      },
      // Rutas antiguas redirigen a la nueva
      {
        path: 'login',
        redirect: '/auth',
      },
      {
        path: 'register',
        redirect: '/auth',
      },
    ],
  },

  // Rutas protegidas
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        name: 'home',
        component: () => import('pages/IndexPage.vue'),
      },
      {
        path: 'eventos',
        name: 'eventos',
        component: () => import('pages/eventos/EventosListPage.vue'),
      },
      {
        path: 'eventos/:id',
        name: 'evento-detail',
        component: () => import('pages/eventos/EventoDetailPage.vue'),
      },
      {
        path: 'calendario',
        name: 'calendario',
        component: () => import('pages/eventos/CalendarioPage.vue'),
      },
      {
        path: 'perfil',
        name: 'perfil',
        component: () => import('pages/perfil/PerfilPage.vue'),
      },
    ],
  },

  // Página de error 404
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue'),
  },
];

export default routes;
