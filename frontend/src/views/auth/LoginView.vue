<template>
  <div class="login-wrapper">
    <div class="login-header">
      <span class="back-arrow">←</span>
      <span class="logo"><img src="/vite.svg" alt="CoinCraft" /> CoinCraft</span>
    </div>
    <div class="login-content">
      <h2>Welcome Back, Money Hero! <span class="emoji">🦸‍♂️</span></h2>
      <p class="subtitle">Ready to continue your awesome adventure?</p>
      <form @submit.prevent="login">
        <label>Your Username</label>
        <div class="input-group">
          <i class="ri-user-line input-icon"></i>
          <input v-model="username" type="text" required placeholder="your username" />
        </div>
        <label>Your Secret Password</label>
        <div class="input-group">
          <i class="ri-lock-2-line input-icon"></i>
          <input :type="showPassword ? 'text' : 'password'" v-model="password" required placeholder="Enter your password" />
          <i class="input-icon eye" :class="showPassword ? 'ri-eye-off-line' : 'ri-eye-line'" @click="showPassword = !showPassword"></i>
        </div>
        <button class="login-btn" type="submit">�� Let's Go!</button>
      </form>
      <div class="divider"><span>or</span></div>
      <div class="demo-btns">
        <button class="demo-btn kid">🧒 Kid Demo</button>
        <button class="demo-btn parent">👨‍👩‍👧‍👦 Parent Demo</button>
      </div>
      <p class="register-link">New to CoinCraft? <router-link to="/auth/register">Join the fun!</router-link></p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useAuthStore } from '../../stores/auth';
import { useRouter } from 'vue-router';

const username = ref('');
const password = ref('');
const showPassword = ref(false);
const auth = useAuthStore();
const router = useRouter();

function login() {
  auth.login(username.value, password.value).then(() => {
    router.push('/');
  });
}
</script>

<style scoped>
.login-wrapper {
  max-width: 400px;
  margin: 40px auto;
  background: #fff;
  border-radius: 24px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.10);
  overflow: hidden;
}
.login-header {
  display: flex;
  align-items: center;
  gap: 12px;
  background: linear-gradient(90deg, #ff7e5f, #feb47b);
  padding: 1.2rem 1.5rem;
  color: #fff;
  font-size: 1.2rem;
  font-weight: 700;
}
.back-arrow {
  font-size: 1.5rem;
  cursor: pointer;
}
.logo img {
  height: 1.5rem;
  vertical-align: middle;
  margin-right: 0.5rem;
}
.login-content {
  padding: 2rem 2rem 1.5rem 2rem;
  text-align: center;
}
.login-content h2 {
  font-size: 1.5rem;
  font-weight: 800;
  margin-bottom: 0.5rem;
  color: #222;
}
.emoji {
  font-size: 1.5rem;
}
.subtitle {
  color: #888;
  margin-bottom: 1.5rem;
}
label {
  display: block;
  text-align: left;
  margin: 1.2rem 0 0.3rem 0.2rem;
  font-weight: 600;
  color: #333;
}
.input-group {
  position: relative;
  display: flex;
  align-items: center;
  background: #f7f7fa;
  border-radius: 10px;
  margin-bottom: 0.7rem;
  border: 1px solid #eee;
}
.input-group input {
  width: 100%;
  border: none;
  background: transparent;
  outline: none;
  font-size: 1rem;
  padding: 0.7rem 2.2rem 0.7rem 2.2rem;
  border-radius: 10px;
}
.input-icon {
  position: absolute;
  left: 0.8rem;
  font-size: 1.2rem;
  color: #888;
  pointer-events: none;
}
.input-icon.eye {
  left: auto;
  right: 0.8rem;
  cursor: pointer;
  pointer-events: auto;
}
.login-btn {
  width: 100%;
  padding: 0.9rem;
  margin-top: 1.2rem;
  background: linear-gradient(90deg, #ff7e5f, #feb47b);
  color: #fff;
  border: none;
  border-radius: 12px;
  font-size: 1.1rem;
  font-weight: 700;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(255,126,95,0.10);
  transition: background 0.2s;
}
.login-btn:hover {
  background: linear-gradient(90deg, #feb47b, #ff7e5f);
}
.divider {
  display: flex;
  align-items: center;
  margin: 1.5rem 0 1rem 0;
  color: #bbb;
  font-size: 0.95rem;
}
.divider span {
  flex: 1;
  border-bottom: 1px solid #eee;
  margin: 0 0.5rem;
}
.demo-btns {
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin-bottom: 1.2rem;
}
.demo-btn {
  flex: 1;
  padding: 0.7rem 0;
  border: none;
  border-radius: 8px;
  background: #f7f7fa;
  color: #333;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}
.demo-btn.kid {
  background: #fffbe7;
}
.demo-btn.parent {
  background: #e7f7ff;
}
.register-link {
  margin-top: 1.2rem;
  color: #222;
  font-size: 1rem;
}
.register-link a {
  color: #4f46e5;
  text-decoration: underline;
  font-weight: 600;
}
</style>
