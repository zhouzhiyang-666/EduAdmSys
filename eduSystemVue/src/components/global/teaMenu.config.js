module.exports = [{
    name: '课表查询',
    id: '1',
    sub: [{
      name: '学期课表',
      componentName: 'TeaTermSchedule'
    }, {
      name: '教室课表',
      componentName: 'TeaRoomCourse'
    }]
  }, {
    name: '教学班级',
    id: '2',
    sub: [{
      name: '学生信息',
      componentName: 'TeaStuInfo'
    }]
  }, {
    name: '教学任务',
    id: '3',
    sub: [{
      name: '教学任务',
      componentName: 'TeaTask'
    }]
  },{
    name: '个人信息',
    id: '4',
    sub: [{
      name: '个人信息',
      componentName: 'TeaSelf'
    }, {
      name: '修改密码',
      componentName: 'TeaRePwd'
    }, {
        name: '换绑手机号',
        componentName: 'TeaRePhone'
      }]
  }]