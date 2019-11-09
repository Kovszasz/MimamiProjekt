<template>
  <div v-observe-visibility="{
                  callback:visibilityChanged,
                  once: true,
                  throttle: 10000
                  }" >
      <p>{{ ViewAdded }}{{ ad.ID }}</p>
      <template v-if="ad!=null" @click="clicked">

      <v-carousel
        height="80%"
        hide-delimiters
        :show-arrows="false"
          cycle
          >
    <v-carousel-item
      v-for="subpost in ad.imgs"
      :key="KeyGenerator(subpost.index)"
      :src="IMGurl(subpost)"
      interval="1000"
    >
      </v-carousel-item>
      </v-carousel>

    </template>
  </div>
</template>

<script>
import { mapState, mapActions , mapGetters} from 'vuex'
import Vue from 'vue'
import { ObserveVisibility } from 'vue-observe-visibility'

Vue.directive('observe-visibility', ObserveVisibility)

export default {
  name: 'Advert',
  props:{
    SingleAd:{
      type:Object,
      default:function(){
        return{
          ID:'',
          AdURL:''
          }
      }
    }

  },
  data: function(){
  return{
    ViewAdded:'NotSeen',
    Clicked:'NotClicked'
    //ad:{ID:''}
  }

  },
    resolve: {
    alias: {
    'vue$': 'vue/dist/vue.esm.js'
    }
  },
  computed:{ ...mapState({
    IsAuthenticated:'authentication/login'
  }),
  ...mapGetters({
    adpool: 'post/advert_in',

  }),
    ad:function(){
      if(this.SingleAd.ID==''){
      var n=this.randomgenerator(this.adpool.length,0.5)
        if (n!=-1){
            return this.adpool[n]
        }else{
            return {
                ID:'',
                AdURL:'',
                imgs:[]
            }
        }

    }else{
      return this.SingleAd

    }
    }

  },
methods:{...mapActions({
        addPost:'post/addPost',
        viewAd:'post/viewAd',
        clickAd:'post/clickAd',
      //  getAd:'post/randomgenerator'
        }),
        randomgenerator(length,Frequency){
            if(Math.random()<Frequency){
                return Math.round(Math.random()*length)
            }
              return -1
        }
        ,
          visibilityChanged(isVisible){
          if(isVisible){
              if(this.IsAuthenticated){
                  this.$store.dispatch('post/viewAd',{post:this.ad.ID,type:'View'})
                  this.ViewAdded='Seen'
                  }
          }else{
              this.ViewAdded='NotSeen'
          }
        },
          clicked:function(){
            if(this.IsAuthenticated){
                this.$store.dispatch('post/clickAd',{post:this.ad.ID,type:'Click'})
          }
            window.open(`${this.ad.AdURL}`, "_blank");
            this.Clicked='Clicked'
          },IMGurl:function(img){
                  return require(`../assets${img.IMG_url.replace('http://localhost:8000','')}`)
                  },
        KeyGenerator:function(index){
            return this.ad.ID+String(index)
        }
  }
,
created() {

},components:{
  ObserveVisibility
}
}
</script>
