
<template>
  <div>
  <template>
    <v-content>
    <Navbar :hideNavDrawer="true" />
      v-content v-if="core">
      <v-col >
        <v-card
          class="pa-2"
          outlined
          tile
        >

        <v-text-field
                   v-model="password"
                   :rules="[rules.required, rules.min]"
                   :type="show1 ? 'text' : 'password'"
                   name="input-10-1"
                   label="Password"
                   hint="At least 8 characters"
                   counter
                   @click:append="show1 = !show1"
                   outlined
        ></v-text-field>
        <v-text-field
                  v-model="confirm"
                  :rules="[rules.required, rules.min]"
                  :type="show1 ? 'text' : 'password'"
                  name="input-10-1"
                  label="Password again"
                  hint="At least 8 characters"
                  counter
                  @click:append="show1 = !show1"
                  outlined
        ></v-text-field>
      <v-btn class="mr-4" @click="confimPassword" >Reset password</v-btn>
      </v-card>
      </v-col>
  </v-content>
  </template>
  </div>
</template>
<script>
import Navbar from './Navbar.vue'
import axios from 'axios'
  export default {
    name: 'ResetPassword',
    data () {
      return {
        password: '',
        confirm:'',
        rules: {
          required: value => !!value || 'Required.',
          min: v => v.length >= 8 || 'Min 8 characters',
          emailMatch: () => ('The email and password you entered don\'t match'),
       },

      }
    },
    methods: {
    async confimPassword() {
      await  axios.post('http://localhost:8000/account/users/reset_password_confirm/',{
        uid:this.$route.params.uid,
        token:this.$route.params.token,
        new_password: this.password,
        }).then(() => {
          this.$router.push({ name: 'login' })
        })
      },
  }

};
</script>
