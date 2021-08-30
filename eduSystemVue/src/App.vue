<template>
  <div id="app">  
  <!-- <el-container">
    <el-header height="60px">
      <v-header></v-header>
    </el-header>
    <el-main style="position:absolute;padding:0;margin:0;margin-top:60px;height:100%;width:100%">
      <router-view>   
      </router-view>
    </el-main>
  </el-container"> -->
  <el-container>
  <el-header class="shadow_out">
      <v-header></v-header>
  </el-header>
    <router-view></router-view>
  </el-container>
  <!-- <v-footer></v-footer> -->
</div>
</template>

<script>
  import header from './components/common/Header.vue'
  import footer from './components/common/Footer.vue'
  import loginUser from './components/login/LoginUser.vue'

  export default {
    name: 'App',
    components:{
      'v-header':header,
      'v-footer':footer,
      'v-loginUser':loginUser,
    },
    created () {
      //在页面加载时读取sessionStorage里的状态信息
      if (sessionStorage.getItem("store") ) {
        console.log('将session保存至state',this.$store.state)
        this.$store.replaceState(Object.assign({}, this.$store.state,JSON.parse(sessionStorage.getItem("store"))))
        // sessionStorage.removeItem('store')
      } 
  
      //在页面刷新时将vuex里的信息保存到sessionStorage里
      window.addEventListener("beforeunload",()=>{
        if(this.$route.path)
        sessionStorage.setItem("store",JSON.stringify(this.$store.state))
      })
    }
  }
</script>

<style>

</style>