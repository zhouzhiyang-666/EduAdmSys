<template>
<div id="loginUser" class="login_div">
  <span class="login_span">用户登录</span>
  <el-divider></el-divider>
  <el-form :model="loginForm" :rules="rules" ref="loginForm">
  <el-form-item prop="user">
      <el-input v-model="loginForm.user" placeholder="用户名" 
                @keyup.enter.native="submitForm('loginForm')"
                @blur="loginForm.user=loginForm.user.replace(/\s*/g, '')"></el-input>
  </el-form-item>
  
  <el-form-item prop="passwd">
    <el-input v-model="loginForm.passwd" placeholder="密码" 
                @keyup.enter.native="submitForm('loginForm')" 
                @blur="loginForm.passwd=loginForm.passwd.replace(/\s*/g, '')"
                show-password></el-input>
  </el-form-item>
  
  <el-form-item prop="vcode">
    <el-col :span="12">
      <el-input v-model="loginForm.vcode" maxlength="5" placeholder="验证码" 
                @keyup.enter.native="submitForm('loginForm')"
                style="width: 130px"
                @blur="loginForm.vcode=loginForm.vcode.replace(/\s*/g, '')"
                ></el-input> 
    </el-col>
    <el-col :span="12">
      <img id="code_img" src="" @click="changeCode()" style="height:40px; width: 100px; margin-left:25px; cursor: pointer;" title="点击更换" >
    </el-col>
  </el-form-item>
  
  <el-form-item style="margin-top: -40px;margin-bottom: 0px;">
    <el-radio v-model="loginForm.userType" label="1">学生</el-radio>
    <el-radio v-model="loginForm.userType" label="2">教师</el-radio>
  </el-form-item>
  
  <el-form-item>
    <el-button @keyup.enter.native="submitForm('loginForm')" type="primary" @click="submitForm('loginForm')" style="width: 250px">登录</el-button>
  </el-form-item>
</el-form>
  <el-link type="primary" style="cursor: pointer;" @click="toForgot">忘记密码?</el-link>
</div>
</template>

<script>
	
import {setCookie, getCookie, delCookie} from '../global/cookie'
import bus from '../global/bus'
import qs from 'qs'
import md5 from "js-md5"
import {mapMutations} from 'vuex'
  export default {
    data() {
      var validateUser = (rule, value, callback) => {
        if (value === '') {
          callback(new Error('用户名不能为空'));
        } else {
          callback();
        }
      }
      var validatePass = (rule, value, callback) => {
        if (value === '') {
          callback(new Error('密码不能为空'));
        } else {
          callback();
        }
      }
      var validateVcode = (rule, value, callback) => {
        if (value === '') {
          callback(new Error('验证码不能为空'));
        } else {
          callback();
        }
      }
      return {
        loginForm: {
          user: '',
          passwd: '',
          vcode: '',
          userType: '1',
        },
        rules: {
          user: [{ validator: validateUser, trigger: 'blur' }],
          passwd: [{ validator: validatePass, trigger: 'blur' }],
          vcode: [{validator: validateVcode, trigger: 'blur' },
            { min:5, max:5, message: '请输入5位验证码', trigger: 'blur'}] 
        }
      }
    },
	mounted() {
		this.changeCode()
	},
  methods: {
    ...mapMutations([
      '$_setUserName',
      '$_setUserId',
      '$_setToken'
    ]),
    submitForm(formName) {
      this.$refs[formName].validate(async (valid) => {
          if (valid) {
            try{
              var ret = await this.$axios.post('/public/login/', {
                user: this.loginForm.user,
                passwd: md5(this.loginForm.passwd),
                // passwd: this.loginForm.passwd,
                vcode: this.loginForm.vcode,
                userType: this.loginForm.userType,
              })
              if (ret.data.code === 1) {
                sessionStorage.setItem("authorization",ret.data.datas.token)
                sessionStorage.setItem("userType",1)
                sessionStorage.removeItem("uuid")
                this.$store.commit('$_setUser',{
                              userid:ret.data.datas.userid,
                              username:ret.data.datas.username,
                              userType: 1
                              })
                this.$store.commit('$_setToken',ret.data.datas.token)
                this.$message.success('登录成功')
                // console.error(this.$store.state.user)
                this.$router.push({ path: '/StuTermSchedule' })
                bus.$emit('updateSystemType', 1)
                }else if(ret.data.code === 2){
                  sessionStorage.setItem("authorization",ret.data.datas.token)
                  sessionStorage.setItem("userType",2)
                  sessionStorage.removeItem("uuid")
                  this.$store.commit('$_setUser',{
                                userid:ret.data.datas.userid,
                                username:ret.data.datas.username,
                                userType: 2
                                })
                  this.$store.commit('$_setToken',ret.data.datas.token)
                  this.$message.success('登录成功')
                  bus.$emit('updateSystemType', 2)
                  this.$router.push({ path: '/TeaTermSchedule' }); //跳转到teacher组件中
                }else{
                  this.$message.warning(ret.data.msg)
                  this.changeCode()
                }
            }catch(e){
              //TODO handle the exception
              this.changeCode()
              console.log(e)
            }
          } else {
              alert('用户名和密码不能为空');
              return false;
          }
      })
    },
    async changeCode(){
      try{
        var ret = await this.$axios.get('/public/checkcode/')
        document.getElementById("code_img").src = 'data:image/jpg;base64,' + ret.data.data
        // setCookie('uuid', ret.data.uuid)
        sessionStorage.setItem('uuid', ret.data.uuid)
        this.$message.success('获取验证码成功,60秒内有效')
      }catch(e){
        //TODO handle the exception
        this.$message.warning(e.message)
      }
    },
    toForgot(){
      this.$router.push({
        name:'forgot',
        query:{
          from:'user'
        }
      })
    }
  }
}
</script>
