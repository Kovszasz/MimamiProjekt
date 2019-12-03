import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios' //!!I just changed axios to api
import MemePost from './MemePost'
import ImgUpload from './uploadUser'
import comment from './comment'
import api from '../../services/api'
import post from './MemePost.js'


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
     user:localStorage.getItem('user') || {complete_account:false},
  }
const  getters= {
    loggedIn: state => {
      return state.accessToken != null
    },
    user:state=>{
      return state.user
    },
    locaStorage:state=>{
      return state
    },
    IsAuthenticated:state=>{
      return state.login
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
    updateUser(state,user){
      localStorage.setItem('user',user)
      state.user=user
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
      //  axios.post('/api/users/', data.user
      axios.post('http://localhost:8000/account/users/',data
      ).then(response => {
            resolve(response)
          })
          .catch(error => {
            console.log("error")
            console.log(error)
            reject(error)
          })

      })
},
completeUserRegistration (context, data) {
      return new Promise((resolve, reject) => {
      api.post(`/users/complete/`,data.user
      ).then(response => {
            console.log('hej')
            ImgUpload(`/api/users/pic/`, data.profile_pic,name='profile_pic')
            .then(response=>{

                console.log("Uploaded picture successfully");
            })
            .catch(err=>{
                console.error(err);
            });
            context.commit('updateUser',response)
          //  async (()=>{
          //     store.dispatch('post/getTimeLine')
            resolve(response)
          })
          .catch(error => {
            console.log("error")
            console.log(error)
            reject(error)
          })
      })
    },
    logoutUser (context) {
      if (context.getters.loggedIn) {
        return new Promise((resolve, reject) => {
          //axios.post('/api/token/logout/')
          axios.get(`/api/users/user_logout/`)
            .then(response => {
              context.commit('updateLocalStorage',{ access:null, refresh:null,login:false })
              context.commit('destroyToken')
              context.commit('updateUser',false,false)
            })
            .catch(err => {
              localStorage.setItem('user',{})
            //  localStorage.removeItem('user-token')
            context.commit('updateLocalStorage',{ access:null, refresh:null,login:false })
            context.commit('destroyToken')
            context.commit('updateUser',false,false)
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
            context.commit('updateUser', response.data)
          /*  async (()=>{
              context.commit('updateUser', response.data)
              resolve()
            }).then(post.dispatch('getTimeLine'))*/
            //post.dispatch('getTimeLine')
          })
          .catch(err => {
            reject(err)
          })
      })
    },
    socialLogin(context,FBaccessToken){

      return new Promise((resolve, reject) => {
          var username
          axios.post('/api/auth/oauth/login/',{
            provider:'facebook',
            access_token:FBaccessToken
          }).then(response=>{
            username=response.data.username
            context.commit('updateLocalStorage',{access:response.data.token,refresh:response.data.token,login:true})

          })
          axios.get(`/api/users/${credentials.username}/user_login/`)
            .then(response =>{
              context.commit('updateUser', response.data)
            /*  async (()=>{
                context.commit('updateUser', response.data)
                resolve()
              }).then(post.dispatch('getTimeLine'))*/
              //post.dispatch('getTimeLine')
            })
            .catch(err => {
              reject(err)
            })

      })
    }
  }
    //getUser(context)
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
