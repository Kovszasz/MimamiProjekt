<template>
  <div class="post">
  <b-container fluid class="bv-example-row">
    <b-row>

        <b-card  header-tag="header" footer-tag="footer" >
          <advert v-slot:header></advert>
          <v-carousel
            height="480"
            width="1024"
            hide-delimiter-background
            :show-arrows='MultipleImgs'
            :show-arrows-on-hover='MultipleImgs'
            :hide-delimiters='!MultipleImgs'
          >
            <v-carousel-item
              v-for="subpost in post.imgs"
              :key="KeyGenerator(subpost.index)"
              :src="IMGurl(subpost)"
              interval="0"
            >
            </v-carousel-item>
          </v-carousel>
            <v-row >
              <v-col v-if="IsLiked"><v-icon color="#fe5552" @click="liking()">mdi-thumb-up</v-icon><p>{{ like }}</p>
              </v-col>
              <v-col v-if="!IsLiked"><v-icon  @click="liking()">mdi-thumb-up</v-icon><p>{{ like }}</p>
              </v-col>
              <v-col><v-icon>mdi-message-text</v-icon></v-col>
              <v-col><v-icon> </v-icon></v-col>
          </v-row>
          <comment_section v-if="IsAuthenticated" v-slot:footer :postID="post.ID"></comment_section>
        </b-card>
      </b-row>
    </b-container>
  </div>
</template>

<script>
import { CardPlugin,CarouselPlugin,LayoutPlugin, FormTextareaPlugin  } from 'bootstrap-vue';
import { mapState, mapActions } from 'vuex'
import Vue from 'vue';
import advert from './Advert.vue';
import comment_section from './CommentSection.vue';
import { NavbarPlugin } from 'bootstrap-vue'
import { mdiShareVariant } from '@mdi/js'
Vue.use(NavbarPlugin)
Vue.use(CarouselPlugin)
Vue.use(CardPlugin)
Vue.use(LayoutPlugin)
Vue.use(FormTextareaPlugin)
Vue.use(comment_section)
Vue.use(CardPlugin);
Vue.use(mdiShareVariant);

export default {
    props:{
      post:Object,
      IsLiked:Boolean
    },data() {
        return {
          like:this.post.NumberOfLikes
        //  get_url:require(`../assets${this.post.IMG_url.replace('http://localhost:8000','')}`) //majd összekötni a valós képekkel
          //IsLiked:this.post.IsLiked
        }
      },
  components:{
    comment_section,
    advert
    },
      resolve: {
      alias: {
      'vue$': 'vue/dist/vue.esm.js'
      }
    },
      computed:{...mapState('authentication',{
        IsAuthenticated:'accessToken',
        refreshToken:'refreshToken',
        user:'user'
    //    ImageURL:function(){
      //  return require(`${this.post.IMG_url.replace('http://localhost:8000','../assets')}`)
  //  }//,post: state => state.post.post //Ide majd az imgs rész fog jönni!

}),    MultipleImgs:function(){
          if (this.post.imgs.length > 1){
              return true

          }else{
              return false
          }
        }

},
  methods:{ ...mapActions('post', {
  addPost:'addPost',
  deletePost:'deletePost',
  LikePost:'LikePost',
  liking(){
      if (this.IsLiked){
          this.LikePost(this.post.ID,1)
          this.like=this.post.NumberOfLikes++
      }else{
          this.LikePost(this.post.ID,-1)
          this.like=this.post.NumberOfLikes--
      }
      this.IsLiked=!this.IsLiked
  }
}),IMGurl:function(img){
        return require(`../assets${img.IMG_url.replace('http://localhost:8000','')}`)
        },
    KeyGenerator:function(index){
      return this.post.ID+String(index)
    }

},
created() {
  this.$store.dispatch('post/getPost',this.post.ID)
}
};

  </script>
