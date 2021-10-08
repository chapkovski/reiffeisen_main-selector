<template>
  <v-dialog v-model="dialog" max-width="600">
    <v-card>
      <v-card-title class="text-h5"> Решение о продаже</v-card-title>

      <v-card-text>
        Вы хотите продать портфель? Если Вы выберете "продать", период
        закончится.
      </v-card-text>

      <v-card-actions>
        <v-spacer></v-spacer>
        <div v-if="!innerSlider">
          <v-btn-toggle>
            <v-btn color="green darken-1" @click="continueKeeping">
              Оставить
            </v-btn>

            <v-btn color="red darken-1" @click="sell"> Продать</v-btn>
          </v-btn-toggle>
        </div>
        <div v-else>
          <slider @sliderValChange="conditionalSelling" />
        </div>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import Comp3 from "./Comp3";
export default {
  props: ["dialog", "currentPrice"],
  components: {
    slider: Comp3,
  },
  data: () => ({ innerSlider: window.innerSlider }),

  methods: {
    async conditionalSelling(val) {
      if (this.$socket.readyState == 1) {
        const obj = {
          name: "slider value changed",
          sliderValue: val,
          currentPrice: this.currentPrice,
        };
        await this.$socket.sendObj(obj);
      }

      if (val == 0) {
        this.sell();
      }
    },
    sell() {
      this.$emit("sell");
    },
    continueKeeping() {
      this.$emit("continueKeeping");
    },
  },
};
</script>
