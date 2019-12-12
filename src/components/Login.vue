<template>
<div>
  <Navbar :hideNavDrawer="true"></Navbar>
  <LoginCore/>
</div>
</template>

<script>
//import { mapState, mapActions } from 'vuex'
import Navbar from './Navbar.vue'
import LoginCore from './LoginCore.vue'
  export default {
    name: 'login',
    components: {
        Navbar,
        LoginCore
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
    async loginUser () { // call loginUSer action
        await this.$store.dispatch('authentication/loginUser', {
          username: this.username,
          password: this.password
        }).then(() => {
              this.wrongCred = false
              async (()=>{
                this.$store.commit('post/emptyPostStorage')
              }).then(this.$router.push({ name: 'home' }))
            })
          .catch(err => {
            //console.log(err)
            this.wrongCred = true // if the credentials were wrong set wrongCred to true
          })
        }
      }
  }
</script>
