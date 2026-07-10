import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const routes = [
  { path: '/', redirect: '/login' },

  { path: '/login', component: () => import('@/views/auth/LoginView.vue'), meta: { guest: true } },
  { path: '/register/student', component: () => import('@/views/auth/StudentRegisterView.vue'), meta: { guest: true } },
  { path: '/register/company', component: () => import('@/views/auth/CompanyRegisterView.vue'), meta: { guest: true } },

  {
    path: '/admin',
    meta: { requiresAuth: true, role: 'admin' },
    children: [
      { path: '', redirect: '/admin/dashboard' },
      { path: 'dashboard', component: () => import('@/views/admin/DashboardView.vue') },
      { path: 'companies', component: () => import('@/views/admin/CompaniesView.vue') },
      { path: 'students', component: () => import('@/views/admin/StudentsView.vue') },
      { path: 'drives', component: () => import('@/views/admin/DrivesView.vue') },
      { path: 'applications', component: () => import('@/views/admin/ApplicationsView.vue') },
    ]
  },

  {
    path: '/company',
    meta: { requiresAuth: true, role: 'company' },
    children: [
      { path: '', redirect: '/company/dashboard' },
      { path: 'dashboard', component: () => import('@/views/company/DashboardView.vue') },
      { path: 'profile', component: () => import('@/views/company/ProfileView.vue') },
      { path: 'drives', component: () => import('@/views/company/DrivesView.vue') },
      { path: 'applications', component: () => import('@/views/company/ApplicationsView.vue') },
    ]
  },

  {
    path: '/student',
    meta: { requiresAuth: true, role: 'student' },
    children: [
      { path: '', redirect: '/student/dashboard' },
      { path: 'dashboard', component: () => import('@/views/student/DashboardView.vue') },
      { path: 'profile', component: () => import('@/views/student/ProfileView.vue') },
      { path: 'applications', component: () => import('@/views/student/ApplicationsView.vue') },
      { path: 'placements', component: () => import('@/views/student/PlacementsView.vue') },
    ]
  },

  { path: '/:pathMatch(.*)*', component: () => import('@/views/NotFoundView.vue') }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const auth = useAuthStore()

  if (to.meta.requiresAuth && !auth.isAuthenticated) return next('/login')
  if (to.meta.guest && auth.isAuthenticated) return next(`/${auth.role}/dashboard`)
  if (to.meta.role && auth.role !== to.meta.role) {
    return auth.isAuthenticated ? next(`/${auth.role}/dashboard`) : next('/login')
  }

  next()
})

export default router