import { createRouter, createWebHistory } from "vue-router";
import { useAuthStore } from "@/stores/auth";

const PlaceholderView = { template: "<div>placeholder</div>" };

const routes = [
  {
    path: "/",
    name: "home",
    redirect: "/login",
  },

  {
    path: "/login",
    name: "login",
    component: PlaceholderView,
    meta: { requiresAuth: false },
  },
  {
    path: "/register/student",
    name: "register-student",
    component: PlaceholderView,
    meta: { requiresAuth: false },
  },
  {
    path: "/register/company",
    name: "register-company",
    component: PlaceholderView,
    meta: { requiresAuth: false },
  },

  {
    path: "/admin/dashboard",
    name: "admin-dashboard",
    component: PlaceholderView,
    meta: { requiresAuth: true, role: "admin" },
  },

  {
    path: "/company/dashboard",
    name: "company-dashboard",
    component: PlaceholderView,
    meta: { requiresAuth: true, role: "company", requiresApproval: true },
  },
  {
    path: "/company/pending",
    name: "company-pending",
    component: PlaceholderView,
    meta: { requiresAuth: true, role: "company" },
  },

  {
    path: "/student/dashboard",
    name: "student-dashboard",
    component: PlaceholderView,
    meta: { requiresAuth: true, role: "student" },
  },

  {
    path: "/:pathMatch(.*)*",
    name: "not-found",
    component: PlaceholderView,
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

function getDashboardPath(role) {
  if (role === "admin") return "/admin/dashboard";
  if (role === "company") return "/company/dashboard";
  if (role === "student") return "/student/dashboard";
  return "/login";
}

router.beforeEach((to) => {
  const authStore = useAuthStore();
  const { isAuthenticated, user } = authStore;

  const requiresAuth = to.meta.requiresAuth;
  const requiredRole = to.meta.role;
  const requiresApproval = to.meta.requiresApproval;

  if (!requiresAuth) {
    if (isAuthenticated && to.name === "login") {
      return getDashboardPath(user.role);
    }
    return true;
  }

  if (!isAuthenticated) {
    return { path: "/login", query: { redirect: to.fullPath } };
  }

  if (requiredRole && user.role !== requiredRole) {
    return getDashboardPath(user.role);
  }

  if (requiresApproval) {
    const token = authStore.token;
    let isApproved = false;

    try {
      const payload = JSON.parse(atob(token.split(".")[1]));
      isApproved = payload.is_approved === true;
    } catch {
      return "/login";
    }

    if (!isApproved) {
      return "/company/pending";
    }
  }

  return true;
});

export default router;
