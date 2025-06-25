<template>
  <div class="auth-container">
    <div class="auth-card">
      <div class="auth-header">
        <button class="back-btn" @click="$router.back()">
          <span>←</span>
        </button>
        <div class="auth-logo">
          <span class="logo-icon">🪙</span>
          <span class="logo-text">CoinCraft</span>
        </div>
      </div>
      <div class="auth-content">
        <div class="auth-welcome">
          <h1>Join the CoinCraft Adventure! <span style="font-size:1.2em;">🌟</span></h1>
          <p>Let's create your awesome account!</p>
        </div>
        <form class="auth-form" @submit.prevent="register">
          <div class="form-group">
            <label>What's Your Name?</label>
            <div class="input-wrapper">
              <span class="input-icon">👤</span>
              <input v-model="name" type="text" required placeholder="Your awesome name" />
            </div>
          </div>
          <div class="form-group">
            <label>Your Username</label>
            <div class="input-wrapper">
              <span class="input-icon">@</span>
              <input v-model="username" type="text" required placeholder="Pick a username" />
            </div>
          </div>
          <div class="form-group">
            <label>Your Email Address</label>
            <div class="input-wrapper">
              <span class="input-icon">📧</span>
              <input v-model="email" type="email" required placeholder="your.email@example.com" />
            </div>
          </div>
          <div class="form-group">
            <label>Register as</label>
            <div class="input-wrapper">
              <span class="input-icon">⭐</span>
              <select v-model="role" required>
                <option value="" disabled>Select role</option>
                <option value="parent">Parent</option>
                <option value="teacher">Teacher</option>
              </select>
            </div>
          </div>
          <div class="form-group">
            <label>Create a Secret Password</label>
            <div class="input-wrapper">
              <span class="input-icon">🔒</span>
              <input :type="showPassword ? 'text' : 'password'" v-model="password" required placeholder="Make it super secret!" />
              <button type="button" class="password-toggle" @click="showPassword = !showPassword">
                <span>{{ showPassword ? '🙈' : '👁️' }}</span>
              </button>
            </div>
            <div class="password-strength">
              <div class="strength-bar">
                <div class="strength-fill" :style="{ width: passwordStrength + '%' }"></div>
              </div>
              <span class="strength-text">Make it strong! 💪</span>
            </div>
          </div>
          <div class="form-group checkbox-group">
            <label class="checkbox-label">
              <input type="checkbox" v-model="agree" required />
              <span class="checkmark">✓</span>
              <span class="checkbox-text">I agree to have fun and learn about money! 🎉</span>
            </label>
          </div>
          <button class="btn btn-large btn-primary auth-submit" type="submit">
            <span class="btn-icon">🚀</span>
            Start My Adventure!
          </button>
        </form>
        <div class="auth-footer">
          <p>Already have an account? <router-link class="link-btn" to="/auth/login">Sign in here!</router-link></p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { useAuthStore } from '../../stores/auth';
import { useRouter } from 'vue-router';

const name = ref('');
const username = ref('');
const email = ref('');
const password = ref('');
const role = ref('');
const agree = ref(false);
const showPassword = ref(false);
const auth = useAuthStore();
const router = useRouter();

const passwordStrength = computed(() => {
  if (!password.value) return 0;
  let score = 0;
  if (password.value.length >= 8) score += 40;
  if (/[A-Z]/.test(password.value)) score += 20;
  if (/[0-9]/.test(password.value)) score += 20;
  if (/[^A-Za-z0-9]/.test(password.value)) score += 20;
  return Math.min(score, 100);
});

function register() {
  if (!agree.value) return;
  auth.register(name.value, username.value, email.value, password.value, role.value).then(() => {
    router.push('/');
  });
}
</script>

<style scoped>
.auth-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f0f0f0;
}

.auth-card {
  background-color: #fff;
  padding: 2rem;
  border-radius: 16px;
  box-shadow: 0 4px 24px rgba(0,0,0,0.08);
  width: 100%;
  max-width: 480px;
  max-height: 90vh;
  overflow-y: auto;
}

.auth-header {
  display: flex;
  align-items: center;
  margin-bottom: 1rem;
}

.back-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  color: #888;
  cursor: pointer;
}

.auth-logo {
  display: flex;
  align-items: center;
  margin-left: 1rem;
}

.logo-icon {
  font-size: 1.5rem;
  margin-right: 0.5rem;
}

.logo-text {
  font-size: 1.5rem;
  font-weight: bold;
}

.auth-content {
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.auth-welcome {
  margin-bottom: 1rem;
}

.auth-welcome h1 {
  font-size: 2rem;
  margin-bottom: 0.5rem;
}

.auth-welcome p {
  font-size: 1rem;
  color: #888;
}

.auth-form {
  margin-bottom: 1rem;
  width: 100%;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: bold;
}

.input-wrapper {
  position: relative;
}

.input-icon {
  position: absolute;
  left: 1rem;
  top: 50%;
  transform: translateY(-50%);
  color: #888;
}

input {
  width: 100%;
  padding: 0.75rem;
  margin: 0.5rem 0 1rem 0;
  border: 1px solid #eee;
  border-radius: 8px;
  font-size: 1rem;
}

select {
  width: 100%;
  padding: 0.75rem;
  margin: 0.5rem 0 1rem 0;
  border: 1px solid #eee;
  border-radius: 8px;
  font-size: 1rem;
}

.checkbox-group {
  margin-bottom: 1rem;
}

.checkbox-label {
  display: flex;
  align-items: center;
  margin-bottom: 0.5rem;
}

.checkbox-label input {
  margin-right: 0.5rem;
}

.checkbox-text {
  color: #888;
}

.auth-submit {
  width: 100%;
  padding: 0.75rem;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: bold;
  color: #fff;
  background-color: #007bff;
  cursor: pointer;
}

.auth-footer {
  margin-top: 1rem;
}

.auth-footer a {
  color: #007bff;
  text-decoration: none;
}
</style> 