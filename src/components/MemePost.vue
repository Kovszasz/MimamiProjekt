<template>
  <div class="post">
  <b-container fluid class="bv-example-row">
    <b-row>

        <b-card  header-tag="header" footer-tag="footer" >
          <advert v-slot:header v-if="!IsRegistration"></advert>
          <template  v-if="IsAuthenticated">
            <v-list-item two-line height="100">
              <v-list-item-avatar size="55" >
                <img :src="AvatarUrl(post.user.mimeuser)">
              </v-list-item-avatar>

              <v-list-item-content>
                <v-list-item-title class="headline"><router-link :to = "{ name:'mypost',params:{user:post.user.username } }" >
                <v-badge
                  color="orange"
                  bottom
                  >
                  <template v-slot:badge>
                    <v-icon dark>
                        mdi-check
                    </v-icon>
                    </template>
                    <span>{{ post.user.username }}</span>
                </v-badge>
                </router-link></v-list-item-title>
                <v-list-item-subtitle>date</v-list-item-subtitle>
              </v-list-item-content>
            <v-list-item-action align="right">
              <v-btn rounded v-if="post.user.username !== user.username">
                  Follow
              </v-btn>
            </v-list-item-action>
            <v-list-item-action align="right">
              <v-btn icon>
                <v-icon color="grey lighten-1">mdi-information</v-icon>
              </v-btn>
            </v-list-item-action>
            </v-list-item>
            <v-divider ></v-divider>
          </template>

          <v-carousel
            height="100%"
            width="100%"
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
          <v-divider></v-divider>
          <v-row
          v-if="!IsRegistration"
            class="mb-9"
            no-gutters
          >
          <v-col v-if="!post.IsLiked"><v-icon :large="true" class="pa-2" @click="liking()">mdi-thumb-up</v-icon><p>{{ like }}</p>
          </v-col>
          <v-col v-if="post.IsLiked"><v-icon :large="true" class="pa-2" color="#fe5552" @click="liking()">mdi-thumb-up</v-icon><p>{{ like }}</p>
          </v-col>
            <v-col ><p class="pa-2" @click="recycle"><img src="@/assets/recycle.jpg" width="50" height="50" /></p>
            </v-col>
            <v-col v-if="!IsRegistration"><comment_section v-if="IsAuthenticated" v-slot:footer :postID="post.ID"></comment_section>
            </v-col>
          </v-row>
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
import {
  mdiAccount,
  mdiPencil,
  mdiShareVariant,
  mdiDelete,
} from '@mdi/js'
Vue.use(NavbarPlugin)
Vue.use(CarouselPlugin)
Vue.use(CardPlugin)
Vue.use(LayoutPlugin)
Vue.use(FormTextareaPlugin)
Vue.use(comment_section)
Vue.use(CardPlugin);
Vue.use(mdiShareVariant);

export default {
  name:'MemePost',
    props:{
      post:Object,
      IsRegistration:{
          type:Boolean,
          default:false
      },
      height:{
      type:Number,
      default:480
      },
      width:{
      type:Number,
      default:1024
      }
    },data() {
        return {
          like:this.post.NumberOfLikes,
          //IsLiked:false
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
}),    MultipleImgs:function(){
          if (this.post.imgs.length > 1){
              return true

          }else{
              return false
          }
        },


},
  methods:{ ...mapActions('post', {
  addPost:'addPost',
  deletePost:'deletePost',
  LikePost:'LikePost',

})
,IMGurl:function(img){
        return require(`../assets${img.IMG_url}`)
        },
AvatarUrl:function(img){
        return require(`../assets${img.avatar}`)
    },
    KeyGenerator:function(index){
      return this.post.ID+String(index)
    },
    liking(){
      this.post.IsLiked=!this.post.IsLiked
        if (this.IsLiked){
            this.LikePost(this.post.ID,1)
            this.like=this.post.NumberOfLikes++
            this.like+=1
        }else{
            this.LikePost(this.post.ID,-1)
            this.like=this.post.NumberOfLikes--
            this.like-=1
        }

    },recycle(){

    }

},
updated(){
  //this.IsLiked= this.$store.state.post.timeline.filter(post => post.ID === this.post.ID).IsLiked

},
mounted() {
  //this.$store.dispatch('post/getPost',this.post.ID)
}
};

  </script>
