<template>
  <div class="auth-container">
    <v-container fluid class="fill-height">
      <v-row justify="center" align="center" class="fill-height">
        <v-col cols="12" sm="8" md="6" lg="5">
          <v-card class="auth-card" elevation="8">
            <!-- Header -->
            <div class="auth-header">
              <v-btn
                icon
                variant="text"
                color="white"
                @click="$router.push('/auth/login')"
                class="back-btn"
              >
                <v-icon>mdi-arrow-left</v-icon>
              </v-btn>
              <div class="logo">
                <span class="logo-icon">🪙</span>
                <span class="logo-text">CoinCraft</span>
              </div>
            </div>

            <!-- Content -->
            <v-card-text class="auth-content">
              <div class="auth-welcome">
                <h1>Join the CoinCraft Adventure! 🌟</h1>
                <p>Let's create your awesome account!</p>
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

              <!-- Registration Form -->
              <v-form
                ref="registerForm"
                v-model="isFormValid"
                @submit.prevent="handleRegister"
                class="auth-form"
              >
                <!-- Full Name -->
                <v-text-field
                  v-model="formData.fullName"
                  label="What's Your Name?"
                  prepend-inner-icon="mdi-account"
                  variant="outlined"
                  :rules="nameRules"
                  :disabled="authStore.isLoading"
                  class="mb-3"
                  color="primary"
                  placeholder="Your awesome name"
                />

                <!-- Email -->
                <v-text-field
                  v-model="formData.email"
                  label="Your Email Address"
                  prepend-inner-icon="mdi-email"
                  variant="outlined"
                  :rules="emailRules"
                  :disabled="authStore.isLoading"
                  class="mb-3"
                  color="primary"
                  placeholder="your.email@example.com"
                />

                <!-- Username -->
                <v-text-field
                  v-model="formData.username"
                  label="Choose a Username"
                  prepend-inner-icon="mdi-at"
                  variant="outlined"
                  :rules="usernameRules"
                  :disabled="authStore.isLoading"
                  class="mb-3"
                  color="primary"
                  placeholder="cooluser123"
                />

                <!-- Role Selection -->
                <v-select
                  v-model="formData.role"
                  label="Who Are You?"
                  prepend-inner-icon="mdi-account-supervisor"
                  variant="outlined"
                  :items="roleOptions"
                  item-title="label"
                  item-value="value"
                  :rules="roleRules"
                  :disabled="authStore.isLoading"
                  class="mb-3"
                  color="primary"
                />

                <!-- Password -->
                <v-text-field
                  v-model="formData.password"
                  :type="showPassword ? 'text' : 'password'"
                  label="Create a Secret Password"
                  prepend-inner-icon="mdi-lock"
                  :append-inner-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
                  @click:append-inner="showPassword = !showPassword"
                  variant="outlined"
                  :rules="passwordRules"
                  :disabled="authStore.isLoading"
                  class="mb-3"
                  color="primary"
                  placeholder="Make it super secret!"
                />

                <!-- Password Strength Indicator -->
                <div v-if="formData.password" class="password-strength mb-4">
                  <div class="strength-bar">
                    <div 
                      class="strength-fill" 
                      :style="{ width: passwordStrength.percentage + '%', backgroundColor: passwordStrength.color }"
                    ></div>
                  </div>
                  <div class="strength-text" :style="{ color: passwordStrength.color }">
                    {{ passwordStrength.text }}
                  </div>
                </div>

                <!-- Terms Agreement -->
                <div class="checkbox-group mb-4">
                  <v-checkbox
                    v-model="agreedToTerms"
                    :rules="termsRules"
                    :disabled="authStore.isLoading"
                    color="primary"
                  >
                    <template #label>
                      <div class="checkbox-text">
                        I agree to have fun and learn about money! 🎉
                      </div>
                    </template>
                  </v-checkbox>
                </div>

                <!-- Submit Button -->
                <v-btn
                  type="submit"
                  color="primary"
                  size="large"
                  block
                  :loading="authStore.isLoading"
                  :disabled="!isFormValid || !agreedToTerms"
                  class="auth-submit mb-4"
                >
                  <v-icon start>mdi-rocket-launch</v-icon>
                  Start My Adventure!
                </v-btn>
              </v-form>

              <!-- Footer -->
              <div class="auth-footer">
                <p>
                  Already have an account?
                  <v-btn
                    variant="text"
                    color="primary"
                    @click="$router.push('/auth/login')"
                    class="pa-0"
                    style="text-decoration: underline;"
                  >
                    Sign In Here!
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
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import type { RegisterData } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

// Form data
const formData = ref<RegisterData>({
  fullName: '',
  email: '',
  username: '',
  role: 'parent',
  password: ''
})

const isFormValid = ref(false)
const showPassword = ref(false)
const agreedToTerms = ref(false)
const registerForm = ref()

// Role options
const roleOptions = [
  { label: '🧑‍💼 I\'m a Parent', value: 'parent' },
  { label: '👩‍🏫 I\'m a Teacher', value: 'teacher' }
]

// Validation rules
const nameRules = [
  (v: string) => !!v || 'Name is required',
  (v: string) => v.length >= 2 || 'Name must be at least 2 characters',
  (v: string) => v.length <= 50 || 'Name must be less than 50 characters'
]

const emailRules = [
  (v: string) => !!v || 'Email is required',
  (v: string) => /.+@.+\..+/.test(v) || 'Email must be valid'
]

const usernameRules = [
  (v: string) => !!v || 'Username is required',
  (v: string) => v.length >= 3 || 'Username must be at least 3 characters',
  (v: string) => v.length <= 20 || 'Username must be less than 20 characters',
  (v: string) => /^[a-zA-Z0-9_]+$/.test(v) || 'Username can only contain letters, numbers, and underscores'
]

const roleRules = [
  (v: string) => !!v || 'Please select your role'
]

const passwordRules = [
  (v: string) => !!v || 'Password is required',
  (v: string) => v.length >= 8 || 'Password must be at least 8 characters',
  (v: string) => /(?=.*[a-z])/.test(v) || 'Password must contain at least one lowercase letter',
  (v: string) => /(?=.*[A-Z])/.test(v) || 'Password must contain at least one uppercase letter',
  (v: string) => /(?=.*\d)/.test(v) || 'Password must contain at least one number'
]

const termsRules = [
  (v: boolean) => !!v || 'You must agree to the terms'
]

// Password strength calculator
const passwordStrength = computed(() => {
  const password = formData.value.password
  if (!password) return { percentage: 0, color: '#ccc', text: '' }

  let score = 0
  let feedback = []

  // Length check
  if (password.length >= 8) score += 25
  else feedback.push('at least 8 characters')

  // Lowercase check
  if (/[a-z]/.test(password)) score += 25
  else feedback.push('lowercase letter')

  // Uppercase check
  if (/[A-Z]/.test(password)) score += 25
  else feedback.push('uppercase letter')

  // Number check
  if (/\d/.test(password)) score += 25
  else feedback.push('number')

  let color = '#f44336' // red
  let text = 'Weak'

  if (score >= 75) {
    color = '#4caf50' // green
    text = 'Strong! 💪'
  } else if (score >= 50) {
    color = '#ff9800' // orange
    text = 'Good! 👍'
  } else if (score >= 25) {
    color = '#ffc107' // yellow
    text = 'Fair 🤔'
  }

  if (feedback.length > 0 && score < 100) {
    text += ` (Need: ${feedback.join(', ')})`
  }

  return { percentage: score, color, text }
})

// Methods
const handleRegister = async () => {
  if (!isFormValid.value || !agreedToTerms.value) return

  try {
    await authStore.register(formData.value)
    
    // Redirect to appropriate dashboard
    const redirectPath = formData.value.role === 'parent' ? '/dashboard/parent' : '/dashboard/teacher'
    router.push(redirectPath)
  } catch (error) {
    // Error is handled by the store
    console.error('Registration failed:', error)
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

.password-strength {
  margin-top: var(--spacing-sm);
}

.strength-bar {
  height: 4px;
  background: #E9ECEF;
  border-radius: 2px;
  overflow: hidden;
  margin-bottom: var(--spacing-xs);
}

.strength-fill {
  height: 100%;
  transition: all 0.3s ease;
}

.strength-text {
  font-size: 0.875rem;
  font-weight: 500;
  font-family: var(--font-primary);
}

.checkbox-group {
  margin-bottom: var(--spacing-xl);
}

.checkbox-text {
  font-family: var(--font-secondary);
  color: var(--medium-gray);
  font-weight: 500;
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
  
  .auth-welcome h1 {
    font-size: 1.5rem;
  }
}
</style>