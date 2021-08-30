<template>
  <div style="width:100%" class="shadow">
  <el-row type="flex" class="row-bg" justify="space-between" style="margin-bottom:5px">
    <el-select v-model="deptSelected" placeholder="请选择学院" style="width:150px" size="small">
        <el-option
          v-for="item in deptOptions"
          :key="item.id" :label="item.name" :value="item.id">
        </el-option>
    </el-select>
     
      <el-select v-model="isPublicCrs" placeholder="请选择课程类型" style="width:150px" size="small">
          <el-option label="全部类型" value="-1"></el-option>
          <el-option value="专业必修"></el-option>
          <el-option value="专业选修"></el-option>
          <el-option value="通识必修"></el-option>
          <el-option value="通识选修"></el-option>
          </el-option>
      </el-select>
     
    <el-col :span="13">
      <el-input v-model="search" placeholder="请输入搜索内容"  size="small">
          <el-button slot="append" icon="el-icon-search" @click="searchOk">搜索</el-button>
      </el-input>
    </el-col>
    
    <el-button type="primary" plain size="small" @click="addCrsBtn" icon="el-icon-plus">添加课程</el-button>
    <el-button type="primary" plain size="small" @click="dialogUploadVisible = true" icon="el-icon-folder-add">导入课程</el-button>
    <el-tooltip class="item" effect="light" content="选中多项可批量删除" placement="top-end">
        <el-button type="warning" plain size="small" @click="batchDelCourse" icon="el-icon-delete">批量删除</el-button>
    </el-tooltip>
  </el-row>

  <div style="background-color:#eff1f2;padding:5px;border-radius: 2px;">
  <el-table
    :data="tables.slice((currentPage-1)*pageSize,currentPage*pageSize)"
    v-loading="loading"
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
    <el-table-column prop="id" fixed label="课程编号" width="150">
    </el-table-column>
    <el-table-column prop="name" label="课程名称" width="180">
    </el-table-column>
    <el-table-column prop="type" label="课程类别" width="150">
    </el-table-column>
    <el-table-column prop="department" label="开设学院" width="200">
    </el-table-column>
    <el-table-column prop="hours" label="学时" width="100">
    </el-table-column>
    <el-table-column prop="credit" label="学分" width="100">
    </el-table-column>
    <el-table-column prop="operate" label="操作" width="150" fixed="right">
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

  <el-dialog :title="dialogTitle" :visible.sync="dialogFormVisible" :close-on-click-modal="false" width="30%">
  <el-form :model="form" :rules="rules" ref="crsForm" status-icon>
    <el-form-item label="课程名称" :label-width="formLabelWidth" prop="name">
      <el-input v-model="form.name" autocomplete="off"></el-input>
    </el-form-item>
    <el-form-item label="开设院校" :label-width="formLabelWidth" prop="dptNo">
      <el-select v-model="form.dptNo" placeholder="请选择">
      <el-option v-for="item in deptOptions2" :key="item.id" :label="item.name" :value="item.id">
          </el-option>
      </el-select>
    </el-form-item>
    <el-form-item label="课程类别" :label-width="formLabelWidth" prop="type">
      <el-select v-model="form.type" placeholder="请选择">
        <el-option value="专业必修"></el-option>
        <el-option value="专业选修"></el-option>
        <el-option value="通识必修"></el-option>
        <el-option value="通识选修"></el-option>
      </el-select>
    </el-form-item>
    <el-form-item>
      <el-col :span="12">
        <el-form-item label="学时" :label-width="formLabelWidth" prop="hours">
          <el-input v-model="form.hours" type="number" min="0" autocomplete="off"></el-input>
        </el-form-item>
      </el-col>
      <el-col :span="12">
        <el-form-item label="学分" :label-width="formLabelWidth" prop="credit">
          <el-input v-model="form.credit" type="number" min="0" autocomplete="off"></el-input>
        </el-form-item>
      </el-col>
    </el-form-item>
  </el-form>
  <div slot="footer" class="dialog-footer">
    <el-button @click="handleCancel('crsForm')">取 消</el-button>
    <el-button type="primary" @click="addCourseData('crsForm')" :style="{display: this.visible1}">提交</el-button>
    <el-button type="primary" @click="editOk('crsForm')" :style="{display: this.visible2}">修改</el-button>
  </div>
</el-dialog>

<el-dialog title="上传文件" :visible.sync="dialogUploadVisible" :close-on-click-modal="false">
  <el-upload
  class="upload-demo"
  ref="upload"
  :multiple="false"
  :show-file-list="true"
  accept=".xls,.xlsx"
  action="http://127.0.0.1:9090/admin/uploadCourse/"
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
  export default {
    data() {
      var validateNum = (rule, value, callback) => {
        console.log(value)
          if(value<0){
              callback(new Error('请输入正整数'))
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
        isPublicCrs:'-1', // 课程类型  选课或者必修课
        deptOptions:[],
        deptOptions2:[],
        deptSelected: '',
        search: '',
        loading: false,
        dialogTitle: '新增开设课程',

        tableData:[],//目前前端所拥有的所有课程信息
        multipleSelection: [],

        pageSize:10,
        pageSizes:[10,20,40,60],
        currentPage:1,
        // totalCount:0,

        dialogFormVisible: false,
        form: {
          id:'',
          name: '',
          dptNo:'',
          department:'',
          type: '',
          hours: '',
          credit: '',
        },
        formLabelWidth: '80px',
        visible2:'none',
        visible1:'inline',
        isDisabled:false,

        dialogUploadVisible: false,
        fileList:[],
        addRules: {
          name: [{ required: true, message: '请输入课程名', trigger: 'blur' },
                 { validator: validateName, trigger: 'input' }
          ],
          dptNo: [{ required: true, message: '请选择学院', trigger: 'change' }],
          department: [{ required: true, message: '请选择学院', trigger: 'change' }],
          type: [{ required: true, message: '请选择类型', trigger: 'change' }],
          hours: [{ required: true, message: '请选择学时', trigger: 'blur' }],
          credit: [{ required: true, message: '请选择学分', trigger: 'blur' }]
        },
        editRules: {
          id: [{ required: true, message: '请输入课程编号', trigger: 'blur' },
            {min:5, max:5, message: '请输入5位课程编号', trigger: 'blur' }],
          name: [{ required: true, message: '请输入课程名', trigger: 'blur' },
                 { validator: validateName, trigger: 'input' }
          ],
          dptNo: [{ required: true, message: '请选择学院', trigger: 'change' }],
          department: [{ required: true, message: '请选择学院', trigger: 'change' }],
          type: [{ required: true, message: '请选择类型', trigger: 'change' }],
          hours: [{ required: true, message: '请选择学时', trigger: 'blur' },
                  { validator: validateNum, trigger: 'input' }
          ],
          credit: [{ required: true, message: '请选择学分', trigger: 'blur' },
                   { validator: validateNum, trigger: 'input' }
          ]
        },
        rules: []
      }
    },
    computed:{
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
      //根据条件请求某一页数据
      getTableData(){
        let params = {}
        params.dpt = this.deptSelected
        if (this.isPublicCrs!=='-1') {
          params.courseType = this.isPublicCrs
        }
        this.$axios
        .post('/admin/getCourseInfo/', params)
        .then((result)=> {
            if (result.data.code === 1) { //返回第一页数据，和
              this.tableData = result.data.datas
              this.currentPage = 1
            }else{
              alert(result.data.msg)
              return false;
            }
        })
        .catch((error)=> {
            alert(error)
        })
      },
      searchOk(){
        this.getTableData()
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
          alert("导入成功，共添加"+total+"条，成功"+success+"条，失败"+failed+"条")
          this.getTableData()
        } else {
          alert(response.msg)
        }
      },
      // 取消模态层
      handleCancel(formName){
        this.dialogFormVisible = false
        this.resetForm(formName)
      },
      resetForm(formName) {
        this.$refs[formName].resetFields();
      },
      
      getDptName(){
        this.$axios
        .post('/admin/getDptName/', {})
        .then((result)=> {
            if (result.data.code === 1) {//返回第一页数据，和
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

      addCrsBtn(){
        this.dialogTitle = "新增开设课程"
        this.rules = this.addRules
        this.form.id = ""
        this.form.name = ""
        this.form.dptNo = ""
        this.form.hours = ""
        this.form.type = ""
        this.form.credit = ""
        this.dialogFormVisible = true 
        this.visible2 = 'none'
        this.visible1 = 'inline'
        this.isDisabled=false
      },

      addCourseData(formName){
        if (this.form.hours < 0 || this.form.credit <0) {
          alert('学分学时必须大于零')
          return
        }
        this.$refs[formName].validate((valid) => {
          if (valid) {
            this.$axios
            .post('/admin/addCourse/', this.form)
            .then((result)=> {
                if (result.data.code === 1) {
                  this.$message({
                    type: 'success',
                    message: '添加成功!'
                  });
                  this.dialogFormVisible = false
                  this.getTableData()
                }else{
                  this.$message({
                    type: 'error',
                    message: result.data.msg
                  });
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

      handleEdit(index,row){
        this.dialogTitle = "编辑开设课程"
        this.rules = this.editRules
        this.form.id = row.id
        this.form.name = row.name
        this.form.dptNo = row.dptNo
        this.form.department = row.department
        this.form.hours = row.hours
        this.form.type = row.type
        this.form.credit = row.credit
        this.visible1 = 'none'
        this.visible2 = 'inline'
        this.isDisabled=true
        this.dialogFormVisible = true
      },

      editOk(){
        if (this.form.name.replace(/\s*/g, '') === '') {
          alert('课程名不能为空')
          return
        }
        if (this.form.hours < 0 || this.form.credit <0) {
          alert('学分学时必须大于零')
          return
        }
        this.$axios
        .post('/admin/editCourse/', this.form)
        .then((result)=> {
            if (result.data.code == 1) {//返回第一页数据，和
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
      },

      handleDelete(index,row){
        this.$confirm('确定删除 '+row.department+'-'+row.id+'-'+row.name+' 吗?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          this.$axios
          .post('/admin/delCourse/', {
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
      handleSelectionChange(val) {
        this.multipleSelection = val;
      },
      batchDelCourse(){
        // console.log(this.multipleSelection)
        if (!this.multipleSelection || this.multipleSelection.length === 0){
          this.$message.warning('请选择要批量删除的课程数据')
          return false
        } else {
          let courseIds = []
          let courseInfoList = []
          for (let item of this.multipleSelection){
            courseIds.push(item.id)
            courseInfoList.push(item.department + '-' + item.id + '-' + item.name)
          }
          this.$confirm('确定删除'+courseInfoList.join('、')+'吗?', '提示', {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }).then(() => {
            // console.log(courseIds)
            this.$axios
            .post('/admin/batchDelCourse/', {
              ids:courseIds
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
      }
    },
    watch: {
      deptSelected: function () {
        // this.$nextTick(function () {
        //   this.getTableData()
        // })
      }
    },
    created(){
      this.getDptName()
    }
  }
</script>