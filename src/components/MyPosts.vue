<template>
  <div>
    <Navbar/>
    <v-content>
    <b-col md="6" offset-md="3">
    <div  v-for="(i,index) in timeline" v-bind:key="index+'_specialview'" >
      <div>
      <v-lazy v-model="isActive" :options="{ threshold: .5 }" transition="fade-transition">
        <meme_post
          v-if="liked"
          v-bind:post="i.post"
          v-bind:like="i.post.NumberOfLikes"
          v-bind:IsLiked="i.post.IsLiked"
        ></meme_post>
        <meme_post
          v-else
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
  import api from '../services/api'
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
          timeline:[],
          page:1
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
    ]),liked(){
      if(this.$route.params.type=='liked'){
        return true
      }else{
        return false
      }
    }

    },
    methods:{ ...mapActions('post', [
      'addPost',
      'deletePost'
    ]),
      ...mapGetters({

      }),async get_posts(){
          var url=`timeline/?page=${this.page}`
            if(this.$route.params.type =='liked'){
                url=url+`&like=true&user=${this.$route.params.user}`
            }else if(this.$route.params.type == 'top'){
                url=url+`&top=true`
            }else{
                url=url+`&user=${this.$route.params.type}`
            }
            await api.get(url)
                  .then((response)=>{
                  console.log(response)
                      this.timeline.push(...response.data.results)
                    this.page++
                  })
          },
          scroll(){
          window.onscroll = () => {
            let bottomOfWindow = document.documentElement.scrollTop + window.innerHeight === document.documentElement.offsetHeight;
            if (bottomOfWindow) {
                this.get_posts()
            }
           }
          }
    },
    mounted() {
        this.scroll();
    },
    created(){
        this.get_posts()
    }
    }
</script>
<style scope>
  .sidemenu{
  margin-top:80px;

  }
</style>
