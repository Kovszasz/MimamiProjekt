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
            <v-btn v-if="!advert" text @click="sendMeme" v-bind:disabled="porncontent">Post</v-btn>
            <v-btn v-if="advert" text @click="sendMeme" v-bind:disabled="porncontent">Publish</v-btn>
          </v-toolbar-items>
        </v-toolbar>
        <h1>{{ porncontents }}|{{ porncontent }}</h1>
        <b-container fluid class="bv-example-row" >
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
                              <v-container>
                              <v-card>
                                  <ImgEditor  v-bind:temp="editedTemplate"></ImgEditor>
                                <v-card-actions>
                                  <v-btn color="green darken-1" text @click="editor_dialog = false">Cancel</v-btn>
                                </v-card-actions>
                                </v-card>
                                </v-container>
                            </v-dialog>
                                <v-switch v-model="IsPublic" label="Public"></v-switch>
                      </template>
                    </v-text-field>
                </template>
                <template v-if="!advert">
                <v-carousel
                  width="100%"
                  height="100%"
                  hide-delimiter-background
                  :show-arrows='MultipleImgs'
                  :show-arrows-on-hover='MultipleImgs'
                  :hide-delimiters='!MultipleImgs'
                >
                  <v-carousel-item
                  interval="0" v-for="(upload,index) in subIMGs"
                  v-bind:key="index+'carouselmeme'"
                  v-if="!upload.isimg"
                  >
                    <picture-input

                      ref="pictureInput"
                      @change="onChange(index)"
                      :prefill="imgSrc"
                      :crop="false"
                      width="600"
                      height="600"
                      margin="16"
                      accept="image/jpeg,image/png,image/gif"
                      size="10"
                      buttonClass="btn"
                      :zIndex="0"
                      :customStrings="{
                        upload: '<h1>Bummer!</h1>',
                        drag: 'Upload meme',
                        remove: 'Remove Photo',
                      }">
                    </picture-input>
                    <p v-if="upload.isimg">{{ upload.img.width }}|{{ upload.img.height }}</p>
                  </v-carousel-item>
                  <v-carousel-item
                   v-for="(upload,index) in subIMGs" v-bind:key="index+'carouselmeme'"
                   v-if="upload.isimg"
                   interval="0"
                    :width=upload.img.width
                    :height=upload.img.height
                    :src="`${upload.img.src}`"
                  >
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
                  <v-carousel-item interval="0" v-for="(upload,index) in subIMGs" v-bind:key="index+'caruseladline'">
                    <picture-input
                      ref="pictureInput"
                      @change="onChange(index)"
                      :crop="false"
                      width="1024"
                      height="600"
                      margin="16"
                      accept="image/jpeg,image/png,image/gif"
                      size="10"
                      buttonClass="btn"
                      :zIndex="0"
                      :customStrings="{
                        upload: '<h1>Bummer!</h1>',
                        drag: 'Upload ad',
                        remove: 'Remove Photo',
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
                  <v-carousel-item interval="0" v-for="(upload,index) in subIMGs" v-bind:key="index+'carousel_ad'">
                    <picture-input
                      ref="pictureInputInLine"
                      @change="onChangeInLine(index)"
                      :crop="false"
                      width="1024"
                      height="100"
                      margin="16"
                      accept="image/jpeg,image/png,image/gif"
                      size="10"
                      buttonClass="btn"
                      :zIndex="0"
                      :customStrings="{
                        upload: '<h1>Bummer!</h1>',
                        drag: 'Upload ad',
                        remove: 'Remove Photo',
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
                <v-combobox
                  v-model="memetext"
                  chips
                  clearable
                  label="Meme text content"
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
                  v-model="templatetabs"
                   background-color="white"
                   color="deep-purple accent-4"
                   right
                 >
                   <v-tab :href="`#my`">MyTemplates</v-tab>
                   <v-tab :href="`#recycle`">Recycle</v-tab>
                   <v-tab :href="`#public`">Browse</v-tab>
                   <v-tab :href="`#search`">Search</v-tab>

                   <v-tab-item
                      value="my"
                   >
                   <v-container fluid>
                   <v-col
                    cols="12"
                    md="4">
                   <picture-input
                     ref="templateInput"
                     @change="templateUploading = true"
                     :crop="false"
                     width="400"
                     height="400"
                     margin="16"
                     accept="image/jpeg,image/png,image/gif"
                     size="10"
                     buttonClass="btn"
                     :zIndex="0"
                     :customStrings="{
                       upload: '<h1>Bummer!</h1>',
                       drag: 'Upload template',
                       remove: 'Remove Photo',
                     }">
                   </picture-input>
                   </v-col>
                       <template v-if="templates!=={}" v-for ="index in templates.my.size">

                             <v-row v-bind:key="index+'_row'">
                           <v-col
                             v-for="i in 3"
                             v-bind:key="index*3+i+'_col'"
                             cols="12"
                             md="4"
                           >
                           <v-hover>
                               <template v-slot:default="{ hover }">
                               <div>
                                 <v-img
                                     v-if="IMGurl((index-1)*3+(i-1),'my')"
                                     :src="IMGurl((index-1)*3+(i-1),'my')"
                                     :lazy-src="IMGurl((index-1)*3+(i-1),'my')"
                                     ></v-img>
                                   <v-fade-transition>
                                     <v-overlay
                                       v-if="hover"
                                       absolute
                                       color="#036358"
                                     >
                                       <v-btn @click="getSrc(IMGurl((index-1)*3+(i-1),'my'),index-1,'my')">Choose</v-btn>
                                     </v-overlay>
                                   </v-fade-transition>
                                   </div>
                               </template>
                             </v-hover>
                         </v-col>
                       </v-row>
                     </template>
                   </v-container>

                   </v-tab-item>
                   <v-tab-item
                      value="recycle"
                   >
                   <v-container fluid>
                       <template v-if="templates!=={}" v-for ="index in templates.recycle.size">
                             <v-row v-bind:key="index+'_row'">
                           <v-col
                             v-for="i in 3"
                             v-bind:key="index*3+i+'_col'"
                             cols="12"
                             md="4"
                           >
                           <v-hover>
                               <template v-slot:default="{ hover }">
                               <div>
                                 <v-img
                                     v-if="IMGurl((index-1)*3+(i-1),'recycle')"
                                     :src="IMGurl((index-1)*3+(i-1),'recycle')"
                                     :lazy-src="IMGurl((index-1)*3+(i-1),'recycle')"
                                     ></v-img>
                                   <v-fade-transition>
                                     <v-overlay
                                       v-if="hover"
                                       absolute
                                       color="#036358"
                                     >
                                       <v-btn @click="getSrc(IMGurl((index-1)*3+(i-1),'recycle'),index-1,'recycle')">Choose</v-btn>
                                     </v-overlay>
                                   </v-fade-transition>
                                   </div>
                               </template>
                             </v-hover>
                         </v-col>
                       </v-row>
                     </template>
                   </v-container>
                   </v-tab-item>
                   <v-tab-item
                      value="public"
                   >
                   <v-container fluid>
                       <template v-if="templates!=={}" v-for ="index in templates.public.size">
                             <v-row v-bind:key="index+'_row'">
                           <v-col
                             v-for="i in 3"
                             v-bind:key="index*3+i+'_col'"
                             cols="12"
                             md="4"
                           >
                           <v-hover>
                               <template v-slot:default="{ hover }">
                               <div>
                                 <v-img
                                     v-if="IMGurl((index-1)*3+(i-1),'public')"
                                     :src="IMGurl((index-1)*3+(i-1),'public')"
                                     :lazy-src="IMGurl((index-1)*3+(i-1),'public')"
                                     ></v-img>
                                   <v-fade-transition>
                                     <v-overlay
                                       v-if="hover"
                                       absolute
                                       color="#036358"
                                     >
                                       <v-btn @click="getSrc(IMGurl((index-1)*3+(i-1),'public'),index-1,'public')">Choose</v-btn>
                                     </v-overlay>
                                   </v-fade-transition>
                                   </div>
                               </template>
                             </v-hover>
                         </v-col>
                       </v-row>
                     </template>
                   </v-container>
                   </v-tab-item>
                   <v-tab-item
                      value="search"
                   >
                   <v-container fluid>
                   <v-text-field
                      class="mx-4"
                      v-model="templateSearch"
                        flat
                        hide-details
                        label="Search"
                        solo-inverted
                        v-on:keyup="searchTemplate"
                        ></v-text-field>
                       <template v-if="templates!=={}" v-for ="index in templates.search.size">
                             <v-row v-bind:key="index+'_row'">
                           <v-col
                             v-for="i in 3"
                             v-bind:key="index*3+i+'_col'"
                             cols="12"
                             md="4"
                           >
                           <v-hover>
                               <template v-slot:default="{ hover }">
                               <div>
                                 <v-img
                                     v-if="IMGurl((index-1)*3+(i-1),'search')"
                                     :src="IMGurl((index-1)*3+(i-1),'search')"
                                     :lazy-src="IMGurl((index-1)*3+(i-1),'search')"
                                     ></v-img>
                                   <v-fade-transition>
                                     <v-overlay
                                       v-if="hover"
                                       absolute
                                       color="#036358"
                                     >
                                       <v-btn @click="getSrc(IMGurl((index-1)*3+(i-1),'search'),index-1,'search')">Choose</v-btn>
                                     </v-overlay>
                                   </v-fade-transition>
                                   </div>
                               </template>
                             </v-hover>
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
                          :locale-data="{ firstDay: 1, format: 'YYYY-MM-DD' }"
                          opens="left"
                          :autoApply="true"
                          v-model="estimation.dateRange"
                        >
                        <div slot="input" slot-scope="picker" style="min-width: 350px;">
                              {{ dateRanges.startDate  }} - {{ dateRanges.endDate }}
                        </div>
                      </date-range-picker>
                    </v-col>
                    <v-col cols="12">
                      <header>Budget for the advert period</header>

                    <v-text-field
                      v-model="estimation.budget"
                      label="Planned budget"
                      v-on:key.enter="estimateUsers"
                        ></v-text-field>
                        </v-col>
                    <v-col cols="12">
                      <header>Website {{ adURL }}</header>
                      <v-text-field
                          v-model="adURL"
                          label="Url..."
                          outlined

                          ></v-text-field>
                    </v-col>
                    <h1>Reached users {{ estimation.reachedUsers }}</h1>
                   </v-row>
                </v-container>
               </v-card>
              </b-col>
            </b-row>
          </b-container>
      </v-card>
      <div class="text-center">
      <v-overlay :value="checking">
        <v-progress-circular indeterminate size="64"></v-progress-circular>
      </v-overlay>
    </div>
    </v-dialog>
    <v-row justify="center">
   <v-dialog v-model="templateUploading" persistent max-width="600px">
     <v-card>
       <v-card-title>
         <span class="headline">User Profile</span>
       </v-card-title>
       <v-card-text>
         <v-container>
         <h2>Template properties</h2>
           <v-row>
             <v-col cols="12">
               <v-text-field label="Name" type="text" v-model="templatePayload.name" required></v-text-field>
             </v-col>
             <v-col cols="12" sm="6">
               <v-select
                 :items="templatePayload.type"
                 label="Template type"
                 required
               ></v-select>
             </v-col>
             <v-col cols="12" sm="6">
             <v-checkbox
              label="Public"
              :value="templatePayload.IsPublic"
              ></v-checkbox>
              </v-col>
           </v-row>
         </v-container>
         <small>*indicates required field</small>
       </v-card-text>
       <v-card-actions>
         <v-spacer></v-spacer>
         <v-btn color="blue darken-1" text @click="templateUploading = false">Close</v-btn>
         <v-btn color="blue darken-1" text @click="uploadTemplate">Save</v-btn>
       </v-card-actions>
     </v-card>
   </v-dialog>
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
import ImgUpload from '../store/modules/upload'
import * as nsfwjs from 'nsfwjs'
import api from '../services/api'
import moment from 'moment'
  export default {
    data () {
      return {
        dialog: false,
        overlay:false,
        editor_dialog:false,
        notifications: false,
        sound: true,
        widgets: false,
        MultipleImgs:false,
        subIMGs:[{isimg:false,index:0}],
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
        templatetabs:'my',
        imgsInLine:[],
        MultipleImgsInLine:false,
        IsSinglePost:true,
        appearance:1,
        template:'',
        editedTemplate:{},
        memetext:[],
        memeTemps:[],
        templateSearch:'',
        templates:{
          my:{
          size:0,
          page:1,
          content:[]
          },
          public:{
          size:0,
          page:1,
          content:[]
          },
          recycle:{
          size:0,
          page:1,
          content:[]
          },
          search:{
          size:0,
          page:1,
          content:[]
          },
        },
        checking:false,
        porncontents:[],
        templateUploading:false,
        estimationInProgress:false,
        estimation:{
          budget:null,
          reachedUsers:null,
          daterange:null}

        ,templatePayload:{
          IsPublic:true,
          name:'',
          type:['portrait','landscape','normal'],

        }
      }
      },
      computed:{ ...mapGetters({
          IsAuthenticated:'authentication/IsAuthenticated',
          user:'authentication/user'
      }),...mapGetters({
  //      get_myTemplate:'post/myTemplates',
  //      get_browserTemplate:'post/publicTemplates',
  //      get_recycledTemplate:'post/recycledTemplates'

      }),porncontent(){
          var contains=false
          for(var i=0;i<this.porncontents.length;i++){
            if(this.porncontents[i]){
                contains=true
            }
          }
          return contains
      },
      dateRanges(){
      return{
        startDate:moment(this.estimation.dateRange.startDate).format('YYYY-MM-DD'),
        endDate:moment(this.estimation.dateRange.endDate).format('YYYY-MM-DD')
        }
      }
      }
      ,
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
      checkImage:async function(image){
        const model = await nsfwjs.load()
        const predictions= await model.classify(image, 1)
        if(predictions[0].className=="Porn"){
          return true
          }else{
            return false
          }
      },onChange: async function(index){
      this.checking=true
      const uploadAllowed = await this.checkImage(this.$refs.pictureInput[index].$refs.previewCanvas)
        if(!uploadAllowed){
            this.checking=false
            this.MultipleImgs=true
            if(index==this.imgs.length){


            this.imgs.push(this.$refs.pictureInput[index])
            this.subIMGs.push({isimg:false,index:this.imgindex})
            this.porncontents.push(false)
            }else{
              this.imgs[index]=this.$refs.pictureInput[index]
              this.porncontents[index]=false
            }

          }else{
            if(index==this.imgs.length){
                this.porncontents.push(true)
              }else{
                this.porncontents[index]=true
              }
            this.checking=false
            alert('No porn Buddy')
          }
        },onChangeInLine(){
          this.MultipleImgsInLine=true
          this.imgs.push(this.$refs.pictureInputInLine[this.inlineindex])
          this.inlineindex+=1
          this.subIMGs.push({isimg:false,index:this.imgindex})
        },
        remove (item) {
        this.chips.splice(this.chips.indexOf(item), 1)
        this.chips = [...this.chips]
      },
      async sendMeme(){
        var id;
        if(!this.advert){
        await  this.addPost({IsAdvert:false,description:this.postText,IsPublic:this.IsPublic,
                    labels:this.chips,
                    meme:{text:this.memetext,imgs:this.imgs,payload:{post:id,size:this.imgs.length}},size:this.imgs.length,templates:this.memeTemps},true)
                    .then(this.$store.dispatch('post/getTimeLine',1))

        }else{
          if(this.IsInlinePost){id='AdInPost'+String(Math.round(Math.random()*10000))
              await this.addPost({AdURL:this.adURL,CampaignTimestart:this.dateRanges.startDate,CampaignTimeend:this.dateRanges.endDate,IsAdvert:true,IsInlinePost:true,AppearenceFrequency:this.appearance,labels:this.chips
                        ,meme:{imgs:this.imgs,payload:{post:id,size:this.imgs.length}},size:this.imgs.length},true)
          }
          if(this.IsSinglePost){
              await  this.addPost({AdURL:this.adURL,CampaignTimestart:this.dateRanges.startDate,CampaignTimeend:this.dateRanges.endDate,IsAdvert:true,IsInlinePost:false,AppearenceFrequency:this.appearance,labels:this.chips
                        ,meme:{imgs:this.imgs,payload:{post:id,size:this.imgs.length}},size:this.imgs.length},true)
          }
        }
        this.postcreated=true
        this.dialog=false
      },
      getSrc(src,index,type){
      var size;
      if(type == 'public'){
          this.memeTemps.push(this.templates.public.content[index].ID)
          size=this.getSize(this.templates.public.content[index].type)
      }else if (type == 'my'){
          this.memeTemps.push(this.templates.my.content[index].ID)
          size=this.getSize(this.templates.my.content[index].type)
      }else if (type == 'search'){
          this.memeTemps.push(this.templates.search.content[index].ID)
          size=this.getSize(this.templates.search.content[index].type)
      }else{
          this.memeTemps.push(this.templates.recycle.content[index].ID)
          size=this.getSize(this.templates.recycle.content[index].type)
      }
        this.editedTemplate={
              id:'try',
              src:src,
              width:size.width,
              height:size.height,
              increment:1.0,
              alignment:'top'
        },
        this.editor_dialog=true
      },
      temp(index,type){


        },IMGurl:function(index,type){
            if(type == 'public'){
              if(this.templates.public.size>index){
                return require(`../assets${this.templates.public.content[index].IMG_url}`)
              }else{
                return false
              }
            }else if (type == 'my'){
            if(this.templates.my.size>index){
              return require(`../assets${this.templates.my.content[index].IMG_url}`)
              }else{
                return false
              }
            }else if(type=='search'){
              if(this.templates.search.size>index){
                  return require(`../assets${this.templates.search.content[index].IMG_url}`)
              }else{
                  return false
              }
            }else{
            if(this.templates.recycle.size>index){
              return require(`../assets${this.templates.recycle.content[index].IMG_url}`)
            }else{
                return false
              }
          }
        },
        getSize(type){
            if(type=='portrait'){

                return {
                  width:800*0.5,
                  height:1200*0.5
                }
            }else if(type=='landscape'){
                return{
                  width:1024*0.5,
                  height:512*0.5
                }
            }else if(type=='standard'){
                  return{
                    width:1200*0.5,
                    height:1200*0.5
                }
            }
        },async uploadTemplate(){
            this.templateUploading=false
            this.checking=true

            const uploadAllowed = await this.checkImage(this.$refs.templateInput.$refs.previewCanvas)
            if(uploadAllowed){
              this.checking=false
              alert('Please buddy, shame on you!')
            }else{
              await  ImgUpload(`/api/template/upload/`, this.$refs.templateInput.file,this.templatePayload,false,name='img')
                .then(response=>{
                  this.$store.commit('post/getTemplate',response.data)
                  this.checking=false
                })
            }
        },
        async estimate(){
                this.estimationInProgress=true
                await api.post('/statistics/estimate/',{startDate:this.estimation.dateRange.startDate,endDate:this.estimation.dateRange.endDate,budget:this.estimation.budget,function:'estimateUsers'})
                .then((response)=>{
                this.estimationInProgress=false
                this.estimation=response.data
                })
        },
        async get_templates(){
            var url=`template/?page=`
              if(this.templatetabs == 'my'){
                  url=url+`${this.templates[this.templatetabs].page}&my=true&user=${this.user.username}`
              }else if(this.templatetabs == 'recycle'){
                  url=url+`${this.templates[this.templatetabs].page}&recycle=true&user=${this.user.username}`
              }else if(this.templatetabs == 'public'){
                  url=url+`${this.templates[this.templatetabs].page}`
              }else if(this.templatetabs == 'search'){
                if(this.templateSearch != ''){
                  url=url+`${this.templates[this.templatetabs].page}&search=${this.templateSearch}`
                }else{

                }
              }
              await api.get(url).then((response)=>{
                    if(this.templatetabs == 'recycle'){
                          if(this.templates[templatetabs].content.length==0){
                                this.templates[this.templatetabs].content.push(...response.data.results.filter(function(item){
                                    return item.template
                                    }))
                          }else{
                          this.templates[this.templatetabs].content.concat(response.data.results.filter(function(item){
                                  return item.template
                                  }))
                          }
                          }else if(this.templatetabs!='search'){
                              if(this.templates[this.templatetabs].content.length==0){
                                  this.templates[this.templatetabs].content.push(...response.data.results)
                              }else{
                                  this.templates[this.templatetabs].content.concat(response.data.results)
                              }
                            this.templates[this.templatetabs].page++
                          }
                      this.templates[this.templatetabs].size=this.templates[this.templatetabs].content.length
                    })
            },
            async searchTemplate(){
              if(this.templateSearch!=''){
                var url=`template/?page=${this.templates.search.page}&search=${this.templateSearch}`
                  await api.get(url).then((response)=>{
                if(this.templates.search.content.length==0){
                      this.templates.search.content.push(...response.data.results)
                }else{
                      this.templates.search.content.concat(response.data.results)
                    }
              })
              this.templates.search.size=this.templates.search.content.length

              }else{
                  this.templates.search={content:[],page:1,size:0}
              }

            }
        ,scroll () {
            window.onscroll = () => {
              let bottomOfWindow = document.documentElement.scrollTop + window.innerHeight === document.documentElement.offsetHeight;
              if (bottomOfWindow) {
                this.get_templates()
             }
          }
        }
      },
      watch:{
        uploadMeme:function(){
        }

      },
    beforeCreate(){
      this.$store.dispatch('post/getTemplate')
    },
    mounted(){
      this.scroll()
    },watch:{
      templatetabs:function(){
        this.get_templates()
      }

    },created(){
    EventBus.$on('new_meme', (data) => {
        if(data.meme.is_file){
            this.MultipleImgs=true
            this.imgs.unshift(data)
            this.imgindex+=1
            this.subIMGs.push({isimg:true,index:this.imgindex, img:data.meme.img})
            this.editor_dialog=false
            this.renderMeme=false
            this.memetext=data.text.content
            //EventBus.$off('new_meme');
        }
      })
      this.get_templates()
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
