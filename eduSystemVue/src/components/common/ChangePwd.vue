<template>
  <div class="changePT" style="height:250">
    <el-form :model="userForm" :rules="rules" ref="userForm" label-width="100px" status-icon>
    <el-form-item label="原密码：" prop="oldPass">
      <el-input v-model="userForm.oldPass" show-password></el-input>
    </el-form-item>
    
     <el-form-item label="新密码：" prop="pass">
      <el-input type="password" v-model="userForm.pass" show-password></el-input>
    </el-form-item>

    <el-form-item label="确认密码：" prop="checkPass">
      <el-input type="password" v-model="userForm.checkPass" show-password></el-input>
    </el-form-item>
    
    <el-form-item>
      <el-button type="primary" @click="submitForm('userForm')" style="width:300px">确认</el-button>
    </el-form-item>
  </el-form>
  </div>
</template>

<script>
// import {getCookie,delCookie} from '../global/cookie'
import md5 from "js-md5"
  export default {
    data() {
        var validatePass = (rule, value, callback) => {
          if (value.replace(/\s*/g, '') === ''){
            callback(new Error('密码不能为空'))
          } else {
            if(!this.$common.checkStr(value, 'pwd')){
                callback(new Error('密码长度在6~18之间，只能包含字母、数字和下划线'))
            }
            callback()
          } 
        }
        var validateOldPass = (rule, value, callback) => {
          if (value.replace(/\s*/g, '') === ''){
            callback(new Error('请输入新密码'))
          } else {
            if(!this.$common.checkStr(value, 'pwd')){
                callback(new Error('密码长度在6~18之间，只能包含字母、数字和下划线'))
            }
            callback()
          } 
        }
        var validatePass2 = (rule, value, callback) => {
            if (value.replace(/\s*/g, '') === '') {
                callback(new Error('请再次输入密码'));
            } else if (value !== this.userForm.pass) {
                callback(new Error('两次输入密码不一致!'));
            } else {
                callback();
            }
        }
        return {
        userForm: {
            oldPass:'',
            pass:'',
            checkPass:''
        },
        rules: {
            oldPass: [{ required:true, validator: validatePass, trigger: 'blur' }],
            pass: [{ required:true, validator: validateOldPass, trigger: 'blur' }],
            checkPass: [{ required:true, validator: validatePass2, trigger: 'blur' }]
        }
      };
    },
    methods: {
      submitForm(formName) {
        this.$refs[formName].validate((valid) => {
            if (valid) {
                this.$axios
                .post('/public/changePwd/', { //  
                    oldPass:md5(this.userForm.oldPass),
                    newPass:md5(this.userForm.pass),
                    checkPass:md5(this.userForm.checkPass)
                })
                .then((result)=> {
                  console.log(result)
                if (result.data.code === 1) {
                  sessionStorage.removeItem('authorization')
                  sessionStorage.removeItem('userType')
                    this.$message.success('密码已修改,请重新登录')
                    var r = (this.$route.path).substr(0,4)
                    if(r=='/Stu'||r=='/Tea'){
                      this.$router.replace({ path: '/login' })
                    }else{
                      this.$router.replace({ path: '/loginAdmin' })
                    }
                }else{
                    this.$message({
                        type: 'warning',
                        message: result.data.msg
                    });
                    return false;
                }
                })
                .catch((error)=> {
                    alert(error)
                })
            } else {
                alert('请检查输入');
                return false;
            }
        })
      }
    }
  }
</script>