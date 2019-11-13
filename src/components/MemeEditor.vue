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
            <v-btn v-if="!advert" text @click="advert = !advert">Create advert</v-btn>
            <v-btn v-if="advert" text @click="advert = !advert">Create meme</v-btn>
            <v-btn  text @click="dialog = false">Save</v-btn>
            <v-btn v-if="!advert" text @click="sendMeme">Post</v-btn>
            <v-btn v-if="advert" text @click="sendMeme">Publish</v-btn>
          </v-toolbar-items>
        </v-toolbar>
        <b-container fluid class="bv-example-row">
          <b-row>
          <b-col cols="8">
              <b-card  header-tag="header" footer-tag="footer" >
                <template v-slot:header v-if="advert">

                </template>
                <template v-slot:header v-if="!advert">
                <v-text-field
                    v-model='postText'
                    placeholder="Post description"
                    filled
                    rounded
                    dense
                    >
                      <template v-slot:append-outer>
                          <v-dialog v-model="editor_dialog" >
                              <template v-slot:activator="{ on }">
                                <v-btn color="primary" dark v-on="on">Edit</v-btn>
                              </template>

                                  <ImgEditor></ImgEditor>
                                <v-card-actions>
                                  <v-spacer></v-spacer>
                                  <v-btn color="green darken-1" text @click="editor_dialog = false">Disagree</v-btn>
                                  <v-btn color="green darken-1" text @click="editor_dialog = false">Agree</v-btn>
                                </v-card-actions>
                            </v-dialog>
                                <v-switch v-model="IsPublic" label="Public"></v-switch>
                      </template>
                    </v-text-field>
                </template>
                <template v-if="!advert">
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
                      :prefill="imgSrc"
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
                </template>
                <template v-if="advert">
                <v-tabs
                  v-model="tab"
                  background-color="transparent"
                  grow
                >
                  <v-tab v-if="IsInlinePost" >
                    Post header advert
                  </v-tab>
                  <v-tab v-if="IsSinglePost">
                    Single post advert
                  </v-tab>
                </v-tabs>
                <v-tabs-items v-model="tab">
                <v-tab-item>
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
                </v-tab-item>
                <v-tab-item>
                <v-carousel
                  hide-delimiter-background
                  :show-arrows='MultipleImgsInLine'
                  :show-arrows-on-hover='MultipleImgsInLine'
                  :hide-delimiters='!MultipleImgsInLine'
                >
                  <v-carousel-item interval="0" v-for="(upload,index) in subIMGs" v-bind:key="upload">
                    <picture-input
                      ref="pictureInputInLine"
                      @change="onChangeInLine"
                      width="1024"
                      height="100"
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
                </v-tab-item>
                </v-tabs-items>
                </template>

                <template v-slot:footer >
                <v-combobox
                  v-model="chips"
                  :items="items"
                  chips
                  clearable
                  label="Meme labels"
                  multiple
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
              <v-card v-if="!advert">
                 <v-tabs
                   background-color="white"
                   color="deep-purple accent-4"
                   right
                 >
                   <v-tab>MyTemplates</v-tab>
                   <v-tab>Recycle</v-tab>
                   <v-tab>Browse</v-tab>

                   <v-tab-item
                   >
                     <v-container fluid>
                       <v-row>
                         <v-col
                           v-for="i in 6"
                           :key="i"
                           cols="12"
                           md="4"
                         >
                           <v-img
                             :src="`https://picsum.photos/500/300?image=${i * 1 * 10 + 10}`"
                             :lazy-src="`https://picsum.photos/10/6?image=${i * 1 * 5 + 10}`"
                             @click="getSrc(`settings.png`)"
                           ></v-img>
                         </v-col>
                       </v-row>
                     </v-container>
                   </v-tab-item>
                   <v-tab-item
                   >
                     <v-container fluid>
                       <v-row>
                         <v-col
                           v-for="i in 6"
                           :key="i"
                           cols="12"
                           md="4"
                         >
                           <v-img
                             :src="`https://picsum.photos/500/300?image=${i * 2 * 10 + 10}`"
                             :lazy-src="`https://picsum.photos/10/6?image=${i * 2 * 5 + 10}`"
                             @click="getSrc(`settings.png`)"
                           ></v-img>
                         </v-col>
                       </v-row>
                     </v-container>
                   </v-tab-item>
                   <v-tab-item
                   >
                     <v-container fluid>
                     <p>{{ user }}</p>
                     <template v-for="index in publicTemplates.length%3">
                       <v-row v-bind:key="index +'_row'">
                         <v-col
                          v-for="n in 3"
                          v-bind:key="index*3 + n+'col'"
                           cols="12"
                           md="4"
                         >
                           <v-img
                             :src="IMG_url(temp(index*3+n,'public'))"
                             :lazy-src="IMG_url(temp(index*3+n,'public'))"
                             @click="getSrc("IMG_url(temp(index*3+n,'public'))")"
                           ></v-img>
                         </v-col>
                       </v-row>
                       </template>
                     </v-container>
                   </v-tab-item>
                 </v-tabs>
               </v-card>
               <v-card v-if="advert">
               <v-container>
                  <v-row justify="space-around">
                    <v-col cols="12">
                      <header>Appearance</header>
                    </v-col>
                    <v-checkbox v-model="IsInlinePost" class="mx-2" label="Post header ad"></v-checkbox>
                    <v-checkbox v-model="IsSinglePost" class="mx-2" label="Single post ad"></v-checkbox>
                    <v-col cols="12">
                      <header>Advertising time frame</header>
                      <date-range-picker
                          ref="picker"
                          opens="left"
                          :autoApply="true"
                          v-model="dateRange"
                          @update="updateValues"
                          @toggle="checkOpen"
                        >
                        <div slot="input" slot-scope="picker" style="min-width: 350px;">
                              {{ picker.startDate  }} - {{ picker.endDate }}
                        </div>
                      </date-range-picker>
                    </v-col>
                    <v-col cols="12">
                      <header>Budget for the advert period</header>

                    <v-select
                      :items="dailyBudget"
                      label="please select a range"
                      dense
                      outlined
                        ></v-select>
                        </v-col>
                    <v-col cols="12">
                      <header>Website {{ adURL }}</header>
                      <v-text-field
                          v-model="adURL"
                          label="Url..."
                          outlined

                          ></v-text-field>
                    </v-col>
                    <h1>Reached users {{ reachedUsers }}</h1>
                   </v-row>
                </v-container>
               </v-card>
              </b-col>
            </b-row>
          </b-container>
      </v-card>
    </v-dialog>
    <v-row justify="center">
  </v-row>
  </v-row>
</template>

<script>
import { mapState, mapActions, mapGetters } from 'vuex'
import RegisterCore from './RegisterCore.vue'
import LoginCore from './LoginCore.vue'
import PictureInput from 'vue-picture-input'
import Template from './Template'
import DateRangePicker from 'vue2-daterange-picker'
import 'vue2-daterange-picker/dist/vue2-daterange-picker.css'
import axios from 'axios'
import ImgEditor from './ImgEditor.vue'
import { EventBus } from './memeeditor/event-bus.js';

  export default {
    data () {
      return {
        dialog: false,
        editor_dialog:false,
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
        postcreated:false,
        imgSrc:'',
        advert:false,
        dateRange:'',
        dailyBudget:[
          1000,
          10000,
          100000
        ],
        IsInlinePost:false,
        adURL:'',
        tab: null,
        inlineindex:0,
        imgsInLine:[],
        MultipleImgsInLine:false,
        IsSinglePost:true,
        appearance:1,
        template:''
      }
      },
      computed:{ ...mapState({
      //      IsAuthenticated:'authentication/accessToken'
          user:'authentication/user'
      }),reachedUsers(){
            return 8

      },...mapGetters({
        get_myTemplate:'post/myTemplates',
        get_browserTemplate:'post/publicTemplates',
        get_recycledTemplate:'post/recycledTemplates'

      }),
      getTemplate(index){
        return this.template[index]
      },
      myTemplates(){
        return this.get_myTemplate(this.user.username)
      },
      publicTemplates(){
        return this.get_browserTemplate
      },
      recycledTemplates(){
        return this.get_recycledTemplate
      }

      },
      components:{
          RegisterCore,
          LoginCore,
          PictureInput,
          Template,
          DateRangePicker,
          ImgEditor
      },
      methods:{...mapActions({
        addPost:'post/addPost',
        addMeme:'post/addMeme'

      }),
        onChange(){
          this.MultipleImgs=true
          console.log(this.$refs.pictureInput)
          this.imgs.push(this.$refs.pictureInput[this.imgindex])
          this.imgindex+=1
          this.subIMGs.push(this.imgindex)
        },onChangeInLine(){
          this.MultipleImgsInLine=true
          this.imgs.push(this.$refs.pictureInputInLine[this.inlineindex])
          this.inlineindex+=1
          this.subIMGs.push(this.inlineindex)
        },
        remove (item) {
        this.chips.splice(this.chips.indexOf(item), 1)
        this.chips = [...this.chips]
      },
      sendMeme(){
      console.log(this.$refs.picker)
        var id;
        if(!this.advert){
        id='Post'+String(Math.round(Math.random()*10000))
        this.addPost({ID:id,IsAdvert:false,description:this.postText,IsPublic:this.IsPublic,
                    labels:this.chips,
                    meme:{imgs:this.imgs,payload:{post:id,size:this.imgs.length}},size:this.imgs.length},true)
        this.$store.dispatch('post/getTimeLine')

        }else{
          if(this.IsInlinePost){
            console.log(this.$refs.picker)
              id='AdPost'+String(Math.round(Math.random()*10000))
              this.addPost({ID:id,AdURL:this.adURL,IsAdvert:true,IsInlinePost:true,AppearenceFrequency:this.appearance,labels:this.chips
                        ,meme:{imgs:this.imgs,payload:{post:id,size:this.imgs.length}},size:this.imgs.length},true)
          }
          if(this.IsSinglePost){
          console.log(this.$refs.picker)
              id='AdInPost'+String(Math.round(Math.random()*10000))
              this.addPost({ID:id,AdURL:this.adURL,IsAdvert:true,IsInlinePost:false,AppearenceFrequency:this.appearance,labels:this.chips
                        ,meme:{imgs:this.imgs,payload:{post:id,size:this.imgs.length}},size:this.imgs.length},true)
          }
        }
        this.postcreated=true
        this.dialog=false
      },
      getSrc(src){
          this.imgSrc=require(`../assets/${src}`)
          this.onChange()
          //this.imgSrc=''
      },
      updateValues(){


      },checkOpen(){


      },
      temp:function(index,type){
              if(type == 'public'){
                  return this.publicTemplates[index]
              }else if (type == 'my'){
                  return this.myTemplates[index]
              }else{
                  return this.recycledTemplates[index]
              }

        },IMGurl:function(img){
              return require(`../assets${img.IMG_url}`)
        },
      },
      watch:{
        uploadMeme:function(){
        }

      },
    beforeCreate(){
      this.$store.dispatch('post/getTemplate')
    },
    created(){
    EventBus.$on('new_meme', (data) => {
        //if(data.IsFile){
        //  console.log(data)
        //}
        console.log(data)
      })
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
