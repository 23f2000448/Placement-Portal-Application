<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-4">
        <h3 class="mb-4 text-center">Login</h3>
        <div v-if="error" class="alert alert-danger">{{ error }}</div>
        <form @submit.prevent="submit">
          <div class="mb-3">
            <label class="form-label">Email</label>
            <input v-model="form.email" type="email" class="form-control" required />
          </div>
          <div class="mb-3">
            <label class="form-label">Password</label>
            <input v-model="form.password" type="password" class="form-control" required />
          </div>
          <button class="btn btn-primary w-100" :disabled="loading">
            {{ loading ? 'Logging in...' : 'Login' }}
          </button>
        </form>
        <div class="mt-3 text-center small">
          <RouterLink to="/register/student">Register as Student</RouterLink>
          &nbsp;|&nbsp;
          <RouterLink to="/register/company">Register as Company</RouterLink>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import api from '@/services/api'

const router = useRouter()
const auth = useAuthStore()

const form = ref({ email: '', password: '' })
const error = ref('')
const loading = ref(false)

async function submit() {
  error.value = ''
  loading.value = true
  try {
    const res = await api.post('/auth/login', form.value)
    auth.setAuth(res.data.data.access_token)
    router.push(`/${auth.role}/dashboard`)
  } catch (err) {
    error.value = err.response?.data?.message || 'Login failed.'
  } finally {
    loading.value = false
  }
}
</script>