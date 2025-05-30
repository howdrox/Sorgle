import type { RouteRecordRaw } from 'vue-router';

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    component: () => import('layouts/MinimalLayout.vue'),
    children: [{ path: '', name: 'home', component: () => import('pages/HomePage.vue') }],
  },
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: 'results', name: 'resutls', component: () => import('pages/ResultsPage.vue') },
      { path: 'profile/:id', name: 'profile', component: () => import('pages/ProfilePage.vue') },
      { path: 'easteregg', name: 'easteregg', component: () => import('pages/EasterEggPage.vue') },
      { path: 'info', name: 'info', component: () => import('pages/InfoPage.vue') },
    ],
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue'),
  },
];

export default routes;
