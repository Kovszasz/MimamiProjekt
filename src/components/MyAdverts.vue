<template>
  <div>
    <Navbar :hideNavDrawer="true"/>
    <v-content>
    <div  v-for="i in timeline" v-bind:key="i.id"  class="justify-center pt-3">
      <div>
      <!--<v-lazy v-model="isActive" :options="{ threshold: .5 }" transition="fade-transition">-->
      <v-card class="d-inline-block mx-auto " max-height="700" >
            <AdStat   v-bind:post="i" >
            </AdStat>
        </v-card>
        <!--</v-lazy>-->
      </div>
    </div>
    </v-content>
  </div>
</template>
<script>
  import Vue from 'vue';
  import { NavbarPlugin } from 'bootstrap-vue'
  Vue.use(NavbarPlugin)
  import Navbar from './Navbar.vue'
  import { mapState, mapActions, mapGetters } from 'vuex'
  import AdStat from './statistics/AdStat.vue'
  //Vue.use(Navbar)
  export default {
    name: 'MyAdverts',
    props:{
        user:String,
    },
    components:{
     Navbar,
     AdStat
     },
    data: function(){
        return{
          isActive: false,
        }
    },
    resolve: {
      alias: {
        'vue$': 'vue/dist/vue.esm.js'
      }
    },
    computed:{ ...mapState({
      IsAuthenticated:'authentication/login',
      //user:'authentication/user'
    }),timeline:function(){
        return this.$store.state.post.advert//.filter(ad=>ad.user.username === this.user)
    }

    },
    methods:{ ...mapActions('post', [
      'addPost',
      'deletePost'
    ]),
      ...mapGetters({

      })

    },
    created() {
      //this.$store.dispatch('post/getTimeLine')
      //this.$store.dispatch('comments/getComment')
      //this.$store.dispatch('post/getAction')
    }
    }
</script>
<style scope>
  .sidemenu{
  margin-top:80px;

  }
</style>
