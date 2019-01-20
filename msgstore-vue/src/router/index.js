import Vue from 'vue'
import Vuetify from 'vuetify'
import Router from 'vue-router'
import Main from '@/components/Main'
import Auth from '@/components/Auth'

import 'vuetify/dist/vuetify.min.css'

Vue.use(Vuetify)
Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'home',
      component: Main
    },
    {
      path: '/login',
      name: 'login',
      component: Auth
    }
  ]
})
