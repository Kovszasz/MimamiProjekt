<template>
  <div class="post">
  <b-container fluid class="bv-example-row">
    <b-row>
    <div v-intersect="seen">
        <b-card  header-tag="header" footer-tag="footer"  >
          <advert v-slot:header v-if="!IsRegistration"></advert>
          <template  v-if="IsAuthenticated">
            <v-list-item two-line height="100">
              <v-list-item-avatar size="55" >
                <img :src="AvatarUrl(post.user)">
              </v-list-item-avatar>

              <v-list-item-content>
                <v-list-item-title class="headline">
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
              <v-btn rounded v-if="post.user.username !== user.username" @click='follow(post.user.username)'>
                  Follow
              </v-btn>
            </v-list-item-action>
            <v-list-item-action align="right">

              <v-menu offset-y>
                <template v-slot:activator="{ on }">
                <v-btn  icon v-on="on">
                  <v-icon>mdi-dots-vertical</v-icon>
                </v-btn>
                </template>
                <v-list>
                  <v-list-item
                  >
                  <v-btn @click='report'>Report</v-btn>
                  </v-list-item>
                    <p>other things</p>
                  <v-list-item
                  >
                    click
                  </v-list-item>
                </v-list>
              </v-menu>
            </v-list-item-action>
            </v-list-item>
            <v-divider ></v-divider>
          </template>

          <v-carousel
            hide-delimiter-background
            width="100%"
            height="100%"
            :show-arrows='MultipleImgs'
            :show-arrows-on-hover='MultipleImgs'
            :hide-delimiters='!MultipleImgs'
          >
            <v-carousel-item
              @click='goToPost()'
              v-for="(subpost,index) in post.imgs"
              :key="KeyGenerator(index)"
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
                        <v-col>
            <template>
              <div class="text-center">
                <v-menu offset-y>
                  <template v-slot:activator="{ on }">
                    <v-btn
                      color="primary"
                      dark
                      v-on="on"
                    >
                      SHARE
                    </v-btn>
                  </template>
                  <v-list>
                    <v-list-item
                    >
                <!--    <social-sharing url="https://vuejs.org/"
                                          title="The Progressive JavaScript Framework"
                                          description="Intuitive, Fast and Composable MVVM for building interactive interfaces."
                                          quote="Vue is a progressive framework for building user interfaces."
                                          hashtags="vuejs,javascript,framework"
                                          twitter-user="vuejs"
                                          inline-template>
                      <div>
                          <network network="facebook">
                            <i class="fa fa-facebook"></i> Facebook
                          </network>
                        </div>
                    </social-sharing>-->
                    </v-list-item>
                  </v-list>
                </v-menu>
              </div>
            </template>
            </v-col>
          </v-row>
          <v-row>
          <v-col v-if="!IsRegistration"><comment_section v-if="IsAuthenticated" v-slot:footer :postID="post.ID"></comment_section></v-col>
          </v-row>
        </b-card>
        </div>
      </b-row>
    </b-container>


    <v-alert
        v-model="successReport"
        border="left"
        close-text="Close Alert"
        color="deep-purple accent-4"
        dark
        dismissible
    >
      Aenean imperdiet. Quisque id odio. Cras dapibus. Pellentesque ut neque. Cras dapibus.

      Vivamus consectetuer hendrerit lacus. Sed mollis, eros et ultrices tempus, mauris ipsum aliquam libero, non adipiscing dolor urna a orci. Sed mollis, eros et ultrices tempus, mauris ipsum aliquam libero, non adipiscing dolor urna a orci. Curabitur blandit mollis lacus. Curabitur ligula sapien, tincidunt non, euismod vitae, posuere imperdiet, leo.
    </v-alert>
  </div>
</template>

<script>
import { CardPlugin,CarouselPlugin,LayoutPlugin, FormTextareaPlugin  } from 'bootstrap-vue';
import { mapState, mapActions } from 'vuex'
import Vue from 'vue';
import advert from './Advert.vue';
import comment_section from './CommentSection.vue';
import { NavbarPlugin } from 'bootstrap-vue'
//var SocialSharing = require('vue-social-sharing');
import VueClipboard from 'vue-clipboard2'
import {
  mdiAccount,
  mdiPencil,
  mdiShareVariant,
  mdiDelete
} from '@mdi/js'
import api from '../services/api'
var Crypto = require('crypto')
Vue.use(VueClipboard)
Vue.use(NavbarPlugin)
Vue.use(CarouselPlugin)
Vue.use(CardPlugin)
Vue.use(LayoutPlugin)
Vue.use(FormTextareaPlugin)
Vue.use(comment_section)
Vue.use(CardPlugin);
Vue.use(mdiShareVariant);
//Vue.user(SocialSharing)
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
          successReport:false,
          isIntersecting:false
        }
      },
  components:{
    comment_section,
    advert
    //SocialSharing
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
      },generateURL() {
        var text=this.post.user.username+'/'+this.post.ID+'/'
//        const iv= 'mimamimimamimima'
        const iv = Crypto.randomBytes(16);
        let cipher = Crypto.createCipheriv('aes-256-ctr', Buffer.from('mimamimimamimimamimimamimimamimi'), iv);
        let encrypted = cipher.update(text);
        encrypted = Buffer.concat([encrypted, cipher.final()]);
        return { iv: iv.toString('hex'), encryptedData: encrypted.toString('hex') };
}
},
  methods:{ ...mapActions('post', {
  addPost:'addPost',
  deletePost:'deletePost',
  LikePost:'LikePost',

})
,IMGurl:function(img){
        if(img.IMG_url==''){
          return require(`../assets/logo.svg`)
        }else{
                return require(`../assets${img.IMG_url}`)
        }
        },
AvatarUrl:function(img){
    if(img==null){
        return require(`../assets/logo.svg`)
    }else{
        return require(`../assets${img.avatar}`)
    }
    },
    KeyGenerator:function(index){
      return this.post.ID+'img'+String(index)
    },
    liking(){
      this.post.IsLiked=!this.post.IsLiked
        if (this.post.IsLiked){
            this.LikePost(this.post.ID,1)
            this.like=this.post.NumberOfLikes++
            this.like+=1
        }else{
            this.LikePost(this.post.ID,-1)
            this.like=this.post.NumberOfLikes--
            this.like-=1
        }

    },recycle(){
      this.post.IsRecycled=!this.post.IsRecycled
      var templates=[]
      for(var i=0;i<this.post.imgs.length;i++){
        templates.push(this.post.imgs[i].template.ID)
      }

      if (this.post.IsRecycled){
          api.post('recycle/',{user:this.user,templates:templates})
          .then((response) => {
            this.$store.dispatch('post/getTemplate')
          })
          .catch((err) => {
            console.log(err);
          })
      }else{
      api.delete('recycle/',{user:this.user,templates:templates})
            .then((response) => {
                console.log('deleted recycle')
            })
            .catch((err) => {
                console.log(err);
      })
      }
    },goToPost(post){
    let link=`http://localhost:8080/meme/${this.generateURL.iv}/${this.generateURL.encryptedData}`
    this.$copyText(link).then(function (e) {
          alert('Copied')
          console.log(e)
      }, function (e) {
        alert('Can not copy')
        console.log(e)
    })
        //return this.$router.push({ name: 'memeview', params: { iv: this.generateURL.iv,data:this.generateURL.encryptedData } })
    },
    follow(user){
      //if (this.post.IsRecycled){
          api.post('follow/',{user:user})
          .then((response) => {
            this.$store.commit('authentication/updateUser',response.data)
          })
          .catch((err) => {
            console.log(err);
          })
    //  }else{
    //  api.delete('recycle/',{user:this.user,templates:templates})
    //        .then((response) => {
    //            console.log('deleted recycle')
    //        })
    //        .catch((err) => {
    //            console.log(err);
    //  })
    //  }
    },
    report(){
      api.post('post/action/',{post:this.post.ID,type:'Report'})
      .then(()=>{
        this.successReport=true

      }).catch((err)=>{
        console.log(err)
      })
    },
    seen(entries, observer) {
      this.$store.dispatch('post/viewAd',{post:this.post.ID,type:'View'})
    }
  }
};

  </script>
