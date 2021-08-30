// 全局变量
const globalObj = {}

// 定义公共方法  vue页面应用   let flag = this.$common.checkIP(ip)

/**
 * 防抖
 * @param {Function} 执行函数
 * @param {Number} delay 延时ms
 */
let _debounceTimeout
globalObj.debounce = function (fn, delay=500) {
	clearTimeout(_debounceTimeout);
	_debounceTimeout = setTimeout(() => {
		fn();
	}, delay);
}
/**
 * 节流
 * @param {Function} 执行函数
 * @param {Number} delay 延时ms
 */
let _throttleRunning = false
globalObj.throttle = function (fn, delay=500) {
	if(_throttleRunning){
		return;
	}
	_throttleRunning = true;
	fn();
	setTimeout(() => {
	    _throttleRunning = false;
	}, delay);
}

/**
 * 检测IP格式是否正确
 * @param ip
 * @return boolean
 */
globalObj.checkIP = function (ip) {
  let pattern = new RegExp(/^((([1-9])|((0[1-9])|([1-9][0-9]))|((00[1-9])|(0[1-9][0-9])|((1[0-9]{2})|(2[0-4][0-9])|(25[0-5]))))\.)((([0-9]{1,2})|(([0-1][0-9]{2})|(2[0-4][0-9])|(25[0-5])))\.){2}(([1-9])|((0[1-9])|([1-9][0-9]))|(00[1-9])|(0[1-9][0-9])|((1[0-9]{2})|(2[0-4][0-9])|(25[0-5])))$/i)
  return pattern.test(ip)
}

/**
 * 判断URL是否合法
 * @param url 链接地址
 * @return boolean
 */
globalObj.checkUrl = function (url) {
  const pattern = /^(?:http(s)?:\/\/)?[\w.-]+(?:\.[\w\.-]+)+[\w\-\._~:/?#[\]@!\$&'\*\+,;=.]+$/
  return pattern.test(url)
}

/**
 * 获取系统时间
 * @param
 * @return 2021-01-14 14:18:56
 */
globalObj.getNowTime = function () {
  let d = new Date()
  let year = d.getFullYear()
  let month = ('0' + (d.getMonth() + 1)).slice('-2')
  let date = ('0' + d.getDate()).slice('-2')
  let hour = ('0' + d.getHours()).slice('-2')
  let minute = ('0' + d.getMinutes()).slice('-2')
  let second = ('0' + d.getSeconds()).slice('-2')
  let time = year + '-' + month + '-' + date + ' ' + hour + ':' + minute + ':' + second
  return time
}

/**
 * 时间相加处理函数
 * @param date 需要计算的时间(xxxx-xx-xx)
 * @param plusDays 要加的天数(整数)
 * @return xxxx-xx-xx 00:00:00
 */
globalObj.calcuDate = function (date, plusDays) {
  var dateArray = date.split('/')
  var year = +dateArray[0]
  var month = +dateArray[1]
  var day = +dateArray[2]
  var oriDay = day
  var secondMonthDays = ((year % 4 === 0 && year % 100 !== 0) || year % 400 === 0) ? 29 : 28
  while (plusDays > 0) {
    oriDay = day
    day += Number(plusDays)
    switch (month) {
      case 4:
      case 6:
      case 9:
      case 11:
        if (day > 30) {
          plusDays -= (30 - oriDay) + 1
          month++
          day = 1
        } else {
          plusDays = 0
        }
        break
      case 2:
        if (day > secondMonthDays) {
          plusDays -= (secondMonthDays - oriDay) + 1
          month++
          day = 1
        } else {
          plusDays = 0
        }
        break
      default:
        if (day > 31) {
          plusDays -= (31 - oriDay) + 1
          day = 1
          month++
        } else {
          plusDays = 0
        }
    }
    if (month > 12) {
      month = 1
      year++
    }
  }
  return year + '-' + month + '-' + day + ' ' + '00:00:00'
}

/**
 * 数组值相加
 * @param arr 数组
 * @return int
 */
globalObj.getSum = function (arr) {
  let sum = 0
  for (let i = 0, len = arr.length; i < len; i++) {
    sum += arr[i]
  }
  return sum
}

/**
 * 密级位掩码
 * @param int 19
 * @return [] 1,2,16
 */
globalObj.getLockData = function (x) {
  let arr = []
  let i = 0
  while (Math.pow(2, i++) <= x) {
  }
  i -= 2
  arr.push(Math.pow(2, i))
  x -= Math.pow(2, i)
  while (Math.pow(2, --i) >= 1) {
    if (Math.pow(2, i) <= x) {
      arr.push(Math.pow(2, i))
      x -= Math.pow(2, i)
    }
  }
  return arr.reverse()
}

/**
 * 导出Excel表
 * @param tHeader, tHeaderKey, jsonData, filename
 * tHeader = ['日期', '文件编号', '回执编号', '上传服务厅', '下载服务厅', '上传时间', '办理时间', '回执时间', '下载时间'] // 导出的表头名信息
 * tHeaderKey = ['date', 'prt_prev', 'file_no', 'upcname', 'download_cname', 'uptime', 'optime', 'retime', 'downtime'] // 导出的表头字段名，需要导出表格字段名,对应Json数据字段名
 * jsonData = this.businessLogList // 你要格式化的Json数据。
 * filename 导出的Excel文件名称
 */
import {export_json_to_excel} from '../excel/Export2Excel.js'

globalObj.export2ExcelFile = function (tHeader, tHeaderKey, jsonData, filename) {
  require.ensure([], () => {
    // console.log(tHeader, data, filename)
    // const {export_json_to_excel} = require('../excel/export2Excel') // 这里必须使用绝对路径，使用@/+存放export2Excel的路径
    let data = globalObj.formatJson(tHeaderKey, jsonData)
    console.log(data)
    export_json_to_excel({
      header: tHeader,
      data,
      filename
    }) // 导出的表格名称，根据需要自己命名
  })
},
/**
 * 格式转换，将json数据转换为excel表数据
 * @param tHeader, data, filename
 * @return Excel文件
 */
globalObj.formatJson = function (filterVal, jsonData) {
  return jsonData.map(v => filterVal.map(j => v[j]))
}
// 数据写入excel    原型
// export2Excel (tHeader, data, filename) {
//   require.ensure([], () => {
//     // console.log(tHeader, data, filename)
//     // const {export_json_to_excel} = require('../excel/export2Excel') // 这里必须使用绝对路径，使用@/+存放export2Excel的路径

//     console.log(data)

//     export_json_to_excel({
//       header: tHeader,
//       data,
//       filename
//     }) // 导出的表格名称，根据需要自己命名
//   })
// },
// // 格式转换，直接复制即可
// formatJson (filterVal, jsonData) {
//   return jsonData.map(v => filterVal.map(j => v[j]))
// }

/**
 * 判断类型集合
 * @param str, type
 * @return boolean
 */
globalObj.checkStr = function (str, type) {
  switch (type) {
    case 'stuNo': //学生编号
      return /([a-zA-Z0-9]){10}$/.test(str)
      case 'teaNo': //教师编号
        return /([a-zA-Z0-9]){8}$/.test(str)
    case 'classNo': //班级编号
      return /([a-zA-Z0-9]){2}$/.test(str)
    case 'mobile': //手机号码
      return /^1[3|4|5|6|7|8|9][0-9]{9}$/.test(str)
    case 'tel': //座机
      return /^(0\d{2,3}-\d{7,8})(-\d{1,4})?$/.test(str)
    case 'card': //身份证
      return /(^\d{15}$)|(^\d{18}$)|(^\d{17}(\d|X|x)$)/.test(str)
    case 'mobileCode': //6位数字验证码
      return /^[0-9]{6}$/.test(str)
    case 'pwd': //密码以字母开头，长度在6~18之间，只能包含字母、数字和下划线
      return /^([a-zA-Z0-9_]){6,18}$/.test(str)
    case 'payPwd': //支付密码 6位纯数字
      return /^[0-9]{6}$/.test(str)
    case 'postal': //邮政编码
      return /[1-9]\d{5}(?!\d)/.test(str)
    case 'QQ': //QQ号
      return /^[1-9][0-9]{4,9}$/.test(str)
    case 'email': //邮箱
      return /^[\w-]+(\.[\w-]+)*@[\w-]+(\.[\w-]+)+$/.test(str)
    case 'money': //金额(小数点2位)
      return /^\d*(?:\.\d{0,2})?$/.test(str)
    case 'URL': //网址
      return /(http|ftp|https):\/\/[\w\-_]+(\.[\w\-_]+)+([\w\-\.,@?^=%&:/~\+#]*[\w\-\@?^=%&/~\+#])?/.test(str)
    case 'IP': //IP
      return /((?:(?:25[0-5]|2[0-4]\\d|[01]?\\d?\\d)\\.){3}(?:25[0-5]|2[0-4]\\d|[01]?\\d?\\d))/.test(str)
    case 'date': //日期时间
      return /^(\d{4})\-(\d{2})\-(\d{2}) (\d{2})(?:\:\d{2}|:(\d{2}):(\d{2}))$/.test(str) || /^(\d{4})\-(\d{2})\-(\d{2})$/
        .test(str)
    case 'number': //数字
      return /^[0-9]$/.test(str)
    case 'english': //英文
      return /^[a-zA-Z]+$/.test(str)
    case 'chinese': //中文
      return /^[\\u4E00-\\u9FA5]+$/.test(str)
    case 'lower': //小写
      return /^[a-z]+$/.test(str)
    case 'upper': //大写
      return /^[A-Z]+$/.test(str)
    case 'HTML': //HTML标记
      return /<("[^"]*"|'[^']*'|[^'">])*>/.test(str)
    default:
      return true
  }
}

/**
 * 去除空格
 * @param value
 * @return boolean
 */
globalObj.delSpace = function(value){
    return value.replace(/\s*/g, '')
}

export default globalObj
