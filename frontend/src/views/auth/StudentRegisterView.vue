<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-4">
        <h3 class="mb-4 text-center">Student Register</h3>
        <div v-if="error" class="alert alert-danger">{{ error }}</div>
        <div v-if="success" class="alert alert-success">{{ success }}</div>
        <form @submit.prevent="submit">
          <div class="mb-3">
            <label class="form-label">Full Name</label>
            <input v-model="form.full_name" type="text" class="form-control" required />
          </div>
          <div class="mb-3">
            <label class="form-label">Email</label>
            <input v-model="form.email" type="email" class="form-control" required />
          </div>
          <div class="mb-3">
            <label class="form-label">Password</label>
            <input v-model="form.password" type="password" class="form-control" required />
          </div>
          <button class="btn btn-primary w-100" :disabled="loading">
            {{ loading ? 'Registering...' : 'Register' }}
          </button>
        </form>
        <div class="mt-3 text-center small">
          Already have an account? <RouterLink to="/login">Login</RouterLink>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import api from '@/services/api'

const form = ref({ full_name: '', email: '', password: '' })
const error = ref('')
const success = ref('')
const loading = ref(false)

async function submit() {
  error.value = ''
  success.value = ''
  loading.value = true
  try {
    await api.post('/auth/register/student', form.value)
    success.value = 'Registered successfully! You can now login.'
    form.value = { full_name: '', email: '', password: '' }
  } catch (err) {
    error.value = err.response?.data?.message || 'Registration failed.'
  } finally {
    loading.value = false
  }
}
</script>