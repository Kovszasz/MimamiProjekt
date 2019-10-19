
<template>
<div>
  <v-form>
    <v-container>
      <v-row>

        <v-col cols="12">
          <v-text-field
            v-model="comment"
            :append-outer-icon="comment ? 'mdi-send' : 'mdi-send'"
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
  <v-row >
  <v-alert  color="#E7DED9" light >
        {{ comment.content }}
        </v-alert>
  </v-row>
  </v-container>
  </div>
</template>
<script>
import { mapState, mapActions } from 'vuex'


  export default {
    data: () => ({
      password: 'Password',
      marker: true,
      show: false,
      comment: '',
    }),props:{
      postID:String

    },methods: mapActions('comments', {
          add:'addComment',
          delete:'deleteComment'
    }),
    computed: mapState({
      comment: state => state.comments.comments,
      clearComment(){
      this.comment = ''
      }
    }),
    created() {
      this.$store.dispatch('comments/getComment')
    }
  }
</script>
