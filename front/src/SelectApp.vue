<template>
  <v-app>
    <v-app-bar app fixed>
      <div>
        Для просмотра типичных траекторий при каждом уровне риска нажмите на
        график. Помните что все графики ориентировочны:
        <br />
        фактическая стоимость Вашего портфеля будет всегда разной. Выберите
        предпочтительный график и нажмите Выбрать
      </div>
      <div>
        <v-card class="mx-3"
          ><v-card-text>
            Выбранный уровень риска: {{ volatilityValue }}</v-card-text
          ></v-card
        >
      </div>
      <v-spacer> </v-spacer>
      <div>
        <v-btn @click="submit" :disabled="volatility === null">Выбрать</v-btn>
      </div>
    </v-app-bar>
    <input type="hidden" name="volatility" :value="volatilityValue" />
    <v-main app>
      <v-btn-toggle
        v-model="volatility"
        dense
        active-class="aa"
        class="d-flex flex-wrap"
      >
        <small-chart
          v-for="i in charts"
          :key="i.volatility"
          :animated="parseFloat(i.volatility) === volatilityValue"
          :data="i.data"
          :yMin="yMin"
          :yMax="yMax"
        ></small-chart>
      </v-btn-toggle>
    </v-main>
  </v-app>
</template>

<script>
/* eslint-disable */
import { differenceInSeconds } from "date-fns";
import SmallChart from "./components/SmallChart";
import _ from "lodash";
const _data = _.map(window.data, (i) => i.data);
const yMin = _.min(_.flattenDeep(_data));
const yMax = _.max(_.flattenDeep(_data)) * 0.5;

export default {
  name: "SelectApp",
  components: {
    SmallChart,
  },
  data: function() {
    return {
      startTime: new Date(),
      charts: window.data,
      volatility: null,
      yMin,
      yMax,
    };
  },
  computed: {
    volatilityValue() {
      if (!(_.isNull(this.volatility) || _.isUndefined(this.volatility))) {
        return window.data[this.volatility].volatility;
      }
    },
  },
  watch: {
    async volatility(val, oldVal) {
      await this.sendMessage({
        name: "Decision_volatility_changed",
        volatility: val,
        old_volatility: oldVal,
      });
    },
  },

  async created() {
    this.$options.sockets.onopen = async () =>
      await this.sendMessage({ name: "Decision_starts" });
  },
  methods: {
    async sendMessage(obj) {
      if (this.$socket.readyState == 1) {
        const inj = {
          secs_since_round_starts: differenceInSeconds(
            new Date(),
            this.startTime
          ),
        };

        await this.$socket.sendObj({ ...obj, ...inj });
      }
    },
    async submit() {
      await this.sendMessage({ name: "Decision_ends" });
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
.v-item--active {
  background: yellow;
}
.aa {
  background: yellow;
}
</style>
