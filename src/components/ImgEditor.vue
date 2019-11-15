<template>
<v-container class="grey lighten-5">
<h1>{{ x }}|{{ y }}</h1>
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
      <my-canvas v-bind:height="temp.height" v-bind:width="temp.width" >
        <my-box
          v-bind:save="IsRender"
          v-bind:texts="meme"
          v-bind:gImgObj="temp"
          :x="0"
          :y="(temp.height*temp.increment)-temp.height"
        >
        </my-box>
      </my-canvas>
        <v-fade-transition>
          <v-overlay
            absolute
          >
          <div id="memecanvas" v-bind:style="`height: ${temp.height*temp.increment}px; width: ${temp.width}px; border: 1px solid red; position: relative;`">
            <img class="meme_bottom" :src="temp.src" :width="temp.width" :height="temp.height" align="middle">
            <TextBox v-for="(t,index) in texts" v-bind:key="index+'_box'" v-bind:text="t.content" v-bind:fontSize="t.textStyle.size" v-bind:Index="index"></TextBox>
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
        <label>#{{ index }}</label><input type="text" v-model="t.content" />
        <v-btn @click="t.textStyle.size++">+</v-btn><input style="text" v-model="t.textStyle.size" :placeholder="t.textStyle.size">
        <v-btn @click="t.textStyle.size--">-</v-btn>
        </div>
    </template>
    <v-btn  @click="addtext">Add text</v-btn>
    <v-btn@click="renderMeme">Save</v-btn>
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
            type:'standard'
        }
    }

    }
  },
  data () {
    return {
      texts:[
        {
        content:'funny text',
        x:10,
        y:10,
        textStyle:{
              size: 40,
              align: 'left',
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
      IsRender:false
    }
  },computed:{
      textsC(){
        return this.texts
    }

  },methods:{
    addtext:function(){
      this.texts.push(this.createText(this.textcontent,20,20))
      this.textcontent=''
    },
    createText(line,x,y){
          return{
                  content: line,
                  textStyle:{
                  size: 80,
                  align: 'left',
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

            },
            x: x,
            y: y
        }
    },renderMeme(){
      this.IsRender=true
      this.meme=this.texts

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
