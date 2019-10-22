<template>
  <div>
    <Navbar/>
    <v-content>
    <div  v-for="i in timeline" v-bind:key="i.id" >
      <div>
      <v-lazy v-model="isActive" :options="{ threshold: .5 }" transition="fade-transition">
        <meme_post
          v-bind:post="i"
          v-bind:like="i.NumberOfLikes"
          v-bind:IsLiked="i.IsLiked"
        ></meme_post>
        </v-lazy>
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
     Navbar,
     timeline:[]
     },
    data: function(){
        return{
          isActive: false
        }
    },
    resolve: {
      alias: {
        'vue$': 'vue/dist/vue.esm.js'
      }
    },
    computed: mapState({
      timeline: state => state.post.timeline,
      IsAuthenticated:'authentication/accessToken'
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
