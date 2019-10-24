<template>
  <div>
    <Navbar/>
    <v-content>
    <div  v-for="i in timeline" v-bind:key="i.id" >
      <div>
        <meme_post
          v-bind:post="i"
          v-bind:like="i.NumberOfLikes"
          v-bind:IsLiked="i.IsLiked"
        ></meme_post>
      </div>
    </div>
    </v-content>
  </div>
</template>
<script>
  import Vue from 'vue';
  import meme_post from './MemePost.vue';
  import comment_section from './CommentSection.vue';
  import { NavbarPlugin } from 'bootstrap-vue'
  Vue.use(NavbarPlugin)
  import Navbar from './Navbar.vue'
  import { mapState, mapActions } from 'vuex'
  //Vue.use(Navbar)
  export default {
    name: 'Index',
    components:{
     meme_post,
     comment_section,
     Navbar
     },
    data: function(){
        return{
        }
    },
    resolve: {
      alias: {
        'vue$': 'vue/dist/vue.esm.js'
      }
    },
    computed: mapState({
      user:'user',
      timeline: state => state.post.timeline.filter(timeline => timeline.user.username == 'User' ),
      IsAuthenticated:'authentication/accessToken',


    }),
    methods: mapActions('post', [
      'addPost',
      'deletePost'
    ]),
    created() {
      this.$store.dispatch('post/getTimeLine')
    }
    }
</script>
