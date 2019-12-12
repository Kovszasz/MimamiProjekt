import api from '@/services/api'
import axios from 'axios'
import ImgUpload from '../store/modules/upload'

export default {
  fetchPost(posturl) {
    return api.get(`post/retrievePost/${posturl}/`)
              .then(response => response.data)
  },
  likePost(postID) {
    return api.get(`post/${postID}/like/`)
              .then(response => response.data)
  },
  postPost(payload,multiple) {
    //api.post(`post/`, payload.post).then(
    return ImgUpload(`/api/post/`, payload.meme.imgs, payload,multiple, name='meme').then(response => response.data)
  },
  deletePost(postID) {
    return api.delete(`post/${postID}`)
              .then(response => response.data)
  },
  fetchTimeLine(page){
    return api.get(`timeline/?page=${page}`)
            .then(response => response.data)
  },
  actionAdvert(payload){
    return api.post(`post/action/`,payload)
            .then(response => response.data)
  },
  getAdvert(){
    return api.get(`post/get_ad/`)
            .then(response => response.data)
  },
  getAction(){
    return api.get(`action/`)
            .then(response => response.data)
  },
  postMeme(payload,multiple) {
    return ImgUpload(`/api/meme/`, payload.imgs, payload.payload,multiple, name='meme')
            .then(response => response.data)
  },
  memeIMGflip(){
    return api.get('template/')
    .then(response => response.data)
  },
  modPost(payload){
    return api.post(`post/${payload.postID}/moderate/`,payload)
      .then(response=>response.data)
  },
  updatePost(payload){
    return api.post('post/',payload)
  }
}
