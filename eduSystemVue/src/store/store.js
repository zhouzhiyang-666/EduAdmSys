//  store.js 中都mutation中增加添加和删除token的方法
import Vue from 'vue'
import Vuex from 'vuex'
Vue.use(Vuex)

const state = {     // 全局管理的数据存储
   isLogin:true,
   user:'',
   user:'',
   token:'',
   activeMenu:'', // 当前点击的菜单
   perm:0,
   deptOptions:[],  // 学院选择
};
export default new Vuex.Store({
	state,
	getters:{    // 监听数据变化的
		getToken(state){   // 获取本地存储的登录信息
		  if(!state.token){
			state.token =JSON.parse(getCookie('Authorization'))
		  }
		  return state.token
		},
		getIsLogin(state){
		  return state.isLogin
		},
		getActiveName(state){
		  return state.activeMenu
		},
    getUser(state){
      return state.user
    },
    getPerm(state){
      return state.perm
    },
    getDeptOptions(state){
      return state.deptOptions
    }
	},
	mutations:{
		$_setToken(state, value) { // 设置存储token
		  state.token = value;
		  // sessionStorage.setItem('authorization', value);
		},
		$_removeToken(state, value){  // 删除token
    state.token = ''
		  // sessionStorage.removeItem('authorization');
		},
		$_setNotLogin(state, value) {
		  state.isLogin = false
		},
		$_setIsLogin(state, value) {
		  state.isLogin = true
		},
		$_setActiveMenu(state, value) {
		  state.activeMenu = value
		},
		$_setUser(state, value) {
		  state.user = value
		},
    $_setPerm(state, value) {
      state.perm = value
    },
    $_setDeptOptions(state, value) {
      // value.unshift({id:'0',name:'全部'})
      state.deptOptions = value
    }
	}
})
