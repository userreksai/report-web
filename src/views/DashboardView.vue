<script setup>
import { computed } from 'vue'
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
import DataProvenance from '../components/DataProvenance.vue'
import DataState from '../components/DataState.vue'
import StatCard from '../components/StatCard.vue'
import { useOpsData } from '../composables/useOpsData'

const { data, meta, loading, error, empty, reload } = useOpsData('dashboard')
const projects = computed(() => data.value?.projects || {})
const database = computed(() => data.value?.database || {})
const security = computed(() => data.value?.security || {})
const resources = computed(() => data.value?.resources || {})

const number = (value) => new Intl.NumberFormat('zh-CN').format(value || 0)
const money = (value) => `¥${new Intl.NumberFormat('zh-CN', { maximumFractionDigits: 0 }).format(value || 0)}`
const percent = (value) => `${Number(value || 0).toFixed(1)}%`
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
        <span class="status-pill success">实时接口汇总</span>
      </header>

      <DateRangeFilter />
      <DataProvenance :meta="meta" />

      <DataState :loading="loading" :error="error" :empty="empty" @retry="reload">
        <section class="metrics-grid">
          <StatCard label="项目工作项" :value="number(projects.jira_total)" :helper="`本周期已完成 ${number(projects.jira_completed)} 项`" :trend="percent(projects.completion_rate)" trend-type="flat" :icon="TicketCheck" />
          <StatCard label="Archery 工单" :value="number(database.archery_tickets)" helper="区间新增工单" :trend="`${number(database.slow_sql_total)} 条慢 SQL`" trend-type="flat" :icon="FileClock" />
          <StatCard label="Lark 安全审批" :value="number(security.completed_approvals)" helper="已完成审批数量" trend="仅统计完成" trend-type="flat" tone="success" :icon="ShieldCheck" />
          <StatCard label="支出费用" :value="money(resources.total_expense)" helper="本周期费用总额" trend="区间发生额" trend-type="flat" :icon="CircleDollarSign" />
        </section>

        <section class="dashboard-grid domain-grid">
          <article class="domain-card project-card">
            <div class="domain-heading">
              <span><TicketCheck :size="21" /></span>
              <div><p>项目管理</p><strong>工作项交付</strong></div>
              <b class="data-value">{{ number(projects.jira_total) }}</b>
            </div>
            <div class="domain-detail"><span>周期完成率</span><strong class="data-value">{{ percent(projects.completion_rate) }}</strong></div>
            <div class="progress-track"><div class="progress-bar" :style="{ width: `${Math.min(projects.completion_rate || 0, 100)}%` }" /></div>
            <RouterLink to="/projects">查看项目概览 <ArrowRight :size="15" /></RouterLink>
          </article>

          <article class="domain-card db-card">
            <div class="domain-heading"><span><Database :size="21" /></span><div><p>数据库管理</p><strong>区间数据量</strong></div><b class="data-value">2 类</b></div>
            <div class="domain-totals">
              <div><span>Archery 工单</span><strong class="data-value">{{ number(database.archery_tickets) }}</strong></div>
              <div><span>慢 SQL</span><strong class="data-value">{{ number(database.slow_sql_total) }}</strong></div>
            </div>
            <RouterLink to="/database">查看数据库汇总 <ArrowRight :size="15" /></RouterLink>
          </article>

          <article class="domain-card security-card">
            <div class="domain-heading"><span><ShieldCheck :size="21" /></span><div><p>安全审批</p><strong>Lark 已完成审批</strong></div><b class="data-value">{{ number(security.completed_approvals) }}</b></div>
            <div class="single-summary"><span class="status-pill success">仅统计已完成</span></div>
            <RouterLink to="/security">查看安全审批 <ArrowRight :size="15" /></RouterLink>
          </article>

          <article class="domain-card resource-card">
            <div class="domain-heading"><span><PackageCheck :size="21" /></span><div><p>资源管理</p><strong>费用与资产</strong></div><b class="data-value">{{ money(resources.total_expense) }}</b></div>
            <div class="domain-detail"><span>本周期支出费用</span><strong class="data-value">{{ money(resources.total_expense) }}</strong></div>
            <RouterLink to="/resources">查看资源明细 <ArrowRight :size="15" /></RouterLink>
          </article>
        </section>
      </DataState>
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
