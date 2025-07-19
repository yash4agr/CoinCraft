<template>
  <div class="child-dashboard">
    <v-app-bar color="primary" dark>
      <v-app-bar-title>
        <div class="logo">
          <img src="/coin.svg" class="logo-icon" alt="coin">
          <span>CoinCraft</span>
        </div>
      </v-app-bar-title>
      
      <v-spacer />
      
      <div class="user-info">
        <span class="user-avatar">{{ authStore.user?.avatar }}</span>
        <span class="user-name">Hi {{ authStore.user?.fullName?.split(' ')[0] }}!</span>
        <v-chip color="warning" variant="elevated" class="coins-chip">
          <v-icon start>mdi-coin</v-icon>
          {{ authStore.user?.coins || 0 }}
        </v-chip>
      </div>
      
      <v-btn icon @click="handleLogout">
        <v-icon>mdi-logout</v-icon>
      </v-btn>
    </v-app-bar>

    <v-main>
      <v-container>
        <v-row>
          <v-col cols="12">
            <h1 class="text-h4 mb-4">Welcome to Your Dashboard! 🎮</h1>
            
            <v-alert type="info" variant="tonal" class="mb-4">
              <v-icon start>mdi-information</v-icon>
              This is a demo dashboard for {{ authStore.user?.role === 'younger_child' ? 'younger children' : 'older children' }}. 
              Full features coming soon!
            </v-alert>
            
            <v-row>
              <v-col cols="12" md="6">
                <v-card>
                  <v-card-title>
                    <v-icon start color="primary">mdi-gamepad-variant</v-icon>
                    Activity Hub
                  </v-card-title>
                  <v-card-text>
                    Play fun games and earn coins!
                  </v-card-text>
                  <v-card-actions>
                    <v-btn color="primary" variant="elevated">
                      Start Playing
                    </v-btn>
                  </v-card-actions>
                </v-card>
              </v-col>
              
              <v-col cols="12" md="6">
                <v-card>
                  <v-card-title>
                    <v-icon start color="orange">mdi-piggy-bank</v-icon>
                    My Piggy Bank
                  </v-card-title>
                  <v-card-text>
                    Check your savings and goals
                  </v-card-text>
                  <v-card-actions>
                    <v-btn color="orange" variant="elevated">
                      View Savings
                    </v-btn>
                  </v-card-actions>
                </v-card>
              </v-col>
            </v-row>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const handleLogout = async () => {
  try {
    await authStore.logout()
    router.push('/')
  } catch (error) {
    console.error('Logout failed:', error)
    // Even if logout fails, redirect to home page
    router.push('/')
  }
}
</script>

<style scoped>
.logo {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 700;
}

.logo-icon {
  font-size: 1.5rem;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.user-avatar {
  font-size: 1.5rem;
}

.user-name {
  font-weight: 600;
}

.coins-chip {
  font-weight: 700;
}
</style>