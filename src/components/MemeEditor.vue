<!--https://github.com/nhn/toast-ui.vue-image-editor-->
<template>
  <v-row justify="center">
    <v-dialog v-model="dialog" fullscreen hide-overlay transition="dialog-bottom-transition">
      <template v-slot:activator="{ on }">
        <v-btn c icon v-on="on"><img src="@/assets/add.png" height="40%" width="40%"/></v-btn>
      </template>

      <v-card>
        <v-toolbar class="color_line">
          <v-btn icon dark @click="dialog = false">
            <v-icon>mdi-close</v-icon>
          </v-btn>
          <v-toolbar-title>Post meme</v-toolbar-title>
          <v-spacer></v-spacer>
          <v-toolbar-items>
            <v-btn class="button" text @click="dialog = false">Save</v-btn>
            <v-btn class="button" text @click="dialog = false">Post</v-btn>
          </v-toolbar-items>
        </v-toolbar>
        <v-row v-if="IsAuthenticated" md="6" cols="2">
        <b-card  header-tag="header" footer-tag="footer" >
          <label>Text</label><input type="text" >
          <v-carousel
            cycle
            height="480"
            width="1024"
            hide-delimiter-background
            show-arrows-on-hover
          >
            <v-carousel-item>
                <v-file-input
                  label="File input"
                  filled
                  prepend-icon="mdi-camera"
                ></v-file-input>
            </v-carousel-item>
          </v-carousel>
        </b-card>
        <v-divider vertical="true"></v-divider>
        </v-row>
        <div v-if="!IsAuthenticated">
        <h1> Sorry, you have to sign in, or sign up for posting</h1>
        <div v-if="!IsSignIn">
            <RegisterCore/>
                  <v-btn  class="mr-4" @click="ChangeSignin">
                         Sign In
                  </v-btn>
        </div>
        <div v-if="IsSignIn">
            <LoginCore/>
              <v-btn  class="mr-4" @click="ChangeSignin">
                    Register
              </v-btn>
        </div>
        </div>
      </v-card>


    </v-dialog>
  </v-row>
</template>

<script>
import { mapState, mapActions } from 'vuex'
import RegisterCore from './RegisterCore.vue'
import LoginCore from './LoginCore.vue'
  export default {
    props:{
    IsAuthenticated:Boolean

  },
    data () {
      return {
        dialog: false,
        notifications: false,
        sound: true,
        widgets: false,
        IsSignIn:true
      }
      },
      computed: mapState({
      //      IsAuthenticated:'authentication/accessToken'
      }),
      components:{
          RegisterCore,
          LoginCore
      },
      methods:{
          ChangeSignin:function(){
              this.IsSignIn=!this.IsSignIn
          }
      }
    }

</script>
<style>
.color_line {
  background: -webkit-linear-gradient(right,#fe9a22, #fe5552);
  -webkit-text-fill-color: transparent;
  z-index:-1;
}
.button {
  background: "#f6cbca";
  -webkit-text-fill-color: transparent;
}
</style>
