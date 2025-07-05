<template>
  <div class="teacher-dashboard">
    <v-app-bar color="primary" dark>
      <v-app-bar-title>
        <div class="logo">
          <img src="/coin.svg" class="logo-icon" alt="coin">
          <span>CoinCraft - Teacher Portal</span>
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
            <h1 class="text-h4 mb-4">Classroom Management 🏫</h1>
            
            <v-alert type="info" variant="tonal" class="mb-4">
              <v-icon start>mdi-information</v-icon>
              This is a demo teacher dashboard. Full classroom management features coming soon!
            </v-alert>
            
            <v-row>
              <v-col cols="12" md="6">
                <v-card>
                  <v-card-title>
                    <v-icon start color="primary">mdi-school</v-icon>
                    Class Progress
                  </v-card-title>
                  <v-card-text>
                    Monitor student learning and engagement
                  </v-card-text>
                  <v-card-actions>
                    <v-btn color="primary" variant="elevated">
                      View Progress
                    </v-btn>
                  </v-card-actions>
                </v-card>
              </v-col>
              
              <v-col cols="12" md="6">
                <v-card>
                  <v-card-title>
                    <v-icon start color="purple">mdi-book-open-page-variant</v-icon>
                    Assign Modules
                  </v-card-title>
                  <v-card-text>
                    Create and assign learning modules
                  </v-card-text>
                  <v-card-actions>
                    <v-btn color="purple" variant="elevated">
                      Create Module
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