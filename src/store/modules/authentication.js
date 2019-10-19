import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios' //!!I just changed axios to api
//import api from '../../services/api'

Vue.use(Vuex)
/*const token = localStorage.getItem('user-token')
if (token) {
  axios.defaults.headers.common['Authorization'] =JWT ${token}
}*/
const  state= {
     accessToken: localStorage.getItem('access_token') || null,
    // token:localStorage.getItem('user-token') || null,
    // refreshing the page
     refreshToken: localStorage.getItem('refresh_token') || null,
     APIData: '' // received data from the backend API is stored here.
  }
const  getters= {
    loggedIn: state => {
      return state.accessToken != null
    }
  }
const  mutations= {
    updateLocalStorage (state, { access, refresh, user }) {
      localStorage.setItem('access_token', access)
      localStorage.setItem('refresh_token', refresh)
      localStorage.setItem('user-token', user)
      state.accessToken = access
      state.refreshToken = refresh
    },
    updateAccess (state, access) {
      state.accessToken = access
    },
    destroyToken (state) {
      state.accessToken = null
      state.refreshToken = null
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
        axios.post('/api/users/', {
          first_name: data.first_name,
          last_name:data.last_name,
          email: data.email,
          username: data.username,
          password: data.password,
          mimeuser:{
            IsAdvertiser:true
          }
        },
      )
          .then(response => {
            resolve(response)
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
            context.commit('updateLocalStorage', { access: response.data.access, refresh: response.data.refresh}) //, token:response.data.user }) // store the access and refresh token in localstorage
            resolve()
          })
          .catch(err => {
            reject(err)
          })
          /*.then(axios.post('/api/users/User/user_login/', {
                      username: credentials.username,
                      password: credentials.password
                }))*/
      })
    }
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
