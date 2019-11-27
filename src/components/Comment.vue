<template>
  <v-list three-line>
      <v-list-item
        :key="comment.ID +'_item'"
      >
        <v-list-item-avatar>
          <v-img :src="IMGurl(comment.user)"></v-img>
        </v-list-item-avatar>

        <v-list-item-content>
          <v-list-item-title v-html="comment.user.username"></v-list-item-title>
          <p>{{ comment.content }}</p>
        </v-list-item-content>
      </v-list-item>
  </v-list>
</template>
<script>
import { mapState, mapActions, mapGetters } from 'vuex'
import Vue from 'vue';
import MemeEditor from './MemeEditor';
import {NavbarPlugin} from 'bootstrap-vue';
Vue.use(NavbarPlugin);
import api from '../services/api'
export default {
  name: 'Comment',
  props:{
  comment:Object,
  postID:String
  },
  data(){
    return{

    }
  },
  computed:{ ...mapState({

    //user:'authentication/user'
  }),
  comments(){
    //this.$store.dispatch('comments/get_comment',this.postID)
    console.log(this.get_comment(this.postID))

    return this.get_comment(this.postID)
  },

    ...mapGetters({
        get_comment:'comments/postcomment'

    })
  }

  ,
  methods:{ ...mapActions({
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
};
</script>
