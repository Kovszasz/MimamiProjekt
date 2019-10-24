<template>
  <div>
  <v-app-bar app>
    <div><MemeEditor :IsAuthenticated="IsAuthenticated"/></div>
    <v-spacer></v-spacer>
    <v-toolbar-title><router-link :to = "{ name:'home' }" class="title">mimami</router-link></v-toolbar-title>
    <v-spacer></v-spacer>
    <div><v-menu bottom >
      <template v-slot:activator="{ on }">
        <v-btn icon v-on="on">
          <img src="@/assets/settings.png" height="40%" width="40%">
        </v-btn>
      </template>
      <v-list>
          <v-list-item ><v-list-item-title><router-link :to = "{ name:'messages' }" class="dropdown-item">Message</router-link></v-list-item-title></v-list-item>
          <v-list-item v-if="!IsAuthenticated "><v-list-item-title><router-link :to = "{ name:'register' }" class="dropdown-item">Register</router-link></v-list-item-title></v-list-item>
          <v-list-item v-if="!IsAuthenticated "><v-list-item-title><router-link :to = "{ name:'login' }" class="dropdown-item">LogIn</router-link></v-list-item-title></v-list-item>
          <v-list-item v-if="user.is_staff "><v-list-item-title><router-link :to = "{ name:'moderate' }" class="dropdown-item">Moderating</router-link></v-list-item-title></v-list-item>
          <v-list-item v-if="user.is_superuser "><v-list-item-title><router-link :to = "{ name:'statistics' }" class="dropdown-item">Statistics</router-link></v-list-item-title></v-list-item>
          <v-list-item v-if="IsAuthenticated "><v-list-item-title><router-link :to = "{ name:'mypost' }" class="dropdown-item">MyPosts</router-link></v-list-item-title></v-list-item>
          <v-list-item v-if="IsAuthenticated "><v-list-item-title><router-link :to = "{ name:'logout' }" class="dropdown-item">LogOut</router-link></v-list-item-title></v-list-item>
      </v-list>
    </v-menu></div>
    </v-app-bar>
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
  data(){
    return{
    }
  },
  components: {
      MemeEditor
  }, computed: mapState('authentication',{IsAuthenticated:'login',user:'user',IsAdmin:'is_superuser'})
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
</style>
