import Vue from 'vue'
import Router from 'vue-router'
import Index from '@/components/Index'
import MemePost from '@/components/MemePost'
import Login from '@/components/Login'
import Register from '@/components/Register'
import Logout from '@/components/Logout'
import MyPost from '@/components/MyPosts'
import Moderate from '@/components/Moderate'
import Statistics from '@/components/Statistics'
import ImgEditor from '@/components/ImgEditor'
import MyAdverts from '@/components/MyAdverts'
import MemeView from '@/components/MemeView'
import NProgress from 'nprogress'
import Activation from '@/components/Activation'
import Account from '@/components/Account'

Vue.use(Router)
const router = new Router({
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
      path: '/my-posts/:type',
      name: 'mypost',
      component: MyPost,
      props:{
        type:String
      },
      meta: {
        requiresAuth: true
      }


  },
  {
    path: '/meme/:iv/:data',
    name: 'memeview',
    component: MemeView,
    props:{
      iv:{
        type:String,
        default:''
      },
      data:{
        type:String,
        default:''
      }
    }
},
  {
    path: '/statistics',
    name: 'statistics',
    component: Statistics,
    meta: {
      requiresAuth: true
    }
},
{
  path: '/editor',
  name: 'editor',
  component: ImgEditor
},
{
  path: '/advert',
  name: 'advert',
  component: MyAdverts,
  props:{
    user:'AdUser'
  },
},
{
  path: '/activate/:uid/:token',
  name: 'activate',
  component: Activation,
  props:{
    uid:{
      type:String,
      default:''
    },
    token:{
      type:String,
      default:''
    }
  },
},
{
  path: '/account',
  name: 'account',
  component: Account,

},
  ]
})

router.beforeResolve((to, from, next) => {
  // If this isn't an initial page load.
  if (to.name) {
      // Start the route progress bar.
      NProgress.start()
  }
  next()
})

router.afterEach((to, from) => {
  // Complete the animation of the route progress bar.
  NProgress.done()
})
export default router
