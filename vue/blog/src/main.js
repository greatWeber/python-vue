// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import {Get, Post} from './utils/http'
import axios from 'axios'
import mavonEditor from 'mavon-editor'

import alerts from './components/common/alerts.vue'
import confirms from './components/common/confirms.vue'
import paging from './components/common/paging.vue'
import load from './components/common/load.vue'



Vue.prototype.$get = Get;
Vue.prototype.$post = Post;
Vue.prototype.$ajax = axios;
Vue.prototype.HOST = 'http://127.0.0.1:8088/';

Vue.component('alerts',alerts);
Vue.component('confirms',confirms);
Vue.component('paging',paging);
Vue.component('load',load);
Vue.config.productionTip = false;

Vue.use(mavonEditor)

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App  },
  template: '<App/>'
})
