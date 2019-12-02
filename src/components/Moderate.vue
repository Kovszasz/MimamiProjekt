<template>
  <div>
    <Navbar/>
    <v-content>
    <div  v-for="i in timeline" v-bind:key="i.id" >
      <div>
      <v-card>
          <v-btn color="red" @click="moderatePost({postID:i.ID,decision:decision})">Delete post</v-btn>
          <v-btn color="green" @click="moderatePost({postID:i.ID,decision:!decision})">Accept post</v-btn>
        <meme_post
          v-bind:post="i"
          v-bind:like="i.NumberOfLikes"
          v-bind:IsLiked="i.IsLiked"
        ></meme_post>
      </v-card>
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
  import { mapState, mapActions, mapGetters } from 'vuex'
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
        decision:true
        }
    },
    resolve: {
      alias: {
        'vue$': 'vue/dist/vue.esm.js'
      }
    },
    computed:{ ...mapState({
      timeline: state => state.post.timeline.filter(timeline => timeline.IsModerated == false ),
      IsAuthenticated:'authentication/accessToken'
    }),...mapGetters('post',{
          timeline:'reportedMemes'
    })
    },
    methods:{ ...mapActions('post', [
      'addPost',
      'deletePost',
      'moderatePost'
    ])
    },
    created() {
      //this.$store.dispatch('post/getTimeLine')
    }
    }
</script>
