<template>
  <div>
  <v-app-bar app>
  <p>{{ theme }}</p>
    <v-toolbar-title><p @click="goHome" class="title">mimami</p></v-toolbar-title>
    <template v-if="IsAuthenticated">
        <v-switch v-if="themebool" label="Light" v-model="theme"></v-switch>
        <v-switch v-else label="Dark" v-model="theme"></v-switch>
    </template>
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
            <v-list-item v-if="user.is_advertiser"><v-list-item-title><router-link :to = "{ name:'advert',params:{user:user } }" class="dropdown-item">Advert</router-link></v-list-item-title></v-list-item>
            <v-list-item ><v-list-item-title><router-link :to = "{ name:'account'}" class="dropdown-item">Account</router-link></v-list-item-title></v-list-item>
            <v-list-item ><v-list-item-title class="dropdown-item" @click="logout" >LogOut</v-list-item-title></v-list-item>
          </template>
      </v-list>
    </v-menu>
    </v-app-bar>
    <v-navigation-drawer
      v-if="!hideNavDrawer"
      right
      :disable-resize-watcher="true"
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
            <v-list-item-title> <v-btn text :to = "{ name:'mypost', params:{type:'liked',user:user.username } }">
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
        <component
            hide-on-leave
            >
            <v-skeleton-loader
                v-if="loading"
                height="94"
                max-width="600"
                type="card"
              >
          </v-skeleton-loader>

        <v-card v-else flat>
          <template v-if="search_result" v-for='res in search_result'>
          <meme_post
            v-bind:post="res"
              v-bind:key="res.ID"
          ></meme_post>
          </template>
          <template v-else>
            <p>No item found</p>
          </template>
      </v-card>
      </component>
      </v-card>
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
import { EventBus } from './memeeditor/event-bus.js';
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
    dialog:false,
    loading:false,
    theme:false,
    }
  },
  components: {
      MemeEditor,
      meme_post
  }, computed:{ ...mapState('authentication',{
          IsAuthenticated:'login',
          IsAdmin:'is_superuser'}),
          ...mapGetters('authentication',{
          user:'user',
          //themebool:'style'
      }),
      themebool(){
        //this.theme=this.$store.state.authentication.user.DarkMode
        //return this.theme

      }
  },
  methods:{
  IMGurl:function(img){
          return require(`../assets${img.avatar}`)
          },
    async search(){

        if(this.search_field!=='') {
          console.log(this.search_field)
          this.dialog=true
          let api_url = '/spotlight/';
          this.loading = true;
          api_url = `/spotlight/?search=${this.search_field}`

        await api.get(api_url)
            .then((response) => {
              console.log(response.data.results)
              this.search_result = response.data.results;
              if(this.search_result.length==0){
                this.search_result=false
              }
              api.post('/spotlight/',{term:this.search_field,result:response.data})
              this.search_field=''
              this.loading = false;
            })
            .catch((err) => {
              this.loading = false;
              console.log(err);
            })
      }
    },logout(){
      this.$store.dispatch('authentication/logoutUser')
      .then(() => {
        async (()=>{
          this.$store.commit('post/emptyPostStorage')
          this.$store.dispatch('post/getTimeLine',1)
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
  created(){
      this.$vuetify.theme.dark = this.$store.state.authentication.user.DarkMode
      console.log(this.$store.state.authentication.user.DarkMode)
      console.log(this.$vuetify.theme.dark)

  },
  watch:{
    theme:function(){
      //EventBus.$emit('theme', {theme:this.themebool});
      //this.$store.dispatch('authentication/updateUser')
      api.get('users/changeTheme/')
        .then(()=>{
          this.$store.dispatch("authentication/changeTheme")
          window.location.reload()
        })
    }
  }


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
