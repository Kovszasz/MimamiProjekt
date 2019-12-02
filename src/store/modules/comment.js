import commentService from '../../services/commentService'

const state = {
  comments: [],
  postcomment:[]
}

const getters = {
  postcomment: state =>(id) => {
    return state.comments.filter(comment => comment.post === parseInt(id) && comment.reply_to === null)
  },
  comments:state=>{
    return state.comments
  },
  reply:state=>(id)=>{
    return state.comments.filter(comment=>comment.reply_to === parseInt(id))
  }
}

const actions = {
  getComment({ commit }){
    commentService.fetchComment()
    .then(comment => {
        commit('setComment',comment)
    })}
    ,
  addComment({ commit }, comment) {
    commentService.postComment(comment)
    .then(comment => {
      commit('addComment', comment)
    })
  },
  deleteComment( { commit }, cmtId) {
    commentService.deleteComment(cmtId)
    commit('deleteComment', cmtId)
  },
  replyComment( { commit }, reply) {
    commentService.replyComment(reply)
    .then((reply)=>{
        commit('replyComment', reply)
    })
  },
  LikeComment({ commit }, comID) {
    commentService.likeComment(comID)
    .then(() => {
    })},
}

const mutations = {
  setComment(state, comment) {
    state.comments = comment
  //  alert(state.comments)
  },
  addComment(state, comment) {
    state.comments.push(comment)
  },
  deleteComment(state, cmtId) {
    state.comments = state.comments.filter(obj => obj.pk !== cmtId)
  },
  replyComment(state, reply) {
    state.comments.push(reply)
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
