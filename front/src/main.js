import { createApp } from 'vue'
import App from './App.vue'
import router from './router';
import "bootstrap";
import Popper from "vue3-popper";

let app = createApp(App)
app
    .use(router)
    .component("Popper", Popper)
    .mount('#app');
