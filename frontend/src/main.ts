import { createApp } from 'vue'
import { createPinia } from 'pinia'
import router from '@/router'
import App from '@/App.vue'
// import vuetify from '@/plugins/vuetify'

import '@/style.css'
import 'remixicon/fonts/remixicon.css'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)
// app.use(vuetify)

app.mount('#app')