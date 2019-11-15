import postService from '../../services/postService'





const state = {
  post: [],
  action:[],
  advert:[],
  timeline:[],
  memeTemplate:[]
}

const getters = {
  post: state => {
    return state.post
  },
  action: state => {
    return state.action
  },
  advert_in: state =>{
    return state.advert.filter(ad=>ad.IsInlinePost === true)
  },
  advert: state =>{
    return state.advert.filter(ad=>ad.IsInlinePost === false && ad.IsAdvert === true)
  },
  timeline:state =>{
    return state.timeline
  },
  single_post:state=>(id)=>{
      return state.timeline.filter(post=>post.ID === id)
  },
  memeTemplates:state=>{
    return state.memeTemplate
  },
  myTemplates:state=>(id)=>{
    return state.memeTemplate.filter(post=>post.user.username === id)
  },
  publicTemplates:state=>{
    return state.memeTemplate.filter(post=>post.IsPublic === true)
  },
  recycledTemplates:state=>{
    return state.memeTemplate.filter(post=>post.recycler !== true)
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
    },
  getTemplate({ commit },type){
        postService.memeIMGflip()
        .then(template =>{
          commit('getTemplate',template)
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
  },
  getTemplate(state,template){
    state.memeTemplate=template
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
