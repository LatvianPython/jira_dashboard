import Vue from "vue";
import BootstrapVue from "bootstrap-vue";
import Index from "./components/Index";
import Sprint from "./components/Sprint";
import Login from "./components/Login";
import Logoff from "./components/Logoff";
import Selectable from "./components/Selectable";
import ChangeRequests from "./components/ChangeRequests";
import Maintenance from "./components/Maintenance";
import Generic from "./components/Generic";
import Tested from "./components/Tested";
import FixVersions from "./components/FixVersions";
import App from "./App.vue";
import "bootstrap";
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap-vue/dist/bootstrap-vue.css";
import VueRouter from "vue-router";

Vue.config.productionTip = false;
Vue.use(VueRouter);
Vue.use(BootstrapVue);

const routes = [
  { path: "/", component: Index, name: "Index" },
  { path: "/sprint", component: Sprint, name: "Sprint" },
  { path: "/generic/:filter_id", component: Generic, name: "Generic" },
  { path: "/login", component: Login, name: "Login" },
  { path: "/logoff", component: Logoff, name: "Logoff" },
  { path: "/selectable", component: Selectable, name: "Selectable" },
  { path: "/maintenance", component: Maintenance, name: "Maintenance" },
  {
    path: "/change_requests",
    component: ChangeRequests,
    name: "ChangeRequest"
  },
  { path: "/tested", component: Tested, name: "Tested" },
  { path: "/fix_versions", component: FixVersions, name: "FixVersions" }
];

const router = new VueRouter({
  routes: routes,
  mode: "history",
  linkExactActiveClass: "active"
});

import axios from "axios";

axios.interceptors.response.use(
  response => response,
  error => {
    const { status } = error.response;
    const current_path = router.currentRoute.path;
    if (status === 401 && current_path !== "/login") {
      router.push({
        name: "Login",
        query: { redirect: current_path }
      });
    }
    return Promise.reject(error);
  }
);

Vue.prototype.$localStorage = new Vue({
  data: { token: localStorage.getItem("token") },
  watch: {
    token(value) {
      if (value) {
        localStorage.setItem("token", value);
      } else {
        localStorage.removeItem("token");
      }
    }
  }
});

new Vue({
  el: "#app",
  render: h => h(App),
  router: router
}).$mount("#app");
