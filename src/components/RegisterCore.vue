<template>
    <v-content>
  <v-stepper v-model="e1">
    <v-stepper-header>
      <v-stepper-step :complete="e1 > 1" step="1">Registration</v-stepper-step>

      <v-divider></v-divider>

      <v-stepper-step :complete="e1 > 2" step="2">Customization</v-stepper-step>

      <v-divider></v-divider>

      <v-stepper-step step="3">Validation</v-stepper-step>
    </v-stepper-header>

    <v-stepper-items>
      <v-stepper-content step="1">
        <v-card
           class="mx-auto"
           max-width="500"
           raised
         >
         <v-container>
          <form @submit.prevent="registerUser">
            <v-text-field
              v-model="first_name"
              :counter="30"
              label="First name"
              data-vv-name="first_name"
              outlined
            ></v-text-field>
            <v-text-field
              v-model="last_name"
              :counter="30"
              label="Last name"
              data-vv-name="last name"
              outlined
            ></v-text-field>
            <v-text-field
              v-model="email"
              label="E-mail"
              data-vv-name="email"
              required
              outlined
            ></v-text-field>
            <v-text-field
              v-model="username"
              :counter="30"
              label="Username"
              data-vv-name="username"
              outlined
            ></v-text-field>
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
            <!--<ImageUploader/>-->
            <v-btn class="mr-4" @click="registerUser">Register</v-btn>
          </form>
          </v-container>
          </v-card>

        <v-btn
          color="primary"
          @click="e1 = 2"
        >
          Continue
        </v-btn>

        <v-btn text>Cancel</v-btn>
      </v-stepper-content>

      <v-stepper-content step="2">
        <v-card
          class="mb-12"
          color="grey lighten-1"
          height="200px"
        ></v-card>

        <v-btn
          color="primary"
          @click="e1 = 3"
        >
          Continue
        </v-btn>

        <v-btn text>Cancel</v-btn>
      </v-stepper-content>

      <v-stepper-content step="3">
        <v-card
          class="mb-12"
          color="grey lighten-1"
          height="200px"
        ></v-card>

        <v-btn
          color="primary"
          @click="e1 = 1"
        >
          Continue
        </v-btn>

        <v-btn text>Cancel</v-btn>
      </v-stepper-content>
    </v-stepper-items>
  </v-stepper>
  </v-content>
</template>
<script>

  export default {
    name: 'RegisterCore',
    components: {
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
        e1: 0,
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
          mimeuser:{
            IsAdvertiser:true
          }
        }).then(() => {
          this.$router.push({ name: 'login' })
        })
      }
    }
  }
</script>
