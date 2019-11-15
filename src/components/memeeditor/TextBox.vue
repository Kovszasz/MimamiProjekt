<template>
      <vue-draggable-resizable class="playground" :w="100" :h="100" @dragging="onDrag" @resizing="onResize" :parent="true">
          <p class="text" v-bind:style="{ fontSize: fontSize + 'px' }"  >{{ text }}</p>

        </vue-draggable-resizable>
</template>

<script>
import Vue from 'vue'
import VueDraggableResizable from 'vue-draggable-resizable'
import 'vue-draggable-resizable/dist/VueDraggableResizable.css'
Vue.component('vue-draggable-resizable', VueDraggableResizable)
import { EventBus } from './event-bus.js';

export default {
  name: 'TextBox',
  components: {
    VueDraggableResizable
  },
  props:{
    text:String,
    Index:Number,
    fontSize:{
        type:Number,
        default:50
        }
  },
  methods:{
    onResize: function (x, y, width, height) {
      this.x = x
      this.y = y
      this.width = width
      this.height = height
       EventBus.$emit('textbox', {index:this.Index,x:x,y:y,width:width,height:height});
    },
    onDrag: function (x, y) {
      this.x = x
      this.y = y
      EventBus.$emit('textbox', {index:this.Index,x:x,y:y,width:this.width,height:this.height});
    }
  }
}
</script>
<style>
.text{
  font:'Impact';
}
.playground{
    text-align:center;
}

</style>
