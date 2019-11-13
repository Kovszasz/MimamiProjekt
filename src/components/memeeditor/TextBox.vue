<template>
      <vue-draggable-resizable :w="100" :h="100" @dragging="onDrag" @resizing="onResize" :parent="true">
          <p>{{ text }}</p>
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
    Index:Number
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
</style>
