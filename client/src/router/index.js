import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import Login from '../views/Login.vue'
import TestRoute from '../views/TestRoute.vue'
import store from '../store/index'
import Unauthorized from '../views/permissions/Unauthorized.vue' 
Vue.use(VueRouter)
const routes = [
  {
    path: '/',
    name: 'home',
    component: Home
  },
  {
    path: '/test_route',
    name: 'test_route',
    component: TestRoute,
    meta: { }
  },
  {
    path: '/login',
    name: 'login',
    component: Login,
    meta: { noNav: true }
  },
  {
    path: '/error',
    name: 'unauthorized',
    component: Unauthorized,
  },
]

const router = new VueRouter({
  routes
})
const loggedIn = store.getters.isloggedIn

router.beforeEach((to, from, next) => {
  if(to.matched.some(record => record.meta.requiresAuth)) {
      if (!loggedIn) {
          next({
              path: 'login',
              params: { nextUrl: to.fullPath }
          })
      } else {
         next();
      }
    } else {
      next()
    }
  })

router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.roles)) {
       if (!loggedIn) {
          next({
            path: 'login',
            params: { nextUrl: to.fullPath }
        })
       } else {
        const roles = to.meta.roles;                                                                                                                                           
        if (!roles.includes(store.state.auth.user.role)) {
          next({
            path: 'unauthorized'
          })
          // TODO: handle this ;)
        } else {
          next();
        }
    }
  } else {
    next()
  }
})  



export default router
