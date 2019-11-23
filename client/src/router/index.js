import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import NewPost from '../views/NewPost.vue'
import Login from '../views/Login.vue'
Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'home',
    component: Home
  },
  {
    path: '/new',
    name: 'new',
    component: NewPost
  },
  {
    path: '/login',
    name: 'login',
    component: Login,
    meta: { noNav: true, noHeader: true }
  }
]

const router = new VueRouter({
  routes
})

export default router
