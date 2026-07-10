<template>
  <AdminLayout>
    <h4 class="mb-4">Drives</h4>
    <div class="row g-2 mb-3">
      <div class="col-md-3">
        <select v-model="statusFilter" class="form-select" @change="fetchData">
          <option value="">All</option>
          <option value="pending">Pending</option>
          <option value="approved">Approved</option>
          <option value="rejected">Rejected</option>
          <option value="closed">Closed</option>
        </select>
      </div>
    </div>
    <div v-if="msg" class="alert alert-info alert-dismissible">
      {{ msg }} <button type="button" class="btn-close" @click="msg = ''"></button>
    </div>
    <div class="table-responsive">
      <table class="table table-hover table-sm align-middle">
        <thead class="table-dark">
          <tr>
            <th>Company</th><th>Job Title</th><th>Deadline</th><th>Min CGPA</th><th>Status</th><th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="!drives.length">
            <td colspan="6" class="text-center text-muted">No drives found.</td>
          </tr>
          <tr v-for="d in drives" :key="d.id">
            <td>{{ d.company_name }}</td>
            <td>{{ d.job_title }}</td>
            <td>{{ d.application_deadline?.slice(0, 10) }}</td>
            <td>{{ d.min_cgpa ?? '—' }}</td>
            <td><span :class="`badge bg-${badge(d.status)}`">{{ d.status }}</span></td>
            <td>
              <template v-if="d.status === 'pending'">
                <button class="btn btn-success btn-sm me-1" @click="doAction(d.id, 'approve')">Approve</button>
                <button class="btn btn-danger btn-sm" @click="doAction(d.id, 'reject')">Reject</button>
              </template>
              <template v-else-if="d.status === 'approved'">
                <button class="btn btn-secondary btn-sm" @click="doAction(d.id, 'close')">Close</button>
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

const drives = ref([])
const statusFilter = ref('')
const msg = ref('')

function badge(s) {
  return { pending: 'warning', approved: 'success', rejected: 'danger', closed: 'secondary' }[s] || 'secondary'
}

async function fetchData() {
  const res = await api.get('/admin/drives', { params: { status: statusFilter.value } })
  drives.value = res.data.data
}

async function doAction(id, act) {
  await api.patch(`/admin/drives/${id}/action`, { action: act })
  msg.value = `Drive ${act}d.`
  fetchData()
}

onMounted(fetchData)
</script>