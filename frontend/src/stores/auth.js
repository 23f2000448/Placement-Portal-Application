import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('token') || null)
  const user = ref(JSON.parse(localStorage.getItem('user') || 'null'))

  const isAuthenticated = computed(() => !!token.value)
  const role = computed(() => user.value?.role || null)
  const isApproved = computed(() => user.value?.is_approved ?? false)

  function setAuth(accessToken) {
    token.value = accessToken
    const payload = JSON.parse(atob(accessToken.split('.')[1]))
    user.value = {
      id: payload.user_id,
      email: payload.email,
      role: payload.role,
      is_approved: payload.is_approved ?? false,
    }
    localStorage.setItem('token', accessToken)
    localStorage.setItem('user', JSON.stringify(user.value))
  }

  function clearAuth() {
    token.value = null
    user.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('user')
  }

  return { token, user, isAuthenticated, role, isApproved, setAuth, clearAuth }
})