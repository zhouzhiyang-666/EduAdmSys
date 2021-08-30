<template>
  <div style="width:100%">
  <el-row type="flex" justify="space-between" style="margin-bottom:5px">
    <el-col :span="3">
      <!-- <el-select v-model="deptSelected" @change="deptSelect" placeholder="请选择学院" style="width:150px" size="small"> -->
      <el-select v-model="deptSelected" placeholder="请选择学院"  size="small">
        <el-option
          v-for="item in deptOptions"
          :key="item.id" :label="item.name" :value="item.id">
        </el-option>
      </el-select>
    </el-col>
    <el-col :span="2">
        <el-select v-model="gradeSelected" @change="gradeSelect" placeholder="请选择年级" size="small">
            <el-option
            v-for="item in gradeOptions"
            :key="item.grade"
            :label="item.label"
            :value="item.grade">
            </el-option>
        </el-select>
    </el-col>
    <el-col :span="4">
        <el-select v-model="classSearch" placeholder="请选择班级" size="small">
            <el-option
            v-for="item in classOptions"
            :key="item.classId"
            :label="item.classFullName"
            :value="item.classId">
            </el-option>
        </el-select>
    </el-col>
    <el-col :span="5">
      <el-input v-model="search" placeholder="请输入搜索内容"  size="small">
        <el-button slot="append" icon="el-icon-search" @click="searchOk">搜索</el-button>
      </el-input>
    </el-col>
     <el-button type="primary" plain size="small" @click="addStuBtn" icon="el-icon-plus">添加学生</el-button>
     <el-button type="primary" plain size="small" @click="dialogUploadVisible = true" icon="el-icon-upload2">导入学生</el-button>
     <el-button type="primary" plain size="small" @click="exportExcel" :icon="downIcon" :disabled="allowDownBtn">导出学生</el-button>
     <el-tooltip class="item" effect="light" content="选中多项可批量删除" placement="top-end">
         <el-button type="warning" plain size="small" @click="batchDelStu" icon="el-icon-delete">批量删除</el-button>
     </el-tooltip>
  </el-row>

  <div style="background-color:#eff1f2;padding:5px;border-radius: 2px;">
  <el-table id="tableId"
    :data="tables.slice((currentPage-1)*pageSize,currentPage*pageSize)"
    border
    stripe
    style="width: 100%"
    :header-row-style="{height:0+'px'}"
    :header-cell-style="{padding:0+'px'}"
    :row-style="{height:'20px'}"
    :cell-style="{padding:'2px'}"
    @selection-change="handleSelectionChange">
    <!-- <el-table-column type="index" label="序号" width="59">
    </el-table-column> -->
    <el-table-column
          type="selection"
          width="59">
    </el-table-column>
    <el-table-column prop="id" fixed label="学号" width="110">
    </el-table-column>
    <el-table-column prop="name" fixed label="姓名" width="150">
    </el-table-column>
    <el-table-column prop="status" label="状态" width="60">
    </el-table-column>
    <el-table-column prop="sex" label="性别" width="50">
    </el-table-column>
    <el-table-column prop="classAndGrade" label="班级" width="100">
    </el-table-column>
    <el-table-column prop="department" label="学院" width="180">
    </el-table-column>
    <el-table-column prop="idCard" label="身份证号" width="200">
    </el-table-column>
    <el-table-column prop="birth" label="出生日期" width="110">
    </el-table-column>
    <el-table-column prop="political" label="政治面貌" width="120">
    </el-table-column>
    <el-table-column prop="graduate" label="毕业学校" width="200">
    </el-table-column>
    <el-table-column prop="telephone" label="电话号码" width="120">
    </el-table-column>
    <el-table-column fixed="right" prop="operate" label="操作" width="150">
      <template slot-scope="scope">
          <el-button size="mini" plain type="primary"
            @click="handleEdit(scope.$index, scope.row)">编辑</el-button>
          <el-button size="mini" plain type="danger"
            @click="handleDelete(scope.$index, scope.row)">删除</el-button>
        </template>
    </el-table-column>
  </el-table>
  </div>
  <el-pagination
  background
  layout="total, sizes, prev, pager, next, jumper"
  :page-size="pageSize"
  :page-sizes="pageSizes"
  :total="totalCount"
  :current-page="currentPage"
  @size-change="handleSizeChange"
  @current-change="handleCurrentChange"
  style="text-align:center">
  </el-pagination>

    <!-- 编辑模态层 -->
   <el-dialog :title="dialogTitle" :visible.sync="dialogFormVisible" :close-on-click-modal=false width="50%">
  <el-form :model="form" :rules="rules" ref="stuForm" status-icon>
    <el-form-item>
      <el-col :span="10">
        <el-form-item label="学号" :label-width="formLabelWidth" prop="id">
          <el-input v-model="form.id" autocomplete="off" 
                          :disabled="isDisabled" 
                          maxlength="10" 
                          @blur="form.id=form.id.replace(/\s*/g, '')"
                          show-word-limit></el-input>
        </el-form-item>
      </el-col>
      <el-col :span="14">
        <el-form-item label="姓名" :label-width="formLabelWidth" prop="name">
          <el-input v-model="form.name" autocomplete="off" maxlength="20" @blur="form.name=form.name.replace(/\s*/g, '')"></el-input>
        </el-form-item>
      </el-col>
    </el-form-item>
    <el-form-item>
      <el-col :span="10">
        <el-form-item label="性别" :label-width="formLabelWidth" prop="sex">
          <el-select v-model="form.sex" placeholder="请选择">
            <el-option label="男" value="男"></el-option>
            <el-option label="女" value="女"></el-option>
          </el-select>
        </el-form-item>
      </el-col>
      <el-col :span="14">
        <el-form-item label="毕业院校" :label-width="formLabelWidth" >
          <el-input v-model="form.graduate" autocomplete="off" @blur="form.graduate=form.graduate.replace(/\s*/g, '')"></el-input>
        </el-form-item>
      </el-col>
    </el-form-item>
    <el-form-item>
      <el-col :span="10">
        <el-form-item label="出生日期" :label-width="formLabelWidth" >
          <el-date-picker style="width: 100%;" v-model="form.birth" type="date" placeholder="选择日期" value-format="yyyy-MM-dd">
          </el-date-picker>
        </el-form-item>
      </el-col>
      <el-col :span="14">
        <el-form-item label="身份证号" :label-width="formLabelWidth" prop="idCard">
          <el-input v-model="form.idCard" autocomplete="off" @blur="form.idCard=form.idCard.replace(/\s*/g, '')"></el-input>
        </el-form-item>
      </el-col>
    </el-form-item>
    <el-form-item>
      <el-col :span="10">
        <el-form-item label="政治面貌" :label-width="formLabelWidth" prop="political">
          <el-select v-model="form.political" placeholder="请选择">
            <el-option value="群众"></el-option>
            <el-option value="共青团员"></el-option>
            <el-option value="入党积极分子"></el-option>
            <el-option value="共产党员"></el-option>
            <el-option value="其他党派"></el-option>
          </el-select>
        </el-form-item>
      </el-col>
      <el-col :span="14">
        <el-form-item label="电话号码" :label-width="formLabelWidth" prop="telephone">
          <el-input v-model="form.telephone" autocomplete="off" maxlength="11" show-word-limit></el-input>
        </el-form-item>
      </el-col>
    </el-form-item>
    <el-form-item>
      <el-col :span="8">
        <el-form-item label="学院" :label-width="formLabelWidth" prop="dptNo">
          <el-select v-model="form.dptNo" @change="deptChange" placeholder="请选择">
          <el-option
            v-for="item in deptOptions2" :key="item.id" :label="item.name" :value="item.id">
          </el-option>
          </el-select>
        </el-form-item>
      </el-col>
      <el-col :span="8">
        <el-form-item label="班级" :label-width="formLabelWidth" prop="classAndGrade">
          <el-select v-model="form.classAndGrade" placeholder="请选择">
          <el-option
              v-for="item in editClassOptions" :key="item.classId" :label="item.classFullName" :value="item.classId">
              </el-option>
          </el-select>
        </el-form-item>
      </el-col>
      <el-col :span="8">
        <el-form-item label="状态" :label-width="formLabelWidth" prop="status">
          <el-select v-model="form.status" placeholder="请选择">
            <el-option value="毕业"></el-option>
            <el-option value="在校"></el-option>
            <el-option value="休学"></el-option>
            <el-option value="退学"></el-option>
          </el-select>
        </el-form-item>
      </el-col>
    </el-form-item>
    <el-form-item>
      <el-col :span="10">
        <el-form-item label="密码" :label-width="formLabelWidth" prop="pwd">
          <el-input type="password" v-model="form.pwd" autocomplete="off" :disabled="!isDisabled" placeholder="为空则不修改密码" show-password></el-input>
        </el-form-item>
      </el-col>
    </el-form-item>
  </el-form>
  <div slot="footer" class="dialog-footer">
    <el-button @click="handleCancel('stuForm')">取 消</el-button>
    <el-button type="primary" @click="addStudentData('stuForm')" :style="{display: this.visible1}">提交</el-button>
    <el-button type="primary" @click="editOk('stuForm')" :style="{display: this.visible2}">修改</el-button>
  </div>
</el-dialog>

<el-dialog title="上传文件" :visible.sync="dialogUploadVisible" :close-on-click-modal="false">
  <el-upload
  class="upload-demo"
  ref="upload"
  :multiple="false"
  accept=".xls,.xlsx"
  action="http://127.0.0.1:9090/admin/uploadStuFiles/"
  :with-credentials="true" 
  :on-success="handleAvatarSuccess"
  :headers="headers"
  :file-list="fileList"
  :on-change="changeMe"
  :auto-upload="false">
  <el-button slot="trigger" size="small" type="primary">选取文件</el-button>
  <el-button style="margin-left: 10px;" size="small" type="success" @click="submitUpload">上传到服务器</el-button>
  <div slot="tip" class="el-upload__tip">上传表格文件</div>
</el-upload>
</el-dialog>


  </div>
</template>

<script>
import {getCookie} from '../global/cookie'
import FileSaver from 'file-saver'
import XLSX from 'xlsx'
import md5 from "js-md5"
  export default {
    data() {
      var validateStuNo = (rule, value, callback) => {
          if(!this.$common.checkStr(value,'stuNo')){
              callback(new Error('11位学生编号，可带英文字母'))
          }
          callback()
      }
      var validateName = (rule, value, callback) => {
          if(value.replace(/\s*/g, '') === ''){
              callback(new Error('请输入姓名'))
          }
          callback()
      }
      var validateTel = (rule, value, callback) => {
        let reg = /^1[3456789]\d{9}$/
        if (value === '') {
          callback(new Error('手机号不能为空'))
        } else if (value.length !== 11) {
          callback(new Error('手机号必须为11位'))
        } else {
          if(!reg.test(value)){
              callback(new Error('请输入正确的手机号'))
          }
          callback()
        }
      }
      var validatePwd = (rule, value, callback) => {
        if (value === ''){
          callback()
        } else {
          if(!this.$common.checkStr(value, 'pwd')){
              callback(new Error('密码长度在6~18之间，只能包含字母、数字和下划线'))
          }
          callback()
        } 
      }
      var validateidCard = (rule, value, callback) => {
        if (value === '') {
          callback(new Error('身份证号码不能为空'))
        }
        // 加权因子
        var weight_factor = [7,9,10,5,8,4,2,1,6,3,7,9,10,5,8,4,2];
        // 校验码
        var check_code = ['1', '0', 'X' , '9', '8', '7', '6', '5', '4', '3', '2'];
        var code = value + "";
        var last = value[17];//最后一位
        var seventeen = code.substring(0,17);
        // ISO 7064:1983.MOD 11-2
        // 判断最后一位校验码是否正确
        var arr = seventeen.split("");
        var len = arr.length;
        var num = 0;
        for(var i = 0; i < len; i++){
            num = num + arr[i] * weight_factor[i];
        }
        // 获取余数
        var resisue = num%11;
        var last_no = check_code[resisue];
        // 格式的正则
        // 正则思路
        /*
        第一位不可能是0
        第二位到第六位可以是0-9
        第七位到第十位是年份，所以七八位为19或者20
        十一位和十二位是月份，这两位是01-12之间的数值
        十三位和十四位是日期，是从01-31之间的数值
        十五，十六，十七都是数字0-9
        十八位可能是数字0-9，也可能是X
        */
        var idcard_patter = /^[1-9][0-9]{5}([1][9][0-9]{2}|[2][0][0|1][0-9])([0][1-9]|[1][0|1|2])([0][1-9]|[1|2][0-9]|[3][0|1])[0-9]{3}([0-9]|[X])$/;
        // 判断格式是否正确
        var format = idcard_patter.test(value);
        // 返回验证结果，校验码和格式同时正确才算是合法的身份证号码
        last === last_no && format ? callback() : callback(new Error('请输入正确的身份证号码'));
      }
      return {
        deptOptions:[],
        deptOptions2:[],
        deptSelected: '',
        gradeSelected:'',
        classSearch: '',
        editClassOptions: [],
        classOptions:[],
        search: '',
        loading: false,
        dialogTitle: '新增学生档案',
        allowDownBtn: false, // 下载按钮控制防抖
        downIcon: 'el-icon-download',

        tableData:[],  //目前前端所拥有的所有信息
        multipleSelection: [],

        pageSize:10,
        pageSizes:[10,20,40,60],
        currentPage:1,
        // totalCount:0,

        dialogFormVisible: false,
        form: {
          id:'',
          name: '',
          sex:'',
          graduate:'',
          birth:'',
          idCard: '',
          political:'',
          telephone:'',
          department:'',
          dptNo:'',
          classAndGrade:'',
          status:'',
          pwd:'',
        },
        formLabelWidth: '80px',
        visible2:'none',
        visible1:'inline',
        isDisabled:false,
        editIndex:0,

        dialogUploadVisible: false,
        fileList:[],
        rules: {
          id: [{ required: true, message: '请输入学号', trigger: 'blur' },
               { validator: validateStuNo, trigger: 'input' }
          ],
          name: [{ required: true, message: '请输入姓名', trigger: 'blur' },
                 { validator: validateName, trigger: 'input' }
          ],
          sex: [{ required: true, message: '请选择性别', trigger: 'change' }],
          political: [{ required: true, message: '请选择政治面貌', trigger: 'change' }],
          department: [{ required: true, message: '请选择学院', trigger: 'change' }],
          dptNo: [{ required: true, message: '请选择学院', trigger: 'change' }],
          classAndGrade: [{ required: true, message: '请选择班级', trigger: 'change' }],
          status: [{ required: true, message: '请选择状态', trigger: 'change' }],
          telephone: [{ required: true, validator: validateTel, trigger: 'blur' }],
          idCard: [{ required: true, validator: validateidCard, trigger: 'blur' }],   // 身份证严格校验模式
          // idCard: [{ required: true, message: '请输入身份证号', trigger: 'blur' }],
          pwd: [{ validator: validatePwd, trigger: 'blur' }]
        }
      }
    },
    computed:{
      gradeOptions(){
          let myData = new Date()
          var year1 = myData.getFullYear()
          let month1 = myData.getMonth()
          var options = []
          if(month1<8){
              year1--
          }
          for(var i=0;i<6;i++){
              options[i] = {
                  grade:year1,
                  label:year1+'级'
              }
              year1--
          }
          options.unshift({grade:'0',label:'全部年级'})
          return options
      },
      gradeOptions2(){
          let myData = new Date()
          var year1 = myData.getFullYear()
          let month1 = myData.getMonth()
          var options = []
          if(month1<8){
              year1--
          }
          for(var i=0;i<6;i++){
              options[i] = {
                  grade:year1,
                  label:year1+'级'
              }
              year1--
          }
          return options
      },
      tables () {
        const search = this.search
        if (search) {
          return this.tableData.filter(data => {
            return Object.keys(data).some(key => {
              return String(data[key]).toLowerCase().indexOf(search) > -1
            })
          })
        }
        return this.tableData
      },
      headers(){
        return {
          authorization: this.$store.getters.getToken,
          userid: this.$store.getters.getUser.userid
        }
      },
      totalCount(){
        if (!this.tables.length) {
          return 0
        }
        return this.tables.length
      }
    },
    methods:{
      getTableData(params){
        if(this.deptSelected == ""||this.gradeSelected == "" ||this.classSearch == ""){
          alert('请选择班级')
          return
        }
        if (params) {
          params =  Object.assign(params,{page:this.currentPage,size:this.pageSize})
        } else {
          params = {
            dpt:this.deptSelected,
            grade:this.gradeSelected,
            classId:this.classSearch,
            page:this.currentPage,
            size:this.pageSize
          }
        }
        this.$axios
        .post('/admin/getStuData/', params)
        .then((result)=> {
            if (result.data.code === 1) {//返回第一页数据，和
              this.tableData = result.data.datas
            }else{
              alert(result.data.msg)
              return false;
            }
        })
        .catch((error)=> {
            alert(error)
        })
      },
      
      getAllClass(type, params={}){
        this.$axios
        .post('/admin/getAllClass/', params)
        .then((result)=> {
            if (result.data.code === 1) {   
              if (type === 'search') {
                this.classOptions = result.data.datas
                this.classOptions.unshift({classId:'0',classFullName:'所有班级'})
              } else if (type === 'edit_1') {
                this.editClassOptions = result.data.datas
              } else if (type === 'edit_2') {
                this.editClassOptions = result.data.datas
                this.form.classAndGrade = ''
              } else {
                this.classOptions = []
                this.editClassOptions = []
              }
              
            }else{
              if (type === 'search') {this.classOptions = []}
              else if (type === 'edit') {this.editClassOptions = []}
              
              this.$message({
                showClose:true,
                type: 'error',
                message: result.data.msg
              });
            }
        })
        .catch((error)=> {
            alert(error)
        })
      },
      
      submitUpload() {
        this.$refs.upload.submit();
      },
      changeMe(file,fileList){
        this.fileList=fileList;
      },
      handleAvatarSuccess(response, file, fileList){
        console.log(response)
        if (response.code === 1) {
          let success = response.datas.success
          let total = response.datas.totalNum
          let failed = response.datas.failed
          alert("导入成功，共添加"+total+"条，成功"+success+"条，失败"+failed+"条"+'----'+
          '导入失败的学生档案：'+ response.datas.errorList.join('、'))
          if (this.classSearch === '') {
            this.getTableData({
              dpt:this.deptSelected,
              grade:this.gradeSelected
            })
          } else {
            this.getTableData({
              dpt:this.deptSelected,
              grade:this.gradeSelected,
              classId:this.classSearch
            })
          }
          
        } else {
          alert(response.msg)
        }
      },

      getDptName(){
        this.$axios
        .post('/admin/getDptName/', {})
        .then((result)=> {
            if (result.data.code === 1) {  // 返回第一页数据，和
              this.deptOptions = result.data.datas
              this.deptOptions2 = JSON.parse(JSON.stringify(this.deptOptions))
              // console.log(this.deptOptions2)
              this.deptOptions.unshift({id:'0',name:'全部学院'})
              // console.log(this.deptOptions2)
              this.deptSelected = result.data.datas[0].id
            }else{
              return false;
            }
        })
        .catch((error)=> {
            alert(error)
        })
      },

      gradeSelect(){
        if(this.deptSelected == ""){
          return
        }
        this.classSearch = ''
        this.getAllClass('search',{dpt:this.deptSelected,grade:this.gradeSelected})
      },

      addStuBtn(){
        this.dialogTitle = '新增学生档案'
        this.form.pwd = ""
        this.form.id = ""
        this.form.name = ""
        this.form.sex = ""
        this.form.graduate = ""
        this.form.birth = ""
        this.form.idCard = ""
        this.form.political = ""
        this.form.telephone = ""
        this.form.department = ""
        this.form.dptNo = ""
        this.form.classAndGrade = ""
        this.form.status = ""
        this.dialogFormVisible = true 
        this.visible2 = 'none'
        this.visible1 = 'inline'
        this.isDisabled=false
      },

      addStudentData(formName){
        // console.log(this.form)
        this.$refs[formName].validate((valid) => {
          if (valid) {
            this.$axios
            .post('/admin/addStu/', this.form)
            .then((result)=> {
                if (result.data.code === 1) {//返回第一页数据，和
                  this.$message({
                    type: 'success',
                    message: '添加成功!'
                  });
                  this.dialogFormVisible = false
                  this.getTableData()
                }else{
                  this.$message({
                    showClose:true,
                    type: 'error',
                    message: result.data.msg
                  });
                  // this.dialogFormVisible = false
                }
                
            })
            .catch((error)=> {
                alert(error)
            })
          } else {
            alert('请按要求填充数据')
            return false;
          }
        });
      },
      
      handleCancel(formName){
        this.resetForm(formName)
        this.dialogFormVisible = false
      },
      resetForm(formName) {
        this.$refs[formName].resetFields();
      },
      
      handleEdit(index,row){
          this.getAllClass('edit_1',{dpt:this.deptSelected})
          this.form.pwd = ''
          this.dialogTitle = '编辑学生档案'
          this.form.id = row.id
          this.form.name = row.name
          this.form.sex = row.sex
          this.form.graduate = row.graduate
          this.form.birth = row.birth
          this.form.idCard = row.idCard
          this.form.political = row.political
          this.form.telephone = row.telephone
          this.form.department = this.deptSelected
          this.form.dptNo = row.dptNo
          this.form.classAndGrade = row.classId
          this.form.classId = row.classId
          this.form.status = row.status
          this.visible1 = 'none'
          this.visible2 = 'inline'
          this.isDisabled=true
          this.dialogFormVisible = true
      },
      editOk(formName){
        this.$refs[formName].validate((valid) => {
          if (valid) {
            this.$axios
            .post('/admin/editStu/', {
              id : this.form.id,
              name :this.form.name,
              sex :this.form.sex,
              graduate:this.form.graduate,
              birth:this.form.birth,
              idCard:this.form.idCard,
              political:this.form.political,
              telephone:this.form.telephone,
              department:this.form.department,
              dptNo:this.form.dptNo,
              classAndGrade:this.form.classAndGrade,
              classId:this.form.classId,
              status:this.form.status,
              pwd : this.form.pwd===''?'':md5(this.form.pwd)
            })
            .then((result)=> {
                if (result.data.code === 1) {//返回第一页数据，和
                  this.$message({
                    type: 'success',
                    message: '修改成功!'
                  });
                  this.getTableData()
                }else{
                  this.$message({
                    type: 'error',
                    message: result.data.msg
                  });
                }
                this.dialogFormVisible = false
                this.form.pwd = ''
            })
            .catch((error)=> {
                this.form.pwd = ''
                alert(error)
            })
          } else {
            alert('请按要求填充数据')
            return false;
          }
        })
      },

      handleDelete(index,row){
        this.$confirm('确定删除'+row.name+'吗?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          this.$axios
          .post('/admin/delStu/', {
            id:row.id
          })
          .then((result)=> {
            if (result.data.code === 1) {
              this.getTableData()
              this.$message({
                type: 'success',
                message: '删除成功!'
              });
            }else{
              this.$message({
                type: 'error',
                message: result.data.msg
              });
            }
          }).catch((error)=> {
            alert(error)
          })
        }).catch(() => {});
      },
      

      handleCurrentChange(val) {
        this.currentPage = val
        // this.getTableData()
      },
      handleSizeChange(val) {
        this.pageSize = val
        // this.getTableData()
      },
      deptChange(){
        let dept = this.form.dptNo
        this.form.classAndGrade = ''
        this.getAllClass('edit_2',{dpt:dept})
      },
      searchOk(){
        this.currentPage = 1
        this.getTableData({
          dpt:this.deptSelected,
          grade:this.gradeSelected,
          classId:this.classSearch
        })
      },
      // 批量删除
      handleSelectionChange(val) {
        this.multipleSelection = val;
      },
      batchDelStu(){
        // console.log(this.multipleSelection)
        if (!this.multipleSelection || this.multipleSelection.length === 0){
          this.$message.warning('请选择要批量删除的学生档案数据')
          return false
        } else {
          let stuIds = []
          let stuInfoList = []
          for (let item of this.multipleSelection){
            stuIds.push(item.id)
            stuInfoList.push(item.classAndGrade + '-' + item.id + '-' + item.name)
          }
          this.$confirm('确定删除  '+stuInfoList.join('、')+'  吗?', '提示', {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }).then(() => {
            // console.log(stuIds)
            this.$axios
            .post('/admin/batchDelStu/', {
              ids:stuIds
            })
            .then((result)=> {
              if (result.data.code === 1) {
                this.getTableData()
                this.$message({
                  type: 'success',
                  message: '删除成功!'
                });
              }else{
                this.$message({
                  type: 'error',
                  message: result.data.msg
                });
              }
            }).catch((error)=> {
              alert(error)
            })
          }).catch(() => {});
        }
      },
      exportExcel(){
        if (!this.tables || this.tables.length === 0){
          this.$message.warning('请筛选您需要导出的学生数据')
          return false
        }
        this.downIcon = 'el-icon-loading'
        this.allowDownBtn = true
        try{
          require.ensure([], () => {
            const { export_json_to_excel } = require('../../excel/Export2Excel')
            const tHeader = [ '学号', '姓名', '性别', '班级', '学院', '身份证号', '出生日期', '政治面貌', '毕业学校', '电话号码']
            const filterVal = ['id', 'name', 'sex', 'classAndGrade', 'department', 'idCard', 'birth', 'political', 'graduate', 'telephone']
            const list = this.tables
            const data = this.formatJson(filterVal, list)
            const filename = this.classSearch? this.deptSelected +'-'+ this.gradeSelected +'-'+ this.classSearch:this.deptSelected +'-'+ this.gradeSelected
            export_json_to_excel(tHeader, data, filename)
          })
          setTimeout(() => {
            this.downIcon = 'el-icon-download'
            this.allowDownBtn = false
          },5000)
        }catch(e){
          setTimeout(() => {
            this.downIcon = 'el-icon-download'
            this.allowDownBtn = false
          },5000)
          //TODO handle the exception
        }
      },
      formatJson(filterVal, jsonData){
        return jsonData.map(v => filterVal.map(j => v[j]))
      }
    },
    watch: {
      deptSelected: function () {
        this.$nextTick(function () {
          this.getAllClass('search',{dpt:this.deptSelected,grade:this.gradeSelected})
          this.classSearch = ''
        })
      }
    },
    mounted() {
      this.gradeSelected = this.gradeOptions[0].grade
      this.getDptName()
    }
  }
</script>