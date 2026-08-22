<script setup>
import {
  ArrowRight,
  CircleDollarSign,
  Database,
  FileClock,
  PackageCheck,
  ShieldCheck,
  TicketCheck,
} from '@lucide/vue'
import AppShell from '../components/AppShell.vue'
import DateRangeFilter from '../components/DateRangeFilter.vue'
import StatCard from '../components/StatCard.vue'
</script>

<template>
  <AppShell title="首页">
    <div class="page">
      <header class="page-heading">
        <div>
          <p class="page-eyebrow">Operations Overview</p>
          <h1 class="page-title">运维工作数据总览</h1>
          <p class="page-description">汇总项目工作、数据库工单、安全审批与支出费用。</p>
        </div>
        <span class="status-pill success">数据已于 16:42 更新</span>
      </header>

      <DateRangeFilter />

      <section class="metrics-grid">
        <StatCard label="项目工作项" value="142" helper="本周期已完成 98 项" trend="12.6%" trend-type="up" :icon="TicketCheck" />
        <StatCard label="Archery 工单" value="24" helper="已完成" trend="6 项" trend-type="up" :icon="FileClock" />
        <StatCard label="Lark 安全审批" value="12" helper="已完成审批数量" trend="全部完成" trend-type="flat" tone="success" :icon="ShieldCheck" />
        <StatCard label="支出费用" value="¥45,200" helper="本周期费用总额" trend="6.8%" trend-type="down" :icon="CircleDollarSign" />
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
            <div><p>数据库管理</p><strong>数据总量</strong></div>
            <b class="data-value">2 类</b>
          </div>
          <div class="domain-totals">
            <div><span>Archery 工单</span><strong class="data-value">24</strong></div>
            <div><span>慢 SQL</span><strong class="data-value">1,402</strong></div>
          </div>
          <RouterLink to="/database">查看数据库汇总 <ArrowRight :size="15" /></RouterLink>
        </article>

        <article class="domain-card security-card">
          <div class="domain-heading">
            <span><ShieldCheck :size="21" /></span>
            <div><p>安全审批</p><strong>Lark 已完成审批</strong></div>
            <b class="data-value">12</b>
          </div>
          <div class="single-summary"><span class="status-pill success">全部完成</span></div>
          <RouterLink to="/security">查看安全审批 <ArrowRight :size="15" /></RouterLink>
        </article>

        <article class="domain-card resource-card">
          <div class="domain-heading">
            <span><PackageCheck :size="21" /></span>
            <div><p>资源管理</p><strong>费用与资产</strong></div>
            <b class="data-value">¥45.2K</b>
          </div>
          <div class="domain-detail"><span>本周期支出费用</span><strong class="data-value">¥45,200</strong></div>
          <RouterLink to="/resources">查看资源明细 <ArrowRight :size="15" /></RouterLink>
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
  min-height: 37px;
  align-items: center;
  justify-content: space-between;
  margin: 14px 0 6px;
  color: var(--text-muted);
  font-size: 10px;
}

.domain-detail strong {
  color: var(--text-soft);
}

.domain-totals {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 8px;
  margin: 14px 0 0;
}

.domain-totals > div {
  display: grid;
  gap: 3px;
  padding: 9px 10px;
  background: rgba(5, 15, 25, 0.42);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
}

.domain-totals span {
  color: var(--text-muted);
  font-size: 9px;
}

.domain-totals strong {
  font-size: 15px;
}

.single-summary {
  display: flex;
  min-height: 59px;
  align-items: center;
  margin-top: 8px;
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

@media (max-width: 600px) {
  .domain-heading b {
    font-size: 16px;
  }
}
</style>
