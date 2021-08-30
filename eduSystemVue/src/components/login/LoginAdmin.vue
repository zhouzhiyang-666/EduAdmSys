<template>
<div id="loginAdmin" class="login_div">
  <span class="login_span">管理员</span>
  <el-divider></el-divider>
  <el-form :model="userForm" :rules="rules" ref="userForm">
  <el-form-item prop="user">
      <el-input v-model="userForm.user" placeholder="用户名" 
                @keyup.enter.native="submitForm('userForm')"
                @blur="userForm.user=userForm.user.replace(/\s*/g, '')"></el-input>
  </el-form-item>
  
  <el-form-item prop="passwd">
    <el-input v-model="userForm.passwd" placeholder="密码" show-password 
                @keyup.enter.native="submitForm('userForm')"
                @blur="userForm.passwd=userForm.passwd.replace(/\s*/g, '')"></el-input>
  </el-form-item>
  
  <el-form-item prop="vcode">
    <el-col :span="12">
      <el-input v-model="userForm.vcode" maxlength="5" 
                @keyup.enter.native="submitForm('userForm')" 
                placeholder="验证码" style="width: 130px"
                @blur="userForm.vcode=userForm.vcode.replace(/\s*/g, '')"
                ></el-input> 
    </el-col>
    <el-col :span="12">
      <img id="code_img" src="" @click="changeCode()" style="height:40px; width: 100px; margin-left:25px; cursor: pointer;" title="点击更换" >
    </el-col>
  </el-form-item>
  
  <el-form-item>
    <el-button type="primary" @click="submitForm('userForm')" style="width: 250px">登录</el-button>
  </el-form-item>
  
  <el-link type="primary" style="cursor: pointer;" @click="toForgot">忘记密码?</el-link>
  
</el-form>
  
</div>
</template>

<script>
import {setCookie, getCookie, delCookie} from '../global/cookie.js'
import bus from '../global/bus'
import md5 from "js-md5"   //加密登录密码
import {mapGetters,mapMutations} from 'vuex'

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
        userForm: {
          user: '',
          passwd: '',
          vcode: ''
        },
        rules: {
          user: [
            { validator: validateUser, trigger: 'blur' }
          ],
          passwd: [
            { validator: validatePass, trigger: 'blur' }
          ],
          vcode: [{validator: validateVcode, trigger: 'blur' },
            { min:5, max:5, message: '请输入5位验证码', trigger: 'blur'},
          ] 
        }
      };
    },
	mounted() {
	},
  created() {
    this.changeCode()
  },
    methods: {
      ...mapMutations([
        '$_setUserId',
        '$_setUserName',
        '$_setToken',
        '$_setPerm'
      ]),
      submitForm(formName) {
        this.$refs[formName].validate(async (valid) => {
          if (valid) {
						try{
							var ret = await this.$axios.post('/admin/login/', {
								user: this.userForm.user,
								passwd: md5(this.userForm.passwd),
								vcode: this.userForm.vcode
							})
              // console.log(ret)
							if (ret.data.code === 1) {
								this.$message.success('登录成功!');
                sessionStorage.setItem("authorization",ret.data.datas.token)
                sessionStorage.setItem("userType",3)
                sessionStorage.removeItem("uuid")
                this.$store.commit('$_setUser',{
                              userid:ret.data.datas.userid,
                              username:ret.data.datas.username,
                              userType: 3
                              })
                this.$store.commit('$_setToken',ret.data.datas.token)
                if( ret.data.datas.perm ){
                  this.$store.commit('$_setPerm',ret.data.datas.perm)
                }
								// console.error(this.$store.state.user)
                bus.$emit('updateSystemType', 3)
								this.$router.push({ path: '/AdmStuFiles' })
								}else{
                  this.changeCode()
                  this.$message.warning(ret.data.msg)
							}
						}catch(e){
							//TODO handle the exception
							// alert(e.message)
              this.changeCode()
							this.$message.warning(e.message)
						}
          } else {
            return false;
          }
        })
      },
      async changeCode(){
				try{
					var ret = await this.$axios.get('/public/checkcode/')
					document.getElementById("code_img").src = 'data:image/jpg;base64,' + ret.data.data
					// setCookie('uuid', ret.data.uuid)
          sessionStorage.setItem("uuid",ret.data.uuid)
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
            from:'admin'
          }
        })
      }

    }
  }
</script>