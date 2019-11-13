<!-- https://jsfiddle.net/mani04/r4mbh6nu/1/-->
<template>
<div>
    <section class="meme-container ">

        <div class="meme-control">
            <canvas ref="memeCanvas">
                Your browser does not support the HTML5 canvas tag.
            </canvas>

            <div class="txts-list">
                <!-- js render -->
            </div>
        </div>

        <button @click="newTxtBtnClicked()">
            <i class="fas fa-plus"></i>  Add Line
        </button>
        <a id="dl" download="meme.png" href="#" @click="dlCanvas(this)">
            <span>
                <i class="fas fa-cloud-download-alt"></i> Download
            </span>
        </a>

    </section>

    <section class="contact">

    </section>
</div>
</template>


<script>


export default {
  name:'MemeGenerator',
  props:{
    //ImgId:String,
    //gMeme:Object,
    //gCtx:Object,
    gImgObj:{
      type:Object,
      default(){
      return{
      id:'proba',
      src:'https://i.ytimg.com/vi/3bNUjxQuPfA/hqdefault.jpg',
      width:500,
      height:300
      }
      }
    }
  },
  data() {
      return{
      gMeme:{},
      exampleContent: "This is TEXT",
      gCtx:{context:null},
      canvas:{

      }
      }
  },
  methods:{
  createTxt(line, x, y) {
    return {
        //object txt = {property:value}
        line: line,
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
        x: x,
        y: y
        }
    },
    createGmeme(imgId){
      return this.gMeme= {
        selectedImgId: imgId,
        txts: [this.createTxt('Your Text', 150, 70), this.createTxt('Your Text', 150, 300)]
    }
  },
/*  initCanvas() {

    var canvas = document.querySelector('.memeCanvas');
    gCtx = canvas.getContext('2d');



    this.gImgObj.onload = function () {
        canvas.width = this.gImgObj.width;
        canvas.height = this.gImgObj.height;
        this.gMeme.txts[1].y = this.gImgObj.height - 70;

        this.drawCanvas();
    };


}*/
drawCanvas() {
    console.log(this.gCtx)
    this.gCtx.drawImage(this.gImgObj, 0, 0);

    this.gMeme.txts.forEach(function (txt) {
        this.drawTxt(txt);
    })

  },
  addTxtShadow(txt) {
    this.gCtx.shadowColor = txt.shadowColor;
    this.gCtx.shadowOffsetX = txt.shadowOffsetX;
    this.gCtx.shadowOffsetY = txt.shadowOffsetY;
    this.gCtx.shadowBlur = txt.shadowBlur;
},
addTxtOutline(txt) {
    this.gCtx.strokeStyle = txt.strokeStyle;
    this.gCtx.lineWidth = txt.lineWidth;
    this.gCtx.strokeText(txt.line, txt.x, txt.y);
}

,
  drawTxt(txt) {
    this.gCtx.font = txt.size + 'px' + ' ' + txt.fontFamily;
    this.gCtx.textAlign = txt.align;
    this.gCtx.fillStyle = txt.color;
    if (txt.isShadow) this.addTxtShadow(txt);
    if (txt.isOutline) this.addTxtOutline(txt);

    this.gCtx.fillText(txt.line, txt.x, txt.y);
    },
  editTxt(elinput, txtIdx) {
    var property = elinput.dataset.property;  // using data-* attributes
    var value;

    switch (elinput.type) {
        case 'select-one':
            value = elinput.options[elinput.selectedIndex].value;
            break;
        case 'checkbox':
            value = elinput.checked;
            break;
        default: // text, number
            value = elinput.value;
            break;
    }
    this.gMeme.txts[txtIdx][property] = value;

    this.drawCanvas();
},
newTxtBtnClicked() {
    this.gMeme.txts.push(this.createTxt('New Line', 150, 150));
    this.drawCanvas();
    this.renderTxtsEditor();
},
deleteTxt(txtIdx) {
    this.gMeme.txts.splice(txtIdx, 1); //arr.splice(start, deleteCount)
    this.drawCanvas();
    this.renderTxtsEditor();
},

renderTxtsEditor() {
    var strHtml = this.gMeme.txts.map(function (txt, idx) {
        return `
        <div class="txt-editor">

                    <p>
                    <button onclick="deleteTxt(${idx})"><i class="fas fa-eraser"></i></button>
                    <input type="text" data-property="line" placeholder="${txt.line}" oninput="editTxt(this,${idx})">
                    <i class="fas fa-text-height"></i> <input type="range" value="${txt.size}"  min="10" step="2" data-property="size" oninput="editTxt(this ,${idx})">
                    <input type="color" value="${txt.color}" data-property="color" oninput="editTxt(this,${idx})">
                    Family:
                    <select data-property="fontFamily" oninput="editTxt(this,${idx})">
                    <option value="${txt.fontFamily}">${txt.fontFamily}</option>
                    <option value="Tahoma">Tahoma</option>
                    <option value="Geneva">Geneva</option>
                    <option value="Verdana">Verdana</option>
                    </select>
                    </p>

                    <p>
                    <i class="fas fa-arrows-alt-h"></i> <input type="number" value="${txt.x}"  min="0" step="5" data-property="x" oninput="editTxt(this ,${idx})">
                    <i class="fas fa-arrows-alt-v"></i> <input type="number" value="${txt.y}"  min="0" step="5" data-property="y" oninput="editTxt(this ,${idx})">

                    <select data-property="align" oninput="editTxt(this,${idx})">
                    <option value="left">left</option>
                    <option value="center">center</option>
                    <option value="right">right</option>
                     </select>
                    </p>

                    <p>
                    <input id="outline" type="checkbox" data-property="isOutline" checked onclick="editTxt(this,${idx})">
                    <label for="outline">Outline</label>
                    Width: <input type="number" value="${txt.lineWidth}"  min="0" step="1" data-property="lineWidth" oninput="editTxt(this ,${idx})">
                    <input type="color" value="${txt.strokeStyle}" data-property="strokeStyle" oninput="editTxt(this,${idx})">
                    </p>
                    <p>

                    <input id="shadow" type="checkbox" data-property="isShadow" onclick="editTxt(this,${idx})">
                    <label for="shadow">Shadow</label>
                    <input type="color" value="${txt.shadowColor}" data-property="shadowColor" oninput="editTxt(this,${idx})">
                    <i class="fas fa-arrows-alt-h"></i> <input type="number" value="${txt.shadowOffsetX}"  step="1" data-property="shadowOffsetX" oninput="editTxt(this ,${idx})">
                    <i class="fas fa-arrows-alt-v"></i><input type="number" value="${txt.shadowOffsetY}"  step="1" data-property="shadowOffsetY" oninput="editTxt(this ,${idx})">
                    Blur: <input type="number" value="${txt.shadowBlur}" data-property="shadowBlur" oninput="editTxt(this,${idx})">
                    </p>

                </div>
        `
    })
        .join(' ');

    document.querySelector('.txts-list').innerHTML = strHtml;

},
dlCanvas(eldllink) {

    var dt = this.canvas.toDataURL('image/png');
    /* Change MIME type to trick the browser to downlaod the file instead of displaying it */
    dt = dt.replace(/^data:image\/[^;]*/, 'data:application/octet-stream');

    /* In addition to <a>'s "download" attribute, you can define HTTP-style headers */
    dt = dt.replace(/^data:application\/octet-stream/, 'data:application/octet-stream;headers=Content-Disposition%3A%20attachment%3B%20filename=canvas.png');

    eldllink.href = dt;
}

},
provide () {
  return {
    provider: this.gCtx
  }
}
,
mounted(){
    this.gCtx.context = this.$refs['memeCanvas'].getContext('2d')
    this.canvas = this.$refs['memeCanvas']
    this.$refs['memeCanvas'].width = 500
    this.$refs['memeCanvas'].height = 300
  /*  this.gImgObj.onload = function () {
        this.canvas.canvas.width = this.gImgObj.width;
        this.canvas.canvas.height = this.gImgObj.height;
        this.gMeme.txts[1].y = this.gImgObj.height - 70;

        this.drawCanvas();
    }*/

},
  directives: {


  },created(){
      this.createGmeme(this.gImgObj.id)
      //this.initCanvas()
  }

}
</script>

<style scoped>
canvas{
  border:'1px'
}
</style>
