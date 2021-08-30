<template>
  <div style="width:1100px">
  <el-row type="flex" class="row-bg" justify="space-between" style="margin-bottom:5px">
  <el-col :span="5">
    <label>学期：</label>
    <el-select v-model="termSelected" placeholder="请选择学期" @change="getTermSelected" style="width:180px" size="small">
    <el-option
      v-for="item in termOptions"
      :key="item.term"
      :label="item.label"
      :value="item.term">
    </el-option>
    </el-select>
  </el-col>
  <el-col :span="5">
    <label>课程：</label>
    <el-select v-model="crsSelected" placeholder="请选择课程" style="width:180px" size="small">
      <el-option
        v-for="item in crsOptions"
        :key="item.id"
        :label="item.name"
        :value="item.id">
      </el-option>
    </el-select>
  </el-col>
    <el-button style="margin-left: 10px;" type="primary" size="small" icon="el-icon-search" @click="searchOk">搜索</el-button>
    <el-button type="primary" plain size="small" @click="exportExcel">导出学生成绩</el-button>
  </el-row>

  <div style="background-color:#eff1f2;padding:5px;border-radius: 2px;">
  <el-row type="flex" class="row-bg" justify="space-between" style="margin-bottom:5px">
    <el-col :span="20">
      <el-input v-model="search" placeholder="请输入搜索内容"  size="mini">
        <el-button slot="append" icon="el-icon-search"></el-button>
      </el-input>
    </el-col>
      <el-button-group>
        <el-button size="mini" type="primary" icon="el-icon-edit" @click="show = true" round></el-button>
        <el-button size="mini" type="primary" icon="el-icon-check" @click="show = false" round></el-button>
      </el-button-group>
      <el-button size="mini" type="success" @click="postListData" round>提交</el-button>
  </el-row>
  
  <el-table id="classListTable"
    :data="tables.slice((currentPage-1)*pageSize,currentPage*pageSize)"
    border
    stripe
    style="width: 100%"
    :header-row-style="{height:0+'px'}"
    :header-cell-style="{padding:0+'px'}"
    :row-style="{height:'20px'}"
    :cell-style="{padding:'2px'}">
    <el-table-column type="index" label="序号" width="59">
    </el-table-column>
    <el-table-column prop="stuId" label="学号" width="150">
    </el-table-column>
    <el-table-column prop="classAndGrade" label="班级" width="150">
    </el-table-column>
    <el-table-column prop="stuName" label="姓名" width="200">
    </el-table-column>
    <el-table-column prop="courseName" label="课程" width="150">
    </el-table-column>
    <el-table-column prop="score" label="成绩" width="200">
      <template slot-scope="scope">
        <el-input size="mini" type="number" min="0" max="100" v-show="show" v-model="scope.row.score" @blur="checkScore(scope.row)"></el-input>
        <span v-show="!show">{{scope.row.score}}</span>
      </template>
    </el-table-column>
    <el-table-column prop="tag" label="标签" width="170">
        <template slot-scope="scope">
          <el-tag size="mini"
          :type="(scope.row.score==null||scope.row.score=='')? 'info':(scope.row.score >= 60) ? 'success' : 'danger'"
          disable-transitions>{{(scope.row.score==null ||scope.row.score=='')? '未录入':(scope.row.score >= 60)?'合格':'不合格'}}
          </el-tag>
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
  </div>
</template>

<script>
import {getCookie} from '../global/cookie'
import termOptions from '../global/termOptions.js'
import FileSaver from 'file-saver'
import XLSX from 'xlsx'
  export default {
    data() {
      return {
        termOptions:termOptions,
        termSelected: '',
        crsOptions:'',
        crsSelected:'',

        classListTableData:[],
        search: '',
        show: false,

        pageSize:10,
        pageSizes:[10,20,40,60],
        currentPage:1,
        // totalCount:0,
        loading:false
      }
    },
    computed:{
      tables () {
        const search = this.search
        if (search) {
          return this.classListTableData.filter(data => {
            return Object.keys(data).some(key => {
              return String(data[key]).toLowerCase().indexOf(search) > -1
            })
          })
        }
        return this.classListTableData
      },
      totalCount () {
        if (!this.tables.length) {
          return 0
        }
        return this.tables.length
      }
    },
	mounted() {
		this.loadData()
	},
    methods:{
	  async loadData(){
		  let ret = await this.$axios.post('/teacher/getStuScore/',{})
		  if (ret.data.code === 1) {
			  this.classListTableData = ret.data.datas
		  }
	  },
      getTermSelected(){
        this.classListTableData = []
        this.$axios
        .post('/teacher/getCourse/', {
            term: this.termSelected
        })
        .then((result)=> {
            if (result.data.code === 1) {
              this.crsOptions=result.data.datas
              this.crsSelected = ''
            }
        })
        .catch((error)=> {
            alert(error)
        })
      },

      searchOk(){
        this.selectOk()
      },
      checkScore(row){
        console.log(row)
        if (row.score < 0 || row.score > 100) {
          row.score = ''
          this.$message.warning('分数不在0-100之间，请重新输入!')
        }
      },
      selectOk(){
        this.classListTableData = []
        if(this.termSelected===''||this.crsSelected===''){
          alert("请检查查询条件")
          return
        }
        this.$axios
        .post('/teacher/getScoreData/', { //获取查询学生名单接口
            crsId:this.crsSelected
        })
        .then((result)=> {
            if (result.data.code === 1) {
              this.classListTableData = result.data.datas
            }
        })
        .catch((error)=> {
            alert(error)
        })
      },

      postListData(){
        if(this.show==true){
          this.$message({
            type: 'info',
            message: '编辑状态不能提交'
          });
          return
        }
        if (this.tables.length===0){
          alert('没有数据，不需要提交')
          return
        }
        
        this.$confirm('确定提交成绩吗?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          this.$axios
          .post('/teacher/postScoreList/', {
            scoreList:this.tables
          })
          .then((result)=> {
              if (result.data.code === 1) {
                this.$message({
                  type: 'success',
                  message: '成绩更新成功'
                });
              }
          })
          .catch((error)=> {
              alert(error)
          })
        }).catch(() => {})
      },

      exportExcel(){
        if (this.tables.length === 0){
          alert('请筛选需要导出的数据')
          return
        }
        require.ensure([], () => {
          const { export_json_to_excel } = require('../../excel/Export2Excel');
          const tHeader = [ '学号', '班级', '姓名', '课程', '成绩'];
          const filterVal = ['stuId', 'classAndGrade', 'stuName', 'courseName', 'score'];
          const list = this.tables;
          const data = this.formatJson(filterVal, list);
          export_json_to_excel(tHeader, data, 'studentInfoList');
        })
      },
      formatJson(filterVal, jsonData){
        return jsonData.map(v => filterVal.map(j => v[j]))
      },
      handleCurrentChange(val) {
        this.currentPage=val
      },
      handleSizeChange(val) {
        console.log(`每页 ${val} 条`);
      }
    }
  }
</script>