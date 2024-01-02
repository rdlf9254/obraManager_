import { createApp } from 'vue'
import stores from './stores'
import App from './App.vue'
import router from './router'
const app = createApp(App);

import "@/scss/master.scss"

app.use(router)
app.use(stores)


app.mount('#app')



