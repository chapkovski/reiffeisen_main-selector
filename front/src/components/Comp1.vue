<template>
  <v-card elevation="4" height="150">
    <v-card-text class="d-flex align-items-center justify-center my-3 ">
      <div>
        <div>
          Довольны результатом? Переместите слайдер вправо (макс 100).
          Недовольны - влево (мин.0).
        </div>
        <div>
          Если хотите продать портфель до срока, переместите слайдер влево до
          упора (на 0). Вас попросят подтвердить решение.
        </div>
      </div>

      <div
        class="d-flex align-items-center justify-center my-3"
        :style="{ height: 150 }"
      >
        <round-slider
          radius="50"
          rangeColor="green"
          :value="sliderValue"
          start-angle="315"
          end-angle="+270"
          line-cap="round"
          :change="changeSliderValue"
        />
      </div>
    </v-card-text>
  </v-card>
</template>

<script>
import RoundSlider from "vue-round-slider";
export default {
  props: ["sliderValue"],
  components: {
    RoundSlider,
  },
  name: "comp1",
  data: () => ({}),
  mounted() {},

  methods: {
    changeSliderValue(val) {
      this.$emit("sliderValChange", val.value);
    },
  },
};
</script>
