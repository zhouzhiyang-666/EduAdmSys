import Vue from 'vue'
import Router from 'vue-router'
import Login from '@/components/login/LoginUser'
import Forgot from '@/components/login/Forgot'
import LoginAdmin from '@/components/login/LoginAdmin'
import Student from '@/components/student/Student'
import Header from '@/components/common/Header'
import StuTermSchedule from '@/components/student/StuTermSchedule'
import StuRoomCourse from '@/components/student/StuRoomCourse'
import StuScore from '@/components/student/StuScore'
import StuSelectCourse from '@/components/student/StuSelectCourse'
import StuSelf from '@/components/student/StuSelf'
import StuRePwd from '@/components/student/StuRePwd'
import StuRePhone from '@/components/student/StuRePhone'

import TeaRePhone from '@/components/teacher/TeaRePhone'
import TeaRePwd from '@/components/teacher/TeaRePwd'
import TeaSelf from '@/components/teacher/TeaSelf'
import TeaTask from '@/components/teacher/TeaTask'
import TeaStuInfo from '@/components/teacher/TeaStuInfo'
import TeaRoomCourse from '@/components/teacher/TeaRoomCourse'
import TeaTermSchedule from '@/components/teacher/TeaTermSchedule'
import Teacher from '@/components/teacher/Teacher.vue'

import AdmStuFiles from '@/components/admin/StuFiles'
import AdmTeaFiles from '@/components/admin/TeaFiles'
import CourseManage from '@/components/admin/CourseManage'
import ClassManage from '@/components/admin/ClassManage'
import CourseArrange from '@/components/admin/CourseArrange'
import AdmRePwd from '@/components/admin/AdmRePwd'
import AdmRePhone from '@/components/admin/AdmRePhone'
import Empower from '@/components/admin/Empower'
import Admin from '@/components/admin/Admin.vue'

Vue.use(Router)

export default new Router({
  mode:'history',
    routes: [
      {
        path: '/',
        redirect: '/login'
      },
        {
          path: '/login',
          component: Login,
          meta:{
            keepalive:false,
            requireAuth: false
          }
        },
        {
          path:'/loginAdmin',
          component:LoginAdmin,
          meta:{
            keepalive:false,
            requireAuth: false
          }
        },{
          path:'/header',
          component:Header,
          meta:{
            keepalive:false
          }
        },
        {
          path:'/forgot',
          name:'forgot',
          component:Forgot
        },
        {
          path: '/Student',
          component: Student,
          meta:{
            keepalive: false,
            requireAuth: true
          },
          children:[
            {
              path:'/StuTermSchedule',
              component:StuTermSchedule,
              meta:{
                requireAuth: true
              }
            },
            {
              path:'/StuRoomCourse',
              component:StuRoomCourse,
              meta:{
                requireAuth: true
              }
            },
            {
              path:'/StuScore',
              component:StuScore,
              meta:{
                requireAuth: true
              }
            },
            {
              path:'/StuSelectCourse',
              component:StuSelectCourse,
              meta:{
                requireAuth: true
              }
            },
            {
              path:'/StuSelf',
              component:StuSelf,
              meta:{
                requireAuth: true
              }
            },
            {
              path:'/StuRePwd',
              component:StuRePwd,
              meta:{
                requireAuth: true
              }
            },
            {
              path:'/StuRePhone',
              component:StuRePhone,
              meta:{
                requireAuth: true
              }
            },
          ]
          
        },{
          path: '/Teacher',
          component: Teacher,
          meta:{
            keepalive: false,
            requireAuth: true
          },
          children:[
            {
              path:'/TeaTermSchedule',
              component:TeaTermSchedule,
              meta:{
                requireAuth: true
              }
            },
            {
              path:'/TeaRoomCourse',
              component:TeaRoomCourse,
              meta:{
                requireAuth: true
              }
            },
            {
              path:'/TeaStuInfo',
              component:TeaStuInfo,
              meta:{
                requireAuth: true
              }
            },
            {
              path:'/TeaTask',
              component:TeaTask,
              meta:{
                requireAuth: true
              }
            },
            {
              path:'/TeaSelf',
              component:TeaSelf,
              meta:{
                requireAuth: true
              }
            },
            {
              path:'/TeaRePwd',
              component:TeaRePwd,
              meta:{
                requireAuth: true
              }
            },
            {
              path:'/TeaRePhone',
              component:TeaRePhone,
              meta:{
                requireAuth: true
              }
            },
          ]
          
        },{
          path: '/Admin',
          name:'/Admin',
          component: Admin,
          meta:{
            keepalive: false,
            requireAuth: true
          },
          children:[
            {
              path:'/AdmStuFiles',
              // name:'/AdmStuFiles',
              component:AdmStuFiles,
              meta:{
                requireAuth: true
              }
            },
            {
              path:'/AdmTeaFiles',
              component:AdmTeaFiles,
              meta:{
                requireAuth: true
              }
            },
            {
              path:'/CourseManage',
              component:CourseManage,
              meta:{
                requireAuth: true
              }
            },{
              path:'/ClassManage',
              component:ClassManage,
              meta:{
                requireAuth: true
              }
            },
            {
              path:'/CourseArrange',
              component:CourseArrange,
              meta:{
                requireAuth: true
              }
            },
            {
              path:'/AdmRePwd',
              component:AdmRePwd,
              meta:{
                requireAuth: true
              }
            },
            {
              path:'/AdmRePhone',
              component:AdmRePhone,
              meta:{
                requireAuth: true
              }
            },
            {
              path:'/Empower',
              component:Empower,
              meta:{
                requireAuth: true
              }
            }
          ]
          
        },
        {
          path: '/403',
          // name: 'Page403',
          component: () => import('@/components/common/403'),
          meta: {
            requireAuth: false
          }
        },
        {
          path: '/404',
          // name: 'Page404',
          component: () => import('@/components/common/404'),
          meta: {
            requireAuth: false
          }
        },
        {
          path: '*',
          // name: 'redirect',
          redirect: '/404'
        }
      ]
});