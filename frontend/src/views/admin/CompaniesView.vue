<template>
  <AdminLayout>
    <h4 class="mb-4">Companies</h4>
    <div class="row g-2 mb-3">
      <div class="col-md-5">
        <input v-model="search" class="form-control" placeholder="Search by name or industry" @keyup.enter="fetchData" />
      </div>
      <div class="col-md-3">
        <select v-model="approvalStatus" class="form-select" @change="fetchData">
          <option value="">All</option>
          <option value="pending">Pending</option>
          <option value="approved">Approved</option>
          <option value="rejected">Rejected</option>
          <option value="blacklisted">Blacklisted</option>
        </select>
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
            <th>Name</th><th>Email</th><th>Industry</th><th>Status</th><th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="!companies.length">
            <td colspan="5" class="text-center text-muted">No companies found.</td>
          </tr>
          <tr v-for="c in companies" :key="c.id">
            <td>{{ c.name }}</td>
            <td>{{ c.user?.email }}</td>
            <td>{{ c.industry || '—' }}</td>
            <td><span :class="`badge bg-${badge(c.approval_status)}`">{{ c.approval_status }}</span></td>
            <td>
              <template v-if="c.approval_status === 'pending'">
                <button class="btn btn-success btn-sm me-1" @click="doAction(c.id, 'approve')">Approve</button>
                <button class="btn btn-danger btn-sm" @click="doAction(c.id, 'reject')">Reject</button>
              </template>
              <template v-else-if="c.approval_status === 'approved'">
                <button class="btn btn-warning btn-sm me-1" @click="doAction(c.id, 'blacklist')">Blacklist</button>
                <button class="btn btn-secondary btn-sm" @click="doAction(c.id, 'deactivate')">Deactivate</button>
              </template>
              <template v-else-if="c.approval_status === 'rejected'">
                <button class="btn btn-success btn-sm" @click="doAction(c.id, 'approve')">Approve</button>
              </template>
              <template v-else>
                <button class="btn btn-success btn-sm" @click="doAction(c.id, 'activate')">Activate</button>
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

const companies = ref([])
const search = ref('')
const approvalStatus = ref('')
const msg = ref('')

function badge(s) {
  return { pending: 'warning', approved: 'success', rejected: 'danger', blacklisted: 'dark' }[s] || 'secondary'
}

async function fetchData() {
  const res = await api.get('/admin/companies', { params: { search: search.value, approval_status: approvalStatus.value } })
  companies.value = res.data.data
}

async function doAction(id, act) {
  await api.patch(`/admin/companies/${id}/action`, { action: act })
  msg.value = `Company ${act}d.`
  fetchData()
}

onMounted(fetchData)
</script>