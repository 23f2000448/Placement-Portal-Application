<template>
  <AdminLayout>
    <h4 class="mb-4">Dashboard</h4>
    <div v-if="loading" class="text-muted">Loading...</div>
    <div v-else class="row g-3">
      <div v-for="card in cards" :key="card.label" class="col-6 col-md-4">
        <div class="card text-center h-100">
          <div class="card-body">
            <h2 :class="card.color">{{ card.value }}</h2>
            <p class="text-muted mb-0 small">{{ card.label }}</p>
          </div>
        </div>
      </div>
    </div>
  </AdminLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import AdminLayout from '@/components/AdminLayout.vue'
import api from '@/services/api'

const loading = ref(true)
const stats = ref({})

const cards = computed(() => [
  { label: 'Students',          value: stats.value.total_students,     color: '' },
  { label: 'Companies',         value: stats.value.total_companies,    color: '' },
  { label: 'Drives',            value: stats.value.total_drives,       color: '' },
  { label: 'Applications',      value: stats.value.total_applications, color: '' },
  { label: 'Pending Companies', value: stats.value.pending_companies,  color: 'text-warning' },
  { label: 'Pending Drives',    value: stats.value.pending_drives,     color: 'text-warning' },
])

onMounted(async () => {
  const res = await api.get('/admin/dashboard')
  stats.value = res.data.data
  loading.value = false
})
</script>