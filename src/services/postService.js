import api from '@/services/api'
import axios from 'axios'
export default {
  fetchPost(postID) {
    return api.get(`post/${postID}`)
              .then(response => response.data)
  },
  likePost(postID,token) {
    token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTcxNjQ4MDg0LCJqdGkiOiJmNTM1ZWY5NmNiZjg0NzQ3OGYyZDUxNmRkOWM2Mzc5OCIsInVzZXJuYW1lIjoiVXNlciJ9.a2ehjc3PyyuCHp4ndvQwPu32IayN5zhbvarGoForWSs'
    const base={
      baseURL:'/api',
      headers: { Authorization: `JWT ${token}` },
    }
    alert(token)
    const p=axios.create(base)
    return p.get(`post/${postID}/like/`)
              .then(response => response.data)
  },
  postPost(payload) {
    return api.post(`post/`, payload)
              .then(response => response.data)
  },
  deletePost(postID) {
    return api.delete(`post/${postID}`)
              .then(response => response.data)
  },
  fetchTimeLine(){
    return api.get('post/')
            .then(response => response.data)
  },
  actionAdvert(postID,type){
    return api.get(`post/action/`,{
                    type:type,
                    post:postID
            })
            .then(response => response.data)
  },
  getAdvert(){
    return api.get(`post/get_ad/`)
            .then(response => response.data)
  }
}
