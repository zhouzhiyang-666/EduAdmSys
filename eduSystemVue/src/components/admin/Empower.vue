<template>
  <div style="width:100%">
  <div style="background-color:#eff1f2;padding:5px;border-radius: 2px;">
  <el-row type="flex" class="row-bg" justify="space-between" style="margin-bottom:5px">
    <el-col :span="19">
    <el-input v-model="search" placeholder="请输入搜索内容" size="mini" clearable>
        <el-button slot="append" icon="el-icon-search" @click="searchOk"></el-button>
    </el-input>
    </el-col>
    <el-button size="mini" plain type="success"  @click="dialogFormVisible = true" icon="el-icon-plus" round>添加</el-button>
    <el-tooltip class="item" effect="light" content="选中多项可批量删除" placement="top-end">
        <el-button type="warning" plain size="mini" @click="batchDelAdm" icon="el-icon-delete" round>批量删除</el-button>
    </el-tooltip>
  </el-row>
  
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
          :selectable="checkSelect"
          width="59"></el-table-column>
    <el-table-column prop="uid" label="工号" width="150"></el-table-column>
    <el-table-column prop="teaName" label="姓名" width="150"></el-table-column>
    <el-table-column prop="department" label="学院" width="230"></el-table-column>
    <el-table-column prop="telephone" label="手机号" width="200"></el-table-column>
    <el-table-column prop="name" label="权限" width="100"></el-table-column>
    <el-table-column prop="operate" label="操作" width="160" fixed="right">
      <template slot-scope="scope">
        <div v-if="scope.row.uid === userid || scope.row.uid === '12345678'">
          <span> -- -- </span>
        </div>
        <div v-else>
          <el-col :span="12">
            <el-button size="mini" plain type="primary" @click="handleUp(scope.$index, scope.row)" :style="{display: (scope.row.name==='管理员')? 'inline':'none'}" >提权</el-button>
          </el-col>
          <el-col :span="12">
            <el-button size="mini" plain type="primary" @click="handleDown(scope.$index, scope.row)" :style="{display: (scope.row.name==='超级管理员')? 'inline':'none'}">降权</el-button>
          </el-col>
          <el-col :span="12">
            <el-button size="mini" plain type="danger" @click="handleDelete(scope.$index, scope.row)">删除</el-button>
          </el-col>
        </div>
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

  <el-dialog title="新增管理员" :visible.sync="dialogFormVisible" :close-on-click-modal=false width="30%">
    <el-form :model="form" :rules="rules" ref="admForm" status-icon>
      <el-form-item label="工号" :label-width="formLabelWidth" prop="uid">
        <el-input v-model="form.uid" maxlength="8" autocomplete="off" show-word-limit></el-input>
        <el-tooltip class="item" effect="light" content="点击校验职工名字" placement="right">
            <el-button type="warning" plain size="small" @click="getAdmName('admForm')" icon="el-icon-user">校验名字</el-button>
        </el-tooltip>
      </el-form-item>
      
      <el-form-item label="管理员名" :label-width="formLabelWidth" prop="admName">
        <el-input v-model="form.admName" autocomplete="off" disabled></el-input>
      </el-form-item>

      <el-form-item label="权限" :label-width="formLabelWidth" prop="name">
        <el-select v-model="form.name" placeholder="请选择">
          <el-option label="管理员" value="admin"></el-option>
          <el-option label="超级管理员" value="super_admin"></el-option>
        </el-select>
      </el-form-item>
      
    </el-form>
    <div slot="footer" class="dialog-footer">
      <el-button @click="handleCancel('admForm')">取 消</el-button>
      <el-button type="primary" @click="addData('admForm')">提交</el-button>
    </div>
  </el-dialog>

</div>
</template>

<script>
import {getCookie} from '../global/cookie'
  export default {
    data() {
      return {
        tableData:[],
        multipleSelection: [],

        search: '',

        pageSize:10,
        pageSizes:[10,20,40,60],
        currentPage:1,
        // totalCount:0,
        loading:false,

        dialogFormVisible: false,
        formLabelWidth: '80px',
        form: {
          name: '',  // 权限
          uid:'',   // 管理员工号即教师工号
          admName: ''  //管理员名字
        },
        allowPost: false, // 是否允许添加管理员
        rules: {
          uid: [{ required: true, message: '请输入工号', trigger: 'blur' },
            {min:8, max:8, message: '请输入8位工号', trigger: 'blur' }],
          name: [{ required: true, message: '请选择权限', trigger: 'blur' }],
          admName: [{ required: true, message: '请输入正确的工号获取名字', trigger: 'blur' }]
        }
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
      totalCount () {
        if (!this.tables.length) {
          return 0
        }
        return this.tables.length
      },
      userid () {
        return this.$store.getters.getUser.userid
      }
    },
    methods:{
      checkSelect (row, index) {
        let isChecked = false
        if (row.uid === this.userid || row.uid === '12345678') { // 判断里面是否存在某个参数
          isChecked = false
        } else {
          isChecked = true
        }
        return isChecked
      },
      searchOk(){
        this.getTableData()
      },
      addData(formName){
        this.$refs[formName].validate((valid) => {
          if (valid && this.allowPost) {
            this.$axios
            .post('/admin/addAdmin/', {
              uid:this.form.uid,
              name:this.form.name
            })
            .then((result)=> {
                if (result.data.code === 1) {
                  this.tableData.unshift(result.data.datas)
                  this.dialogFormVisible = false
                  this.$message.success('添加成功!')
                  this.$refs[formName].resetFields()
                  this.getTableData()
                }else{
                  this.$message.warning(result.data.msg)
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
      getAdmName(formName){
        if(this.form.uid.length === 8){
          let that = this
          this.$axios
          .post('/admin/getTeaName/',{teaNo:this.form.uid})
          .then((result)=> {
            if (result.data.code === 1) {
              // this.$set(this.form, 'admName', result.data.datas.teacherName)
              that.form.admName = result.data.datas.teacherName
              this.$forceUpdate()
              this.allowPost = true
            } else{
              that.form.admName = ''
              this.allowPost = false
              alert('请输入正确的工号')
            }
          })
          .catch((error)=> {
            that.form.admName = ''
            this.allowPost = false
            alert(error)
          })
        } else {
          this.allowPost = false
        }

      },
      handleDelete(index,row){
        this.$confirm('确定删除'+row.teaName+'吗?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          this.$axios
          .post('/admin/delAdmin/', {
            id:row.uid
          })
          .then((result)=> {
            if (result.data.code === 1) {
              for(var i = 0; i < this.tableData.length;i++){
                if(this.tableData[i].uid===row.uid){
                  this.tableData.splice(i, 1)
                  break;
                }
              }
              this.$message.success('删除成功!');
              this.getTableData()
            }else{
              alert(result.data.msg)
              return false;
            }
          })
          .catch((error)=> {
            alert(error)
          })
        }).catch(() => {});
      },
      // 取消模态层
      handleCancel(formName){
        this.dialogFormVisible = false
        this.resetForm(formName)
      },
      resetForm(formName) {
        this.$refs[formName].resetFields();
      },
      // 批量删除
      handleSelectionChange(val) {
        this.multipleSelection = val;
      },
      batchDelAdm(){
        // console.log(this.multipleSelection)
        if (!this.multipleSelection || this.multipleSelection.length === 0){
          this.$message.warning('请选择要批量删除的管理员信息')
          return false
        } else {
          let admIds = []
          let admInfoList = []
          for (let item of this.multipleSelection){
            admIds.push(item.uid)
            admInfoList.push(item.department + '-' + item.uid + '-' + item.teaName)
          }
          this.$confirm('确定删除 '+admInfoList.join('、')+' 吗?', '提示', {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }).then(() => {
            // console.log(admIds)
            this.$axios
            .post('/admin/batchDelAdm/', {
              ids:admIds
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
      handleUp(index,row){
        this.$confirm('确定提权吗?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          this.$axios
          .post('/admin/upToSuperAdmin/', {
            id:row.uid
          })
          .then((result)=> {
              if (result.data.code === 1) {
                row.name = "超级管理员"
              }else{
                alert(result.data.msg)
                return false;
              }
          })
          .catch((error)=> {
              alert(error)
          })
        })
      },
      handleDown(index,row){
        this.$confirm('确定降吗?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          this.$axios
          .post('/admin/upToAdmin/', {
            id:row.uid
          })
          .then((result)=> {
              if (result.data.code === 1) {
                row.name = "管理员"
              }else{
                alert(result.data.msg)
                return false;
              }
          })
          .catch((error)=> {
              alert(error)
          })
        })
      },
      getTableData(){
        this.$axios
        .post('/admin/getRoleData/', {})
        .then((result)=> {
            if (result.data.code === 1) {
              this.totalCount=result.data.datas.length
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
      handleCurrentChange(val) {
        this.currentPage = val
      },
      handleSizeChange(val) {
        this.pageSize = val
        console.log(`每页 ${val} 条`);
      },
    }
  }
</script>