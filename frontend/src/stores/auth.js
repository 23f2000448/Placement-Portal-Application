import { defineStore } from "pinia";
import api from "@/services/api";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    token: null,
    user: null,
    isAuthenticated: false,
  }),

  getters: {
    isAdmin: (state) => state.user?.role === "admin",
    isCompany: (state) => state.user?.role === "company",
    isStudent: (state) => state.user?.role === "student",
  },

  actions: {
    async login(credentials) {
      const response = await api.post("/auth/login", credentials);
      const { access_token, role } = response.data.data;

      const payload = JSON.parse(atob(access_token.split(".")[1]));

      const user = {
        id: payload.user_id,
        role: role,
        email: payload.email,
      };

      this.token = access_token;
      this.user = user;
      this.isAuthenticated = true;

      localStorage.setItem("token", access_token);
      localStorage.setItem("user", JSON.stringify(user));
    },

    logout() {
      this.token = null;
      this.user = null;
      this.isAuthenticated = false;

      localStorage.removeItem("token");
      localStorage.removeItem("user");
    },

    initAuth() {
      const token = localStorage.getItem("token");
      const user = localStorage.getItem("user");

      if (token && user) {
        this.token = token;
        this.user = JSON.parse(user);
        this.isAuthenticated = true;
      }
    },
  },
});
