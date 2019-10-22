
<template>
<div>
  <v-form>
    <v-container>
      <v-row>

        <v-col cols="12">
          <v-text-field
            v-model="comment_"
            :append-outer-icon="comment_ ? 'mdi-send' : 'mdi-send'"
            :prepend-icon="'mdi-emoticon-excited'"
            outlined
            clear-icon="mdi-close-circle"
            clearable
            label="Comment..."
            type="text"
            @click:append-outer="add"
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
      comment_: '',
      comments:[]
    }),props:{
      postID:String

    },methods: mapActions('comments', {
          add:'comments/addComment',
          delete:'comments/deleteComment',
          getComments(){
            this.$store.dispatch('comments/getComment',this.postID)
            this.comments=this.$store.state.comments.comments
          }
    }),
    computed: mapState({
      //comments: state => state.comments.comments,
      clearComment(){
      this.comment_ = ''
      }
    }),
    created() {
    //  this.$store.dispatch('comments/getComment',this.postID)
    }
  }
</script>
