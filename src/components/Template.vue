<template>
<v-card>
   <v-tabs
     background-color="white"
     color="deep-purple accent-4"
     right
   >
     <v-tab>MyTemplates</v-tab>
     <v-tab>Recycle</v-tab>
     <v-tab>Browse</v-tab>

     <v-tab-item
       v-for="n in 3"
       :key="n"
     >
       <v-container fluid>
         <v-row>
           <v-col
             v-for="i in 6"
             :key="i"
             cols="12"
             md="4"
           >
             <v-img
               :src="`https://picsum.photos/500/300?image=${i * n * 10 + 10}`"
               :lazy-src="`https://picsum.photos/10/6?image=${i * n * 5 + 10}`"
             ></v-img>
           </v-col>
         </v-row>
       </v-container>
     </v-tab-item>
   </v-tabs>
 </v-card>
</template>
<script>
export default {
  name:'Name',
  data () {
    return {
    }
    },
    computed:{},
    components:{
    },
    methods:{
    }
  }

</script>
