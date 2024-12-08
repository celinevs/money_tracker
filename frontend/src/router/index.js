import { createRouter, createWebHistory } from 'vue-router'
import workspace from '@/components/workspace.vue'
import form from '@/components/form.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [ {
    path:'/workspace',
    name:'workspace',
    component:workspace,
  },
  {
    path:'/form',
    name:'form',
    component:form,
  }
    
  ],
})

export default router
