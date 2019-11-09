<template>
  <div class="post">
  <v-container class="" >
  <b-card no-body header-tag="header" class="" max-height="700">
  <b-row no-gutters>
    <b-col md="6">
    <b-card
        header-tag="header"
        >
          <template v-slot:header v-if="!post.IsInlinePost">
          <v-carousel
            height="80%"
            hide-delimiters
            :show-arrows="false"
              cycle
              >
        <v-carousel-item
          v-for="subpost in post.imgs"
          :key="KeyGenerator(subpost.index)"
          :src="IMGurl(subpost)"
          interval="1000"
        >
        </v-carousel-item>
        </v-carousel>
          </template>

          <b-card-img src="https://picsum.photos/400/400/?image=20" class="rounded-0" v-if="!post.IsInlinePost"></b-card-img>
          <v-carousel
            v-if="post.IsInlinePost"
            v-bind:height="height"
            v-bind:width="width"
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
          </b-card>
    </b-col>
    <b-col md="6">
      <v-card >
          <v-tabs
            v-model="tab"
            background-color="transparent"
            grow
          >
            <v-tab
            >
              Statistics
            </v-tab>
            <v-tab
            >
              Settings
            </v-tab>
          </v-tabs>

          <v-tabs-items v-model="tab">
            <v-tab-item>
              <v-col class="px-0">
                <v-card
                    class="md-6"
                  >
                    <v-card-subtitle class="pb-0">Number 10</v-card-subtitle>
                        <area-chart :data="{'2017-01-01 00:00:00 -0800': 2, '2017-01-01 00:01:00 -0800': 5}"></area-chart>
                  </v-card>

                  <v-card
                      class="md-6"
                    >
                  <v-card-subtitle class="pb-0">Number 10</v-card-subtitle>
                      <column-chart :data="[['Sun', 32], ['Mon', 46], ['Tue', 28]]"></column-chart>
                  </v-card>
                  <v-card
                      class="md-6"
                    >
                  <v-card-subtitle class="pb-0">Number 10</v-card-subtitle>
                      <pie-chart :data="[['Blueberry', 44], ['Strawberry', 23]]"></pie-chart>
                  </v-card>
                </v-col>
            </v-tab-item>
            <v-tab-item
            >
            <div>
               <v-row justify="space-around">
                </v-row>
             </div>
            </v-tab-item>
          </v-tabs-items>
        </v-card>
            </b-col>
          </b-row>
        </b-card>
      </v-container>
  </div>
</template>

<script>
import { CardPlugin,CarouselPlugin,LayoutPlugin, FormTextareaPlugin  } from 'bootstrap-vue';
import { mapState, mapActions } from 'vuex'
import Vue from 'vue';
import { NavbarPlugin } from 'bootstrap-vue'
import { mdiShareVariant } from '@mdi/js'
import Chartkick from 'vue-chartkick'
import Chart from 'chart.js'

Vue.use(Chartkick.use(Chart))
Vue.use(NavbarPlugin)
Vue.use(CarouselPlugin)
Vue.use(CardPlugin)
Vue.use(LayoutPlugin)
Vue.use(FormTextareaPlugin)
Vue.use(CardPlugin);
Vue.use(mdiShareVariant);

export default {
    name:"AdStat",
    props:{
      post:Object,
      IsRegistration:{
          type:Boolean,
          default:false
      },
      height:{
      type:Number,
      default:100
      },
      width:{
      type:Number,
      default:100
      }
    },data() {
        return {
          like:this.post.NumberOfLikes,
          IsLiked:false,
          tab: null,
          success:true
        }
      },
  components:{
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
        }

},
  methods:{ ...mapActions('post', {
  addPost:'addPost',
  deletePost:'deletePost',
  LikePost:'LikePost',

}),IMGurl:function(img){
        return require(`../../assets${img.IMG_url.replace('http://localhost:8000','')}`)
        },
    KeyGenerator:function(index){
      return this.post.ID+String(index)
    },
    liking(){
      this.IsLiked=!this.IsLiked
        if (this.IsLiked){
          //  this.LikePost(this.post.ID,1)
            //this.like=this.post.NumberOfLikes++
            this.like+=1
        }else{
          //  this.LikePost(this.post.ID,-1)
            //this.like=this.post.NumberOfLikes--
            this.like-=1
        }

    }

},
updated(){
  //this.IsLiked= this.$store.state.post.timeline.filter(post => post.ID === this.post.ID).IsLiked

},
mounted() {
}
};

  </script>
  <style>
  .img
  {
  width:"50px"

  }
  </style>
