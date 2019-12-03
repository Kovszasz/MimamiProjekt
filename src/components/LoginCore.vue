<template>
<div>
  <v-content>
<v-card
   class="mx-auto"
   max-width="500"
   raised
 >
 <h1>{{ fb }}</h1>
 <v-container>
  <form @submit.prevent="loginUser">
    <v-text-field
      v-model="username"
      label="Username"
      data-vv-name="username"
      outlined
    ></v-text-field>
    <v-text-field
               v-model="password"
               label="Password"
               outlined
    ></v-text-field>
    <v-btn class="mr-4" @click="loginUser">Login</v-btn>
    <!--<v-btn class="mr-4" @click="">Login via Facebook</v-btn>-->
    <v-facebook-login app-id="557410681489785" @login="loginFacebook"></v-facebook-login>
    <!--<GoogleLogin :params="params" :renderParams="renderParams" ></GoogleLogin>-->
    <v-btn class="mr-4" @click="reset= true ">Forgot password?</v-btn>
  </form>
  </v-container>
  </v-card>
  <v-row justify="center">
   <v-dialog v-model="reset" persistent max-width="600px">
     <v-card>
       <v-card-title>
         <span class="headline">Reset password</span>
       </v-card-title>
         <v-container>
           <v-row>
             <v-col cols="12">
               <v-text-field label="Email*" required v-model="reset_passwordEmail"></v-text-field>
             </v-col>
          </v-row>
          </v-container>
       <v-card-actions>
         <v-spacer></v-spacer>
         <v-btn color="blue darken-1" text @click="resetPassword">Save</v-btn>
       </v-card-actions>
     </v-card>
   </v-dialog>
 </v-row>
  </v-content>
</div>
</template>

<script>
//import { mapState, mapActions } from 'vuex'
import VFacebookLogin from 'vue-facebook-login-component'
import GoogleLogin from 'vue-google-login';

import axios from 'axios'
  export default {
    name: 'LoginCore',
    components: {
     VFacebookLogin,
      GoogleLogin
    },
    props:{
      IsEmbed:Boolean
    },
    data () {
      return {
        username: '',
        password: '',
        reset:false,
  //      IsEmbed:true,
        wrongCred: false, // activates appropriate message if set to true,
        reset_passwordEmail:'',
        params: {
          client_id: "1012380128036-o90dbehao1ff34lm547li3a9v0s2ku52.apps.googleusercontent.com"
        },
        renderParams: {
          width: 250,
          height: 50,
          longtitle: true
          },
          fb:''
      }
    },
    methods:{
      loginUser () { // call loginUSer action
        this.$store.dispatch('authentication/loginUser', {
          username: this.username,
          password: this.password
        }).then(() => {
              this.wrongCred = false
              this.$router.push({ name: 'home' })
            })
          .catch(err => {
            //console.log(err)
            this.wrongCred = true // if the credentials were wrong set wrongCred to true
          })
        },
        async resetPassword(){
          this.reset=false
        await  axios.post('http://localhost:8000/account/users/reset_password/',{email:this.reset_passwordEmail})
          .then(response=>{
              alert('check email')
          })
        },
        async loginFacebook(response){
          await this.$store.dispatch('authentication/socialLogin',response.authResponse.accessToken)
            .then(this.$router.push({ name: 'home' }))

        }
      }
  }
</script>
