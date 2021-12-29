import Vue from "vue";
import SelectApp from "./SelectApp.vue";
import vuetify from "./plugins/vuetify";
import Highcharts from "highcharts";
import Stock from "highcharts/modules/stock";
import HighchartsVue from "highcharts-vue";
import VueNativeSock from "vue-native-websocket";
import "vuetify/dist/vuetify.min.css";
Stock(Highcharts);
Vue.use(HighchartsVue);
Vue.config.productionTip = false;

const ws_scheme = window.location.protocol === "https:" ? "wss" : "ws";
const ws_path = ws_scheme + "://" + window.location.host + window.socket_path;

Vue.use(VueNativeSock, ws_path, {
  format: "json",
  reconnection: true, // (Boolean) whether to reconnect automatically (false)
  reconnectionAttempts: 5, // (Number) number of reconnection attempts before giving up (Infinity),
  reconnectionDelay: 3000,
});

new Vue({
  vuetify,
  render: (h) => h(SelectApp),
}).$mount("#app");
