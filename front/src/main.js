// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import Element from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import VueResource from 'vue-resource'
import axios from 'axios'

Vue.prototype.axios = axios

Vue.prototype.axios.interceptors.request.use(config => {
  let token = sessionStorage.getItem('accessToken')
  console.log(token)
  if (token) {
    config.headers.Authorization = token
  }
  return config
}, error => {
  return Promise.reject(error)
})

Vue.use(Element)
Vue.use(VueResource)
Vue.config.productionTip = false
router.beforeEach((to, from, next) => {
  // 如果即将进入的路由对象是登录页，则进行跳转，否则验证是否携带accessToken,如果有，则进
  // 行跳转，没有，则不允许跳转
  if (to.path === '/login') {
    next()
  } else {
    if (sessionStorage.getItem('accessToken')) {
      if (to.path === '/adminIndex') {
        if (sessionStorage.getItem('role') === '10') {
          next()
        } else {
          next('/login')
        }
      } else {
        next()
      }
    } else {
      next('/login')
    }
  }
})

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
