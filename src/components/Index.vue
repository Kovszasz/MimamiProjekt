<template>
  <div>
    <Navbar/>
    <v-content>
    <b-col md="6" offset-md="3">
    <div  v-for="(i,index) in timeline" v-bind:key="i.id" >
      <div>
      <v-lazy v-model="isActive" :options="{ threshold: .5 }" transition="fade-transition">
        <meme_post
          v-bind:post="i"
        ></meme_post>
        </v-lazy>
      </div>
      <v-lazy v-model="isActive" :options="{threshold: .5}" transition="fade-transition" v-if="index%5===0" >
            <advert :SingleAd="ad"></advert>
      </v-lazy>
    </div>
      </b-col>
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
  import advert from './Advert.vue';
  //Vue.use(Navbar)
  export default {
    name: 'Index',
    components:{
     meme_post,
     comment_section,
     Navbar,
     advert
     },
    data: function(){
        return{
          isActive: false,
          text:''
        }
    },
    resolve: {
      alias: {
        'vue$': 'vue/dist/vue.esm.js'
      }
    },
    computed:{ ...mapState({
      timeline: state => state.post.timeline.reverse(),
      IsAuthenticated:'authentication/login'
    }),
    ...mapGetters({
      adpool:'post/advert'
    }),
    ad:function(){
      var n=this.randomgenerator(this.adpool.length,1)
        if (n!=-1){
            this.text=n
            return this.adpool[n]
        }else{
            return {
                ID:'',
                AdURL:'',
                imgs:[]

            }
        }
    }

    },
    methods:{ ...mapActions('post', [
      'addPost',
      'deletePost'
    ]),
    randomgenerator(length,Frequency){
        if(Math.random()<Frequency){
            return Math.round(Math.random()*length)
        }
          return -1
    }

    },
    beforeCreate() {
      this.$store.dispatch('post/getTimeLine')
      this.$store.dispatch('comments/getComment')
      this.$store.dispatch('post/getAction')
    }
    }
</script>
<style scope>
  .sidemenu{
  margin-top:80px;

  }
</style>
