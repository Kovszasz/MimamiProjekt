import Vue from 'vue'
import Vuex from 'vuex'
import messages from './modules/messages'
import post from  './modules/MemePost'
import comments from  './modules/comment'
import authentication from  './modules/authentication'

Vue.use(Vuex)
export default new Vuex.Store({
  modules: {
    messages,
    post,
    comments,
    authentication
  },
  rules: {
      'no-console': 'off',
  }
})
