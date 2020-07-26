/**
 * axios: 0.19.2
 * https://www.npmjs.com/package/axios
 * 可配置参数：
 * - https://www.npmjs.com/package/axios#request-config
 * - https://www.npmjs.com/package/axios#response-schema
 * - https://www.npmjs.com/package/axios#config-defaults
 * Interceptors：
 * You can intercept requests or responses before they are handled by then or catch.
 * - https://www.npmjs.com/package/axios#interceptors
 */
import axios from 'axios'
import config from '@/config'
import Vue from 'vue'

axios.defaults.baseURL = config.api;
axios.defaults.timeout = 30000;

/**
// Add a request interceptor
axios.interceptors.request.use(function (config) {
    // Do something before request is sent
    return config;
  }, function (error) {
    // Do something with request error
    return Promise.reject(error);
  });
 
// Add a response interceptor
axios.interceptors.response.use(function (response) {
    // Any status code that lie within the range of 2xx cause this function to trigger
    // Do something with response data
    return response;
  }, function (error) {
    // Any status codes that falls outside the range of 2xx cause this function to trigger
    // Do something with response error
    return Promise.reject(error);
  });
*/

axios.loadData = async function (url) {
    const resp = await axios.get(url);
    return resp.data;
}

Vue.prototype.$http = axios;                   //插件。https://cn.vuejs.org/v2/guide/plugins.html
