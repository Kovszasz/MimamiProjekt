<template>
<div>
  <v-row md="12" justify="center" >
  <v-col md="2">
  </v-col>
  <v-col md="10" align="center">
  <v-container class="grey lighten-5 pr-5 dashboard" fluid>
    <!-- Stack the columns on mobile by making one full-width and the other half-width -->
    <v-row>
      <v-col
        cols="12"
        md="8"
      >
        <v-card
          class="pa-2"
          outlined
          tile
        >
          <area-chart :data="{'2017-01-01 00:00:00 -0800': 2, '2017-01-01 00:01:00 -0800': 5}"></area-chart>
        </v-card>
      </v-col>
      <v-col
        cols="6"
        md="4"
      >
        <v-card
          class="pa-2"
          outlined
          tile
        >
            <pie-chart :refresh="10" data="/api/statistics/users/"></pie-chart>
        </v-card>
      </v-col>
    </v-row>

    <!-- Columns start at 50% wide on mobile and bump up to 33.3% wide on desktop -->
    <v-row>
      <v-col
        cols="6"
        md="4"
      >
        <v-card
          class="pa-2"
          outlined
          tile
        >
          <column-chart :data="[['Sun', 32], ['Mon', 46], ['Tue', 28]]"></column-chart>
        </v-card>
      </v-col>
      <v-col
        cols="6"
        md="4"
      >
        <v-card
          class="pa-2"
          outlined
          tile
        >
          <column-chart :data="[['Sun', 32], ['Mon', 46], ['Tue', 28]]"></column-chart>
        </v-card>
      </v-col>
      <v-col
        cols="6"
        md="4"
      >
        <v-card
          class="pa-2"
          outlined
          tile
        >
          <column-chart :data="[['Sun', 32], ['Mon', 46], ['Tue', 28]]"></column-chart>
        </v-card>
      </v-col>
    </v-row>

    <!-- Columns are always 50% wide, on mobile and desktop -->
    <v-row>
      <v-col
        cols="6"
      >
        <v-card
          class="pa-2"
          outlined
          tile
        >
          <geo-chart :data="[['United States', 44], ['Germany', 23], ['Brazil', 22]]"></geo-chart>
        </v-card>
      </v-col>
      <v-col
        cols="6"
      >
        <v-card
          class="pa-2"
          outlined
          tile
        >
          <scatter-chart :data="[[174.0, 80.0], [176.5, 82.3]]" xtitle="Size" ytitle="Population"></scatter-chart>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
  </v-col>
  </v-row>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex'

export default {
  name: "Dashboard",
  data() {
    return {
      subject: "",
      msgBody: "",
    };
  },
  computed: mapState({
    messages: state => state.messages.messages
  }),
  methods: mapActions('messages', [
    'addMessage',
    'deleteMessage'
  ]),
  created() {
    this.$store.dispatch('messages/getMessages')
  },
  components:{
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
hr {
  max-width: 65%;
}

.msg {
  margin: 0 auto;
  max-width: 30%;
  text-align: left;
  border-bottom: 1px solid #ccc;
  padding: 1rem;
}

.msg-index {
  color: #ccc;
  font-size: 0.8rem;
  /* margin-bottom: 0; */
}

img {
  width: 250px;
  padding-top: 50px;
  padding-bottom: 50px;
}

.sidemenu{
margin-top:80px;

}
.dashboard{
    margin-top:80px
}

</style>
