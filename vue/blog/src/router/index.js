import Vue from 'vue'
import Router from 'vue-router'
import home from '@/components/home'
import addPage from '@/components/addPage'
import pageList from '@/components/pageList'
import editPage from '@/components/editPage'
import detail from '@/components/detail'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'home',
      component: home
    },
    {
      path: '/home',
      name: 'home',
      component: home
    },
    {
      path: '/pageList',
      name: 'pageList',
      component: pageList
    },
    {
      path: '/addPage',
      name: 'addPage',
      component: addPage
    },
    {
      path: '/editPage/:id',
      name: 'editPage',
      component: editPage
    },
    {
      path: '/detail/:id',
      name: 'detail',
      component: detail
    }
  ]
})
