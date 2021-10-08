<template>
  <v-card
    elevation="4"
    height="150"
    class="d-flex align-center justify-center"
    width="100%"
  >
    <v-card-text>
      <v-btn
        color="red"
        @click="showIntentionSlider = true"
        v-show="!showIntentionSlider"
        >Обдумываю возможность продажи</v-btn
      >
      <div v-show="showIntentionSlider">
        <v-slider
          class="my-3"
          v-model="sellingDecision"
          :tick-labels="ticksLabels"
          :max="3"
          step="1"
          ticks="always"
          tick-size="20"
          :thumb-size="70"
          @change="changeSliderValue"
        />
      </div>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  props: ["reset", "initialSliderValue"],
  data() {
    return {
      sellingDecision: this.initialSliderValue,
      ticksLabels: ["Продать", "Скорее продать", "Скорее держать", "Держать"],
      showIntentionSlider: false,
    };
  },
  watch: {
    reset(newV, oldV) {
      if (!newV && oldV) {
        this.sellingDecision = 2;
      }
    },
  },

  methods: {
    clickOnIntention() {
       this.showIntentionSlider = true;
       this.sellingDecision=this.initialSliderValue
    },
    changeSliderValue(val) {
      if (val === 3) {
        this.showIntentionSlider = false;
        this.sellingDecision=this.initialSliderValue
      }
      this.$emit("sliderValChange", val);
    },
  },
};
</script>
