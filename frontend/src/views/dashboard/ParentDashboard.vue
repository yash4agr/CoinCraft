<template>
  <div class="parent-dashboard">
    <v-app-bar color="primary" dark>
      <v-app-bar-title>
        <div class="logo">
          <img src="/coin.svg" class="logo-icon" alt="coin">
          <span>CoinCraft - Parent Portal</span>
        </div>
      </v-app-bar-title>
      
      <v-spacer />
      
      <div class="user-info">
        <span class="user-avatar">{{ authStore.user?.avatar }}</span>
        <span class="user-name">{{ authStore.user?.fullName }}</span>
      </div>
      
      <v-btn icon @click="handleLogout">
        <v-icon>mdi-logout</v-icon>
      </v-btn>
    </v-app-bar>

    <v-main>
      <v-container>
        <v-row>
          <v-col cols="12">
            <h1 class="text-h4 mb-4">Family Overview 👨‍👩‍👧‍👦</h1>
            
            <v-alert type="info" variant="tonal" class="mb-4">
              <v-icon start>mdi-information</v-icon>
              This is a demo parent dashboard. Full family management features coming soon!
            </v-alert>
            
            <v-row>
              <v-col cols="12" md="6">
                <v-card>
                  <v-card-title>
                    <v-icon start color="primary">mdi-account-multiple</v-icon>
                    Manage Children
                  </v-card-title>
                  <v-card-text>
                    View your children's progress and assign tasks
                  </v-card-text>
                  <v-card-actions>
                    <v-btn color="primary" variant="elevated">
                      View Children
                    </v-btn>
                  </v-card-actions>
                </v-card>
              </v-col>
              
              <v-col cols="12" md="6">
                <v-card>
                  <v-card-title>
                    <v-icon start color="green">mdi-cash</v-icon>
                    Coin Management
                  </v-card-title>
                  <v-card-text>
                    Set up coin redemption and rewards
                  </v-card-text>
                  <v-card-actions>
                    <v-btn color="green" variant="elevated">
                      Manage Coins
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
  await authStore.logout()
  router.push('/')
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
</style>