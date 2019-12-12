<template>
<div>
    <v-list-item
        v-for="reply in replies"
        :key="reply.ID"
        >
        <comment :comment="reply" :postID="postID" ></comment>
      </v-list-item>
      <v-btn @click="get_replies">More replies pls...</v-btn>
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
import api from '../services/api'
Vue.use(mdiShareVariant);

  export default {
  name:'Reply',
    data: () => ({
      password: 'Password',
      marker: true,
      show: false,
      replies:[],
      content:'',
      replypage:1,
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
        await api.post(`comment/reply/`,{content:this.content,comment:this.commentID,post:this.postID})
                .then((response) =>{
                this.content = ''
                this.replies.push(response.data)
            })
      },
      async get_replies(){
        await api.get(`comments/?post=${this.postID}&reply=${this.commendID}&page=${this.replypage}`)
          .then((response)=>{
          console.log(response)
              this.replies.push(...response.data.results)
            this.replypage++
          })
        }
    },
    components:{
        comment
    }
  }
</script>
