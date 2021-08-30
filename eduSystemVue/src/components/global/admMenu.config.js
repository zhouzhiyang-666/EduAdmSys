module.exports = [{
    name: '档案管理',
    id: '1',
    sub: [{
      name: '学生档案',
      componentName: 'AdmStuFiles'
    }, {
      name: '教师档案',
      componentName: 'AdmTeaFiles'
    }]
  }, {
    name: '班级管理',
    id: '2',
    sub: [{
      name: '班级管理',
      componentName: 'ClassManage'
    }]
  },{
    name: '排课',
    id: '3',
    sub: [{
        name: '课程开设',
        componentName: 'CourseManage'
    },{
      name: '选课安排',
      componentName: 'CourseArrange'
    },{
      name: '学生必修课安排(待完善)',
      componentName: 'StuCourseArrange'
    }]
  },{
    name: '个人账号',
    id: '4',
    sub: [{
      name: '修改密码',
      componentName: 'AdmRePwd'
    }, {
        name: '换绑手机号',
        componentName: 'AdmRePhone'
    }]
}]