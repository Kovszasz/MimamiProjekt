<template>
  <div id="editor">
  <h1>{{ x }}|{{ y }}</h1>
    <my-canvas :height="temp.height*temp.increment" :width="temp.width" v-bind:save="IsRender">
      <my-box
        v-bind:texts="meme"
        :gImgObj="temp"
        :x="0"
        :y="(temp.height*temp.increment)-temp.height"
      >
      </my-box>
    </my-canvas>
    <v-container class="grey lighten-5">
    <v-row>
      <v-col
        cols="12"
        md="8"
      >
        <v-card
          class="pa-2"
          outlined
          tile
        >
        <div id="memecanvas" style="height: 500px; width: 500px; border: 1px solid red; position: relative;">
          <img class="meme_bottom" :src="temp.src" :width="temp.width" :height="temp.height" align="middle">
          <TextBox v-for="(t,index) in texts" v-bind:key="index+'_box'" v-bind:text="t.content" v-bind:Index="index"></TextBox>
        </div>
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
            </div>
        </template>
        <v-btn  @click="addtext">Add text</v-btn>
        <v-btn@click="renderMeme">Save</v-btn>
        </v-card>
      </v-col>
    </v-row>
    </v-container>
  </div>
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
            width:500,
            height:300,
            increment:1.7,
            alignment:'center'
        }
    }

    }
  },
  data () {
    return {
      texts:[
        {
        content:'hejj',
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
      textcontent:"dfdfdfd",
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
    addimg:function(e){
  //        this.temp['width']=200,
  //        this.temp['height']=200,
  //        this.temp['src']=e.target.src
      },
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

#editor {
  position: relative;
  height: 100vh;
  width: 100vw;
  padding: 20px;
  box-sizing: border-box;
}
#meme_bottom:{
  position:absolute;
  top:40px;

}
</style>
