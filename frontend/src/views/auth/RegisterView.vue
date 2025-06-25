<template>
  <div class="register-container">
    <h1>Join <span class="highlight">CoinCraft</span></h1>
    <form @submit.prevent="register">
      <label>Name</label>
      <input v-model="name" type="text" required placeholder="Enter your name" />
      <label>Username</label>
      <input v-model="username" type="text" required placeholder="Choose a username" />
      <!-- <label>Email</label>
      <input v-model="email" type="email" required placeholder="Enter your email" /> -->
      <span class="input-icon">📧</span>
      <input type="email" id="email" placeholder="your.email@example.com" required>
      <label>Password</label>
      <input v-model="password" type="password" required placeholder="Create a password" />
      <label>Register as</label>
      <select v-model="role" required>
        <option value="">Select role</option>
        <option value="parent">Parent</option>
        <option value="teacher">Teacher</option>
      </select>
      <button class="btn btn-large btn-primary auth-submit" type="submit">Register</button>
    </form>
    <p class="login-link">Already have an account? <router-link to="/auth/login">Sign In</router-link></p>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useAuthStore } from '../../stores/auth';
import { useRouter } from 'vue-router';

const name = ref('');
const username = ref('');
const email = ref('');
const password = ref('');
const role = ref('');
const auth = useAuthStore();
const router = useRouter();

function register() {
  auth.register(name.value, username.value, email.value, password.value, role.value).then(() => {
    router.push('/');
  });
}
</script>

<style scoped>
.register-container {
  max-width: 400px;
  margin: 60px auto;
  padding: 2rem;
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 4px 24px rgba(0,0,0,0.08);
  text-align: center;
}

input {
  width: 100%;
  padding: 0.75rem;
  margin: 0.5rem 0 1rem 0;
  border: 1px solid #eee;
  border-radius: 8px;
  font-size: 1rem;
}

.login-link {
  margin-top: 1rem;
}
select {
  width: 100%;
  padding: 0.75rem;
  margin: 0.5rem 0 1rem 0;
  border: 1px solid #eee;
  border-radius: 8px;
  font-size: 1rem;
}
</style> 