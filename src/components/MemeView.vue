<template>
  <div class="post">
  <Navbar></Navbar>
  <b-container fluid class="bv-example-row">
    <b-row>

        <b-card  header-tag="header" footer-tag="footer" >
          <template  v-if="IsAuthenticated">
            <v-list-item two-line height="100">
              <v-list-item-avatar size="55" >
                <img :src="AvatarUrl(post.user)">
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
            <v-row  v-if="!IsRegistration">
              <v-col v-if="IsLiked"><v-icon color="#fe5552" @click="liking()">mdi-thumb-up</v-icon><p>{{ like }}</p>
              </v-col>
              <v-col v-if="!IsLiked"><v-icon  @click="liking()">mdi-thumb-up</v-icon><p>{{ like }}</p>
              </v-col>
              <v-col><comment_section v-if="IsAuthenticated" v-slot:footer :postID="post.ID"></comment_section></v-col>
              <v-col><v-icon> </v-icon></v-col>
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
import comment_section from './CommentSection.vue';
import { NavbarPlugin } from 'bootstrap-vue'
import { mdiShareVariant } from '@mdi/js'
import Navbar from './Navbar.vue'
var Crypto = require('crypto')
Vue.use(NavbarPlugin)
Vue.use(CarouselPlugin)
Vue.use(CardPlugin)
Vue.use(LayoutPlugin)
Vue.use(FormTextareaPlugin)
Vue.use(comment_section)
Vue.use(CardPlugin);
Vue.use(mdiShareVariant);

export default {
  name:'MemeView',
  data() {
        return {

        }
      },
  components:{
    comment_section,
    Navbar
    },
      resolve: {
      alias: {
      'vue$': 'vue/dist/vue.esm.js'
      }
    },
      computed:{...mapState('authentication',{
        IsAuthenticated:'accessToken',
        refreshToken:'refreshToken',
        user:'user',
        post:state=>state.post.timeline.filter(p=>p.ID === this.$refs.params.post)
}),    MultipleImgs:function(){
          if (this.post.imgs.length > 1){
              return true

          }else{
              return false
          }
        },
        post(){
          return this.$store.state.post.post//timeline.filter(post=>post.ID === this.$route.params.post)
        },
        decodePosttoken(){
            let iv = Buffer.from(this.$route.params.iv, 'hex');
            console.log(iv)
            let encryptedText = Buffer.from(this.$route.params.data, 'hex');
            let decipher = Crypto.createDecipheriv('aes-256-ctr', Buffer.from('mimamimimamimimamimimamimimamimi'), iv);
            let decrypted = decipher.update(encryptedText);
            decrypted = Buffer.concat([decrypted, decipher.final()]);
            return decrypted.toString();
}


},

  methods:{ ...mapActions('post', {
  getPost:'getPost',
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
      return this.$refs.params.post+String(index)
    },
    liking(){
      this.IsLiked=!this.IsLiked
        if (this.IsLiked){
          //  this.LikePost(this.$refs.params.post,1)
            //this.like=this.post.NumberOfLikes++
            this.like+=1
        }else{
          //  this.LikePost(this.$refs.params.post,-1)
            //this.like=this.post.NumberOfLikes--
            this.like-=1
        }

    }

},
updated(){
  //this.IsLiked= this.$store.state.post.timeline.filter(post => post.ID === this.$refs.params.post).IsLiked

},
created() {
  console.log(this.decodePosttoken)
  this.$store.dispatch('post/getPost',this.decodePosttoken.toString())
}
};

  </script>
