import Vue from 'vue'
import Vuex from 'vuex'
import post from  './modules/MemePost'
import comments from  './modules/comment'
import authentication from  './modules/authentication'
import createPersistedState from "vuex-persistedstate";

Vue.use(Vuex)
export default new Vuex.Store({
  plugins: [createPersistedState()],
  modules: {
    post,
    comments,
    authentication
  },
  rules: {
      'no-console': 'off',
  }
})
