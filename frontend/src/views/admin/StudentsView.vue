<template>
  <AdminLayout>
    <h4 class="mb-4">Students</h4>
    <div class="row g-2 mb-3">
      <div class="col-md-5">
        <input v-model="search" class="form-control" placeholder="Search by name, roll or email" @keyup.enter="fetchData" />
      </div>
      <div class="col-auto">
        <button class="btn btn-primary" @click="fetchData">Search</button>
      </div>
    </div>
    <div v-if="msg" class="alert alert-info alert-dismissible">
      {{ msg }} <button type="button" class="btn-close" @click="msg = ''"></button>
    </div>
    <div class="table-responsive">
      <table class="table table-hover table-sm align-middle">
        <thead class="table-dark">
          <tr>
            <th>Name</th><th>Email</th><th>Roll No</th><th>Branch</th><th>CGPA</th><th>Status</th><th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="!students.length">
            <td colspan="7" class="text-center text-muted">No students found.</td>
          </tr>
          <tr v-for="s in students" :key="s.id">
            <td>{{ s.full_name }}</td>
            <td>{{ s.user?.email }}</td>
            <td>{{ s.roll_number || '—' }}</td>
            <td>{{ s.branch || '—' }}</td>
            <td>{{ s.cgpa ?? '—' }}</td>
            <td><span :class="`badge bg-${badge(s.status)}`">{{ s.status }}</span></td>
            <td>
              <template v-if="s.status === 'active'">
                <button class="btn btn-warning btn-sm me-1" @click="doAction(s.id, 'blacklist')">Blacklist</button>
                <button class="btn btn-secondary btn-sm" @click="doAction(s.id, 'deactivate')">Deactivate</button>
              </template>
              <template v-else>
                <button class="btn btn-success btn-sm" @click="doAction(s.id, 'activate')">Activate</button>
              </template>
            </td>
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

const students = ref([])
const search = ref('')
const msg = ref('')

function badge(s) {
  return { active: 'success', inactive: 'secondary', blacklisted: 'dark' }[s] || 'secondary'
}

async function fetchData() {
  const res = await api.get('/admin/students', { params: { search: search.value } })
  students.value = res.data.data
}

async function doAction(id, act) {
  await api.patch(`/admin/students/${id}/action`, { action: act })
  msg.value = `Student ${act}d.`
  fetchData()
}

onMounted(fetchData)
</script>