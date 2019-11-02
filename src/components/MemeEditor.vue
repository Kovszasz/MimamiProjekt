<!--https://github.com/nhn/toast-ui.vue-image-editor-->
<template>
  <v-row justify="center">
    <v-dialog v-model="dialog" fullscreen hide-overlay transition="dialog-bottom-transition">
      <template v-slot:activator="{ on }">
        <v-btn c icon v-on="on"><img src="@/assets/add.png" height="40%" width="40%"/></v-btn>
      </template>

      <v-card>
        <v-toolbar >
          <v-btn icon dark @click="dialog = false">
            <v-icon>mdi-close</v-icon>
          </v-btn>
          <v-toolbar-title>Post meme</v-toolbar-title>
          <v-spacer></v-spacer>
          <v-toolbar-items>
            <v-btn  text @click="dialog = false">Save</v-btn>
            <v-btn  text @click="sendMeme">Post</v-btn>
          </v-toolbar-items>
        </v-toolbar>
        <b-container fluid class="bv-example-row">
          <b-row>
          <b-col cols="8">
              <b-card  header-tag="header" footer-tag="footer" >
                <template v-slot:header >
                <v-text-field
                    v-model='postText'
                    placeholder="Post description"
                    filled
                    rounded
                    dense
                    >
                      <template v-slot:append-outer>
                          <v-btn>Edit</v-btn>
                                <v-switch v-model="IsPublic" label="Public"></v-switch>
                      </template>
                    </v-text-field>
                </template>
                <v-carousel
                  hide-delimiter-background
                  :show-arrows='MultipleImgs'
                  :show-arrows-on-hover='MultipleImgs'
                  :hide-delimiters='!MultipleImgs'
                >
                  <v-carousel-item interval="0" v-for="(upload,index) in subIMGs" v-bind:key="upload">
                    <picture-input
                      ref="pictureInput"
                      @change="onChange"
                      width="1024"
                      height="600"
                      margin="16"
                      accept="image/jpeg,image/png,image/gif"
                      size="10"
                      buttonClass="btn"
                      :zIndex="0"
                      :customStrings="{
                        upload: '<h1>Bummer!</h1>',
                        drag: 'Drag a 😺 GIF or GTFO'
                      }">
                    </picture-input>
                  </v-carousel-item>
                </v-carousel>
                <template v-slot:footer >
                <v-combobox
                  v-model="chips"
                  :items="items"
                  chips
                  clearable
                  label="Meme labels"
                  multiple
                  prepend-icon="filter_list"
                  solo
                >
                  <template v-slot:selection="{ attrs, item, select, selected }">
                    <v-chip
                      v-bind="attrs"
                      :input-value="selected"
                      close
                      @click="select"
                      @click:close="remove(item)"
                    >
                      <strong>{{ item }}</strong>&nbsp;
                    </v-chip>
                  </template>
                </v-combobox>
                </template>
              </b-card>
              </b-col>
              <b-col cols="4">
              <Template/>
              </b-col>
            </b-row>
          </b-container>
      </v-card>


    </v-dialog>
  </v-row>
</template>

<script>
import { mapState, mapActions } from 'vuex'
import RegisterCore from './RegisterCore.vue'
import LoginCore from './LoginCore.vue'
import PictureInput from 'vue-picture-input'
import Template from './Template'
  export default {
    data () {
      return {
        dialog: false,
        notifications: false,
        sound: true,
        widgets: false,
        MultipleImgs:false,
        subIMGs:[0],
        imgs:[],
        IsPublic:false,
        chips: [],
        items: [],
        imgindex:0,
        postText:'',
        postcreated:false
      }
      },
      computed: mapState({
      //      IsAuthenticated:'authentication/accessToken'
      }),
      components:{
          RegisterCore,
          LoginCore,
          PictureInput,
          Template
      },
      methods:{...mapActions({
        addPost:'post/addPost',
        addMeme:'post/addMeme'

      }),
        onChange(){
          this.MultipleImgs=true
          this.imgs.push(this.$refs.pictureInput[this.imgindex])
          this.imgindex+=1
          this.subIMGs.push(this.imgindex)
        },
        remove (item) {
        this.chips.splice(this.chips.indexOf(item), 1)
        this.chips = [...this.chips]
      },
      sendMeme(){
        var id='Post'+String(Math.round(Math.random()*10000))
        this.addPost({post:{post:{ID:id,description:this.postText,IsPublic:this.IsPublic},labels:this.chips}
                      ,meme:{imgs:this.imgs,payload:{post:id,size:this.imgs.length}}},true)
        this.postcreated=true
        this.$store.dispatch('post/getTimeLine')
        this.dialog=false

      }
      },
      watch:{
        uploadMeme:function(){
          if ( this.postcreated){
            return this.addMeme({imgs:this.imgs,payload:{post:id,size:this.imgs.length}},true)
          }
        }

      }
    }

</script>
<style>
.color_line {
  background: -webkit-linear-gradient(right,#fe9a22, #fe5552);
  -webkit-text-fill-color: transparent;
}
.button {
  background: "#f6cbca";
  -webkit-text-fill-color: transparent;
}
</style>
