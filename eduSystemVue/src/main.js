import Vue from 'vue'
import App from './App.vue'
import axios from 'axios'
import './components/global/global.css'
import router from '../router/index'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import {post,fetch,patch,put} from "./http.js"
import {getCookie} from './components/global/cookie'
import store from './store/store.js'
import common from './utils/common.js'

import {Message} from 'element-ui'
Vue.use(ElementUI)
// require('./mock.js')
 
axios.defaults.withCredentials = true
axios.defaults.crossOrigin = true
Vue.prototype.$axios=axios
Vue.prototype.$post=post
Vue.prototype.$fetch=fetch
Vue.prototype.$patch=patch
Vue.prototype.$put=put
Vue.prototype.$common = common    // 全局变量
axios.defaults.baseURL='http://127.0.0.1:9090/'
Vue.prototype.$message = Message

// axios.defaults.headers.post['Content-Type'] = 'application/json;charset=UTF-8'

Vue.config.productionTip = false

// 全局路由构造函数，判断是否登录和要跳转到页面
router.beforeEach((to, from, next) => {
  // console.log(to.matched.some(record=>record.meta.requireAuth))
  let token = sessionStorage.getItem('authorization')
  if(!token){
    // 1、当用户打开localhost，to.matched === []，匹配的是空路由，此时需要重定向到login
    // 2、重定向到login之后，to.matched === [name: "login", path: "/login"...] 就是上一步的login页面
    // to.matched.some(item => item.meta.requiresAuth) 这句的意思是 进入的路由页需要登录认证，取反就是不用登录，直接通过
    if(to.matched.length > 0 && !to.matched.some(m => m.meta.requireAuth)){
      next();  // 跳过，进入下一个导航钩子。比如：在 /login 路由页刷新页面会走到此逻辑
    } else {
      next({ path: '/login' })
    }
  } else {
    next()
    // 菜单权限在这里实现操作
  }
})

// 22全局路由构造函数，判断是否登录和要跳转到页面
// router.beforeEach((to, from, next) => {
//   if (to.matched.some(m => m.meta.requireAuth)) {    // 需要登录
//     let token = getCookie('authorization')
//     // if(token && window.localStorage.isLogin === '1'){
//     if(token){
//       next()
//     } else if (to.path !== '/login') {
//       // let token = window.localStorage.token;
//       if (token === 'null' || token === '' || token === undefined){
//           next({path: '/login'})
//           // Toast({ message: '检测到您还未登录,请登录后操作！', duration: 1500 })
//           console.log('请你登录')
//       }
//     } else {
//       next()
//     }
//   // } else {   // 不需要登录
//   //   next()
//   }
// })

new Vue({
  store,
  router,
  render: h => h(App),
}).$mount('#app')
