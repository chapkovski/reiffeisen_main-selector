import Vue from "vue";
import SelectApp from "./SelectApp.vue";
import vuetify from "./plugins/vuetify";
import Highcharts from "highcharts";
import Stock from "highcharts/modules/stock";
import HighchartsVue from "highcharts-vue";

import "vuetify/dist/vuetify.min.css";
Stock(Highcharts);
Vue.use(HighchartsVue);
Vue.config.productionTip = false;

new Vue({
  vuetify,
  render: (h) => h(SelectApp),
}).$mount("#app");
