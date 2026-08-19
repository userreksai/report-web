<script setup>
import {
  Activity,
  AlertTriangle,
  ArrowRight,
  BadgeCheck,
  CircleDotDashed,
  Database,
  FileCheck2,
  Gauge,
  PackageCheck,
  ShieldCheck,
  TicketCheck,
} from '@lucide/vue'
import AppShell from '../components/AppShell.vue'
import DateRangeFilter from '../components/DateRangeFilter.vue'
import StatCard from '../components/StatCard.vue'

const notices = [
  { title: '生产集群容量预警', meta: '数据库 · 10 分钟前', tone: 'warning' },
  { title: 'SSL 证书将在 14 天后到期', meta: '资源 · 1 小时前', tone: 'danger' },
  { title: '季度权限复核已完成', meta: '安全 · 3 小时前', tone: 'success' },
]

const activities = [
  { title: '完成支付服务灰度发布', owner: '陈晓 · 项目管理', time: '14:36' },
  { title: '审批生产库查询工单', owner: '王宁 · DBA', time: '13:20' },
  { title: '更新海外 CDN 资源', owner: '李敏 · 资源管理', time: '11:48' },
  { title: '关闭高危漏洞整改项', owner: '赵强 · 安全中心', time: '09:15' },
]
</script>

<template>
  <AppShell title="首页">
    <div class="page">
      <header class="page-heading">
        <div>
          <p class="page-eyebrow">Operations Overview</p>
          <h1 class="page-title">运维工作数据总览</h1>
          <p class="page-description">汇总当前运维工作量、风险与资源状态，帮助团队快速定位异常。</p>
        </div>
        <span class="status-pill success">数据已于 16:42 更新</span>
      </header>

      <DateRangeFilter />

      <section class="metrics-grid">
        <StatCard label="项目工作项" value="142" helper="本周期已完成 98 项" trend="12.6%" trend-type="up" :icon="TicketCheck" />
        <StatCard label="活动告警" value="12" helper="其中 3 项需要处理" trend="2 项" trend-type="down" tone="warning" :icon="AlertTriangle" />
        <StatCard label="数据库工单" value="24" helper="总计 86 项" trend="8.2%" trend-type="up" tone="success" :icon="Database" />
        <StatCard label="慢 SQL 统计" value="842" helper="生产环境占 60.1%" trend="持平" trend-type="flat" tone="danger" :icon="Gauge" />
      </section>

      <section class="dashboard-grid domain-grid">
        <article class="domain-card project-card">
          <div class="domain-heading">
            <span><TicketCheck :size="21" /></span>
            <div><p>项目管理</p><strong>工作项交付</strong></div>
            <b class="data-value">142</b>
          </div>
          <div class="domain-detail">
            <span>周期完成率</span><strong class="data-value">69%</strong>
          </div>
          <div class="progress-track"><div class="progress-bar" style="width: 69%" /></div>
          <RouterLink to="/projects">查看项目概览 <ArrowRight :size="15" /></RouterLink>
        </article>

        <article class="domain-card db-card">
          <div class="domain-heading">
            <span><Database :size="21" /></span>
            <div><p>数据库管理</p><strong>运行质量</strong></div>
            <b class="data-value">98.7%</b>
          </div>
          <div class="domain-detail"><span>Archery 工单</span><strong class="data-value">24</strong></div>
          <div class="progress-track"><div class="progress-bar" style="width: 84%" /></div>
          <RouterLink to="/database">查看数据库 <ArrowRight :size="15" /></RouterLink>
        </article>

        <article class="domain-card security-card">
          <div class="domain-heading">
            <span><ShieldCheck :size="21" /></span>
            <div><p>安全中心</p><strong>审批与合规</strong></div>
            <b class="data-value">12</b>
          </div>
          <div class="domain-detail"><span>Lark 审批完成</span><strong class="data-value">91%</strong></div>
          <div class="progress-track"><div class="progress-bar" style="width: 91%" /></div>
          <RouterLink to="/security">查看安全审批 <ArrowRight :size="15" /></RouterLink>
        </article>

        <article class="domain-card resource-card">
          <div class="domain-heading">
            <span><PackageCheck :size="21" /></span>
            <div><p>资源管理</p><strong>续费与资产</strong></div>
            <b class="data-value">¥45.2K</b>
          </div>
          <div class="domain-detail"><span>待续期证书</span><strong class="data-value">14</strong></div>
          <div class="progress-track"><div class="progress-bar" style="width: 73%" /></div>
          <RouterLink to="/resources">查看资源明细 <ArrowRight :size="15" /></RouterLink>
        </article>
      </section>

      <section class="split-grid">
        <article class="panel">
          <div class="section-heading">
            <div><h2 class="section-title">近期运维动态</h2><p class="section-subtitle">跨模块最新操作记录</p></div>
            <Activity :size="19" class="heading-icon" />
          </div>
          <div class="activity-list">
            <div v-for="item in activities" :key="item.title" class="activity-item">
              <span class="activity-dot"><CircleDotDashed :size="15" /></span>
              <div><strong>{{ item.title }}</strong><small>{{ item.owner }}</small></div>
              <time class="data-value">{{ item.time }}</time>
            </div>
          </div>
        </article>

        <article class="panel">
          <div class="section-heading">
            <div><h2 class="section-title">需要关注</h2><p class="section-subtitle">按风险优先级排列</p></div>
            <AlertTriangle :size="19" class="heading-icon warning" />
          </div>
          <div class="notice-list">
            <div v-for="notice in notices" :key="notice.title" class="notice-item">
              <span :class="notice.tone">
                <BadgeCheck v-if="notice.tone === 'success'" :size="17" />
                <AlertTriangle v-else :size="17" />
              </span>
              <div><strong>{{ notice.title }}</strong><small>{{ notice.meta }}</small></div>
            </div>
          </div>
        </article>
      </section>
    </div>
  </AppShell>
</template>

<style scoped>
.domain-grid {
  margin-top: 2px;
}

.domain-card {
  padding: 19px;
  background: linear-gradient(145deg, rgba(19, 37, 56, 0.96), rgba(13, 29, 44, 0.98));
  border: 1px solid var(--border);
  border-radius: var(--radius);
}

.domain-heading {
  display: grid;
  grid-template-columns: auto 1fr auto;
  align-items: center;
  gap: 12px;
}

.domain-heading > span {
  display: grid;
  width: 38px;
  height: 38px;
  color: var(--primary);
  background: var(--primary-soft);
  border-radius: 9px;
  place-items: center;
}

.domain-heading p {
  margin: 0;
  color: var(--text-muted);
  font-size: 10px;
}

.domain-heading strong {
  font-size: 13px;
}

.domain-heading b {
  font-size: 19px;
}

.domain-detail {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin: 18px 0 8px;
  color: var(--text-muted);
  font-size: 10px;
}

.domain-detail strong {
  color: var(--text-soft);
}

.domain-card a {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  margin-top: 16px;
  color: var(--text-soft);
  font-size: 11px;
}

.domain-card a:hover {
  color: var(--primary);
}

.heading-icon {
  color: var(--primary);
}

.heading-icon.warning {
  color: var(--warning);
}

.activity-list,
.notice-list {
  display: grid;
}

.activity-item,
.notice-item {
  display: flex;
  min-height: 54px;
  align-items: center;
  gap: 11px;
  border-top: 1px solid var(--border);
}

.activity-item:first-child,
.notice-item:first-child {
  border-top: 0;
}

.activity-dot {
  display: grid;
  width: 30px;
  height: 30px;
  flex: 0 0 auto;
  color: var(--primary);
  background: var(--primary-soft);
  border-radius: 7px;
  place-items: center;
}

.activity-item > div,
.notice-item > div {
  display: grid;
  min-width: 0;
  flex: 1;
}

.activity-item strong,
.notice-item strong {
  overflow: hidden;
  font-size: 12px;
  font-weight: 580;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.activity-item small,
.notice-item small {
  color: var(--text-muted);
  font-size: 10px;
}

.activity-item time {
  color: var(--text-muted);
  font-size: 10px;
}

.notice-item > span {
  display: grid;
  width: 31px;
  height: 31px;
  flex: 0 0 auto;
  border-radius: 7px;
  place-items: center;
}

.notice-item > span.warning {
  color: var(--warning);
  background: rgba(243, 182, 74, 0.09);
}

.notice-item > span.danger {
  color: var(--danger);
  background: rgba(255, 107, 118, 0.09);
}

.notice-item > span.success {
  color: var(--success);
  background: rgba(49, 209, 139, 0.09);
}

@media (max-width: 600px) {
  .domain-heading b {
    font-size: 16px;
  }
}
</style>
