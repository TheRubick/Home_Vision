import { createRouter, createWebHistory } from '@ionic/vue-router';
import Home from '../views/Home.vue';
import AddFace from '../views/AddFace.vue';
import Settings from '../views/Settings.vue';
import FindObject from '../views/FindObject.vue';
import Help from '../views/Help.vue';
import LiveStream from '../views/LiveStream.vue';


const routes = [
  {
    path: '/',
    redirect: '/home'
  },
  {
    path: '/home',
    name: 'Home',
    component: Home
  },
  {
    path: '/home/addface',
    name: 'AddFace',
    component: AddFace
  },
  {
    path: '/home/findobject',
    name: 'FindObject',
    component: FindObject
  },
  {
    path: '/home/livestream',
    name: 'LiveStream',
    component: LiveStream
  },
  {
    path: '/home/settings',
    name: 'Settings',
    component: Settings
  },
  {
    path: '/home/help',
    name: 'Help',
    component: Help
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
