<script>
// Note how there's no template or styles in this component.
//http://jsfiddle.net/BaG4J/2/
//https://github.com/mauricius/vue-draggable-resizable
// Helper functions to convert a percentage of canvas area to pixels.
const percentWidthToPix = (percent, ctx) => Math.floor((ctx.canvas.width / 100) * percent)
const percentHeightToPix = (percent, ctx) => Math.floor((ctx.canvas.height / 100) * percent)
import { EventBus } from './memeeditor/event-bus.js';
export default {
  // Gets us the provider property from the parent <my-canvas> component.
  inject: ['provider'],
  props: {
  gImgObj:Object,
  save:Boolean,
  texts:{
    type:Array,
    default(){
      return []
    }

    },
    dark:Boolean,
    x: {
      type: Number,
      default: 0
    },
    y: {
      type: Number,
      default: 0
    },
  },

  data () {
    return {
      // We cache the dimensions of the previous
      // render so that we can clear the area later.
      oldBox: {
        x: null,
        y: null,
        w: null,
        h: null
      }
    }
  },methods:{
    printAt( context , text, x, y, lineHeight, fitWidth,textStyle){
        context.fillStyle = textStyle.fillStyle
        context.font = `${textStyle.size}px Impact`//textStyle.fontFamily
        context.strokeStyle= textStyle.storeStyle
        context.lineWidth=2
        context.textAlign = textStyle.texalign
        context.isOutline= true //textStyle.isOutline
        context.isShadow=false //textStyle.isShadow
        context.shadowColor=textStyle.shadowColor
        context.shadowOffsetX=textStyle.shadowOffsetX
        context.shadowOffsetY=textStyle.shadowOffsetY
        context.shadowBlur=textStyle.shadowBlur
        fitWidth = fitWidth || 0;
        if (fitWidth <= 0){
          context.fillText( text, x, y );
          return;
        }
        for (var idx = 1; idx <= text.length; idx++){
            var str = text.substr(0, idx);
            if (context.measureText(str).width > fitWidth){
              context.fillText( text.substr(0, idx-1), x, y );
              this.printAt(context, text.substr(idx-1), x, y + lineHeight, lineHeight,  fitWidth, textStyle);
              return;
          }
        }
        context.fillText( text, x, y );
    },saveMeme(ctx,name,width,height){
          var image=ctx.toDataURL('image/png')
          var blobBin = atob(image.split(',')[1]);
          var array = [];
              for(var i = 0; i < blobBin.length; i++) {
                    array.push(blobBin.charCodeAt(i));
                    }
        var blob=new Blob([new Uint8Array(array)], {type: 'image/png'});
        var file = new File([blob],name,{type:'image/png'})
          return {file:file,is_file:true,img:{src:image,width:width,height:height}}
      },
      drawMeme(ctx,canvas,imgobj){
      if(!this.save){
          ctx.clearRect(0,0,canvas.width,canvas.height)
        }
          //ctx.fillStyle =this.isdark;
          //ctx.fillRect(0, 0, canvas.width, canvas.height);
          var img = new Image()
          img.width=imgobj.width
          img.height=imgobj.height
          img.id=imgobj.id
          console.log(img)
      img.onload = function() {
          if(imgobj.alignment=='bottom'){
                ctx.drawImage(img, this.x, this.y,img.width,img.height)
          }else if(imgobj.alignment=='top'){
                ctx.drawImage(img, 0, 0,img.width,img.height)
          }else if(imgobj.alignment=="center"){
                ctx.drawImage(img, this.x, (ctx.canvas.height/2)-(this.y*imgobj.increment/2),img.width,img.height)
          }else{
                ctx.drawImage(img,0,0,img.width,img.height)
          }
      }
      img.src=imgobj.src

      for(var i=0;i<this.texts.length;i++){
          this.printAt(ctx, this.texts[i].content, this.texts[i].x,this.texts[i].y+35, 10, this.texts[i].width,this.texts[i].textStyle)

      }
      }
  },

  computed: {
    isdark(){
        if(this.dark){
          return '#000000'
        }else{
          return '#ffffff'
        }
    }
  },render () {
    if(!this.provider.context) return;
    const canvas = this.provider.context
    const ctx=canvas.getContext('2d');
    const imgobj=this.gImgObj
    this.drawMeme(ctx,canvas,imgobj)
      if(this.save){
      this.drawMeme(ctx,canvas,imgobj)
      EventBus.$emit('new_meme', this.saveMeme(canvas,'meme.png',imgobj.width,imgobj.height*imgobj.increment));
     }
  }
}
</script>
