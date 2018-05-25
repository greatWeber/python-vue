import Vue from 'vue'
import Router from 'vue-router'
import home from '@/components/home'
import addPage from '@/components/addPage'

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
      path: '/addPage',
      name: 'addPage',
      component: addPage
    },
    {
      path: '/detail/:id',
      name: 'detail',
      component: addPage
    }
  ]
})
