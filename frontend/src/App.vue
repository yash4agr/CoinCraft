<template>
   <v-app>
    <router-view />
  </v-app>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useUserStore } from '@/stores/user'

const authStore = useAuthStore()
const userStore = useUserStore()

onMounted(() => {
  // Initialize authentication from localStorage on app startup
  authStore.initializeAuth()
})
</script>

<style>
</style>