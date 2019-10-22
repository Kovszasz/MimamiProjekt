<template>
<div>
  <v-content>
<v-card
   class="mx-auto"
   max-width="500"
   raised
 >
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
    <!--<ImageUploader/>-->
    <v-btn class="mr-4" @click="loginUser">Login</v-btn>
  </form>
  </v-container>
  </v-card>
  </v-content>
</div>
</template>

<script>
//import { mapState, mapActions } from 'vuex'
  export default {
    name: 'LoginCore',
    components: {
    },
    props:{
      IsEmbed:Boolean
    },
    data () {
      return {
        username: '',
        password: '',
  //      IsEmbed:true,
        wrongCred: false // activates appropriate message if set to true
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
        }
      }
  }
</script>
