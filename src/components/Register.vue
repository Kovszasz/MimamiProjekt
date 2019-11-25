<template>
<div>
    <Navbar :hideNavDrawer="true" />
      <RegisterCore/>
  </div>
</template>
<script>
import Navbar from './Navbar.vue'
import RegisterCore from './RegisterCore.vue'

  export default {
    name: 'register',
    components: {
        Navbar,
        RegisterCore
    },
    props:{
      IsEmbed:Boolean

    },
    data () {
      return {
        first_name: '',
        last_name: '',
        email: '',
        username: '',
        password: '',
        confirm: '',
        show1: false,
        show2: true,
        show3: false,
        show4: false,
      //  IsEmbed:true,
       rules: {
         required: value => !!value || 'Required.',
         min: v => v.length >= 8 || 'Min 8 characters',
         emailMatch: () => ('The email and password you entered don\'t match'),
      }
      }
    },
    methods: {
      registerUser () {
        this.$store.dispatch('authentication/registerUser', {
          first_name: this.first_name,
          last_name:this.last_name,
          email: this.email,
          username: this.username,
          password: this.password,
          IsAdvertiser:true
        }).then(() => {
          this.$router.push({ name: 'login' })
        })
      }
    }
  }
</script>
