<template>
  <div>
    <Navbar/>
    <v-content>
    <b-col md="6" offset-md="3">
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
    </div></b-col>
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
    name: 'MyPost',
    props:{
      user:String,
    },
    components:{
     meme_post,
     comment_section,
     Navbar,
     },
    data: function(){
        return{
          isActive: false,
        }
    },
    resolve: {
      alias: {
        'vue$': 'vue/dist/vue.esm.js'
      }
    },
    computed:{ ...mapState({
      IsAuthenticated:'authentication/login'
    }),...mapGetters('post',[
            'likedMeme',
            'topMemes'
    ])
    ,timeline:function(){
        if(this.$route.params.type =='liked'){
          return this.likedMeme
        }else if(this.$route.params.type == 'top'){

          return this.topMemes
        }else{
          return this.$store.state.post.timeline.filter(post=>post.user.username === this.$route.params.type)
        }
    }

    },
    methods:{ ...mapActions('post', [
      'addPost',
      'deletePost'
    ]),
      ...mapGetters({

      })

    },
    created() {
      //this.$store.dispatch('post/getTimeLine')
      //this.$store.dispatch('comments/getComment')
      //this.$store.dispatch('post/getAction')
    }
    }
</script>
<style scope>
  .sidemenu{
  margin-top:80px;

  }
</style>
