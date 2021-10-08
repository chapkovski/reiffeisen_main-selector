<template>
  <v-card elevation="4" height="150" class='d-flex align-center justify-center'>
    <v-card-text>
      <v-btn-toggle>
        <v-btn color='red' @click='sellClicked'>Продать</v-btn>
        
      </v-btn-toggle>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  data: () => ({}),
  methods:{sellClicked(){
    this.$emit('showDialog')
  }}
};
</script>
