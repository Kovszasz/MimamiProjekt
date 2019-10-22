import Vue from 'vue'
import App from '@/App.vue'
import IdleVue from 'idle-vue'
import store from '@/store'
import router from '@/router'
import vuetify from './plugins/vuetify';
import axios from 'axios'

// Add modified axios instance to Vue prototype so that to be available globally via Vue instance
//Vue.prototype.$http = axios;

const eventsHub = new Vue()
Vue.use(IdleVue, {
  eventEmitter: eventsHub,
  idleTime: 720000
}) // sets up the idle time,i.e. time left to logout the user on no activity
Vue.config.productionTip = false
/*
router.beforeEach((to, from, next) => {
  // if any of the routes in ./router.js has a meta named 'requiresAuth: true'
  // then check if the user is logged in before routing to this path:
  if (to.matched.some(record => record.meta.requiresAuth)) {
        if (!store.authentication.state.accessToken)
         {
      next({ name: 'login' })
    } else {
      next()
    }
  }
  // else if any of the routes in ./router.js has a meta named 'requiresLogged: true'
  // then check if the user is logged in; if true continue to home page else continue routing to the destination path
  // this comes to play if the user is logged in and tries to access the login/register page
  else if (to.matched.some(record => record.meta.requiresLogged)) {
    if (store.authentication.getters.loggedIn) {
      next({ name: 'home' })
    } else {
      next()
    }
  } else {
    next()
  }
})
*/
const vue = new Vue({
  router,
  store,
  vuetify,
  render: h => h(App)
})

vue.$mount('#app')
