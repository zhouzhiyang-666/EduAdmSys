<template>
<div style="width:100%">
  <el-row type="flex" style="margin-bottom:5px" :gutter="5">
    <el-col :span="4">
      <el-select v-model="deptSelected" placeholder="请选择学院" size="small">
            <el-option
            v-for="item in deptOptions"
            :key="item.id"
            :label="item.name"
            :value="item.id">
            </el-option>
        </el-select>
    </el-col>
    <el-col :span="3">
        <el-select v-model="gradeSelected" placeholder="请选择年级" size="small">
            <el-option
            v-for="item in gradeOptions"
            :key="item.grade"
            :label="item.label"
            :value="item.grade">
            </el-option>
        </el-select>
    </el-col>
    <el-col :span="5">
      <el-select v-model="termSelected" placeholder="请选择学年" size="small">
        <el-option
          v-for="item in termOptions"
          :key="item.term"
          :label="item.label"
          :value="item.term">
        </el-option>
      </el-select>
    </el-col>
    <el-col :span="3">
      <el-button type="primary" plain size="small" @click="selectOk" icon="el-icon-search">查询</el-button>
    </el-col>
    <el-col :span="4">
      <el-button type="primary" plain size="small" @click="dialogUploadVisible = true" icon="el-icon-upload2">导入课程安排</el-button>
    </el-col>
    <el-col :span="4">
      <el-tooltip class="item" effect="light" content="选中多项可批量删除" placement="top-end">
        <el-button type="warning" plain size="small" @click="batchDel" icon="el-icon-delete">批量删除选课</el-button>
      </el-tooltip>
    </el-col>
    <el-col :span="3">
        <el-select v-model="openGradeSelected" placeholder="选课年级" size="small" :disabled="this.isOpen==true">
            <el-option
            v-for="item in gradeOptions"
            :key="item.grade"
            :label="item.label"
            :value="item.grade">
            </el-option>
        </el-select>
    </el-col>
    <el-col :span="5">
      <el-select v-model="openTermSelected" placeholder="开启的选课学年" size="small" 
                  :style="{display: this.visible}"
                  :disabled="this.isOpen==true">
        <el-option
          v-for="item in termOptions"
          :key="item.term"
          :label="item.label"
          :value="item.term">
        </el-option>
      </el-select>
    </el-col>
    <el-col :span="3">
      <el-button type="danger" size="small" plain
                :style="{display: this.visible}" 
                @click="openOrClose">{{this.isOpen==true?"结束选课":"开启选课"}}</el-button>
    </el-col>
  </el-row>

  <div style="background-color:#eff1f2;padding:5px;border-radius: 2px;">
    <el-table
    :data="tableData.slice((currentPage-1)*pageSize,currentPage*pageSize)"
    border
    stripe
    style="width: 100%"
    :header-row-style="{height:0+'px'}"
    :header-cell-style="{padding:0+'px'}"
    :row-style="{height:'20px'}"
    :cell-style="{padding:'2px'}"
    @selection-change="handleSelectionChange">
    <!-- <el-table-column type="index" label="序号" width="49"></el-table-column> -->
    <el-table-column
          type="selection"
          width="45">
    </el-table-column>
    <el-table-column prop="courseno" fixed label="课程编号" width="80"></el-table-column>
    <el-table-column prop="courseName" fixed label="课程名称" width="170"></el-table-column>
    <el-table-column prop="type" label="课程类型" width="100"></el-table-column>
    <el-table-column prop="hours" label="学时" width="50"></el-table-column>
    <el-table-column prop="credit" label="学分" width="50"></el-table-column>
    <el-table-column prop="crsDate" label="时间" width="130"></el-table-column>
    <el-table-column prop="area,room" label="地点" width="150">
      <template slot-scope="scope"> {{scope.row.area}}{{scope.row.room}} </template>
    </el-table-column>
    <el-table-column prop="teacherName" label="任课教师" width="100"></el-table-column>
    <el-table-column prop="total" label="人数" width="50"></el-table-column>
    <el-table-column prop="grade" label="年级" width="60"></el-table-column>
    <el-table-column fixed="right" prop="operate" label="操作" width="160">
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

  <el-dialog title="课程安排" :visible.sync="dialogFormVisible" :close-on-click-modal="false" width="40%">
  <el-form :model="form" :rules="rules" ref="courseForm" status-icon>
    <el-form-item label="年级学年" label-width="80px">
      <el-select v-model="form.grade" placeholder="请选择年级" style="width:150px">
        <el-option v-for="item in gradeOptions2" :key="item.grade" :label="item.label" :value="item.grade"> </el-option>
      </el-select>
      <el-select v-model="form.term" placeholder="请选择学年" style="width:180px;margin-left:10px">
        <el-option v-for="item in termOptions" :key="item.term" :label="item.label" :value="item.term"> </el-option>
      </el-select>
    </el-form-item>
    <el-form-item label="上课地点" label-width="80px">
      <el-select v-model="form.area" placeholder="请选择区域" @change="getAreaSelected" style="width:180px">
        <el-option v-for="item in areaOptions" :key="item.area" :label="item.label" :value="item.area"></el-option>
      </el-select>
      <el-select v-model="form.room" placeholder="请选择教室" style="width:180px;margin-left:10px">
        <el-option v-for="item in roomOptions" :key="item.id" :label="item.room" :value="item.id"></el-option>
      </el-select>
    </el-form-item>
    <el-form-item label="上课时间" label-width="80px">
      <el-select v-model="form.week" placeholder="请选择星期" style="width:180px">
          <el-option v-for="item in weekOptions" :key="item.value" :label="item.label" :value="item.value"></el-option>
      </el-select>
      <el-select v-model="form.time" placeholder="请选择时间" style="width:180px;margin-left:10px">
          <el-option v-for="item in timeOptions" :key="item.value" :label="item.label" :value="item.value"></el-option>
      </el-select>
    </el-form-item>
    <el-form-item label="任课教师" label-width="80px" prop="teacherno">
      <el-input maxlength="8" v-model="form.teacherno" style="width:180px" show-word-limit></el-input>
      <el-button type="warning" plain style="margin-left: 5px;" size="small" @click="getTeaName" icon="el-icon-right"></el-button>
      <el-input v-model="form.teacherName" style="width:180px;margin-left:10px" disabled></el-input>
    </el-form-item>
    <el-form-item label="课程编号" label-width="80px" prop="courseno">
      <el-input maxlength="5" v-model="form.courseno" style="width:180px" show-word-limit></el-input>
      <el-button type="warning" plain style="margin-left: 5px;" size="small" @click="getCourseName" icon="el-icon-right"></el-button>
      <el-input v-model="form.courseName" style="width:180px;margin-left:10px" disabled></el-input>
    </el-form-item>
    <el-form-item label="最大人数" label-width="80px" type="number" prop="total">
      <el-input type="number" min="0" v-model="form.total" style="width:180px" @blur="checkNumber(form)"></el-input>
    </el-form-item>

  </el-form>
  <div slot="footer" class="dialog-footer">
    <el-button @click="dialogFormVisible = false">取 消</el-button>
    <el-button type="primary" @click="editOk">提交</el-button>
  </div>
  </el-dialog>

  <el-dialog title="上传文件" :visible.sync="dialogUploadVisible" :close-on-click-modal="false">
    <el-upload
        class="upload-demo"
        ref="upload"
        :multiple="false"
        accept=".xls,.xlsx"
        action="http://127.0.0.1:9090/admin/uploadCourseArrange/"
        :on-success="handleAvatarSuccess"
        :on-error="handleAvatarError"
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
import areaOptions from '../global/areaOptions.js'
import weekOptions from '../global/weekOptions.js'
import timeOptions from '../global/timeOptions.js'
import termOptions from '../global/openCourseTerm.js'
import {tryHideFullScreenLoading } from '../../loading.js'

  export default {
    data() {
      var validateTeaNo = (rule, value, callback) => {
        if ( value == '' || value == undefined) {
          callback(new Error('请输入教师工号'));
          return false
        } else if(value.length !== 8){
          callback(new Error('请输入8位教师工号'));
          return false
        } else{
          callback();
          return true
        }
      };
      var validateCourseNo = (rule, value, callback) => {
        if ( value == '' || value == undefined) {
          callback(new Error('请输入课程号'));
          return false
        } else{
          callback();
          return true
        }
      };
      return {
        deptOptions:[],
        termOptions:termOptions,
        deptSelected: '',
        gradeSelected:'',
        termSelected:'',
        openGradeSelected: '',
        openTermSelected:'',
        roomOptions:[],

        tableData:[],
        tableInfo:{
          term:'',
          grade:''
        },

        pageSize:10,
        pageSizes:[10,20,40,60],
        currentPage:1,
        totalCount:0,

        areaOptions:areaOptions,
        weekOptions:weekOptions,
        timeOptions:timeOptions,
        multipleSelection: [],

        isOpen:false,
        visible:'inline',

        dialogFormVisible:false,
        editIndex:0,
        form:{
          teaCrsNo:'',
          grade:'',
          term:'',
          teacherno:'',
          teacherName: '',
          courseno:'',
          courseName: '',
          spotNo:'',
          area:'',
          room:'',
          week:'',
          time:'',
          total:''
        },
        rules: {
          teacherno: [{ validator: validateTeaNo, trigger: 'blur' }],
          courseno: [{ validator: validateCourseNo, trigger: 'blur' }],
          total: [{ required: true, message: '请输入人数', trigger: 'change' }],
        },
        dialogUploadVisible: false,
        fileList:[],
        allowPost: false,
        allowPost2: false
      }
    },
    computed:{
      gradeOptions(){
        let myData = new Date()
        var year1 = myData.getFullYear()
        let month1 = myData.getMonth()
        var n = 4
        var options = []
          if(month1<8){
            n=5
          }
          for(var i=0;i<n;i++){
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
        var n = 4
        var options = []
          if(month1<8){
            n=5
          }
          for(var i=0;i<n;i++){
            options[i] = {
              grade:JSON.stringify(year1),
              label:year1+'级'
            }
              year1--
          }
        return options
      },
      // termOptions(){
      //   let myData = new Date()
      //   var year1 = myData.getFullYear()
      //   let month1 = myData.getMonth()
      //   var options = []
      //   if(month1<8){
      //     options[0] = {
      //       term:year1+"2",
      //       label:year1+'-'+(year1+1)+'第一学期'
      //     }
      //   }else{
      //     options[0] = {
      //       term:(year1+1)+"1",
      //       label:year1+'-'+(year1+1)+'第二学期'
      //     }
      //   }
      //   return options
      // },
      headers(){
        return {
          authorization: this.$store.getters.getToken,
          userid: this.$store.getters.getUser.userid
        }
      }
    },

    methods:{
      getDptName(){
        this.$axios
        .post('/admin/getDptName/', {})
        .then((result)=> {
            if (result.data.code === 1) {//返回第一页数据，和
              this.deptOptions = result.data.datas
              this.deptOptions.unshift({id:'0',name:'全部学院'})
              this.deptSelected = '0'
              this.gradeSelected = '0'
            }else{
              return false;
            }
        })
        .catch((error)=> {
            alert(error)
        })
      },
      getActiveSelect(){
        this.$axios
        .post('/admin/getActiveSelect/', {})
        .then((result)=> {
          console.log(result)
            if (result.data.code === 1) {//返回第一页数据，和
                this.openGradeSelected = result.data.datas.grade
                this.openTermSelected = result.data.datas.term
            }else{
              return false;
            }
        })
        .catch((error)=> {
            alert(error)
        })
      },
      getAreaSelected(){
        this.$axios
        .post('/public/getRoomByArea/', { 
          area:this.form.area
        })
        .then((result)=> {
          console.log(result)
          this.form.room = ""
          this.roomOptions = result.data.datas
        })
        .catch((error)=> {
            alert(error)
        })
      },

      selectOk(){
        if(this.deptSelected==""||this.gradeSelected==""||this.termSelected==""){
          alert('请选择条件')
          return;
        }
        this.tableInfo.term = this.termSelected
        this.tableInfo.grade = this.gradeSelected
        this.$axios
        .post('/admin/getCrsArrange/', {
          dpt: this.deptSelected,
          grade: this.gradeSelected,
          term: this.termSelected
        })
        .then((result)=> {
            if (result.data.code === 1) {//返回第一页数据，和
              let crsData = result.data.datas
              for (let item of crsData){   // 该日期为中文
                let dateZH = ''
                for (let weekTemp of this.weekOptions){
                  if (item.week == weekTemp.value){
                    dateZH = dateZH + weekTemp.label
                  }
                }
                for (let timeTemp of this.timeOptions){
                  if (item.time == timeTemp.value){
                    dateZH = dateZH + '-'+ timeTemp.time
                  }
                }
                item.crsDate = dateZH
              }
              this.tableData = crsData
              this.totalCount = result.data.datas.length
              this.currentPage = 1
            }else{
              return false;
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
        // console.log(this.fileList)
      },
      handleAvatarError(response, file, fileList){
        console.log(response.msg, file, fileList)
        alert('文件格式不符合规范，请检查后再上传!')
      },
      handleAvatarSuccess(response, file, fileList){
        // var errorMsg = []
        // for(let val of response.datas.errorList){
        //   errorList.push()
        // }
        console.log(response)
        if (response.code === 1) {
          let success = response.datas.success
          let total = response.datas.totalNum
          let failed = response.datas.failed
          alert("导入成功，共添加"+total+"条，成功"+success+"条，失败"+failed+"条"+'----'+
          '存在冲突的课程：'+ response.datas.errorList.join('、'))
          this.selectOk()
        } else {
          alert(response.msg)
        }
      },
      
      openOrClose(){
        if (!this.openTermSelected && !this.isOpen && this.openGradeSelected){
          alert('请选择要开启的选课学期')
          return false
        }
        this.$confirm('确定'+(this.isOpen==true?"结束选课":"开启选课")+'吗?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          this.$axios
          .post('/admin/openOrCloseStuSelect/', {active:this.openTermSelected,grade:this.openGradeSelected})
          .then((result)=> {
            if (result.data.code === 1) {
              this.$message.success(result.data.msg);
              this.isOpen = !this.isOpen
            }else{
              return false;
            }
          })
        }).catch(() => {});
      },
      loadButton(){
        this.$axios
        .post('/admin/loadButton/', {})
        .then((result)=> {
          if (result.data.code === 1) {
            this.isOpen = result.data.datas.isOpen==1? true: false
            this.visible = result.data.datas.isSuper==1? 'inline':'none'
          }else{
            return false;
          }
        })
        .catch((error)=> {
            alert(error)
        })
      },

      handleDelete(index,row){
        this.$confirm('确定删除 '+row.teacherName+'的《'+row.courseName+'》 吗?删除后该选课数据随同学生选课的数据一同删除', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          this.$axios
          .post('/admin/delCrsArrange/', {
            id:row.teaCrsNo
          })
          .then((result)=> {
            if (result.data.code === 1) {
              this.tableData.splice(index, 1)
              this.$message({
                type: 'success',
                message: '删除成功!'
              });
            }
          }).catch((error)=> {
            alert(error)
          })
        }).catch(() => {});
      },
      handleEdit(index,row){
        this.roomOptions = []
        this.allowPost = true
        this.allowPost2 = true
        this.form.teaCrsNo = row.teaCrsNo
        // this.form.grade = this.tableInfo.grade
        // this.form.term =this.tableInfo.term
        this.form.grade = row.grade
        this.form.term =row.term
        this.form.courseno = row.courseno
        this.form.courseName = row.courseName
        this.form.teacherno = row.teacherno
        this.form.teacherName = row.teacherName
        this.form.area = row.area
        this.form.room = row.spotNo
        this.form.spotNo = row.spotNo
        this.form.week = row.week
        this.form.time = row.time
        this.form.total = row.total
        this.editIndex = index
        this.dialogFormVisible = true
      },
      // 批量删除
      handleSelectionChange(val) {
        this.multipleSelection = val;
      },
      batchDel(){
        // console.log(this.multipleSelection)
        if (!this.multipleSelection || this.multipleSelection.length === 0){
          this.$message.warning('请选择要批量删除的教师档案数据')
          return false
        } else {
          let crsArrangeIds = []
          let crsArrangeInfoList = []
          for (let item of this.multipleSelection){
            crsArrangeIds.push(item.teaCrsNo)
            crsArrangeInfoList.push(item.teacherName + '-' + item.courseno + '-' + item.courseName)
          }
          this.$confirm('确定删除 '+crsArrangeInfoList.join('、')+' 的课程安排吗?', '提示', {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }).then(() => {
            // console.log(crsArrangeIds)
            this.$axios
            .post('/admin/batchDelCourseArrange/', {
              ids:crsArrangeIds
            })
            .then((result)=> {
              if (result.data.code === 1) {
                this.selectOk()
                this.$message({type: 'success',message: '删除成功!'});
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
      
      getTeaName(){
        this.$refs.courseForm.validate((valid) => {
          if (valid) {
            let that = this
            this.$axios
            .post('/admin/getTeaName/',{teaNo:this.form.teacherno})
            .then((result)=> {
              if (result.data.code === 1) {
                // this.$set(this.form, 'teacherName', result.data.datas.teacherName)
                that.form.teacherName = result.data.datas.teacherName
                this.$forceUpdate()
                this.allowPost = true
              } else{
                this.allowPost = false
                that.form.teacherName = '没有该教师信息'
                this.$forceUpdate()
                alert('请输入正确的工号')
              }
            })
            .catch((error)=> {
              this.allowPost = false
              alert(error)
            })
          } else {
            this.allowPost = false
          }
        })
      },
      getCourseName(){
        this.$refs.courseForm.validate((valid) => {
          if (valid) {
            let that = this
            this.$axios
            .post('/admin/getCourseName/',{courseno:this.form.courseno})
            .then((result)=> {
              if (result.data.code === 1) {
                // this.$set(this.form, 'teacherName', result.data.datas.teacherName)
                that.form.courseName = result.data.datas.courseName
                this.$forceUpdate()
                this.allowPost2 = true
              } else{
                this.allowPost2 = false
                that.form.courseName = '没有该课程信息'
                this.$forceUpdate()
                alert('请输入正确的课程号')
              }
            })
            .catch((error)=> {
              this.allowPost2 = false
              alert(error)
            })
          } else {
            this.allowPost2 = false
          }
        })
      },
      
      editOk(){
        if(!this.allowPost){
          alert('请输入正确的教师工号')
          return false
        } else if(!this.allowPost2){
          alert('请输入正确的课程号')
          return false
        } else if(!this.allowPost && !this.allowPost2){
          alert('请输入正确的教师工号和课程号')
          return false
        } else if(!this.form.room){
          alert('请选择上课地点')
          return false
        }
        if(this.form.total < 0){
          return
        }
        if(this.form.total === ''){
          alert('请输入人数')
          return
        }
        this.$confirm('确定修改为'+this.form.teacherName+'和《'+this.form.courseName+'》吗?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
            this.$axios
            .post('/admin/editCrsArrange/', this.form)
            .then((result)=> {
              if (result.data.code === 1) {
                this.$message({
                  type: 'success',
                  message: '修改成功!'
                });
                var i = this.editIndex
                if(this.form.grade!=this.tableInfo.grade||this.form.term!=this.tableInfo.term){
                  this.tableData.splice(i, 1)
                }else{
                  this.tableData[i].grade = this.form.grade
                  this.tableData[i].term =this.form.term
                  this.tableData[i].courseno = this.form.courseno
                  this.tableData[i].teacherno = this.form.teacherno
                  this.tableData[i].area = this.form.area
                  this.tableData[i].room = this.form.room
                  this.tableData[i].week = this.form.week
                  this.tableData[i].time = this.form.time
                  this.tableData[i].total = this.form.total
                }
                this.dialogFormVisible = false
                this.selectOk()
              }else{
                alert(result.data.msg)
                return false
              }
            })
            .catch((error)=> {
                alert(error)
            })
        })
      },
     
      handleCurrentChange(val) {
        this.currentPage = val
      },
      handleSizeChange(val) {
        this.pageSize = val
        console.log(`每页 ${val} 条`);
      },
      checkNumber(row){
        console.log(row)
        if (row.total < 0) {
          row.total = ''
          this.$message.warning('人数不能为负值，请重新输入!')
          return false
        }
        return true
      },
  },
  created(){
    this.getDptName()
    this.loadButton()
    this.getActiveSelect()
  }
}
</script>