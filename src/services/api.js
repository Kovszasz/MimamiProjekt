import axios from 'axios'
//import Cookies from 'js-cookie'
import store from '../store'



const api= axios.create({
  baseURL: '/api',
  timeout: 5000,
  headers: {
    'Content-Type': 'application/json',
  }
})

/*api.interceptors.request.use(
  (config) => {
    console.log(localStorage)
    let login = localStorage.getItem('login')
    if (login){
      let token = localStorage.getItem('access_token');
      console.log('token'+token)
          if (token) {
              config.headers['Authorization'] = `JWT ${ token }`;

      }else{
          store.dispatch('authentication/refreshToken')//.then(access=>{
          let access = localStorage.getItem('accessToken');
          if (access) {
            config.headers['Authorization'] = `JWT ${ access }`;
          }
  //  })
    }
  }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);
*/

api.interceptors.request.use(
  (config) => {
    let token = localStorage.getItem('access_token');
    console.log(localStorage)
    if (token) {
      config.headers['Authorization'] = `JWT ${ token }`;
    }

    return config;
  },

  (error) => {
    return Promise.reject(error);
  }
);


export default api
