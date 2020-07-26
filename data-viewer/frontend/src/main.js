// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import '@/http'
import qs from 'qs'
import Vuetify from 'vuetify'
import 'vuetify/dist/vuetify.min.css'
import '@mdi/font/css/materialdesignicons.css'                                 //Ensure you are using css-loader
import 'material-design-icons-iconfont/dist/material-design-icons.css'         //Ensure you are using css-loader
import store from '@/store'


Vue.prototype.$qs = qs;
Vue.use(Vuetify);
const opts = {
  icons: {
    iconfont: 'md',                                                            //default - only for display purposes
  },
};

Vue.config.productionTip = false;

/* eslint-disable no-new */
new Vue({
  data: {
    sharedState: store.state
  },
  el: '#app',
  router,
  vuetify: new Vuetify(opts),
  components: { App },
  template: '<App/>'
});
