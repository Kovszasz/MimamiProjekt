<template>
  <div>
      <h1>{{ predictions }}</h1>
      <img id='img' src="@/assets/media/post/meme_3jmT4GK_nqI4QRl_g4jNGOt.png"/>
      <button @click="predict" >Predict</button>
      <div class="text-center">
  <v-btn
    color="deep-purple accent-4"
    class="white--text"
    @click="overlay = !overlay"
  >
    Launch Application
    <v-icon right>mdi-open-in-new</v-icon>
  </v-btn>

  <v-overlay :value="overlay">
    <v-progress-circular indeterminate size="64"></v-progress-circular>
  </v-overlay>
</div>
  </div>
</template>
<script>
import * as nsfwjs from 'nsfwjs'



export default {
    name: 'laboratory',
    data(){
      return{
        predictions:'heeeeej',
        overlay:false
      }
    },
    methods: {
      predict:async function(){
      const img = document.getElementById('img')
      console.log(img)
      const model = await nsfwjs.load()
      const predictions= await model.classify(img, 1)
      if(predictions[0].className=="Porn"){
        this.predictions=true
      }else{
        this.predictions=false
      }
    }



    },
    watch: {
  overlay (val) {
    val && setTimeout(() => {
      this.overlay = false
    }, 3000)
  },
},
};
</script>
