<template>
<div style="width:1101px">
    <div style="margin-bottom: 10px">
        <label>学期：</label>
        <!-- <el-select v-model="termSelected" placeholder="请选择学期" @change="getTermSelected"> -->
        <el-select v-model="termSelected" placeholder="请选择学期" size="small">
        <el-option
        v-for="item in options"
        :key="item.term"
        :label="item.label"
        :value="item.term">
        </el-option>
        </el-select>
        <el-button style="margin-left: 10px;" plain type="primary" size="small" icon="el-icon-search" @click="searchOk">搜索</el-button>
    </div>
    <el-table
    :data="gradeTableData"
    border
    stripe
    style="width: 100%;"
    :row-style="{height:0+'px'}"
    :cell-style="{padding:5+'px'}">
    <el-table-column label="你的学期成绩">
      <el-table-column
        type="index"
        width="50">
      </el-table-column>
      <el-table-column
        prop="id"
        label="课程编号"
        width="100">
      </el-table-column>
      <el-table-column
        prop="type"
        label="课程类型"
        width="200">
      </el-table-column>
      <el-table-column
        prop="credit"
        label="学分"
        width="100">
      </el-table-column>
      <el-table-column
        prop="hours"
        label="学时"
        width="100">
      </el-table-column>
      <el-table-column
        prop="name"
        label="课程名"
        width="230">
      </el-table-column>
      <el-table-column
        prop="score"
        label="成绩"
        width="150">
      </el-table-column>
      <el-table-column prop="tag" label="标签" width="170">
          <template slot-scope="scope">
            <el-tag size="mini"
            :type="(scope.row.score==null)? 'info':(scope.row.score >= 60) ? 'success' : 'danger'"
            disable-transitions>{{(scope.row.score==null)? '未录入':(scope.row.score >= 60)?'合格':'不合格'}}
            </el-tag>
          </template>
      </el-table-column>
    </el-table-column>
  </el-table>
  </div>
</template>

<script>
// import stuGradeTable from '../global/stuGradeTable.js'
import {getCookie} from '../global/cookie'
import termOptions from '../global/termOptions.js'
export default {
    data(){
        return{
            gradeTableData: [],
            options:termOptions,
            termSelected: ''
        }
    },
    methods: {
      getTermSelected(){
        this.$axios
        .post('/student/getScoreTable/', { //获取查询学生学期成绩接口
            term: this.termSelected
        })
        .then((result)=> {
            if (result.data.code === 1) {
                this.gradeTableData = result.data.datas
            } if (result.data.code === -1) {
                this.gradeTableData = []
            }else{
                console.log("查询失败");
                return false;
            }
        })
        .catch((error)=> {
            alert(error)
        })
      },
      searchOk(){ 
        if(this.termSelected == ''){
          alert('请选择学年')
          return
        }
        this.getTermSelected()
      }
    },
    mounted(){
    },
    created(){
      this.options.unshift({
        term: '0',
        label: '全部学年'
      })
    }
}
</script>