import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import VueCookies from 'vue-cookies'
Vue.config.productionTip = false
Vue.use(VueCookies)
require('./assets/main.scss');
new Vue({
  store,
  router,
  render: h => h(App)
}).$mount('#app')
