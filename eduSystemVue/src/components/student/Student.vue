<template>
<el-container>
    <el-aside width="240px" style="background-color: #d6d6d6;">
        <v-leftMenuStu></v-leftMenuStu>
    </el-aside>
    <el-main class="shadow_in_img" :style="{backgroundImage: 'url(' + backImg + ')',backgroundSize:'100% 100%'}">
    <!-- <el-main class="shadow_in_img" style="margon-top:10px;height:700px;backgroundColor:#e3e3e3;"> -->
        <el-row type="flex" justify="center"><el-col :span="21">
            <router-view></router-view>
        </el-col></el-row>
    </el-main>
</el-container>
</template>

<script>
import {getCookie} from '../global/cookie'
import leftMenuStu from './LeftMenuStu.vue'
import backImg from '@/assets/back16.jpg'
import { mapMutations } from 'vuex'

export default {
    data(){
        return{
            backImg,
        }
    },
    components:{
        'v-leftMenuStu': leftMenuStu
    },
    methods:{
      ...mapMutations({
        setDeptOptions:'$_setDeptOptions'
      }),
      getDptName(){
        this.$axios
        .post('/admin/getDptName/', {})
        .then((result)=> {
            if (result.data.code === 1) {  // 返回第一页数据，和
              // this.deptOptions = result.data.datas
              this.setDeptOptions(result.data.datas)
            }else{
              return false;
            }
        })
        .catch((error)=> {
            alert(error)
        })
      }
    },
    created(){
      if(sessionStorage.getItem("userType")!=1){
          alert("请先登录")
          this.$router.replace({ path: '/' });
          return false
      }
      this.getDptName()
    }
}
</script>