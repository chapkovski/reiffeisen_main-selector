<template>
  <v-app>
    <input type="hidden" :value="currentPrice" name="exit_price" />
    <v-app-bar app height="220">
      <v-card elevation="4" v-if="newPrice" height="150" min-width="200">
        <v-card-title>
          <span class="word-break">Текущая цена портфеля:</span>
        </v-card-title>
        <v-card-text class="text-h5 font-weight-bold">
          <h2>
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
          <h2>{{ parseFloat(currentROR * 100).toFixed(2) }}%</h2>
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
import { differenceInSeconds } from "date-fns";
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

function sd(array) {
  const n = array.length;
  const mean = array.reduce((a, b) => a + b) / n;
  return Math.sqrt(
    array.map((x) => Math.pow(x - mean, 2)).reduce((a, b) => a + b) / n
  );
}

export default {
  name: "App",
  components: {
    highcharts: Chart,
    ConfirmDialog,
  },
  data: function() {
    const chunkSize = 10;
    const firstVal = window.data.slice(0, chunkSize);

    return {
      previousChunk: firstVal,
      submittable: false,
      startTime: new Date(),
      endTime: null,
      timeSpent: null,
      initialSliderValue: 2,
      reset: false,
      sliderValue: 100,
      newPrice: _.last(firstVal),

      dialog: false,

      tweenedPrice: null,
      counter: chunkSize,
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
              value: 100,
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
    currentPrice() {
      return _.last(this.chartOptions.series[0].data);
    },
    currentROR() {
      return (this.newPrice - window.data[0]) / window.data[0];
    },
    formattedTween() {
      return this.tweenedPrice.toFixed(2);
    },
    customComp() {
      return comps[`Comp${window.componentNumber}`];
    },
  },
  watch: {
    async submittable(val) {
      if (val) {
        await this.sendMessage({ name: "Trade_ends" });
        document.getElementById("form").submit();
      }
    },
    newPrice: function(newValue) {
      gsap.to(this.$data, {
        duration: 0.5,
        tweenedPrice: newValue,
        onUpdate: this.tweenUpd,
      });
    },
  },
  async created() {
    this.$options.sockets.onopen = async () =>
      await this.sendMessage({ name: "Trade_starts" });
    this.$options.sockets.onmessage = (data) => console.log(data);
  },
  async mounted() {
    this.stockInterval = setInterval(async () => {
      if (!this.dialog) {
        this.previousChunk = window.data.slice(
          this.counter - this.chunkSize,
          this.counter
        );
        const newCounter = this.counter + this.chunkSize;
        this.newPrice = window.data[newCounter];
        const oldCounter = this.counter;

        this.previousPrice = window.data[this.counter];

        const newData = window.data.slice(this.counter, newCounter);
        this.counter += this.chunkSize;

        if (this.newPrice) {
          this.checkForSharpChanges(newData, oldCounter);
          this.chartOptions.series[0].data.push(...newData);
          this.chartOptions.xAxis.plotBands[0].from = oldCounter;
          this.chartOptions.xAxis.plotBands[0].to = newCounter;
        } else {
          this.submittable = true;
        }
      }
    }, this.tickFrequency * 1750);
  },
  methods: {
    checkForSharpChanges(data, startPosition) {
      const mean = _.mean(this.previousChunk);
      const std = sd(this.previousChunk);
      const that = this;
      _.forEach(data,  function(v, k) {
        const normalizedValue = Math.abs((v - mean) / std);
        if (normalizedValue > 15) {
          const msg = {
            name: "sharpChangeDetected",
            value: v,
            position: k + startPosition,
          };
          that.sendMessage(msg);
          return false;


        }
      });
    },
    async sendMessage(obj) {
      if (this.$socket.readyState == 1) {
        const inj = {
          currentPrice: this.currentPrice,
          priceIndex: this.counter,
          secs_since_round_starts: differenceInSeconds(
            new Date(),
            this.startTime
          ),
        };

        await this.$socket.sendObj({ ...obj, ...inj });
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
      });

      this.sliderValue = val;
      if (val == 0) {
        await this.sendMessage({
          name: "show confirming dialog",
        });
        this.dialog = true;
      }
    },

    async continueKeeping() {
      await this.sendMessage({
        name: "Continue keeping",
      });
      this.sliderValue = 100;
      this.dialog = false;

      this.initialSliderValue = 2;
    },
    async sell() {
      await this.sendMessage({ name: "Sell" });
      this.dialog = false;
      this.submittable = true;
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
