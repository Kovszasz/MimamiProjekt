
<template>
<div>
  <v-form>
    <v-container>
      <v-row>
        <v-col cols="12">
          <v-text-field
            v-model="content"
            :append-outer-icon="content ? 'mdi-send' : 'mdi-send'"
            :prepend-icon="'mdi-emoticon-excited'"
            outlined
            clear-icon="mdi-close-circle"
            clearable
            label="Comment..."
            type="text"
            @click:append-outer="sendComment"
          ></v-text-field>
        </v-col>
      </v-row>
    </v-container>
  </v-form>
  <v-container>
  <v-col><v-icon @click="getComments()">mdi-message-text</v-icon></v-col>
  <v-row v-for="comment in comments" v-bind:key="comment.ID">
  <v-alert  color="#E7DED9" light >
         {{ comment.content }}
        </v-alert>
  </v-row>
  </v-container>
  </div>
</template>
<script>
import Vue from 'vue'
import { mapState, mapActions } from 'vuex'
import { mdiShareVariant } from '@mdi/js'
Vue.use(mdiShareVariant);

  export default {
    data: () => ({
      password: 'Password',
      marker: true,
      show: false,
      comments:[],
      content:''
    }),props:{
      postID:String

    },methods: mapActions({
          add:'comments/addComment',
          delete:'comments/deleteComment',
          getComments(){
            //this.$store.dispatch('comments/getComment',this.postID)
            this.comments = state => state.comment.comment.filter(comment => comment.post.ID == this.postID )
          },
          sendComment(){
            this.add({ID:String(Math.round(Math.random()*10000)),content:this.content,post:this.postID})
            this.comments = state => state.comment.comment.filter(comment => comment.post.ID == this.postID )
          }
    }),
    computed: mapState({
    //  comments: state => state.comments.comments,
      clearComment(){
      this.content = ''
      }

      //user:'authentication/user'
    }),
    created() {
    //  this.$store.dispatch('comments/getComment',this.postID)
    }
  }
</script>
