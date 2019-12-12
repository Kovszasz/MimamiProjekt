<template>
    <div id="app">
    <v-app :dark="true">
      <router-view v-bind:key="$route.fullPath"></router-view>
    </v-app>
    </div>
</template>
<script>

import { mapState, mapActions, mapGetters } from 'vuex'
//import Vue from 'vue';
//import MemeEditor from './components/MemeEditor';
import Navbar from './components/Navbar';
//import {NavbarPlugin} from 'bootstrap-vue';
//Vue.use(NavbarPlugin);

export default {
  name: 'App',
  data(){
    return{
    }
  },
  components: {
    //  Index,
      Navbar
  },
  computed:{ ...mapState({
    timeline: state => state.post.timeline,
    IsAuthenticated:'authentication/login'
  }),...mapGetters('authentication',{
        themebool:'style'
  })

  },
  methods: mapActions('post', [
    'addPost',
    'deletePost'
  ]),
  beforeCreate() {
  //  this.$store.dispatch('post/getTimeLine')
//    this.$store.dispatch('comments/getComment')
//    this.$store.dispatch('post/getAction')
    this.$store.dispatch('post/getAdvert')
    this.$store.dispatch('post/getTemplate')
  },
  created(){
    //EventBus.$on('theme', (data) => {
        //this.$vuetify.theme.dark = this.themebool
    //})
  }
};
</script>
<style>
.title {
  font-size: 300px;
	font-weight: 900;
  background: -webkit-linear-gradient(right,#fe9a22, #fe5552);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
</style>
