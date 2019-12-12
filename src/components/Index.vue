<template>
  <div>
    <Navbar v-if="user.complete_account"/>
    <Navbar v-if="!user.complete_account" :hideNavDrawer="true"/>
    <v-content v-if="pageloading">
    <v-skeleton-loader
      ref="skeleton"
      :boilerplate="false"
      type="article"
      class="mx-auto"
      ></v-skeleton-loader>
    </v-content>
    <v-content v-else>
    <v-container fluid>
    <v-row>
    <v-col  cols="9" >
    <template v-if="!IsAuthenticated">
    <v-row justify="center" no-gutters>
      <template v-for="(i,index) in timeline" >
        <div v-bind:key="index+'random_div_element'">
        <v-lazy v-bind:key="index+'lazy2'" v-model="isActive" :options="{ threshold: .5 }" transition="fade-transition">
          <meme_post
            v-bind:post="i"
              v-bind:key="i.ID"
          ></meme_post>
            </v-lazy>
            </div>
            <v-lazy v-bind:key="index+'lazy2ad'"  v-model="isActive" :options="{threshold: .5}" transition="fade-transition" v-if="index%5===0" >
              <advert v-if="ad!=null" :SingleAd="ad"></advert>
            </v-lazy>
          </template>
      </v-row>
      </template>
      <template v-if="IsAuthenticated">
        <div>
          <template v-if="!user.complete_account">
          <RegisterCore :core="false" :user="user"/>
         </template>
          <template v-if="user.complete_account">
          <v-row justify="center" no-gutters>
            <template v-for="(i,index) in timeline" >
              <div v-bind:key="index+'random_div_element2'">
              <v-lazy v-bind:key="index+'lazy1'" v-model="isActive" :options="{ threshold: .5 }" transition="fade-transition">
                <meme_post
                  v-bind:post="i"
                    v-bind:key="i.ID"
                ></meme_post>
                  </v-lazy>
                  </div>
                  <v-lazy v-bind:key="index+'lazy1ad'"  v-model="isActive" :options="{threshold: .5}" transition="fade-transition" v-if="index%5===0" >
                    <advert v-if="ad!=null" :SingleAd="ad"></advert>
                  </v-lazy>
                </template>
            </v-row>
            </template>
        </div>
      </template>
      </v-col>
      </v-row>
      </v-container>
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
  import RegisterCore from './RegisterCore.vue'
  //Vue.use(Navbar)
  export default {
    name: 'Index',
    components:{
     meme_post,
     comment_section,
     RegisterCore,
     Navbar,
     advert,
     },
    data: function(){
        return{
          isActive: false,
          text:'',
          pageloading:true,
          page:2
        }
    },
    resolve: {
      alias: {
        'vue$': 'vue/dist/vue.esm.js'
      }
    },
    computed:{
     ...mapGetters({
      IsAuthenticated:'authentication/IsAuthenticated',
      user:'authentication/user',
      timeline:'post/timeline',
      adpool:'post/advert',
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
    },
    async loadPage(){
      this.pageloading=true
    await this.$store.dispatch('comments/getComment')
    await this.$store.dispatch('post/getTimeLine',1)
    .then(this.pageloading=false)

    },
  async scroll () {
      window.onscroll = () => {
        let bottomOfWindow = document.documentElement.scrollTop + window.innerHeight === document.documentElement.offsetHeight;
        if (bottomOfWindow) {
         this.$store.dispatch('post/getTimeLine',this.page)
            .then(()=>{
                this.page++
            })
        }
       }
      }
    },mounted(){

      this.scroll();

    },created() {
      this.loadPage()

  /*    this.$store.subscribe((mutation, state) => {
        console.log(mutation.type)
        if (mutation.type === 'authentication/updateUser') {
            this.$store.dispatch('post/getTimeLine')
            this.$store.dispatch('post/getAction')
          }
      });*/
    },
  }
</script>
<style scope>
  .sidemenu{
  margin-top:80px;

  }
</style>
