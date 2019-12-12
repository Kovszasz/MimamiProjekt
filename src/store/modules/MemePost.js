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
  },
  topMemes:state=>{
  const items = [...state.timeline.filter(post=>post.IsLiked !==true)].sort((a,b) => {
    if(a.PopularityScore > b.PopularityScore){return 1}
    if(a.PopularityScore < b.PopularityScore){return -1}
    return 0
    })
    items.reverse()
    console.log(items)
    return items
  },
  likedMeme:state=>{
    return state.timeline.filter(post=>post.IsLiked === true)
  },
  reportedMemes:state=>{
    const items = [...state.timeline.filter(post=>post.IsModerated !==true)].sort((a,b) => {
      if(a.ReportScore > b.ReportScore){return 1}
      if(a.ReportScore < b.ReportScore){return -1}
      return 0
      })
      return items.reverse()

  }

}

const actions = {
  getTimeLine({ commit},page){
    postService.fetchTimeLine(page)
    .then(timeline => {
        commit('getTimeLine',timeline.results)
    })
  },
  getPost ({ commit },posturl) {
    //postID='Post1'
    postService.fetchPost(posturl)
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
      //commit('getAdvert',advert)
    })},
  clickAd({ commit },payload) {
    postService.actionAdvert(payload)
    .then(advert => {
      //commit('getAdvert',advert)
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
      },
  moderatePost({commit},payload){
    postService.modPost(payload)
    .then(()=>{

        if(payload.decision){
          commit('moderatePost', payload.postID)
        }

    })

  },
  editPost({commit},post){
    postService.updatePost(post)
    .then(response=>{
      commit('editPost',response)
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
      for(var i=0;i<timeline.length;i++){
        if(Math.random()<timeline[i].PersonalFit){
            state.timeline.push(timeline[i])
        }

      }
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
  },
  followPostUser(state,username){
      const timeline = state.timeline.filter(function(item) {
            if(item.user.username == username){
              item.user.IsFollowed=!item.user.IsFollowed
            }
            return item
      })
      state.timeline=timeline
    },
  moderatePost(state,postID){
      state.timeline.filter(function(item){
        if(item.ID == postID){
          item.IsModerated=true
        }
        return item
      })
      state.timeline=state.timeline
    },
  editPost(state,post){
    state.timeline.filter(function(item){
      if(item.ID == post.ID){
          item = post
      }
      return item
    })
    state.timeline=state.timeline
  },
  updateAd(state,post){
    state.advert.filter(function(item){
      if(item.ID == post.ID){
          item = post
      }
      return item
    })
    state.advert=state.advert

  },
  emptyPostStorage(state){
    for(var i in state.keys){
      state[i]=[]
    }
  }

  }

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
