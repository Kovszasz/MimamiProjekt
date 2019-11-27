<template>
  <v-card
  >
    <v-list >
      <v-list-group
      >
      <v-list-item>
      <v-form>
        <v-container>
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
        </v-container>
      </v-form>
      </v-list-item>
      <v-divider
        :inset="true"
      ></v-divider>
        <template v-slot:activator>
          <p>Comments</p>
        </template>

        <v-list-group
          v-for="comment in comments"
          :key="comment.ID+'_l'"
          sub-group
        >
          <template v-slot:activator>
              <comment :comment="comment" :postID="postID"></comment>
          </template>
          <v-divider
            :inset="true"
          ></v-divider>
          <reply :commentID="comment.ID" :postID="postID"></reply>
        </v-list-group>
      </v-list-group>
    </v-list>
  </v-card>
</template>


<script>
import Vue from 'vue'
import { mapState, mapActions, mapGetters } from 'vuex'
import { mdiShareVariant } from '@mdi/js'
import comment from './Comment.vue'
import reply from './Reply.vue'
Vue.use(mdiShareVariant);

  export default {
    data: () => ({
      password: 'Password',
      marker: true,
      show: false,
      //comments:[],
      content:'',
      dialog:false,
    }),props:{
      postID:String

    },methods:{ ...mapActions({
          add:'comments/addComment',
          delete:'comments/deleteComment',
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
      async sendComment(){
        await  this.add({content:this.content,post:this.postID})
        .then(this.content = '')
      }
    },
    computed:{ ...mapState({

      //user:'authentication/user'
    }),
    comments(){
      console.log(this.get_comment(this.postID))

      return this.get_comment(this.postID)
    }, ...mapGetters({
          get_comment:'comments/postcomment'

      })
    },components:{
        comment,
        reply
    },created(){
        //this.generateContentModels()
    }

  }
</script>
