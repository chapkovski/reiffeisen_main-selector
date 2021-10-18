<template>
  <v-btn tile height="100%" active-class="aa">
    <div>
      <v-card class="p-3 m-3">
        <v-card-text>
          <highcharts
            :constructorType="'stockChart'"
            class="hc"
            :options="chartOptions"
            :updateArgs="updateArgs"
            ref="priceGraph"
          ></highcharts>
        </v-card-text>
      </v-card>
    </div>
  </v-btn>
</template>

<script>
import { Chart } from "highcharts-vue";
import _ from "lodash";
const _data = _.map(window.data, (i) => i.data);
const yMin = _.min(_.flattenDeep(_data));
const yMax = _.max(_.flattenDeep(_data));
export default {
  components: {
    highcharts: Chart,
  },
  props: ["data", "animated"],
  name: "SmallChart",
  data: function() {
    return {
      counter: 0,
      pointer: 0,
      updateArgs: [true, true, true],
      chartOptions: {
        chart: {
          height: 200,
          width: 300,
          type: "line",
        },
        credits: false,
        tooltip: { enabled: false },
        navigator: {
          enabled: false,
        },
        rangeSelector: {
          enabled: false,
        },
        yAxis: {
          labels: {
            enabled: true,
          },
          resize: {
            enabled: false,
          },
          gridLineColor: "transparent",
        },
        scrollbar: { enabled: false },
        xAxis: {
          visible: false,
          labels: {
            enabled: false,
          },
        },
        series: [
          {
            data: this.data[0],
          },
        ],
      },
    };
  },
  mounted() {
    this.stockInterval = setInterval(() => {
      if (this.animated) {
        this.counter++;
        this.pointer = this.counter % this.data.length;
        this.$refs.priceGraph.chart.series[0].setData(this.data[this.pointer]);
      }
    }, 1000);
  },

  methods: {},
};
</script>
<style scoped>
.aa {
  background: yellow !important;
}
</style>
