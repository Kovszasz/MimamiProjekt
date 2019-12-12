<template>
  <v-card
  >
    <v-list >
      <v-list-group
      >
      <v-list-item>
      <v-form>
<emoji-picker @emoji="insert" :search="search">
    <div class="emoji-invoker" slot="emoji-invoker" slot-scope="{ events }" v-on="events">
        <button type="button">open</button>
    </div>
    <div slot="emoji-picker" slot-scope="{ emojis, insert, display }">
        <div>
            <div>
                <input type="text" v-model="search">
            </div>
            <div>
                <div v-for="(emojiGroup, category) in emojis" :key="category">
                    <h5>{{ category }}</h5>
                    <div>
                        <span
                            v-for="(emoji, emojiName) in emojiGroup"
                            :key="emojiName"
                            @click="insert(emoji)"
                            :title="emojiName"
                        >{{ emoji }}</span>
                    </div>
                </div>
            </div>
        </div>
    </div>
</emoji-picker>
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
    <v-btn @click="get_comments">More comments pls...</v-btn>
  </v-card>
</template>


<script>
import Vue from 'vue'
import { mapState, mapActions, mapGetters } from 'vuex'
import { mdiShareVariant } from '@mdi/js'
import comment from './Comment.vue'
import reply from './Reply.vue'
import { EmojiPickerPlugin } from 'vue-emoji-picker'
import api from '../services/api'

Vue.use(EmojiPickerPlugin)
Vue.use(mdiShareVariant);

  export default {
    data: () => ({
      password: 'Password',
      marker: true,
      show: false,
      comments:[],
      content:'',
      dialog:false,
      search: '',
      commentpage:1,
      more_comments:true,
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
        await api.post(`comment/`, {content:this.content,post:this.postID})
                  .then((response) =>{
                      this.content = ''
                      this.comments.push(response.data)
            })
      },
      insert(emoji) {
            this.content += emoji
        },
        async get_comments(){
          await api.get(`comments/?post=${this.postID}&page=${this.commentpage}`)
            .then((response)=>{
              //for(var i=0;i<response.data.results.length;i++){
                this.comments.push(...response.data.results)
              //}
              this.commentpage++
            })
          }
    },
    computed:{ ...mapState({

      //user:'authentication/user'
    })
    },mounted(){
      this.get_comments()
    },components:{
        comment,
        reply,
        EmojiPickerPlugin
    },created(){
        //this.generateContentModels()
    }

  }
</script>
