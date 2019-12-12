<template>
<v-container class="grey lighten-5">
<h1>{{ x }}|{{ y }}|{{ color }}</h1>
<v-row>
  <v-col

  >
    <v-card
      class="pa-2"
      outlined
      tile
    >
  <v-hover>
    <template v-slot:default="{ hover }">
      <v-card
        class="mx-auto"
      >
      <my-canvas v-bind:height="temp.height*temp.increment" v-bind:width="temp.width" >
        <my-box
          v-bind:save="IsRender"
          v-bind:texts="texts"
          :gImgObj="temp"
          v-bind:dark="dark"
          :x="0"
          :y="(temp.height*temp.increment)-temp.height"
        >
        </my-box>
      </my-canvas>
        <v-fade-transition>
          <v-overlay
            absolute
            opacity="1"
          >
          <div id="memecanvas" v-bind:style="`height: ${temp.height*temp.increment}px; width: ${temp.width}px;background-color:${background}; border: 1px solid black; position: relative;`">
            <img class="meme_bottom" :src="temp.src" :width="temp.width" :height="temp.height" align="middle">
            <TextBox v-for="(t,index) in texts" v-bind:key="index+'_box'" v-bind:text="t.content" v-bind:align="t.textStyle.align"  v-bind:fonsFamily="t.textStyle.fontFamily" v-bind:fontSize="t.textStyle.size" v-bind:color ="t.textStyle.color" v-bind:Index="index" v-bind:dark="dark"></TextBox>
          </div>
          </v-overlay>
        </v-fade-transition>
      </v-card>
    </template>
  </v-hover>
  </v-card>
  </v-col>
  <v-col
    cols="6"
    md="4"
  >
    <v-card
      class="pa-2"
      outlined
      tile
    >
    <template v-for="(t,index) in texts">
        <div v-bind:key="index">
          <v-row>
            <v-toolbar dense>
            <v-col>
            <v-text-field width="60" height="50" type="text" v-model="t.content" ></v-text-field>
            </v-col>
            <v-col>
            <v-text-field width="30"  type="number" v-model.number="t.textStyle.size" ></v-text-field>
            </v-col>
                 <v-btn-toggle
                   color="primary"
                   dense
                   group
                   multiple
                 >
                 </v-btn-toggle>
                 </v-toolbar>
                 </v-row>
                 <v-row justify="center">
                   <v-toolbar dense>
                   <v-dialog v-model="colorpicker" persistent max-width="290">
                       <template v-slot:activator="{ on }">
                         <v-btn v-bind:color="t.textStyle.color" dark v-on="on"></v-btn>
                       </template>
                       <v-card>
                       <div class="d-flex justify-center">
                             <v-color-picker v-model="t.textStyle.color"></v-color-picker>
                         </div>
                         <v-spacer></v-spacer>
                         <v-card-actions>
                           <v-spacer></v-spacer>
                           <v-btn color="green darken-1" text @click="colorpicker = false">OK</v-btn>
                         </v-card-actions>
                       </v-card>
                     </v-dialog>
                 </v-btn-toggle>
                 <div class="mx-4"></div>
                 <v-btn-toggle
                   color="primary"
                   dense
                   group
                 >
                   <v-btn @click="t.textStyle.align='left'" text>
                     <v-icon>mdi-format-align-left</v-icon>
                   </v-btn>

                   <v-btn @click="t.textStyle.align='center'" text>
                     <v-icon>mdi-format-align-center</v-icon>
                   </v-btn>

                   <v-btn @click="t.textStyle.align='right'" text>
                     <v-icon>mdi-format-align-right</v-icon>
                   </v-btn>
                   <v-overflow-btn
                     :items="dropdown_font"
                     v-model="t.textStyle.fontFamily"
                     label="Select font"
                     hide-details
                     class="pa-0"
                   ></v-overflow-btn>
                 </v-btn-toggle>
             </v-toolbar>
            </v-row>
        </div>
    </template>
    <v-btn  @click="addtext">Add text</v-btn>
    <v-btn @click="renderMeme">Save</v-btn>
    </v-card>
  </v-col>
</v-row>
</v-container>
</template>
<script>
import MyCanvas from './MemeGenerator.vue';
import MyBox from './canvas.vue';
import TextBox from './memeeditor/TextBox.vue'
import { EventBus } from './memeeditor/event-bus.js';
export default {
  name: 'ImgEditor',
  components: {
    MyCanvas,
    MyBox,
    TextBox
  },
  props:{
    temp:{
    type:Object,
    default(){
        return{
            id:'proba',
            src:require('../assets/media/template/S2.png'),
            width:1200,
            height:1200,
            increment:1,
            alignment:'top',
            type:'standard',
        }
    }

    }
  },
  data () {
    return {
    colorpicker:false,
    color:'#ffffff',
    dropdown_font:[
      'Arial',
      'Times New Roman',
      'Comic Sans',
      'Impact'
    ],
    dialog:false,
      texts:[
        {
        content:'funny text',
        x:10,
        y:10,
        textStyle:{
              size: 40,
              align: 'center',
              color: '#000000', // in color picker, if choosing color from platte notice it stays "solid".
              fontFamily: 'Impact',
              isOutline: true,
              lineWidth: 2, // outline width
              strokeStyle: '#ffffff',
              isShadow: false,
              shadowColor: '#000000',
              shadowOffsetX: 1,
              shadowOffsetY: 1,
              shadowBlur: 0,
              fillStyle:'#000000'
              }

        }
      ],
      textcontent:"TEXT",
      x:0,
      y:0,
      width:0,
      height:0,
      meme:[],
      IsRender:false,
      dark:true
    }
  },computed:{
      textsC(){
        return this.texts
    },background(){
      if(this.dark){
        return '#000000'
      }else{
        return '#ffffff'
      }
    }

  },methods:{
    addtext:function(){
      this.texts.push(this.createText(this.textcontent,20,20))
      this.textcontent=''
    },
    createText(line,x,y){
            var color;
            if(this.dark){
                color='#ffffff'
            }else{
                color='#000000'
            }
          return{
                  content: line,
                  textStyle:{
                  size: 80,
                  align: 'center',
                  color: '#000000', // in color picker, if choosing color from platte notice it stays "solid".
                  fontFamily: 'Impact',
                  isOutline: true,
                  lineWidth: 2, // outline width
                  strokeStyle: color,
                  isShadow: false,
                  shadowColor: '#000000',
                  shadowOffsetX: 1,
                  shadowOffsetY: 1,
                  shadowBlur: 0,
                  fillStyle:'#000000'

            },
            x: x,
            y: y
        }
    },renderMeme(){
      this.IsRender=true
      //this.IsRender = false

    }
  },
  created(){
    EventBus.$on('textbox', (data) => {
      this.x=data.x
      this.y=data.y
      this.texts[data.index].x = data.x;
      this.texts[data.index].y = data.y;
      this.texts[data.index].width = data.width;
      this.texts[data.index].height = data.height;
})
EventBus.$on('new_meme', (data) => {
    if(data.meme.is_file){
        this.IsRender=false
        //EventBus.$off('new_meme');
    }
  })
  }
}
</script>

<style>
html, body {
  margin: 0;
  padding: 0;
}

#meme_bottom:{
  position:absolute;
  top:40px;


}
</style>
