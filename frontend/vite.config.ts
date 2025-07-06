
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'
import vuetify from 'vite-plugin-vuetify'

export default defineConfig({
  plugins: [
    vue(),
    vuetify({autoImport: true})
  ],
  resolve : {
    alias: {
      '@' : path.resolve(__dirname, './src')

    }
  }
})