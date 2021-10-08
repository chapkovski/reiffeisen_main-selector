<template>
  <v-app>
    <v-app-bar app height="220">
      <v-card elevation="4" v-if="newPrice" height="150" min-width="200">
        <v-card-title>
          <span class="word-break">Текущая цена портфеля:</span>
        </v-card-title>
        <v-card-text class="text-h5 font-weight-bold">
          <h2>
            <v-icon x-large :color="direction.color"
              >{{ direction.icon }}
            </v-icon>

            {{ tweenedPrice || newPrice }}
          </h2>
        </v-card-text>
      </v-card>
      <v-card
        elevation="4"
        v-if="currentROR"
        class="mx-3"
        height="150"
        min-width="200"
      >
        <v-card-title>
          <span class="word-break">Текущая доходность:</span>
        </v-card-title>
        <v-card-text class="text-h5 font-weight-bold">
          <h2>
            <v-icon x-large :color="direction.color"
              >{{ direction.icon }}
            </v-icon>

            {{ parseFloat(currentROR * 100).toFixed(2) }}%
          </h2>
        </v-card-text>
      </v-card>
      <component
        :is="customComp"
        @sliderValChange="sliderValChange"
        :sliderValue="sliderValue"
        :initialSliderValue="initialSliderValue"
        @showDialog="innerShowDialog"
        :reset="dialog"
      />
    </v-app-bar>
    <confirm-dialog
      :dialog="dialog"
      :currentPrice="newPrice"
      @sell="sell"
      @continueKeeping="continueKeeping"
    ></confirm-dialog>
    <v-main>
      <v-container fluid>
        <v-row>
          <v-col cols="12">
            <highcharts
              :constructorType="'stockChart'"
              class="hc"
              :options="chartOptions"
              ref="chart1"
              :updateArgs="[true, true, true]"
            ></highcharts>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
/* eslint-disable */

// import(/* webpackChunkName: "about" */ "../views/About.vue")
import { Chart } from "highcharts-vue";
import Comp1 from "./components/Comp1";
import ConfirmDialog from "./components/ConfirmDialog";
import Comp2 from "./components/Comp2";
import Comp3 from "./components/Comp3";
import Comp4 from "./components/Comp4";
const comps = { Comp1, Comp2, Comp3, Comp4 };
import gsap from "gsap";
import _ from "lodash";

const firstOne = window.data[0];
const ror = _.map(window.data, (i) => (i - firstOne) / firstOne);

const formatDown = {
  color: "red",
  icon: "mdi-arrow-down-bold",
};
const formatUp = {
  color: "green darken-3",
  icon: "mdi-arrow-up-bold",
};

export default {
  name: "App",
  components: {
    highcharts: Chart,
    ConfirmDialog,
  },
  data: function() {
    const chunkSize = 10;
    const firstVal = window.data.slice(0, chunkSize);
    const rorFirstVal = ror.slice(0, chunkSize);
    return {
      initialSliderValue: 2,
      reset: false,
      sliderValue: 100,
      currentROR: (_.last(firstVal) - window.data[0]) / window.data[0],
      newPrice: window.data[0],
      previousPrice: window.data[0],

      dialog: false,

      tweenedPrice: null,
      counter: 0,
      chunkSize,
      stockIntervall: null,
      tickFrequency: 3,
      chartOptions: {
        xAxis: {
          max: window.data.length,
          ordinal: false,
          plotBands: [
            {
              borderColor: "red",
              borderWidth: 1,
              color: "#FCFFC5", // Color value
              from: 0,
              to: null,
            },
          ],
        },
        yAxis: {
          min: window.data[0] - (window.data[0] - window.drawdown) * 2,
          plotLines: [
            {
              value: window.drawdown,
              color: "red",
              width: 2,
              dashStyle: "shortdash",
            },
          ],
        },
        navigator: { enabled: false },
        rangeSelector: {
          inputEnabled: false,
          selected: false,
        },
        series: [
          {
            data: firstVal,
          },
        ],
      },
    };
  },
  computed: {
    formattedTween() {
      return this.tweenedPrice.toFixed(2);
    },
    customComp() {
      return comps[`Comp${window.componentNumber}`];
    },
    direction() {
      if (this.currentPrice > this.previousPrice) {
        return formatUp;
      } else {
        return formatDown;
      }
    },
  },
  watch: {
    newPrice: function(newValue) {
      gsap.to(this.$data, {
        duration: 0.5,
        tweenedPrice: newValue,
        onUpdate: this.tweenUpd,
      });
    },
  },
  async mounted() {
    this.$options.sockets.onmessage = (data) => console.log(data);
    this.stockInterval = setInterval(() => {
      const newCounter = this.counter + this.chunkSize;
      this.newPrice = window.data[newCounter];
      const oldCounter = this.counter;
      this.currentROR = (this.newPrice - window.data[0]) / window.data[0];
      this.previousPrice = window.data[this.counter];

      const newData = window.data.slice(this.counter, newCounter);
      this.counter += this.chunkSize;

      if (this.newPrice) {
        this.chartOptions.series[0].data.push(...newData);
        this.chartOptions.xAxis.plotBands[0].from = oldCounter + this.chunkSize;
        this.chartOptions.xAxis.plotBands[0].to = newCounter + this.chunkSize;
      } else document.getElementById("form").submit();
    }, this.tickFrequency * 1000);
  },
  methods: {
    async sendMessage(obj) {
      if (this.$socket.readyState == 1) {
        await this.$socket.sendObj(obj);
      }
    },
    tweenUpd(v) {
      this.tweenedPrice = _.round(this.tweenedPrice, 2);
    },
    innerShowDialog() {
      this.dialog = true;
    },
    async sliderValChange(val) {
      await this.sendMessage({
        name: "slider value changed",
        sliderValue: val,
        currentPrice: this.newPrice,
      });

      this.sliderValue = val;
      if (val == 0) {
        await this.sendMessage({
          name: "show confirming dialog",
          currentPrice: this.newPrice,
        });
        this.dialog = true;
      }
    },

    async continueKeeping() {
      await this.sendMessage({
        name: "Continue keeping",
        currentPrice: this.newPrice,
      });
      this.sliderValue = 100;
      this.dialog = false;

      this.initialSliderValue = 2;
    },
    async sell() {
      await this.sendMessage({ name: "Sell", currentPrice: this.newPrice });
      this.dialog = false;
      document.getElementById("form").submit();
    },
  },
};
</script>

<style>
#app {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
.word-break {
  word-break: break-word;
}
</style>
