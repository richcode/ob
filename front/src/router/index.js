import { createRouter, createWebHistory } from 'vue-router';
import Home from '../views/ProcurementPage.vue';
import Supplier from '../views/SupplierPage.vue';
import Agency from '../views/AgencyPage.vue';

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes: [
        {
            path: '/supplier',
            name: 'Supplier',
            component: Supplier,
            meta: {
                title: 'Supplier'
            }
        },
        {
            path: '/agency',
            name: 'Agency',
            component: Agency,
            meta: {
                title: 'Agency'
            }
        },
        {
            path: '/',
            name: 'Home',
            component: Home,
            meta: {
                title: 'Procurement'
            }
        }
    ]
})

export default router