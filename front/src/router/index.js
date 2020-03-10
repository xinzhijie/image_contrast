import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'
import upload from '@/components/upload'
import contrast from '@/components/contrast'
import login from '@/components/login'
import adminIndex from '@/components/index_admin'
import download from '@/components/download'
import userManage from '@/components/user_manage'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'HelloWorld',
      component: HelloWorld
    },
    {
      path: '/login',
      name: 'login',
      component: login
    },
    {
      path: '/adminIndex',
      name: 'adminIndex',
      component: adminIndex
    },
    {
      path: '/userManage',
      name: 'userManage',
      component: adminIndex,
      children: [{
        path: '/userManage',
        name: 'userManage',
        component: userManage
      }]
    },
    {
      path: '/upload',
      name: 'upload',
      component: adminIndex,
      children: [{
        path: '/upload',
        name: 'upload',
        component: upload
      }]
    },
    {
      path: '/download',
      name: 'download',
      component: HelloWorld,
      children: [{
        path: '/download',
        name: 'download',
        component: download
      }]
    },
    {
      path: '/contrast',
      name: 'contrast',
      component: HelloWorld,
      children: [{
        path: '/contrast',
        name: 'contrast',
        component: contrast
      }]
    }

  ]
})
