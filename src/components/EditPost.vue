<template>
  <v-row justify="center" z-index="100">
    <v-dialog v-model="dialog" persistent max-width="600px">
      <template v-slot:activator="{ on }">
        <v-btn  v-on="on">Edit</v-btn>
      </template>
      <b-card  header-tag="header" footer-tag="footer" >
        <template v-slot:header >
        <v-text-field
            v-model='content'

            filled
            rounded
            dense
            >
            </v-text-field>
        </template>
        <template >
        <v-carousel
          hide-delimiter-background
          width="100%"
          height="100%"
          :show-arrows='MultipleImgs'
          :show-arrows-on-hover='MultipleImgs'
          :hide-delimiters='!MultipleImgs'
        >
          <v-carousel-item
            @click='goToPost()'
            v-for="(subpost,index) in post.imgs"
            :key="KeyGenerator(index)"
            :src="IMGurl(subpost)"
            interval="0"
          >
          </v-carousel-item>
        </v-carousel>
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
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" text @click="dialog = false">Cancel</v-btn>
          <v-btn :loading="updating" color="blue darken-1" text @click="updatePost">Update</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-row>
</template>
<script>

import { mapState, mapActions, mapGetters } from 'vuex'

export default {
  props:{
    post:Object,
    MultipleImgs:Boolean
  },
    data () {
      return {
        IsPublic:false,
        chips:[],// this.post.labels,
        items: ['hejs'],
        content:this.post.description,
        updating:false,
        dialog:false,
        randomstring:''
      }
      },
      methods:{...mapActions({
        editPost:'post/editPost',
      }),
      async updatePost(){
        this.updating=true
        await  this.editPost('postID',{description:this.content,IsPublic:this.IsPublic,labels:this.chips})
                .then(()=>{
                    this.updating=false
                    this.dialog=false

                })
        },
        KeyGenerator:function(index){
          return this.post.ID+'img'+String(index)
        },
      IMGurl:function(img){
              if(img.IMG_url==''){
                return require(`../assets/logo.svg`)
              }else{
                return require(`../assets${img.IMG_url}`)
              }
          },
        setChips(array){
          var array=['fsdf','sdfdsfsdf','asdfdsf','fsdfd']
            for(var i=0;i<this.post.labels.length;i++){
              //  array.push(String(this.post.labels[i]))
              //  this.randomstring=
              //this.chips=+[String(this.post.labels[i])]
            }


        }
      },
      created(){
      //  this.setChips()
      }
  };

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
