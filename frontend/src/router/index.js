import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  { path: '/login', component: () => import('@/views/LoginView.vue'), meta: { public: true } },
  { path: '/register', component: () => import('@/views/RegisterView.vue'), meta: { public: true } },
  {
    path: '/',
    component: () => import('@/views/LayoutView.vue'),
    children: [
      { path: '', redirect: '/dashboard' },
      { path: 'dashboard', component: () => import('@/views/DashboardView.vue') },
      { path: 'goals/new', component: () => import('@/views/NewGoalView.vue') },
      { path: 'goals/:id', component: () => import('@/views/GoalDetailView.vue') },
      { path: 'goals/:id/drill', component: () => import('@/views/DrillView.vue') },
      { path: 'goals/:id/flashcards', component: () => import('@/views/FlashcardView.vue') },
      { path: 'goals/:id/intuition', component: () => import('@/views/IntuitionView.vue') },
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to) => {
  const token = localStorage.getItem('token')
  if (!to.meta.public && !token) return '/login'
})

export default router
