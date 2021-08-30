<template>
  <div style="height:80px">
  <div id="header">
    <img id="markpng" src="../../assets/logo1.png" width="80px" height="80px">
    <p id="header_p"><span id="header_span">{{schoolName}}</span>选课管理系统</p>
    <div id="topicon">
      <el-button type="text" icon="el-icon-info"></el-button>
      <span style="color: #FFFFFF;"><b>{{userid}}&nbsp;{{username}}&nbsp;&nbsp;</b></span>
      <el-button type="text" icon="el-icon-switch-button" :style="{display: visible}" @click="logout">退出登录</el-button>
    </div>
  </div>
  </div>
</template>

<script>
import {delCookie,getCookie} from '../global/cookie'
import bus from '../global/bus'
import {mapGetters,mapMutations} from 'vuex'
export default {
    data(){
      return{
        schoolName: "岭南师范学院",
        typeName:''
      }
    },
    computed:{
      ...mapGetters([
        'getUser'
      ]),
      visible(){
        if(this.$route.path=="/login"|| this.$route.path=="/loginAdmin" || this.$route.path=="/forgot"){
          return 'none'
        }
        return 'inline'
      },
      userid(){
        if(this.$route.path=="/login"|| this.$route.path=="/loginAdmin" || this.$route.path=="/forgot"){
          return ' '
        } 
        return this.getUser.userid
      },
      username(){
        if(this.$route.path=="/login"|| this.$route.path=="/loginAdmin" || this.$route.path=="/forgot"){
          return '请登录'
        }
        return this.getUser.username
      },
      // typeName(){
      //   let type = sessionStorage.getItem("userType")
      //   if (type==='1'){
      //     return '(学生端)'
      //   } else if (type==='2'){
      //     return '(教师端)'
      //   } else if (type==='3'){
      //     return '(管理员端)'
      //   } else {
      //     return ''
      //   }
      // }
      // typeName(){
      //   let type = this.$store.getters.getUser.userType
      //   if (type===1){
      //     return '(学生端)'
      //   } else if (type===2){
      //     return '(教师端)'
      //   } else if (type===3){
      //     return '(管理员端)'
      //   } else {
      //     return ''
      //   }
      // }
    },
    mounted() {
      // let type = sessionStorage.getItem("userType")
      // // console.log(typeof type)
      // let typeName
      // if (type==='1'){
      //   typeName = '(学生端)'
      // } else if (type==='2'){
      //   typeName = '(教师端)'
      // } else if (type==='3'){
      //   typeName = '(管理员端)'
      // }
      this.schoolName += this.typeName
    },
    created() {
      let type = this.$store.getters.getUser.userType
      if (type===1){
        this.typeName =  '(学生端)'
      } else if (type===2){
        this.typeName =  '(教师端)'
      } else if (type===3){
        this.typeName =  '(管理员端)'
      } else {
        this.typeName =  ''
      }
      
      bus.$on('updateSystemType', type => {
        console.log('bustype',type)
        if (type==1){
          this.typeName =  '(学生端)'
        } else if (type==2){
          this.typeName = '(教师端)'
        } else if (type==3){
          this.typeName = '(管理员端)'
        } else {
          this.typeName =  ''
        }
        this.$forceUpdate()
      })
    },
    methods:{
      ...mapMutations([
        '$_setUser'
      ]),
      logout(){
        this.$confirm('确定退出登录?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          this.$axios
          .post('/public/logout/', {})
          .then((result)=> {
            if(result.data.code==302){
              // delCookie('userid')
              // delCookie('authorization')
              // delCookie('username')
              // delCookie('perm')
              sessionStorage.removeItem('authorization')
              sessionStorage.removeItem('store')
              sessionStorage.removeItem('userType')
              
              this.$store.commit('$_removeToken')
              this.$store.commit('$_setUser',{})
              this.$store.commit('$_setPerm','')
              var r = (this.$route.path).substr(0,4)
              bus.$emit('updateSystemType', '')
              if(r=='/Stu'||r=='/Tea'){
                this.$router.replace({ path: '/login' });
              }else{
                this.$router.replace({ path: '/loginAdmin' });
              }
            }
          })
          .catch((error)=> {
            alert(error)
          })
        }).catch(() => {});
      }
    }
  }
</script>
<style>
  #header{
    height: 60px;
    background-color: #547387;
  }
  #markpng{
    position: absolute;
    left: 65px;
    top: 0px;
  }
  #header_p{
    position: relative;
    left: 135px;
    top:8px;
    font-size: 25px;
    font-weight: bold;
    color: white;
  }
  #header_span{
    font-size: 40px;
    font-weight: bold
  }
  #topicon{
    position: relative;
    text-align: right;
    top: -45px;
    right: 30px;
  }
  .el-button{
    margin-right: 20px;
  }
  .el-icon-s-claim{
    font-size: 16px;
    color: #3c4850;
  }
  .el-icon-s-claim:hover{
    color: #a1c4db;
  }
  .el-icon-switch-button{
    font-size: 16px;
    color: #3c4850;
  }
  .el-icon-switch-button:hover{
    color: #a1c4db;
  }
  .el-icon-info{
    font-size: 16px;
    color: #3c4850;
  }
  .el-icon-info:hover{
    color: #a1c4db;
  }
</style>