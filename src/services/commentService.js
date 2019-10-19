import api from '@/services/api'

export default {
  fetchComment() {
    return api.get(`comment/`)
              .then(response => response.data)
  },
  postComment(payload,postID) {
    return api.post(`comment/${postID}`, payload)
              .then(response => response.data)
  },
  deleteComment(comment) {
    return api.delete(`comment/${comment}`)
              .then(response => response.data)
  }
}
