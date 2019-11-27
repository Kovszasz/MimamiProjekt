<template>
<div>
    <v-list-item
        v-for="reply in replies"
        :key="reply.ID"
        >
        <comment :comment="reply" :postID="postID" ></comment>
      </v-list-item>
      <v-list-item>
        <v-form>
          <v-container>
              <v-row>
                  <v-text-field
                      v-model="content"
                      :append-outer-icon="content ? 'mdi-send' : 'mdi-send'"
                      :prepend-icon="'mdi-emoticon-excited'"
                      outlined
                      clear-icon="mdi-close-circle"
                      clearable
                      label="Comment..."
                      type="text"
                      @click:append-outer="replyComment"
                  ></v-text-field>
              </v-row>
            </v-container>
        </v-form>
    </v-list-item>
  </div>
</template>


<script>
import Vue from 'vue'
import { mapState, mapActions, mapGetters } from 'vuex'
import { mdiShareVariant } from '@mdi/js'
import comment from './Comment.vue'
Vue.use(mdiShareVariant);

  export default {
  name:'Reply',
    data: () => ({
      password: 'Password',
      marker: true,
      show: false,
      //comments:[],
      content:'',
      dialog:false,
    }),props:{
      commentID:String,
      postID:String,


    },methods:{ ...mapActions({
          delete:'comments/deleteComment',
          reply:'comments/replyComment'
    }), IMGurl:function(img){
          try{
            return require(`../assets${img.avatar}`)
          }catch{
            return require('../assets/media/profile/e6.png')
        }
      },
      clearComment(){
      this.content = ''
      },
      async replyComment(){
        await  this.reply({content:this.content,comment:this.commentID,post:this.postID})
        .then(this.content = '')
      }
    },
    computed:{
    replies(){
      console.log(this.get_reply(this.postID))

      return this.get_reply(this.commentID)
    }, ...mapGetters({
          get_reply:'comments/reply'

      })
    },components:{
        comment
    }
  }
</script>
