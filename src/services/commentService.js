import api from '@/services/api'

export default {
  fetchComment() {
    return api.get(`comment/`)
              .then(response => response.data)
  },
  postComment(payload) {
    return api.post(`comment/`, payload)
              .then(response => response.data)
  },
  deleteComment(comment) {
    return api.delete(`comment/${comment}`)
              .then(response => response.data)
  },
  replyComment(reply) {
    return api.post(`comment/reply/`,reply)
              .then(response => response.data)
  },
  likeComment(commentID) {
    return api.get(`comment/${commentID}/like/`)
              .then(response => response.data)
  },
}
