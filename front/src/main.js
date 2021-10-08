import Vue from "vue";
import App from "./App.vue";
import vuetify from "./plugins/vuetify";
import Highcharts from "highcharts";
import Stock from "highcharts/modules/stock";
import HighchartsVue from "highcharts-vue";
import VueNativeSock from "vue-native-websocket";

const ws_scheme = window.location.protocol === "https:" ? "wss" : "ws";
const ws_path = ws_scheme + "://" + window.location.host + window.socket_path;
console.debug("WASPATH", ws_path);
Vue.use(VueNativeSock, ws_path, {
  format: "json",
  reconnection: true, // (Boolean) whether to reconnect automatically (false)
  reconnectionAttempts: 5, // (Number) number of reconnection attempts before giving up (Infinity),
  reconnectionDelay: 3000,
});

import "vuetify/dist/vuetify.min.css";
Stock(Highcharts);
Vue.use(HighchartsVue);
Vue.config.productionTip = false;

new Vue({
  vuetify,
  render: (h) => h(App),
}).$mount("#app");
