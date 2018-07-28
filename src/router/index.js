import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/components/Home'
import Dashboard from '@/components/Dashboard'

import MemberList from '@/components/people/memberlist'
import TeacherList from '@/components/people/teacherlist'
import StudentList from '@/components/people/studentlist'

import CourseList from '@/components/course/courselist'
import LessonList from '@/components/course/lessonlist'

import BookingList from '@/components/booking/bookinglist'

import ClassList from '@/components/class/classlist'

import UserList from '@/components/user/list'
import UserChangePwd from '@/components/user/changepwd'
import UserProfile from '@/components/user/profile'

// 懒加载方式，当路由被访问的时候才加载对应组件
const Login = resolve => require(['@/components/Login'], resolve)

Vue.use(Router)

let router = new Router({
// mode: 'history',
  routes: [
    {
      path: '/login',
      name: '登录',
      component: Login
    },
    {
      path: '/',
      name: 'home',
      component: Home,
      redirect: '/dashboard',
      leaf: true, // 只有一个节点
      menuShow: true,
      iconCls: 'iconfont icon-home', // 图标样式class
      children: [
        {path: '/dashboard', component: Dashboard, name: '首页', menuShow: true}
      ]
    },
    /*
    {
      path: '/',
      component: Home,
      name: '用户管理',
      menuShow: true,
      leaf: true, // 只有一个节点
      iconCls: 'iconfont icon-users', // 图标样式class
      children: [
        {path: '/user/list', component: UserList, name: '用户列表', menuShow: true}
      ]
    },
    */
    {
      path: '/',
      component: Home,
      name: '人员管理',
      menuShow: true,
      //leaf: true, // 只有一个节点
      iconCls: 'iconfont icon-users', // 图标样式class
      children: [
        {path: '/people/memberlist', component: MemberList, name: '会员列表', menuShow: true},
        {path: '/people/teacherlist', component: TeacherList, name: '教师列表', menuShow: true},
        {path: '/people/studentlist', component: StudentList, name: '学生列表', menuShow: true}
      ]
    },

    {
      path: '/',
      component: Home,
      name: '班组管理',
      menuShow: true,
      leaf: true, // 只有一个节点
      iconCls: 'iconfont icon-users', // 图标样式class
      children: [
        {path: '/class/classlist', component: ClassList, name: '班组列表', menuShow: true}
      ]
    },


    {
      path: '/',
      component: Home,
      name: '预约管理',
      menuShow: true,
      leaf: true, // 只有一个节点
      iconCls: 'iconfont icon-users', // 图标样式class
      children: [
        {path: '/booking/bookinglist', component: BookingList, name: '预约列表', menuShow: true}
      ]
    },
    {
      path: '/',
      component: Home,
      name: '套餐管理',
      menuShow: true,
      //leaf: true, // 只有一个节点
      iconCls: 'iconfont icon-users', // 图标样式class
      children: [
        {path: '/course/courselist', component: CourseList, name: '套餐列表', menuShow: true},
		    {path: '/course/lessonlist', component: LessonList, name: '课程列表', menuShow: true}
      ]
    },

    {
      path: '/',
      component: Home,
      name: '设置',
      menuShow: true,
      iconCls: 'iconfont icon-setting1',
      children: [
        //{path: '/user/profile', component: UserProfile, name: '个人信息', menuShow: true},
        {path: '/user/changepwd', component: UserChangePwd, name: '修改密码', menuShow: true}
      ]
    }
  ]
})

router.beforeEach((to, from, next) => {
  // console.log('to:' + to.path)
  if (to.path.startsWith('/login')) {
    //window.localStorage.removeItem('access-user')
    window.sessionStorage.removeItem('access-user')
    window.sessionStorage.removeItem('token')
    next()
  } else {
    //let user = JSON.parse(window.localStorage.getItem('access-user'))
    let user = JSON.parse(window.sessionStorage.getItem('access-user'))
    if (!user) {
      next({path: '/login'})
    } else {
      next()
    }
  }
})

export default router
