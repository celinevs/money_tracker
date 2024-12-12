import { createRouter, createWebHistory } from 'vue-router'
import workspace from '@/components/workspace.vue'
import form from '@/components/form.vue'
import login from '@/components/login.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [ {
    path:'/workspace',
    name:'workspace',
    component:workspace,
  },
  {
    path:'/form/:category',
    name:'form',
    component:form,
  },
  {
    path:'/login',
    name:'login',
    component:login,
  }
    
  ],
})

export default router
