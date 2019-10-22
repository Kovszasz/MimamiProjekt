import api from '@/services/api'
/*
api.interceptors.request.use(
  (config) => {
    let token = localStorage.getItem('accessToken');

    if (token) {
      config.headers['Authorization'] = `JWT ${ token }`;
    }

    return config;
  },

  (error) => {
    return Promise.reject(error);
  }
);
*/


export default {
  fetchComment(postID) {
    return api.get(`comment/${postID}`)
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
