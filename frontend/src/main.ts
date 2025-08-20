import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { storeResetPlugin } from './plugins/storeReset'
import App from '@/App.vue'
import router from '@/router'
import vuetify from '@/plugins/vuetify'

import '@/style.css'
import 'remixicon/fonts/remixicon.css'

const app = createApp(App)
const pinia = createPinia()

pinia.use(storeResetPlugin)
app.use(pinia)
app.use(router)
app.use(vuetify)

app.mount('#app')