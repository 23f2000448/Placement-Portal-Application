<template>
  <AdminLayout>
    <h4 class="mb-4">All Applications</h4>
    <div class="table-responsive">
      <table class="table table-hover table-sm align-middle">
        <thead class="table-dark">
          <tr>
            <th>Student</th><th>Roll No</th><th>Company</th><th>Drive</th><th>Status</th><th>Applied At</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="!apps.length">
            <td colspan="6" class="text-center text-muted">No applications yet.</td>
          </tr>
          <tr v-for="a in apps" :key="a.id">
            <td>{{ a.student_name }}</td>
            <td>{{ a.student_roll || '—' }}</td>
            <td>{{ a.company_name }}</td>
            <td>{{ a.drive_title }}</td>
            <td><span :class="`badge bg-${badge(a.status)}`">{{ a.status }}</span></td>
            <td>{{ a.applied_at?.slice(0, 10) }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </AdminLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import AdminLayout from '@/components/AdminLayout.vue'
import api from '@/services/api'

const apps = ref([])

function badge(s) {
  return { applied: 'primary', shortlisted: 'info', selected: 'success', rejected: 'danger' }[s] || 'secondary'
}

onMounted(async () => {
  const res = await api.get('/admin/applications')
  apps.value = res.data.data
})
</script>