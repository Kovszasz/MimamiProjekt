import api from '@/services/api'

export default {
  fetchPost(postID) {
    return api.get(`post/${postID}`)
              .then(response => response.data)
  },
  likePost(postID) {
    return api.get(`post/${postID}/like/`)
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
