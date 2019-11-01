import commentService from '../../services/commentService'

const state = {
  comments: [],
  postcomment:[]
}

const getters = {
  postcomment: state =>(id) => {
    return state.comments.filter(comment => comment.post === id)
  },
  comments:state=>{
    return state.comments
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
    .then(() => {
      commit('addComment', comment)
    })
  },
  deleteComment( { commit }, cmtId) {
    commentService.deleteComment(cmtId)
    commit('deleteComment', cmtId)
  }
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
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
