import { createRouter, createWebHistory } from 'vue-router'
import Login from '../components/Login.vue'
import Register from '../components/Register.vue'
import AdminPage from '../components/AdminPage.vue'
import UserPage from '../components/UserPage.vue'
import SpotsPage from '../components/spots.vue'



const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login', component: Login },
  { path: '/register', component: Register },
  { path: '/admin', component: AdminPage },
  { path: '/user/:id', component: UserPage, name: 'UserPage', props: true },
  { path: '/spots/:lotId', component: SpotsPage, name: 'SpotsPage' }

]

export default createRouter({
  history: createWebHistory(),
  routes
})
