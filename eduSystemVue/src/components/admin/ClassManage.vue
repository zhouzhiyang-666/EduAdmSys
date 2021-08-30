<template>
  <div style="width:100%">
  <el-row type="flex" justify="space-between" style="margin-bottom:5px">
    <el-col :span="3">
      <el-select v-model="deptSelected" @change="deptSelect" placeholder="请选择学院" size="small">
        <el-option
          v-for="item in deptOptions"
          :key="item.id" :label="item.name" :value="item.id">
        </el-option>
      </el-select>
    </el-col>
    <el-col :span="3">
        <el-select v-model="gradeSelected" @change="gradeSelect" placeholder="请选择年级" size="small">
            <el-option
            v-for="item in gradeOptions"
            :key="item.grade"
            :label="item.label"
            :value="item.grade">
            </el-option>
        </el-select>
    </el-col>
    <el-col :span="9">
      <el-input v-model="search" placeholder="请输入搜索内容"  size="small">
        <el-button slot="append" icon="el-icon-search" @click="searchOk">搜索</el-button>
      </el-input>
    </el-col>
    <el-button type="primary" plain size="small" @click="addStuBtn" icon="el-icon-plus">添加班级</el-button>
    <el-button type="primary" plain size="small" @click="dialogUploadVisible = true" icon="el-icon-folder-add">导入班级</el-button>
    <el-tooltip class="item" effect="light" content="选中多项可批量删除" placement="top-end">
        <el-button type="warning" plain size="small" @click="batchDelClass" icon="el-icon-delete">批量删除</el-button>
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
    <!-- <el-table-column type="index" label="序号" width="59"></el-table-column> -->
    <el-table-column
          type="selection"
          width="59">
    </el-table-column>
    <el-table-column prop="classId" fixed label="班级编号" width="110">
    </el-table-column>
    <el-table-column prop="classFullName" label="班级全名" width="220">
    </el-table-column>
    <el-table-column prop="classGrade" label="年级" width="70">
    </el-table-column>
    <el-table-column prop="dptNo" label="学院编号" width="100">
    </el-table-column>
    <el-table-column prop="className" label="班级名称" width="180">
    </el-table-column>
    <el-table-column prop="dptName" label="学院名称" width="200">
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
  <el-form :model="form" :rules="rules" ref="classForm" status-icon>
    <el-form-item>
      <el-col :span="10">
        <el-form-item label="班级编号" :label-width="formLabelWidth" prop="classId">
          <el-input v-model="form.classId" autocomplete="off" :disabled="isDisabled" 
          :maxlength="classLength" show-word-limit :placeholder="classTip">
          </el-input>
        </el-form-item>
      </el-col>
      <el-col :span="14">
        <el-form-item label="班级名称" :label-width="formLabelWidth" prop="className">
          <el-input v-model="form.className" autocomplete="off" placeholder="请输入班级名称,如文学1班"></el-input>
        </el-form-item>
      </el-col>
    </el-form-item>
    <el-form-item>
      <el-col :span="10">
        <el-form-item label="年级" :label-width="formLabelWidth" prop="classGrade">
          <el-select v-model="form.classGrade" placeholder="请选择">
            <el-option v-for="item in gradeOptions2" :key="item.grade" :label="item.grade" :value="item.grade"></el-option>
          </el-select>
        </el-form-item>
      </el-col>
      <el-col :span="14">
        <el-form-item label="学院" :label-width="formLabelWidth" prop="dptNo">
          <el-select v-model="form.dptNo" placeholder="请选择">
            <el-option v-for="item in deptOptions2" :key="item.id" :label="item.name" :value="item.id"></el-option>
          </el-select>
        </el-form-item>
      </el-col>
    </el-form-item>
  </el-form>
  <div slot="footer" class="dialog-footer">
    <el-button @click="handleCancel('classForm')">取 消</el-button>
    <el-button type="primary" @click="addStudentData('classForm')" :style="{display: this.visible1}">提交</el-button>
    <el-button type="primary" @click="editOk('classForm')" :style="{display: this.visible2}">修改</el-button>
  </div>
</el-dialog>

<el-dialog title="上传文件" :visible.sync="dialogUploadVisible" :close-on-click-modal="false">
  <el-upload
  class="upload-demo"
  ref="upload"
  :multiple="false"
  accept=".xls,.xlsx"
  action="http://127.0.0.1:9090/admin/uploadClass/"
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
// import { mapGetters } from 'vuex'
  export default {
    data() {
      var validateClass = (rule, value, callback) => {
          if(!this.$common.checkStr(value,'classNo')){
              callback(new Error('班级编号，可带英文字母'))
          }
          callback()
      }
      var validateName = (rule, value, callback) => {
          if(value.replace(/\s*/g, '') === ''){
              callback(new Error('请输入班级名称'))
          }
          callback()
      }
      return {
        deptOptions:[],
        deptOptions2:[],
        deptSelected: '',
        gradeSelected:'',
        classOptions:'',
        search: '',
        loading: false,
        classLength:8, //编号
        classTip:'',
        dialogTitle: '新增班级信息',

        tableData:[],  //目前前端所拥有的所有信息
        multipleSelection: [],

        pageSize:10,
        pageSizes:[10,20,40,60],
        currentPage:1,
        // totalCount:0,

        dialogFormVisible: false,
        form: {
          classId:'',
          className: '',
          dptName:'',
          dptNo:'',
          classGrade:''
        },
        formLabelWidth: '80px',
        visible2:'none',
        visible1:'inline',
        isDisabled:false,
        editIndex:0,

        dialogUploadVisible: false,
        fileList:[],
        addRules: {
          classId: [{ required: true, message: '请输入班级编号', trigger: 'blur' },
                    { min: 2, max:2, message: '请输入正确的班级编号,如01,02...', trigger: 'blur' },
                    { validator: validateClass, trigger: 'input' }
          ],
          className: [{ required: true, message: '请输入班级名称', trigger: 'blur' },
                      { validator: validateName, trigger: 'input' }
          ],
          classGrade: [{ required: true, message: '请选择所属年级', trigger: 'change' }],
          dptNo: [{ required: true, message: '请选择所属学院', trigger: 'change' }]
        },
        editRules: {
          className: [{ required: true, message: '请输入班级名称', trigger: 'blur' },
                      { validator: validateName, trigger: 'input' }
          ],
          classGrade: [{ required: true, message: '请选择所属年级', trigger: 'change' }],
          dptNo: [{ required: true, message: '请选择所属学院', trigger: 'change' }]
        },
        rules:[]
      }
    },
    computed:{
      // ...mapGetters({
      //   // 把 `this.getDeptOptions` 映射为 `this.$store.getters.getDeptOptions`
      //   getDeptOptions: 'getDeptOptions'
      // }),
      // deptOptions(){
      //   return this.getDeptOptions
      // },
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
      totalCount(){
        if (!this.tables.length) {
          return 0
        }
        return this.tables.length
      },
      headers(){
        return {
          authorization: this.$store.getters.getToken,
          userid: this.$store.getters.getUser.userid
        }
      }
    },
    methods:{
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
          '录入失败的班级信息：'+ response.datas.errorList.join('、'))
          this.getTableData()
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

      deptSelect(){
        // if(this.gradeSelected == ""){
        //   return
        // }
        // this.getTableData()
      },
      gradeSelect(){
        // if(this.deptSelected == ""){
        //   return
        // }
        // this.getTableData()
      },
      getTableData(){
        if(this.deptSelected == ""||this.gradeSelected == ""){
          return
        }
        this.$axios
        .post('/admin/getAllClass/', { 
          dpt:this.deptSelected,
          grade:this.gradeSelected,
        })
        .then((result)=> {
            if (result.data.code === 1) {//返回第一页数据，和
              this.tableData = result.data.datas
              this.currentPage = 1
            }else{
              this.tableData = []
              alert(result.data.msg)
              return false;
            }
        })
        .catch((error)=> {
            alert(error)
        })
      },
      getAllClass(params={}){
        this.$axios
        .post('/admin/getAllClass/', params)
        .then((result)=> {
            if (result.data.code === 1) {   //返回第一页数据，和
              this.classOptions = result.data.datas
            }else{
              this.classOptions = []
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

      addStuBtn(){
        this.rules = this.addRules
        this.dialogTitle = '新增班级信息'
        this.classLength = 2
        this.classTip = '请输入两位班级编号'
        this.showTip = true
        
        this.form.classId = ""
        this.form.className = ""
        this.form.dptNo = ""
        this.form.classGrade = ""
        this.form.dptName = ""
        this.dialogFormVisible = true 
        this.visible2 = 'none'
        this.visible1 = 'inline'
        this.isDisabled=false
      },

      addStudentData(formName){
        this.$refs[formName].validate((valid) => {
          if (valid) {
            this.$axios
            .post('/admin/addClass/', this.form)
            .then((result)=> {
                if (result.data.code === 1) {//返回第一页数据，和
                  this.$message({
                    type: 'success',
                    message: '修改成功!'
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
        })
      },
      handleCancel(formName){
        this.resetForm(formName)
        this.dialogFormVisible = false
      },
      resetForm(formName) {
        this.$refs[formName].resetFields();
      },

      handleEdit(index,row){
        this.rules = this.editRules
        this.dialogTitle = '编辑班级信息'
        this.classLength = 8
        this.classTip = ''
        
        this.form.classId = row.classId
        this.form.className = row.className
        this.form.dptNo = row.dptNo
        this.form.classGrade = row.classGrade
        this.form.dptName = row.dptName
        this.visible1 = 'none'
        this.visible2 = 'inline'
        this.isDisabled=true
        this.dialogFormVisible = true
      },
      editOk(formName){
        this.$refs[formName].validate((valid) => {
          if (valid) {
            this.$axios
            .post('/admin/editClass/', this.form)
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
            })
            .catch((error)=> {
                alert(error)
            })
          } else {
            alert('请按要求填充数据')
            return false;
          }
        })
      },

      handleDelete(index,row){
        this.$confirm('确定删除-'+row.classGrade+'级'+row.className+'-吗?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          this.$axios
          .post('/admin/delClass/', {
            classId:row.classId
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
      // 批量删除
      handleSelectionChange(val) {
        this.multipleSelection = val;
      },
      batchDelClass(){
        // console.log(this.multipleSelection)
        if (!this.multipleSelection || this.multipleSelection.length === 0){
          this.$message.warning('请选择要批量删除的班级数据')
          return false
        } else {
          let classIds = []
          let classInfoList = []
          for (let item of this.multipleSelection){
            classIds.push(item.classId)
            classInfoList.push(item.classId + '-' + item.className)
          }
          this.$confirm('确定删除  '+classInfoList.join('、')+'  吗?', '提示', {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }).then(() => {
            // console.log(teaIds)
            this.$axios
            .post('/admin/batchDelClass/', {
              ids:classIds
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

      handleCurrentChange(val) {
        this.currentPage = val
      },
      handleSizeChange(val) {
        this.pageSize = val
        console.log(`每页 ${val} 条`);
      },
      deptChange(){
        let dept = this.form.department
        this.getAllClass({department:dept})
      },
      searchOk(){
        this.getTableData()
      },
    },
    watch: {
      deptSelected: function () {
        // this.$nextTick(function () {
        //   this.getTableData()
        // })
      }
    },
    created(){
      this.gradeSelected = this.gradeOptions[0].grade
      this.getDptName()
    }
  }
</script>