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
      {
        path: 'callback',
        name: 'auth-callback',
        component: () => import('pages/auth/LoginPage.vue'),
        meta: { requiresAuth: false },
      },
    ],
  },

  // Rutas principales (demo sin autenticación)
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
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
        path: 'perfil',
        name: 'perfil',
        component: () => import('pages/perfil/PerfilPage.vue'),
      },
      {
        path: 'configuracion',
        name: 'configuracion',
        component: () => import('pages/ConfiguracionPage.vue'),
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
