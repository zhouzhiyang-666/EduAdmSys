module.exports = [{
    name: '课表查询',
    id: '1',
    sub: [{
      name: '学期课表',
      componentName: 'StuTermSchedule'
    }, {
      name: '教室课表',
      componentName: 'StuRoomCourse'
    }]
  }, {
    name: '成绩查询',
    id: '2',
    sub: [{
      name: '学期成绩',
      componentName: 'StuScore'
    }]
  }, {
    name: '网上选课',
    id: '3',
    sub: [{
      name: '网上选课',
      componentName: 'StuSelectCourse'
    }]
  },{
    name: '个人信息',
    id: '4',
    sub: [{
      name: '个人信息',
      componentName: 'StuSelf'
    }, {
      name: '修改密码',
      componentName: 'StuRePwd'
    }, {
        name: '换绑手机号',
        componentName: 'StuRePhone'
      }]
  }]