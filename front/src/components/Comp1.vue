<template>
  <v-card elevation="4" height="210">
    <v-card-text class="d-flex align-items-top justify-center my-6 text-h6 mb-1">
      <div>
        <div>
          Перемещайте слайдер влево (мин.0) если не удовлетворены результатом,
          <br>
          вправо (макс 100) - если удовлетворены.
          <br>
          Чтобы продать портфель, переместите слайдер влево до
          упора (на 0).
          <br>
          Вам надо будет подтвердить решение.
        </div>
      </div>

      <div
        class="d-flex align-items-top justify-top my-auto"
        :style="{ height: 210 }"
      >
        <round-slider
          radius="90"
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
