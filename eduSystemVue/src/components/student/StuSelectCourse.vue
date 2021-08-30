<template>
    <div style="width:1051px">
      <div style="margin-bottom: 10px">
          <label>学院：</label>
          <el-select v-model="deptSelected" @change="deptSelect" placeholder="请选择学院" style="width:150px" size="small">
            <el-option
              v-for="item in deptOptions"
              :key="item.id" :label="item.name" :value="item.id">
            </el-option>
          </el-select>
          <el-button style="margin-left: 10px;" plain
                     type="primary" size="small" icon="el-icon-search" 
                     @click="searchOk">搜索</el-button>
      </div>
      
      <el-table
      :data="selectCrsData.slice((currentPage-1)*pageSize,currentPage*pageSize)"
      v-loading="loading"
      border
      stripe
      style="width: 100%"
      :header-row-style="{height:'20px'}"
      :header-cell-style="{padding:'4px'}"
      :row-style="{height:'20px'}"
      :cell-style="{padding:'2px'}">
      <el-table-column label="选课课程信息">
        <!-- <el-table-column type="index" width="50"></el-table-column> -->
        <el-table-column prop="courseno" label="课程编号" width="100"></el-table-column>
        <el-table-column prop="type" label="课程类型" width="90"></el-table-column>
        <el-table-column prop="courseName" label="课程名" width="200"></el-table-column>
        <el-table-column prop="credit" label="学分" width="60"></el-table-column>
        <el-table-column prop="hours" label="学时" width="60"></el-table-column>
        <el-table-column prop="area,room" label="地点" width="140">
          <template slot-scope="scope"> {{scope.row.area}}{{scope.row.room}} </template>
        </el-table-column>
        <el-table-column prop="time" label="上课时间" width="120"></el-table-column>
        <el-table-column prop="teacherName" label="任课教师" width="100"></el-table-column>
        <el-table-column prop="selected,total" label="已选/总数" width="80">
          <template slot-scope="scope"> {{scope.row.selected}}<span>/</span>{{scope.row.total}} </template>
        </el-table-column>
        <el-table-column prop="grade" label="选项" width="100">
            <template slot-scope="scope">
              <el-button size="mini" plain type="primary"
                @click="handleAdd(scope.$index, scope.row)">选课</el-button>
            </template>
        </el-table-column>
      </el-table-column>
    </el-table>
    <el-pagination
    background
    layout="total, sizes, prev, pager, next, jumper"
    :page-size="pageSize"
    :page-sizes="pageSizes"
    :total="totalCount"
    :current-page="currentPage"
    @current-change="handleCurrentChange"
    @size-change="handleSizeChange"
    style="text-align:center">
    </el-pagination>
    
    <!-- 学生已选课程 -->
    <el-table
      :data="selectedCourse"
      v-loading="loading"
      border
      stripe
      style="width: 100%;margin-top: 150px;"
      :header-row-style="{height:'20px'}"
      :header-cell-style="{padding:'4px'}"
      :row-style="{height:'20px'}"
      :cell-style="{padding:'2px'}">
      <el-table-column label="已选课程信息">
        <el-table-column prop="courseno" label="课程编号" width="100">
        </el-table-column>
        <el-table-column prop="type" label="课程类型" width="90">
        </el-table-column>
        <el-table-column prop="courseName" label="课程名" width="220">
        </el-table-column>
        <el-table-column prop="credit" label="学分" width="60">
        </el-table-column>
        <el-table-column prop="hours" label="学时" width="60">
        </el-table-column>
        <el-table-column prop="area,room" label="地点" width="200">
          <template slot-scope="scope"> {{scope.row.area}}{{scope.row.room}} </template>
        </el-table-column>
        <el-table-column prop="time" label="上课时间" width="120"></el-table-column>
        <el-table-column prop="teacherName" label="任课教师" width="100">
        </el-table-column>
        <el-table-column prop="grade" label="选项" width="100">
            <template slot-scope="scope">
              <el-popconfirm
                :title="'确定退选《'+scope.row.courseName+'》吗？'"
                @confirm="handleDelete(scope.$index, scope.row)"
              >
                <el-button size="mini" plain type="danger" slot="reference"
                 >退课
                </el-button>
              </el-popconfirm>
            </template>
        </el-table-column>
      </el-table-column>
    </el-table>

  </div>
</template>

<script>
import {getCookie} from '../global/cookie'
export default {
    data(){
        return{
          selectCrsData: [],
          selectedCourse: [],
          pageSize:15,
          pageSizes: [5,10,15,20],
          currentPage:1,
          totalCount:1,
          loading:false,
          deptSelected: '',
          deptOptions: []
        }
    },
    methods: {
      handleAdd(index,row){
        console.log(index,row)
        this.$axios
        .post('/student/addSelectCourse/', row)
        .then((result)=> {
	        if(result.data.code === 1){
            row.selected++
            alert("选课成功")
            this.getSelectedCourse()
          }else{
            alert(result.data.msg)
          }
        })
        .catch((error)=> {
            alert(error)
        })
      },
      handleDelete(index,row){
        this.$axios
        .post('/student/delSelectCourse/', row )
        .then((result)=> {
	        if(result.data.code === 1){
            row.selected--
            alert("退课成功")
            this.getSelectCrsData()
            this.getSelectedCourse()
          }else{
            alert(result.data.msg)
          }
        })
        .catch((error)=> {
            alert(error)
        })
      },
      handleCurrentChange(val) {
        this.currentPage=val
      },
      handleSizeChange(val) {
        this.pageSize = val
        console.log(`每页 ${val} 条`);
      },
      getDptName(){
        this.$axios
        .post('/admin/getDptName/', {})
        .then((result)=> {
            if (result.data.code === 1) {  // 返回第一页数据，和
              this.deptOptions = result.data.datas
              this.deptOptions.unshift({id:'0',name:'全部'})
              // this.deptSelected = result.data.datas[0].id
            }else{
              return false;
            }
        })
        .catch((error)=> {
            alert(error)
        })
      },
      deptSelect(){
        // if(this.deptSelected == ""){
        //   return
        // }
        // this.getSelectCrsData({dptNo:this.deptSelected})
      },
      getSelectCrsData(params={}){   //获取所有选课数据
        this.$axios
        .post('/student/getNewCourseArrange/', params)
        .then((result)=> {
            if (result.data.code === 1) {
                this.selectCrsData = result.data.datas
                this.totalCount = result.data.datas.length
            }else{
                this.selectCrsData = []
                alert("选课通道未开放")
                return false;
            }
        })
        .catch((error)=> {
            alert(error)
        })
      },
      getSelectedCourse(){   //获取学生本人选课信息
        this.$axios
        .post('/student/getSelectedCourseArrange/', {})
        .then((result)=> {
            if (result.data.code === 1) {
                this.selectedCourse = result.data.datas
            }else{
                this.selectedCourse = []
                return false;
            }
        })
        .catch((error)=> {
            alert(error)
        })
      },
      searchOk(){
        if (this.deptSelected === ''){
          alert('请选择学院')
          return
        }
        this.getSelectCrsData({dptNo:this.deptSelected})
        this.getSelectedCourse()
      }
    },
    created:function(){
      this.getDptName()
      // this.getSelectCrsData()
      this.getSelectedCourse()
    }
}
</script>