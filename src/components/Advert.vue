<template>
  <div v-observe-visibility="{
                  callback:visibilityChanged,
                  once: true,
                  throttle: 10000
                  }" >

      <div @click="clicked" >
          <p>{{ ViewAdded }}</p>
          <v-responsive :aspect-ratio="10/1">
            <img src="@/assets/media/post/adheader.png"/>
          </v-responsive>
      </div>
  </div>
</template>

<script>
import { mapState, mapActions , mapGetters} from 'vuex'
import Vue from 'vue'
import { ObserveVisibility } from 'vue-observe-visibility'

Vue.directive('observe-visibility', ObserveVisibility)

export default {
  name: 'Advert',
  data: function(){
  return{
    ViewAdded:'NotSeen',
    Clicked:'NotClicked',
    //ad:{ID:''}
  }

  },
    resolve: {
    alias: {
    'vue$': 'vue/dist/vue.esm.js'
    }
  },
  computed:{ ...mapState({
    IsAuthenticated:'authentication/accessToken'
  }),
  ...mapGetters({
    ad: 'post/advert'
  })

  },
methods: mapActions({
        addPost:'post/addPost',
        viewAd:'post/viewAd',
        clickAd:'post/clickAd',
        visibilityChanged(isVisible){
          if(isVisible){
              this.$store.dispatch('post/viewAd',{post:'AdPost1',type:'View'})
              this.ViewAdded='Seen'
          }else{
              this.ViewAdded='NotSeen'
          }
        },
        clicked:function(){
          this.$store.dispatch('post/clickAd',{post:'AdPost1',type:'Click'})
          window.open("https://dreher.hu", "_blank");
          this.Clicked='Clicked'
        }
})
,
created() {
//this.$store.dispatch('post/getAdvert/')
},components:{
  ObserveVisibility
}
}
</script>
