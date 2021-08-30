import {getCookie} from './components/global/cookie'
import axios from 'axios'
import store from './store/store.js'
import {showFullScreenLoading,tryHideFullScreenLoading } from './loading.js'
axios.defaults.timeout = 5000  //超时终止请求
axios.defaults.baseURL ='http://127.0.0.1:9090'  //配置请求地址
import router from '../router/index'

//http request 拦截器
axios.interceptors.request.use(
  config => {
    if (config.data) {
      config.data = JSON.stringify(config.data).replace(/\s*/g, '') // 去除空格
    }
    
    config.headers = {
      'Content-Type':'application/json;charset=UTF-8' 
    }
    var authorization =  sessionStorage.getItem("authorization")
		var uuid = sessionStorage.getItem('uuid')
		var userid = store.state.user.userid
			if(authorization){
				config.headers.authorization = authorization
			}
		if(uuid){
			config.headers.uuid = uuid
		}
		if(userid){
			config.headers.userid = userid
		}
    // console.log(config)
    showFullScreenLoading()
    return config;
  },
  error => {
    return Promise.reject(error)
  }
);
 
//http response 拦截器
axios.interceptors.response.use(
  response => {
    tryHideFullScreenLoading()
    if(response.data.code == 0){
      var str = (window.location.href).split('/')
      var r = str[str.length-1]
      r = r.substr(0,3)
      if(r=='Stu'||r=='Tea'){
        router.replace("/login")
      }else{
        router.replace("/loginAdmin")
      }
    }
    return response;
  },
  error => {
    tryHideFullScreenLoading()
    return Promise.reject(error)
  }
)
 

/**
 * 封装get方法
 * @param url
 * @param data
 * @returns {Promise}
 */
 
export function fetch(url,params={}){
  return new Promise((resolve,reject) => {
    axios.get(url,{
      params:params
    })
      .then(response => {
        resolve(response.data);
      })
      .catch(err => {
        reject(err)
      })
  })
}
 
/**
 * 封装post请求
 * @param url
 * @param data
 * @returns {Promise}
 */
 
export function post(url,data = {}){
  return new Promise((resolve,reject) => {
    axios.post(url,data)
      .then(response => {
        resolve(response.data);
      },err => {
        reject(err)
      })
  })
}
 
/**
 * 封装patch请求
 * @param url
 * @param data
 * @returns {Promise}
 */
 
export function patch(url,data = {}){
  return new Promise((resolve,reject) => {
    axios.patch(url,data)
      .then(response => {
        resolve(response.data);
      },err => {
        reject(err)
      })
  })
}
 
/**
 * 封装put请求
 * @param url
 * @param data
 * @returns {Promise}
 */
 
export function put(url,data = {}){
  return new Promise((resolve,reject) => {
    axios.put(url,data)
      .then(response => {
        resolve(response.data);
      },err => {
        reject(err)
      })
  })
}