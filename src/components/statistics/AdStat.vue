<template>
  <div class="post">
  <v-container class="" >
  <b-row no-gutters justify="center">
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

          <b-card-img src="https://picsum.photos/400/400/?image=20" class="rounded-0" v-if="post.IsInlinePost"></b-card-img>
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
            <v-container>
            <v-row align="center">
              <v-col>
                <v-window
                  v-model="window"
                  class="elevation-1"
                  vertical
                >
                  <v-window-item>
                  <v-col class="px-0">
                    <v-card
                        class="md-6"
                      >
                        <v-card-subtitle class="pb-0">Number 10</v-card-subtitle>
                            <area-chart :data="{'2017-01-01 00:00:00 -0800': 2, '2017-01-01 00:01:00 -0800': 5}"></area-chart>
                      </v-card>
                      </v-col>
                  </v-window-item>
                  <v-window-item>
                    <v-col class="px-0">
                      <v-card
                          class="md-6"
                        >

                      <v-card-subtitle class="pb-0">Number 10</v-card-subtitle>
                          <column-chart :data="[['Sun', 32], ['Mon', 46], ['Tue', 28]]"></column-chart>
                      </v-card>
                      </v-col>
                  </v-window-item>
                  <v-window-item>
                    <v-col class="px-0">
                      <v-card
                          class="md-6"
                        >
                      <v-card-subtitle class="pb-0">Number 10</v-card-subtitle>
                          <pie-chart data="`/post/gender_stat/${post.ID}/`"></pie-chart>
                      </v-card>
                    </v-col>

                  </v-window-item>
                </v-window>
                </v-col>
                <v-item-group
                  v-model="window"
                  class="shrink mr-6"
                  mandatory
                  tag="v-flex"
                >
                  <v-item
                    v-for="n in 3"
                    :key="n"
                    v-slot:default="{ active, toggle }"
                  >
                    <div>
                      <v-btn
                        :input-value="active"
                        icon
                        @click="toggle"
                      >
                        <v-icon>mdi-record</v-icon>
                      </v-btn>
                    </div>
                  </v-item>
                </v-item-group>
            </v-row>
            </v-container>
            </v-tab-item>
            <v-tab-item>
            <v-container>
            <div>
               <v-row justify="space-around">
                  <v-row justify="space-around">
                    <v-col cols="12">
                    <v-container>
                      <header>Advertising time frame</header>
                      <date-range-picker
                          ref="picker"
                          :locale-data="{ firstDay: 1, format: 'YYYY-MM-DD' }"
                          opens="left"
                          :autoApply="true"
                          v-model="dateRange"
                        >
                        <div slot="input" slot-scope="picker" style="min-width: 350px;">
                              {{ dateRanges.startDate  }} - {{ dateRanges.endDate }}
                        </div>
                      </date-range-picker>
                      </v-container>
                    </v-col>
                    <v-col cols="12">
                    <v-container>
                      <v-btn :loading="changeActivityOn" v-if="post.IsActive" @click="changeActivity">Stop campaign</v-btn>
                      <v-btn :loading="changeActivityOn" v-else @click="changeActivity">Continue campaign</v-btn>
                    </v-container>
                    <v-divider></v-divider>
                    <v-btn :loading="updatingOn" @click="updateAdvert">Save changes</v-btn>
                    </v-col>
                   </v-row>
                </v-row>
             </div>
             </v-container>
            </v-tab-item>
          </v-tabs-items>
        </v-card>
            </b-col>
          </b-row>
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
import DateRangePicker from 'vue2-daterange-picker'
import api from '../../services/api'
import moment from 'moment'
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
          IsLiked:false,
          tab: null,
          success:true,
          length: 3,
          window: 0,
          appearance:1,
          dateRange:{
            startDate:this.post.CampaignTimestart,
            endDate:this.post.CampaignTimeend
          },
          changeActivityOn:false,
          updatingOn:false
        }
      },
  components:{
      DateRangePicker,
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
        dateRanges(){
        var s=new Date()
        var e=new Date(this.dateRange.endDate)
        return{
          startDate:moment(this.dateRange.startDate).format('YYYY-MM-DD'),
          endDate:moment(this.dateRange.endDate).format('YYYY-MM-DD')
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
    async changeActivity(){
      this.post.IsActive=!this.post.IsActive
      this.changeActivityOn=true
      await api.post('post/updateAd/',{ID:this.post.ID,IsAdvert:true,IsActive:this.post.IsActive, CampaignTimestart:this.dateRange.startDate, CampaignTimeend:this.dateRange.endDate})
        .then((response)=>{
          this.$store.commit('post/updateAd',response)
          this.changeActivityOn=false
        })

    },
    async updateAdvert(){
      this.updatingOn=true
      console.log(this.post)
      this.post.IsActive=this.post.IsActive
      await api.post('post/updateAd/',{ID:this.post.ID,IsAdvert:true,IsActive:this.post.IsActive, CampaignTimestart:this.dateRange.startDate, CampaignTimeend:this.dateRange.endDate})
        .then((response)=>{
          this.$store.commit('post/updateAd',response)
        this.updatingOn=false
      })

    },

    }
};

  </script>
  <style>
  .img
  {
  width:"50px"

  }
  </style>
