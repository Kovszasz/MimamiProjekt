<template>
  <div>
  <v-app-bar app>
    <v-toolbar-title><router-link :to = "{ name:'home' }" class="title">mimami</router-link></v-toolbar-title>
    <!--<v-switch v-model="switch1" inset ></v-switch>-->
    <v-spacer></v-spacer>
    <v-text-field
    class="mx-4"
    flat
    hide-details
    label="Search"
    solo-inverted
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
          <v-list-item ><v-list-item-title><router-link :to = "{ name:'messages' }" class="dropdown-item">Message</router-link></v-list-item-title></v-list-item>
          <v-list-item v-if="!IsAuthenticated "><v-list-item-title><router-link :to = "{ name:'register' }" class="dropdown-item">Register</router-link></v-list-item-title></v-list-item>
          <v-list-item v-if="!IsAuthenticated "><v-list-item-title><router-link :to = "{ name:'editor' }" class="dropdown-item">Editor</router-link></v-list-item-title></v-list-item>
          <v-list-item v-if="!IsAuthenticated "><v-list-item-title><router-link :to = "{ name:'login' }" class="dropdown-item">LogIn</router-link></v-list-item-title></v-list-item>
          <v-list-item v-if="user.is_staff "><v-list-item-title><router-link :to = "{ name:'moderate' }" class="dropdown-item">Moderating</router-link></v-list-item-title></v-list-item>
          <v-list-item v-if="user.is_superuser "><v-list-item-title><router-link :to = "{ name:'statistics' }" class="dropdown-item">Statistics</router-link></v-list-item-title></v-list-item>
          <v-list-item v-if="IsAuthenticated "><v-list-item-title><router-link :to = "{ name:'logout' }" class="dropdown-item">LogOut</router-link></v-list-item-title></v-list-item>
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
          <v-list-item-group color="#b12233">
            <v-list-item>
              <v-list-item-avatar >
                <v-img src="@/assets/top.png"></v-img>
              </v-list-item-avatar>
              <v-list-item-content>
                <v-list-item-title >Top memes</v-list-item-title>
              </v-list-item-content>
            </v-list-item>
            <v-list-item v-if="IsAuthenticated ">
              <v-list-item-avatar >
                <v-img src="@/assets/mymeme.png"></v-img>
              </v-list-item-avatar>
              <v-list-item-content  >
            <v-list-item-title> <v-btn text :to = "{ name:'mypost', params:{user:user.username } }">
                  MyMemes
              </v-btn></v-list-item-title>
              </v-list-item-content>
            </v-list-item>
            <v-list-item v-if="IsAuthenticated ">
              <v-list-item-avatar >
              <v-icon color="#fe5552" >mdi-thumb-up</v-icon>
              </v-list-item-avatar>
              <v-list-item-content  >
            <v-list-item-title> <v-btn text :to = "{ name:'mypost', params:{user:user.username } }">
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
               <v-img :src="IMGurl(c.profile)"></v-img>
              </v-list-item-avatar>
              <v-list-item-content>
                <v-list-item-title ><v-btn :to = "{ name:'mypost', params:{user:c.channel.username } }">{{ c.channel.username }}</v-btn></v-list-item-title>
              </v-list-item-content>
            </v-list-item>
          </v-list-item-group>
          </v-list>
        </v-card>
      </v-navigation-drawer>
    </div>

</template>
<script>

import { mapState, mapActions } from 'vuex'
import Vue from 'vue';
import MemeEditor from './MemeEditor';
import {NavbarPlugin} from 'bootstrap-vue';
Vue.use(NavbarPlugin);
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
    User:'User'
    }
  },
  components: {
      MemeEditor
  }, computed:{ ...mapState('authentication',{IsAuthenticated:'login',user:'user',IsAdmin:'is_superuser'})},
  methods:{
  IMGurl:function(img){
          return require(`../assets${img.avatar}`)
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
