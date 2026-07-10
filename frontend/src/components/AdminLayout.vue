<template>
  <div class="d-flex">
    <nav class="bg-dark" style="min-width: 210px; min-height: calc(100vh - 56px);">
      <ul class="nav flex-column pt-2">
        <li v-for="link in links" :key="link.to" class="nav-item">
          <RouterLink :to="link.to" class="nav-link text-white-50" active-class="text-white fw-semibold">
            <i :class="`bi ${link.icon} me-2`"></i>{{ link.label }}
          </RouterLink>
        </li>
      </ul>
    </nav>
    <main class="flex-grow-1 p-4">
      <slot />
    </main>
  </div>
</template>

<script setup>
const links = [
  { to: '/admin/dashboard',    icon: 'bi-speedometer2',      label: 'Dashboard'    },
  { to: '/admin/companies',    icon: 'bi-building',          label: 'Companies'    },
  { to: '/admin/students',     icon: 'bi-people',            label: 'Students'     },
  { to: '/admin/drives',       icon: 'bi-briefcase',         label: 'Drives'       },
  { to: '/admin/applications', icon: 'bi-file-earmark-text', label: 'Applications' },
]
</script>