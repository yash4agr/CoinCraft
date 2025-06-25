import { defineStore } from 'pinia';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null as null | { name: string; username: string; email: string; role: string },
    loading: false,
    error: null as null | string,
  }),
  actions: {
    async login(email: string, password: string) {
      this.loading = true;
      this.error = null;
      // Dummy async login logic
      await new Promise((resolve) => setTimeout(resolve, 1000));
      if (email && password) {
        this.user = { name: 'Demo User', username: 'demo', email, role: 'parent' };
      } else {
        this.error = 'Invalid credentials';
      }
      this.loading = false;
    },
    async register(name: string, username: string, email: string, password: string, role: string) {
      this.loading = true;
      this.error = null;
      // Dummy async register logic
      await new Promise((resolve) => setTimeout(resolve, 1000));
      if (name && username && email && password && role) {
        this.user = { name, username, email, role };
      } else {
        this.error = 'Please fill all fields';
      }
      this.loading = false;
    },
    logout() {
      this.user = null;
    },
  },
}); 