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

router.beforeEach((to, from, next) => {
  if(to.matched.some(record => record.meta.requiresAuth)) {
    // check if both tokens are valid
      if (this.$store.state.refresh_token == null || this.$store.state.access_token == null) {
        console.log('this is atest');
          next({
              path: '/login',
              params: { nextUrl: to.fullPath }
          })
      } else {
          let user = this.$store.state.user
          if(to.matched.some(record => record.meta.is_admin)) {
              if(user.is_admin == 1){
                  next()
              }
              else{
                  next({ name: 'userboard'})
              }
          }else {
              next()
          }
      }
  } else {
      next() 
  }
})

export default router
