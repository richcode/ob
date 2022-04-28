import { createRouter, createWebHistory } from 'vue-router';
import Home from '../views/TestPage.vue';

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes: [
        {
            path: '/',
            name: 'Home',
            component: Home,
            meta: {
                title: '1'
            }
        }
    ]
})

export default router