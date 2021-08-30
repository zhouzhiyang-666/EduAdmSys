<template>
<el-container>
    <el-aside width="240px" style="background-color: #d6d6d6;">
        <v-leftMenuTea></v-leftMenuTea>
    </el-aside>
    <el-main class="shadow_in_img" :style="{backgroundImage: 'url(' + backImg + ')',backgroundSize:'100% 100%'}">
        <el-row type="flex" justify="center"><el-col :span="21">
            <router-view></router-view>
        </el-col></el-row>
    </el-main>
</el-container>
</template>

<script>
import {getCookie} from '../global/cookie'
import leftMenuTea from './LeftMenuTea.vue'
import backImg from '@/assets/back16.jpg'
export default {
    data(){
        return{
            backImg
        }
    },
    components:{
        'v-leftMenuTea': leftMenuTea
    },
    mounted(){
      if(sessionStorage.getItem("userType")!=2){
          alert("请先登录")
          this.$router.replace({ path: '/' });
      }
    }
}
</script>