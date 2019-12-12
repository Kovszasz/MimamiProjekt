<!-- https://www.trell.se/blog/file-uploads-json-apis-django-rest-framework/-->
<template>
<div>

  <v-content v-if="!core">
  <h1>{{ choose }} is remained</h1>
  <v-row align="center">
    <v-item-group
      v-model="window"
      class="shrink mr-6"
      mandatory
      tag="v-flex"
    >
      <v-item
        v-for="n in length"
        :key="n"
        v-slot:default="{ active, toggle }"
      >
        <div>
          <v-btn
            :input-value="active"
            icon
            @click="toggle"
          >
            <v-icon>mdi-record</v-icon>
          </v-btn>
        </div>
      </v-item>
    </v-item-group>

        <v-col>
          <v-window
            v-model="window"
            class="elevation-1"
            vertical
          >
          <v-window-item>
          <v-container class="grey lighten-5">
    <v-row no-gutters>
        <v-col >
          <v-card
            class="pa-2"
            outlined
            tile
          >
          <picture-input
            ref="pictureInput"
            :prefill="prefill"
            @change="onChange"
            max-width="800"
            max-height="800"
            margin="16"
            accept="image/jpeg,image/png,image/gif"
            size="10"
            buttonClass="btn"
            :zIndex="0"
            radius="50"
            :customStrings="{
              upload: '<h1>Bummer!</h1>',
              drag: 'Upload profile picture'
            }">
          </picture-input>

          </v-card>
        </v-col>
        <v-col >
          <v-card
            class="pa-2"
            outlined
            tile
          >
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
          <v-container>
            <header>Birthday</header>
            <datepicker v-model="birthday.date" :bootstrap-styling="true">
              <div slot="beforeCalendarHeader" class="calender-header">
                Birthday
              </div>
            </datepicker>
            </v-container>
          </v-card>
        </v-col>

        </v-row>
          </v-container>
          </v-window-item>
            <v-window-item>
              <v-card flat>
              <template v-for ="index in postsize">
              <v-row v-bind:key="index+'_row'">
                <v-col
                  v-for="i in 4"
                  v-bind:key="index*4+i+'_col'"
                  cols="12"
                  md="3"
                >
                <v-hover>
                  <template v-slot:default="{ hover }">
                  <div>
                  <meme_post v-if="postindex((index-1)*4+(i-1))" :post="postindex((index-1)*4+(i-1))" :IsRegistration="true" :width="200" :height="250" />
                  <v-fade-transition>
                      <v-overlay
                          v-if="hover"
                          absolute
                          color="#036358"
                          >
                            <v-btn @click.native="chooseMeme((index-1)*4+(i-1))">Like</v-btn>
                        </v-overlay>
                  </v-fade-transition>
                  </div>
                  </template>
                  </v-hover>
                  </v-col>
                </v-row>
                </template>
              </v-card>
            </v-window-item>
          </v-window>
        </v-col>
  </v-row>
  <div class="text-center">
   <v-bottom-sheet v-model="disabled">
     <v-sheet class="text-center" height="100px">
       <v-btn
         class="mt-6"
         flat
         color="green"
          @click="completeRegistration">
       Finish
       </v-btn>
       <div>The registration is completed enjoy Mimami</div>
     </v-sheet>
   </v-bottom-sheet>
 </div>
  </v-content>
  <v-content v-if="core">
  <v-col >
    <v-card
      class="pa-2"
      outlined
      tile
    >
    <v-text-field
      v-model="username"
      :counter="30"
      label="Username"
      data-vv-name="username"
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
    <v-checkbox v-model="agreed" class="mx-2" label="Agree" ></v-checkbox><a @click="terms = true">Terms & Conditions</a>
  <v-btn class="mr-4" @click="registerUser" :disabled="!agreed">Register</v-btn>
  <v-btn class="mr-4" @click="" >Register with Facebook</v-btn>
  <v-btn class="mr-4" @click="" >Register with Google</v-btn>

    </v-card>
  </v-col>

  </v-content>
  <v-dialog v-model="terms" width="600px">
    <v-card>
      <v-card-title>
        <span class="headline">Use Google's location service?</span>
      </v-card-title>
      <v-card-text></v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="green darken-1" text @click="agreeTerms">Agree</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
  </div>
</template>
<script>
import { mapState, mapActions, mapGetters } from 'vuex'
import PictureInput from 'vue-picture-input'
import meme_post from './MemePost.vue';
import Datepicker from 'vuejs-datepicker';
import moment from 'moment'
export default {
    name: 'RegisterCore',
    props:{
    core:{
      type:Boolean,
      default:true
    },
    user:{
    type:Object,
    default(){
      return{
        username:''
      }
    }
    }
    },
    components: {
    meme_post,
    PictureInput,
     Datepicker
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
        overlay:[],
        sheet: false,
        birthday: new Date(),
        e1: 0,
       rules: {
         required: value => !!value || 'Required.',
         min: v => v.length >= 8 || 'Min 8 characters',
         emailMatch: () => ('The email and password you entered don\'t match'),
      },
      choose:2,
      memes:[],
      disabled:false,
      agreed:false,
      terms:false,
      length: 2,
      window: 0,
      page:1
      }
    },
    methods: {
      async completeRegistration () {
          console.log(moment(this.birthday).format('YYYY-MM-DD'))
      await this.$store.dispatch('authentication/completeUserRegistration', {user:{
          first_name: this.first_name,
          last_name:this.last_name,
          is_advertiser:false,
          birthday:moment(this.birthday).format('YYYY-MM-DD'),
          meme:this.memes,
          },
          profile_pic:this.$refs.pictureInput.file
          }).then(() => {
              this.$router.push({name:'home'})
              })
            .catch(err => {
            })
          //await this.$store.dispatch('post/getTimeLine')

          }
      ,registerUser(){
        this.$store.dispatch('authentication/registerUser',{
          username:this.username,
          email:this.email,
          password:this.password
        }).then(() => {
          this.$router.push({ name: 'login' })
        })
      }

      ,
      chooseMeme(index){
        this.choose-=1
        if(this.choose==0){
            this.disabled=true
        }
        this.memes.push(this.posts[index].ID)

      },onChange (image) {
      if (image) {
        this.image = image
      } else {
      }
      },agreeTerms(){
        this.terms=false
        this.agreed=true
      }
      ,
      postindex(index){
        if(index<this.posts.length){
                return this.posts[index]
        }else{
          return false
        }
  },
  async scroll () {
      window.onscroll = () => {
        let bottomOfWindow = document.documentElement.scrollTop + window.innerHeight === document.documentElement.offsetHeight;
        if (bottomOfWindow) {
         this.$store.dispatch('post/getTimeLine',this.page)
            .then(()=>{
                this.page++
            })
        }
       }
  }
  ,IMGurl:function(img){
             if(img.avatar==''){
               return require(`../assets/logo.svg`)
             }else{
                     return require(`../assets${img.avatar}`)
             }
             },
  },computed:{ ...mapState({
    IsAuthenticated:'authentication/login'
  }),
  postsize(){
      return Math.round(this.posts.length/4)+1
  },...mapGetters({
        posts: 'post/timeline',
  }),prefill(){
      try{
        return this.IMGurl(this.$route.params.user)
      }catch{
        return this.IMGurl({avatar:''})
      }
  }

  },
  mounted(){

    this.scroll();

  },created(){
    this.scroll();
  }
}
</script>
