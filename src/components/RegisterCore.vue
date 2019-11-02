<!-- https://www.trell.se/blog/file-uploads-json-apis-django-rest-framework/-->
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
          <picture-input
            ref="pictureInput"
            @change="onChange"
            width="200"
            height="200"
            margin="16"
            accept="image/jpeg,image/png,image/gif"
            size="10"
            buttonClass="btn"
            :zIndex="0"
            radius="50"
            :customStrings="{
              upload: '<h1>Bummer!</h1>',
              drag: 'Drag a 😺 GIF or GTFO'
            }">
          </picture-input>

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
          </form>
          </v-container>
          </v-card>

        <v-btn
          color="primary"
          @click="e1 = 2"
        >
          Continue
        </v-btn>

      </v-stepper-content>

      <v-stepper-content step="2">
      <b-container class="bv-example-row overflow-auto">
      <h1>{{ choose }} is remained</h1>
    <template v-for="(p,index) in posts">
    <b-row >
      <b-col v-bind:key="p.ID">
        <meme_post @click.native="chooseMeme(p)" :post="p" :IsRegistration="true" :width="200" :height="250" />
    </b-col>
    </b-row>
    </template>
    </b-container>

        <v-btn
          color="primary"
          @click="e1 = 3"
          :disabled='disabled'
        >
          Continue
        </v-btn>

        <v-btn   @click="e1 = 1">Back </v-btn>
      </v-stepper-content>

      <v-stepper-content step="3">
        <v-card
          class="mb-12"
          color="grey lighten-1"
          height="200px"
        ></v-card>

        <v-btn
          color="primary"
          @click="e1 = 2"
        >
          Back
        </v-btn>
        <v-btn class="mr-4" @click="registerUser">Register</v-btn>
      </v-stepper-content>
    </v-stepper-items>
  </v-stepper>
  </v-content>
</template>
<script>
import { mapState, mapActions } from 'vuex'
import PictureInput from 'vue-picture-input'
import meme_post from './MemePost.vue';
  export default {
    name: 'RegisterCore',
    components: {
    meme_post,
    PictureInput
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
       rules: {
         required: value => !!value || 'Required.',
         min: v => v.length >= 8 || 'Min 8 characters',
         emailMatch: () => ('The email and password you entered don\'t match'),
      },
      choose:2,
      memes:[],
      disabled:true
      }
    },
    methods: {registerUser() {
    //https://alligator.io/vuejs/uploading-vue-picture-input/
        this.$store.dispatch('authentication/registerUser', {user:{
          first_name: this.first_name,
          last_name:this.last_name,
          email: this.email,
          username: this.username,
          password: this.password,
          mimeuser:{
            IsAdvertiser:true
            //profile_pic:'/media/profile/e2.png'
          }},meme:this.memes,
          profile_pic:this.$refs.pictureInput.file
        }).then(() => {
          this.$router.push({ name: 'login' })
        })
      },
      chooseMeme(post){
        this.choose-=1
        if(this.choose==0){
            this.disabled=false
        }
        this.memes.push(post)

      },onChange (image) {
      console.log('New picture selected!')
      if (image) {
        console.log('Picture loaded.')
        this.image = image
      } else {
        console.log('FileReader API not supported: use the <form>, Luke!')
      }
      }
  }
  ,
  computed:{ ...mapState({
    posts: state => state.post.timeline,
    IsAuthenticated:'authentication/login'
  }),

  },
}
</script>
