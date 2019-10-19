<template>
    <div id="app">
    <v-app>
      <router-view/>
    </v-app>
    </div>
</template>
<script>

//import { mapState } from 'vuex'
//import Vue from 'vue';
//import MemeEditor from './components/MemeEditor';
import Navbar from './components/Navbar';
//import {NavbarPlugin} from 'bootstrap-vue';
//Vue.use(NavbarPlugin);

export default {
  name: 'App',
  data(){
    return{
    }
  },
  components: {
    //  Index,
      Navbar
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
</style>
