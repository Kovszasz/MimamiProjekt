import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios' //!!I just changed axios to api
import MemePost from './MemePost'
import ImgUpload from './upload'
//import api from '../../services/api'

Vue.use(Vuex)
/*const token = localStorage.getItem('user-token')
if (token) {
  axios.defaults.headers.common['Authorization'] =JWT ${token}
}*/
const  state= {
     accessToken: localStorage.getItem('access_token') || null,
     refreshToken: localStorage.getItem('refresh_token') || null,
     APIData: '', // received data from the backend API is stored here.
     login:localStorage.getItem('login') || false,
     user:{
       username:localStorage.getItem('username') || null,
       first_name:localStorage.getItem('first_name') || null,
       last_name:localStorage.getItem('last_name') || null,
       mime_user:localStorage.getItem('mimeuser') || null,
       is_staff:localStorage.getItem('is_staff') || null,
       is_superuser:localStorage.getItem('is_staff') || null,
       is_authenticated:localStorage.getItem('is_authenticated') || null,
       channel:localStorage.getItem('channel') || null
     }

  }
const  getters= {
    loggedIn: state => {
      return state.accessToken != null
    }
  }
const  mutations= {
    updateLocalStorage (state, { access, refresh,login }) {
      localStorage.setItem('access_token', access)
      localStorage.setItem('refresh_token', refresh)
      localStorage.setItem('login', login)
      state.accessToken = access
      state.refreshToken = refresh
      state.login = login
    },
    updateAccess (state, access) {
      state.accessToken = access
    },
    destroyToken (state) {
      state.accessToken = null
      state.refreshToken = null
    },
    updateUser(state,{username,first_name,last_name,mimeuser,is_staff,is_superuser,is_authenticated,channel}){
      localStorage.setItem('username',username)
      localStorage.setItem('first_name',first_name)
      localStorage.setItem('last_name',last_name)
      localStorage.setItem('mimeuser',mimeuser)
      localStorage.setItem('is_staff',is_staff)
      localStorage.setItem('is_superuser',is_superuser)
      localStorage.setItem('is_authenticated',is_authenticated)
      localStorage.setItem('channel',channel)
      state.user.username=username
      state.user.first_name=first_name
      state.user.last_name=last_name
      state.user.mimeuser=mimeuser
      state.user.is_staff=is_staff
      state.user.is_superuser=is_superuser
      state.user.is_authenticated=is_authenticated
      state.user.channel=channel
    }
  }
const  actions= {
    // run the below action to get a new access token on expiration
    refreshToken (context) {
      return new Promise((resolve, reject) => {
        axios.post('/api/token/refresh/', {
          refresh: context.state.refreshToken
        }) // send the stored refresh token to the backend API
          .then(response => { // if API sends back new access and refresh token update the store
          //  console.log('New access successfully generated')
            //Vue.http.headers.common['Authorization'] = `JWT ${response.data.access}`;
            context.commit('updateAccess', response.data.access)
            resolve(response.data.access)
          })
          .catch(err => {
            //console.log('error in refreshToken Task')
            reject(err) // error generating new access and refresh token because refresh token has expired
          })
      })
    },
    registerUser (context, data) {
      return new Promise((resolve, reject) => {
        axios.post('/api/users/', data.user
      )
          .then(response => {
            resolve(response)
            ImgUpload(`/api/users/${data.user.username}/pic/`, data.profile_pic, name='profile_pic')
            .then(response=>{
                console.log("Uploaded picture successfully");
            })
            .catch(err=>{
                console.error(err);
            });

          })
          .catch(error => {
            reject(error)
          })

      })
    },
    logoutUser (context) {
      if (context.getters.loggedIn) {
        return new Promise((resolve, reject) => {
          axios.post('/api/token/logout/')
            .then(response => {
              localStorage.removeItem('access_token')
              localStorage.removeItem('refresh_token')
              localStorage.setItem('user',{})
              localStorage.setItem('login',false)
            //  localStorage.removeItem('user-token')
              context.commit('destroyToken')
            })
            .catch(err => {
              localStorage.removeItem('access_token')
              localStorage.removeItem('refresh_token')
            //  localStorage.removeItem('user-token')
              context.commit('destroyToken')
              resolve(err)
            })//.then(axios.post('/api/users/User/user_logout/'))


        })
      }
    },
    loginUser (context, credentials) {
      return new Promise((resolve, reject) => {
        // send the username and password to the backend API:
        axios.post('/api/token/', {
          username: credentials.username,
          password: credentials.password
        })
        //if successful update local storage:
          .then(response => {
            //console.log(response)
          //  Vue.http.headers.common['Authorization'] = `JWT ${response.data.access}`;
            context.commit('updateLocalStorage', { access: response.data.access, refresh: response.data.refresh,login:true }) //, token:response.data.user }) // store the access and refresh token in localstorage
            resolve()
          })
          .catch(err => {
            reject(err)
          })


          axios.get(`/api/users/${credentials.username}/user_login/`, {

          }).then(response =>{
              context.commit('updateUser', {
                username:response.data.username,
                first_name:response.data.first_name,
                last_name:response.data.last_name,
                mimeuser:response.data.mimeuser,
                is_staff:response.data.is_staff,
                is_superuser:response.data.is_superuser,
                is_authenticated:response.data.is_authenticated,
                channel:response.data.channel

              }) //, token:response.data.user }) // store the access and refresh token in localstorage
              resolve()
          })
          .catch(err => {
            reject(err)
          })
      })
    }
    //getUser(context)
  }
//  if (state.token) {
    //axios.defaults.headers.common['Authorization'] =JWT ${token};
//  }
export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
  rules: {
      'no-console': 'off',
  }
}
