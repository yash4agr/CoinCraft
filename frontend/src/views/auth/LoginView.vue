<template>
  <div class="auth-container">
    <v-container fluid class="fill-height">
      <v-row justify="center" align="center" class="fill-height">
        <v-col cols="12" sm="8" md="6" lg="4">
          <v-card class="auth-card" elevation="8">
            <!-- Header -->
            <div class="auth-header">
              <v-btn
                icon
                variant="text"
                color="white"
                @click="$router.push('/')"
                class="back-btn"
              >
                <v-icon>mdi-arrow-left</v-icon>
              </v-btn>
              <div class="logo">
                <img src="/coin.svg" class="logo-icon" alt="coin">
                <span class="logo-text">CoinCraft</span>
              </div>
            </div>

            <!-- Content -->
            <v-card-text class="auth-content">
              <div class="auth-welcome">
                <h1>Welcome Back! 👋</h1>
                <p>Sign in to continue your money learning adventure!</p>
              </div>

              <!-- Error Alert -->
              <v-alert
                v-if="authStore.error"
                type="error"
                variant="tonal"
                closable
                @click:close="authStore.clearError()"
                class="mb-4"
              >
                {{ authStore.error }}
              </v-alert>

              <!-- Login Form -->
              <v-form
                ref="loginForm"
                v-model="isFormValid"
                @submit.prevent="handleLogin"
                class="auth-form"
              >
                <v-text-field
                  v-model="credentials.username"
                  label="Username"
                  prepend-inner-icon="mdi-account"
                  variant="outlined"
                  :rules="usernameRules"
                  :disabled="authStore.isLoading"
                  class="mb-3"
                  color="primary"
                />

                <v-text-field
                  v-model="credentials.password"
                  :type="showPassword ? 'text' : 'password'"
                  label="Password"
                  prepend-inner-icon="mdi-lock"
                  :append-inner-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
                  @click:append-inner="showPassword = !showPassword"
                  variant="outlined"
                  :rules="passwordRules"
                  :disabled="authStore.isLoading"
                  class="mb-4"
                  color="primary"
                />

                <v-btn
                  type="submit"
                  color="primary"
                  size="large"
                  block
                  :loading="authStore.isLoading"
                  :disabled="!isFormValid"
                  class="auth-submit mb-4"
                >
                  <v-icon start>mdi-login</v-icon>
                  Sign In
                </v-btn>
              </v-form>

              <!-- Demo Login Section -->
              <div class="demo-section">
                <v-divider class="mb-4">
                  <span class="text-medium-emphasis px-4">Try Demo Accounts</span>
                </v-divider>
                
                <div class="demo-text mb-3">
                  <v-icon color="info" class="me-2">mdi-information</v-icon>
                  Quick access to explore different user experiences
                </div>

                <div class="demo-buttons">
                  <v-btn
                    variant="outlined"
                    color="secondary"
                    size="small"
                    @click="handleDemoLogin('younger_child')"
                    :loading="authStore.isLoading"
                    class="demo-btn"
                  >
                    <v-icon start>mdi-emoticon-happy</v-icon>
                    Younger Child
                  </v-btn>

                  <v-btn
                    variant="outlined"
                    color="secondary"
                    size="small"
                    @click="handleDemoLogin('older_child')"
                    :loading="authStore.isLoading"
                    class="demo-btn"
                  >
                    <v-icon start>mdi-school</v-icon>
                    Older Child
                  </v-btn>

                  <v-btn
                    variant="outlined"
                    color="secondary"
                    size="small"
                    @click="handleDemoLogin('parent')"
                    :loading="authStore.isLoading"
                    class="demo-btn"
                  >
                    <v-icon start>mdi-account-supervisor</v-icon>
                    Parent
                  </v-btn>

                  <v-btn
                    variant="outlined"
                    color="secondary"
                    size="small"
                    @click="handleDemoLogin('teacher')"
                    :loading="authStore.isLoading"
                    class="demo-btn"
                  >
                    <v-icon start>mdi-human-male-board</v-icon>
                    Teacher
                  </v-btn>
                </div>
              </div>

              <!-- Footer -->
              <div class="auth-footer">
                <p>
                  Don't have an account?
                  <v-btn
                    variant="text"
                    color="primary"
                    @click="$router.push('/auth/register')"
                    class="pa-0"
                    style="text-decoration: underline;"
                  >
                    Join the Fun!
                  </v-btn>
                </p>
              </div>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import type { LoginCredentials, User } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

// Form data
const credentials = ref<LoginCredentials>({
  username: '',
  password: ''
})

const isFormValid = ref(false)
const showPassword = ref(false)
const loginForm = ref()

// Validation rules
const usernameRules = [
  (v: string) => !!v || 'Username is required',
  (v: string) => v.length >= 3 || 'Username must be at least 3 characters'
]

const passwordRules = [
  (v: string) => !!v || 'Password is required',
  (v: string) => v.length >= 6 || 'Password must be at least 6 characters'
]

// Methods
const handleLogin = async () => {
  if (!isFormValid.value) return

  try {
    await authStore.login(credentials.value)
    
    // Redirect based on user role
    const redirectPath = getRedirectPath(authStore.user?.role)
    router.push(redirectPath)
  } catch (error) {
    // Error is handled by the store
    console.error('Login failed:', error)
  }
}

const handleDemoLogin = async (role: User['role']) => {
  try {
    await authStore.demoLogin(role)
    
    // Redirect based on user role
    const redirectPath = getRedirectPath(role)
    router.push(redirectPath)
  } catch (error) {
    console.error('Demo login failed:', error)
  }
}

const getRedirectPath = (role?: User['role']) => {
  switch (role) {
    case 'younger_child':
      return '/child/dashboard'
    case 'older_child':
      return '/teen/dashboard'
    case 'parent':
      return '/parent/dashboard'
    case 'teacher':
      return '/teacher/dashboard'
    default:
      return '/'
  }
}

onMounted(() => {
  // Clear any previous errors
  authStore.clearError()
})
</script>

<style scoped>
.auth-container {
  min-height: 100vh;
  background: var(--gradient-background);
}

.auth-card {
  border-radius: var(--radius-xl) !important;
  overflow: hidden;
  animation: slideInUp 0.6s ease-out;
}

.auth-header {
  background: var(--gradient-primary);
  padding: var(--spacing-lg);
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
}

.back-btn {
  background: rgba(255, 255, 255, 0.2) !important;
}

.back-btn:hover {
  background: rgba(255, 255, 255, 0.3) !important;
  transform: translateX(-2px);
}

.logo {
  color: var(--white);
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  font-size: 1.5rem;
  font-weight: 700;
  font-family: var(--font-primary);
}

.logo-icon {
  font-size: 2rem;
}

.auth-content {
  padding: var(--spacing-xl) !important;
}

.auth-welcome {
  text-align: center;
  margin-bottom: var(--spacing-xl);
}

.auth-welcome h1 {
  font-size: 1.75rem;
  font-weight: 700;
  margin-bottom: var(--spacing-sm);
  color: var(--dark-gray);
  font-family: var(--font-primary);
}

.auth-welcome p {
  color: var(--medium-gray);
  font-family: var(--font-secondary);
}

.demo-section {
  text-align: center;
  margin-bottom: var(--spacing-xl);
}

.demo-text {
  color: var(--medium-gray);
  font-family: var(--font-secondary);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.9rem;
}

.demo-buttons {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--spacing-sm);
}

.demo-btn {
  font-family: var(--font-primary) !important;
  font-weight: 600 !important;
}

.auth-footer {
  text-align: center;
  color: var(--medium-gray);
  font-family: var(--font-secondary);
}

@keyframes slideInUp {
  from { 
    opacity: 0; 
    transform: translateY(50px); 
  }
  to { 
    opacity: 1; 
    transform: translateY(0); 
  }
}

@media (max-width: 600px) {
  .auth-content {
    padding: var(--spacing-lg) !important;
  }
  
  .demo-buttons {
    grid-template-columns: 1fr;
  }
}
</style>