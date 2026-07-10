<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
    <div class="container-fluid px-4">
      <RouterLink class="navbar-brand fw-bold" to="/">
        <i class="bi bi-mortarboard-fill me-2"></i>Placement Portal
      </RouterLink>
      <div class="d-flex align-items-center">
        <template v-if="auth.isAuthenticated">
          <span class="text-white opacity-75 me-3 small d-none d-sm-inline">{{ auth.user?.email }}</span>
          <span class="badge bg-warning text-dark me-3 text-capitalize">{{ auth.role }}</span>
          <button class="btn btn-outline-light btn-sm" @click="logout">
            <i class="bi bi-box-arrow-right me-1"></i>Logout
          </button>
        </template>
        <template v-else>
          <RouterLink class="btn btn-outline-light btn-sm" to="/login">Login</RouterLink>
        </template>
      </div>
    </div>
  </nav>
  <RouterView />
</template>

<script setup>
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const auth = useAuthStore()
const router = useRouter()

function logout() {
  auth.clearAuth()
  router.push('/login')
}
</script>