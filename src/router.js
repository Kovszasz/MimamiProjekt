import Vue from 'vue'
import Router from 'vue-router'
import Index from '@/components/Index'
import Messages from '@/components/Messages'
import MemePost from '@/components/MemePost'
import Login from '@/components/Login'
import Register from '@/components/Register'
import Logout from '@/components/Logout'
import MyPost from '@/components/MyPosts'
import Moderate from '@/components/Moderate'
import Statistics from '@/components/Statistics'

Vue.use(Router)
export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'home',
      component: Index,
      meta:{
        requiresAuth: true

      }
    },
    {
      path: '/messages',
      name: 'messages',
      component: Messages,
      meta: {
        requiresLogged: true
      }
    },
    {
      path: '/post',
      name: 'post',
      component: MemePost,
      meta:{
          requiresLogged: true

      }
    },
    {
      path: '/login',
      name: 'login',
      component: Login,
      meta:{
        requiresAuth: true

      }
    },
    {
      path: '/register',
      name: 'register',
      component: Register,
      meta: {
        requiresLogged: true
      }
    },
    {
      path: '/logout',
      name: 'logout',
      component: Logout,
      meta: {
        requiresAuth: true
      }}
      ,
      {
        path: '/moderate',
        name: 'moderate',
        component: Moderate,
        meta: {
          requiresAuth: true
        }
    },
    {
      path: '/my-posts',
      name: 'mypost',
      component: MyPost,
      meta: {
        requiresAuth: true
      }
  },
  {
    path: '/statistics',
    name: 'statistics',
    component: Statistics,
    meta: {
      requiresAuth: true
    }
}
  ]
})
