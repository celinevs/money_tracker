import { createRouter, createWebHistory } from 'vue-router'
import workspace from '@/components/workspace.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [ {
    path:'/workspace',
    name:'workspace',
    component:workspace,
  }
    
  ],
})

export default router
