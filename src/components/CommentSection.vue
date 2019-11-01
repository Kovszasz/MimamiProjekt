<template>
  <v-row justify="center">
    <v-dialog v-model="dialog" width="600px">
      <template v-slot:activator="{ on }">
        <v-btn icon v-on="on"><v-icon >mdi-message-text</v-icon></v-btn><p>{{ NumberOfComments }}</p>
      </template>
      <v-card>
        <v-btn icon dark @click="dialog = false">
          <v-icon>mdi-close</v-icon>
        </v-btn>
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
          <v-list three-line>
            <div v-for="comment in comments" v-bind:key="comment.ID">
              <template>
                <v-divider
                  :key="comment.ID +'_divider'"
                  :inset="true"
                ></v-divider>

                <v-list-item
                  :key="comment.ID +'_item'"
                >
                  <v-list-item-avatar>
                    <v-img :src="IMGurl(comment.user.mimeuser)"></v-img>
                  </v-list-item-avatar>

                  <v-list-item-content>
                    <v-list-item-title v-html="comment.user.username"></v-list-item-title>
                    <v-list-item-subtitle v-html="comment.content"></v-list-item-subtitle>
                  </v-list-item-content>
                </v-list-item>
              </template>
              </div>
            </v-list>
          </v-container>
          </div>
      </v-card>
    </v-dialog>
  </v-row>
</template>
<script>
import Vue from 'vue'
import { mapState, mapActions, mapGetters } from 'vuex'
import { mdiShareVariant } from '@mdi/js'
Vue.use(mdiShareVariant);

  export default {
    data: () => ({
      password: 'Password',
      marker: true,
      show: false,
      //comments:[],
      content:'',
      dialog:false
    }),props:{
      postID:String

    },methods:{ ...mapActions({
          add:'comments/addComment',
          delete:'comments/deleteComment',
          sendComment(){
            this.add({ID:String(Math.round(Math.random()*10000)),content:this.content,post:this.postID})
            this.content = ''
          }
    }), IMGurl:function(img){
            return require(`../assets${img.avatar}`)
      },
      clearComment(){
      this.content = ''
      }
    },
    computed:{ ...mapState({

      //user:'authentication/user'
    }),
    comments(){
      //this.$store.dispatch('comments/get_comment',this.postID)
      return this.get_comment(this.postID)
    },

      ...mapGetters({
          get_comment:'comments/postcomment'

      }),NumberOfComments:function(){
              return this.get_comment(this.postID).count
          },
    },
    created() {
      this.$store.dispatch('comments/getComment')
    }
  }
</script>
