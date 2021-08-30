<template>
  <div class="changePT" style="height:200">
    <el-form :model="userForm" :rules="rules" ref="userForm" label-width="100px">
      <el-form-item prop="oldTel" label="原手机号：">
          <el-input v-model="userForm.oldTel" maxlength="11" show-word-limit @blur="checkPhone(userForm.oldTel,'old')"> </el-input>
      </el-form-item>
      <el-form-item prop="tel" label="新手机号：">
          <el-input v-model="userForm.tel" maxlength="11" show-word-limit @blur="checkPhone(userForm.tel,'new')"> </el-input>
      </el-form-item>

      <el-form-item>
        <el-input v-model="userForm.vcode" maxlength="6" placeholder="验证码" style="width: 125px" disabled></el-input> 
        <el-button type="primary" round style="margin-left:10px;width:145px" @click="getCode()" :disabled="getCodeBtnDisable">{{codeBtnWord}}</el-button>
      </el-form-item>
    
      <el-form-item>
        <el-button type="primary" @click="changePhone('userForm')" style="width:300px">确认</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import {getCookie} from '../global/cookie'
export default {
  data() {
      var validateTel = (rule, value, callback) => {
          if (value === '') {
              callback(new Error('手机号不能为空'));
          } else {
              callback();
          }
      };
      return {
      userForm: {
          oldTel:'',
          tel:'',
          vcode:''
      },
      rules: {
        oldTel: [{ validator: validateTel, trigger: 'blur'},
          {min:11, max:11, message: '输入11位手机号码', trigger: 'blur'}],
        tel: [{ validator: validateTel, trigger: 'blur'},
          {min:11, max:11, message: '输入11位手机号码', trigger: 'blur'}]
      },
      codeBtnWord:'获取验证码',
      waitTime:61,
    };
  },
  computed:{
    // 用于校验手机号码格式是否正确
    phoneNumberStyle(){
        let reg = /^1[3456789]\d{9}$/
        if(this.userForm.tel.length !== 11 || this.userForm.oldTel.length !== 11){
          return false
        }
        if(!reg.test(this.userForm.oldTel)){
            return false
        }
        if(!reg.test(this.userForm.tel)){
            return false
        }
        return true
    },
    getCodeBtnDisable:{
      get(){
        if(this.waitTime == 61){
          if(this.phoneNumberStyle){
            return false
          }  
        }
        return true
      },
      set(){}
    }
  },
  methods: {
    checkPhone(val,type){
      if(val.length !== 11){
        return false
      }
      let reg = /^1[3456789]\d{9}$/
      if(!reg.test(val)){
        let msg = type == 'new'? '新':'原'
        alert(`“${msg}”手机号码不符合要求`)
        return false
      }
    },
    changePhone(formName){
      if(this.userForm.tel == '' || this.userForm.oldTel == '' || this.userForm.vcode == ''){
        alert('请输入正确的手机号码,获取验证码');
        return false
      }
      let that = this
      this.$confirm('确定修改手机号为'+this.userForm.tel+'吗?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        that.submitForm(formName)
      }).catch(() => {});
    },
    submitForm(formName) {
      this.$refs[formName].validate((valid) => {
          if (valid) {
              this.$axios
              .post('/public/changePhone/', {
                  oldTel:this.userForm.oldTel,
                  telephone:this.userForm.tel,
                  phoneCode:this.userForm.vcode
              })
              .then((result)=> {
              if (result.data.code === 1) {
                  this.$message.success('手机号更换成功');
              }else{
                  this.$message(result.data.msg);
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
    },
    getCode(){
      this.$axios
      .post('/public/getPhoneCode/', { //获取验证码接口
          phoneNumber:this.userForm.tel
      })
      .then((result)=> {
          if (result.data.code === 1) {
              this.$message.success('验证码已发送,10分钟内有效!');
              this.userForm.vcode = result.data.datas.phoneCode
          }else{
              this.$message(result.data.msg);
          }
      })
      .catch((error)=> {
          alert(error)
      })
      let that = this
      that.waitTime--
      this.codeBtnWord = `${that.waitTime}s 后重新获取`
      let timer = setInterval(function(){
          if(that.waitTime>1){
              that.waitTime--
              that.codeBtnWord = `${that.waitTime}s 后重新获取`
          }else{
              clearInterval(timer)
              that.codeBtnWord = '获取验证码'
              that.waitTime = 61
          }
      },1000)
    }
  }
}
</script>