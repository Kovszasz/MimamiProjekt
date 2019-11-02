import postService from '../../services/postService'





const state = {
  post: [],
  action:[],
  advert:[],
  timeline:[]
}

function randomgenerator(length){
   return state.advert[Math.random()*length]

}
const getters = {
  post: state => {
    return state.post
  },
  action: state => {
    return state.action
  },
  advert: state =>{
    return randomgenerator(state.advert.length)
  },
  timeline:state =>{
    return state.timeline
  }
  /*get_timeline: state =>(id) => {
    return state.timeline.filter(post => post.user.username === id)
  }
  get_timeline:state => {
    return state.timeline.filter(post => post.user.username === 'User')
  }*/
}

const actions = {
  getTimeLine({ commit}){
    postService.fetchTimeLine()
    .then(timeline => {
        commit('getTimeLine',timeline)
    })
  },
  getPost ({ commit },postID) {
    //postID='Post1'
    postService.fetchPost(postID)
    .then(post => {
      commit('setPost', post)
    })
  },
  addPost({ commit }, post,multiple) {
    postService.postPost(post,multiple)
    .then(post => {
      commit('addPost', post)
    })
  },
  deletePost( { commit }, postID) {
    postService.deletePost(postID)
    commit('deletePost', postID)
  },
  LikePost({ commit }, post,change) {
    postService.likePost(post)
    .then(() => {
      commit('likePost', post,change)
    })},
  getAdvert({ commit }) {
      postService.getAdvert()
      .then(advert => {
        commit('getAdvert',advert)
      })},
  viewAd({ commit },payload) {
    postService.actionAdvert(payload)
    .then(advert => {
      commit('getAdvert',advert)
    })},
  clickAd({ commit },payload) {
    postService.actionAdvert(payload)
    .then(advert => {
      commit('getAdvert',advert)
    })
  },
  getAction({ commit }) {
      postService.getAction()
      .then(action => {
        commit('setAction',action)
      })},
  addMeme({ commit }, meme,multiple) {
      postService.postMeme(meme,multiple)
      .then(() => {
      //  commit('addPost', post)
      })
    }
}

const mutations = {
  setPost(state, post) {
    state.post = post
  },
  addPost(state, post) {
    state.post.push(post)
    //state.post=post
  },
  deletePost(state, postId) {
    state.post = state.post.filter(obj => obj.pk !== postId)
  },
  getTimeLine(state, timeline) {
    state.timeline = timeline
  },
  likePost(state, post,change) {
    post.NumberOfLikes=post.NumberOfLikes+change
    state.post.push(post)
  },
  getAdvert(state, advert) {
    state.advert=advert
  },
  setAction(state, action) {
    state.action=action
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
