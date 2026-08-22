import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import DashboardView from '../views/DashboardView.vue'
import ProjectView from '../views/ProjectView.vue'
import DatabaseView from '../views/DatabaseView.vue'
import SecurityView from '../views/SecurityView.vue'
import ResourceView from '../views/ResourceView.vue'
import MonthlyView from '../views/MonthlyView.vue'

const routes = [
  { path: '/login', name: 'login', component: LoginView, meta: { public: true, title: '登录' } },
  { path: '/', name: 'dashboard', component: DashboardView, meta: { title: '首页' } },
  { path: '/projects', name: 'projects', component: ProjectView, meta: { title: '项目概览' } },
  { path: '/database', name: 'database', component: DatabaseView, meta: { title: '数据库管理' } },
  { path: '/security', name: 'security', component: SecurityView, meta: { title: '安全审批概览' } },
  { path: '/resources', name: 'resources', component: ResourceView, meta: { title: '资源管理' } },
  { path: '/monthly', name: 'monthly', component: MonthlyView, meta: { title: '杂项 · 月报' } },
  { path: '/:pathMatch(.*)*', redirect: '/' },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior: () => ({ top: 0 }),
})

router.beforeEach((to) => {
  document.title = `${to.meta.title ?? '运维报告中心'} · 运维报告中心`
  return true
})

export default router
