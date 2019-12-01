<template>
  <div>
  <v-app-bar app>
    <v-toolbar-title><p @click="goHome" class="title">mimami</p></v-toolbar-title>
    <!--<v-switch v-model="switch1" inset ></v-switch>-->
    <v-spacer></v-spacer>
    <v-text-field
    class="mx-4"
    flat
    hide-details
    label="Search"
    v-model="search_field"
    solo-inverted
    v-on:keyup.enter="search()"
  ></v-text-field>
    <MemeEditor v-if="IsAuthenticated" />
    <v-spacer v-if="!IsAuthenticated"></v-spacer>
    <v-menu bottom >
      <template v-slot:activator="{ on }">
        <v-btn icon v-on="on">
          <img src="@/assets/settings.png" height="40%" width="40%">
        </v-btn>
      </template>
      <v-list>
          <v-list-item v-if="!IsAuthenticated "><v-list-item-title><router-link :to = "{ name:'register' }" class="dropdown-item">Register</router-link></v-list-item-title></v-list-item>
          <v-list-item v-if="!IsAuthenticated "><v-list-item-title><router-link :to = "{ name:'editor' }" class="dropdown-item">Editor</router-link></v-list-item-title></v-list-item>
          <v-list-item v-if="!IsAuthenticated "><v-list-item-title><router-link :to = "{ name:'login' }" class="dropdown-item">LogIn</router-link></v-list-item-title></v-list-item>
          <template v-if="IsAuthenticated">
            <v-list-item v-if="user.is_staff "><v-list-item-title><router-link :to = "{ name:'moderate' }" class="dropdown-item">Moderating</router-link></v-list-item-title></v-list-item>
            <v-list-item v-if="user.is_superuser "><v-list-item-title><router-link :to = "{ name:'statistics' }" class="dropdown-item">Statistics</router-link></v-list-item-title></v-list-item>
            <v-list-item v-if="user.is_advertiser"><v-list-item-title><router-link :to = "{ name:'advert',params:{user:user.username } }" class="dropdown-item">Advert</router-link></v-list-item-title></v-list-item>
            <v-list-item ><v-list-item-title><router-link :to = "{ name:'account'}" class="dropdown-item">Account</router-link></v-list-item-title></v-list-item>
            <v-list-item ><v-list-item-title class="dropdown-item" @click="logout" >LogOut</v-list-item-title></v-list-item>
          </template>
      </v-list>
    </v-menu>
    </v-app-bar>
    <v-navigation-drawer
      v-if="!hideNavDrawer"
      right
      permanent
      baseline
      fixed
      class="sidemenu"
    >
      <v-card
        class="mx-auto"
        max-width="400"
        tile
      >
        <v-list avatar rounded >
          <v-subheader>Main</v-subheader>
          <template v-slot:prepend v-if="IsAuthenticated">
              <v-list-item two-line>
                <v-list-item-avatar>
                    <img src="https://randomuser.me/api/portraits/women/81.jpg">
                </v-list-item-avatar>
                <v-list-item-content>
                    <v-list-item-title>Jane Smith</v-list-item-title>
                    <v-list-item-subtitle>Logged In</v-list-item-subtitle>
                  </v-list-item-content>
                  </v-list-item>
                  </template>
          <v-list-item-group color="#b12233">
            <v-list-item>
              <v-list-item-avatar >
                <v-img src="@/assets/top.png"></v-img>
              </v-list-item-avatar>
              <v-list-item-content>
                <v-list-item-title ><v-btn text :to = "{ name:'mypost', params:{type:'top' } }">

                Top memes
                </v-btn></v-list-item-title>
              </v-list-item-content>
            </v-list-item>
            <v-list-item v-if="IsAuthenticated ">
              <v-list-item-avatar >
                <v-img src="@/assets/mymeme.png"></v-img>
              </v-list-item-avatar>
              <v-list-item-content  >
            <v-list-item-title> <v-btn text :to = "{ name:'mypost', params:{type:user.username } }">
                  MyMemes
              </v-btn></v-list-item-title>
              </v-list-item-content>
            </v-list-item>
            <v-list-item v-if="IsAuthenticated ">
              <v-list-item-avatar >
              <v-icon color="#fe5552" >mdi-thumb-up</v-icon>
              </v-list-item-avatar>
              <v-list-item-content  >
            <v-list-item-title> <v-btn text :to = "{ name:'mypost', params:{type:'liked' } }">
                  Liked
              </v-btn></v-list-item-title>
              </v-list-item-content>
            </v-list-item>
          </v-list-item-group>
          </v-list>
        </v-card>
        <v-card
          class="mx-auto"
          max-width="400"
          tile
        >
        <v-list v-if ="IsAuthenticated" avatar rounded >
          <v-subheader>Favourites</v-subheader>
          <v-list-item-group color="#b12233">
          <v-list-item
              v-for="(c, i) in user.channel"
              :key="i"
            >
              <v-list-item-avatar >
               <v-img :src="IMGurl(c.channel)"></v-img>
              </v-list-item-avatar>
              <v-list-item-content>
                <v-list-item-title ><v-btn :to = "{ name:'mypost', params:{type:c.channel.username } }">{{ c.channel.username }}</v-btn></v-list-item-title>
              </v-list-item-content>
            </v-list-item>
          </v-list-item-group>
          </v-list>
        </v-card>
      </v-navigation-drawer>
      <v-row justify="center">
    <v-dialog v-model="dialog" width="800px">
      <v-card>
        <v-card-title>
          <span class="headline">Results</span>
        </v-card-title>
          <template v-for='res in search_result'>
          <meme_post
            v-bind:post="res"
              v-bind:key="res.ID"
          ></meme_post>
          </template>
      </v-card>
      <v-skeleton-loader
  ref="skeleton"
    :boilerplate="false"
    type="article"
    class="mx-auto"
  ></v-skeleton-loader>
    </v-dialog>
  </v-row>
    </div>

</template>
<script>

import { mapState, mapActions, mapGetters } from 'vuex'
import Vue from 'vue';
import MemeEditor from './MemeEditor';
import {NavbarPlugin} from 'bootstrap-vue';
import meme_post from './MemePost.vue';
Vue.use(NavbarPlugin);
import api from '../services/api'
export default {
  name: 'Navbar',
  props:{
  hideNavDrawer:{
  type:Boolean,
  default:false
  }
  },
  data(){
    return{
    search_field:'',
    search_result:[],
    dialog:false
    }
  },
  components: {
      MemeEditor,
      meme_post
  }, computed:{ ...mapState('authentication',{
          IsAuthenticated:'login',
          IsAdmin:'is_superuser'}),
          ...mapGetters('authentication',{
          user:'user'
      })
  },
  methods:{
  IMGurl:function(img){
          return require(`../assets${img.avatar}`)
          },
    async search(){
        this.dialog=true
        let api_url = '/spotlight/';
        this.loading = true;
        if(this.search_field!==''||this.search_term!==null) {
          api_url = `/spotlight/?search=${this.search_field}`
        }
        await api.get(api_url)
            .then((response) => {
              this.search_result = response.data;
              this.loading = false;
              api.post('/spotlight/',{term:this.search_field,result:response.data})
            })
            .catch((err) => {
              this.loading = false;
              console.log(err);
            })
    },logout(){
      this.$store.dispatch('authentication/logoutUser')
      .then(() => {
        async (()=>{
          this.$store.dispatch('post/getTimeLine')
        }).then(this.$route.go())

      })
    },
    async goHome(){
    try{
        await this.$store.dispatch('post/getTimeLine')
        .then(this.$router.push({ name: 'home' }))
    }catch{

    }
    }
  },
  beforeCreate(){
    //this.$store.dispatch('authentication/updateUser')

  },

};
</script>
<style>
.title {
  font-size: 300px;
	font-weight: 900;
  background: -webkit-linear-gradient(right,#fe9a22, #fe5552);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
  .sidemenu{
  margin-top:80px;

  }
</style>
