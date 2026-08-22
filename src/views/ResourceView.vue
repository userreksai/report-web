<script setup>
import { computed, ref } from 'vue'
import {
  Banknote,
  BadgeDollarSign,
  Boxes,
  CircleDollarSign,
  Globe2,
  ShieldCheck,
} from '@lucide/vue'
import AppShell from '../components/AppShell.vue'
import DataProvenance from '../components/DataProvenance.vue'
import DataState from '../components/DataState.vue'
import DateRangeFilter from '../components/DateRangeFilter.vue'
import StatCard from '../components/StatCard.vue'
import { useOpsData } from '../composables/useOpsData'

const detailView = ref('summary')
const { data, meta, loading, error, empty, reload } = useOpsData('resources', () => ({ view: detailView.value }))
const summary = computed(() => data.value?.summary || {})
const expenses = computed(() => data.value?.project_expenses || [])
const breakdown = computed(() => data.value?.expense_breakdown || {})
const budgetUsage = computed(() => summary.value.annual_budget ? (summary.value.total_expense / summary.value.annual_budget) * 100 : 0)
const breakdownTotal = computed(() => Object.values(breakdown.value).reduce((sum, value) => sum + Number(value || 0), 0))
const share = (value) => breakdownTotal.value ? (Number(value || 0) / breakdownTotal.value) * 100 : 0
const ringStyle = computed(() => {
  const cloud = share(breakdown.value.cloud_resource)
  const project = cloud + share(breakdown.value.project_investment)
  const security = project + share(breakdown.value.security_service)
  return { background: `radial-gradient(circle, var(--surface) 55%, transparent 57%), conic-gradient(var(--primary) 0 ${cloud}%, var(--info) ${cloud}% ${project}%, var(--success) ${project}% ${security}%, var(--border-strong) ${security}% 100%)` }
})

const money = (value) => `¥${new Intl.NumberFormat('zh-CN', { maximumFractionDigits: 0 }).format(value || 0)}`
const number = (value) => new Intl.NumberFormat('zh-CN').format(value || 0)
const tone = (usage) => usage >= 90 ? 'danger' : usage >= 70 ? 'warning' : usage <= 30 ? 'success' : 'primary'
</script>

<template>
  <AppShell title="资源管理">
    <div class="page">
      <header class="page-heading">
        <div>
          <p class="page-eyebrow">Resource & Cost</p>
          <h1 class="page-title">资源管理</h1>
          <p class="page-description">查看资产投入、预算消耗与项目费用，提前识别超支风险。</p>
        </div>
        <span class="status-pill success">资源接口已连接</span>
      </header>

      <DateRangeFilter />
      <DataProvenance :meta="meta" />

      <DataState :loading="loading" :error="error" :empty="empty" @retry="reload">
        <section class="metrics-grid">
          <StatCard label="费用续费" :value="money(summary.renewal_expense)" helper="区间实际发生额" trend="按业务日求和" trend-type="flat" :icon="CircleDollarSign" />
          <StatCard label="证书续期" :value="number(summary.certificate_renewals)" :helper="`${number(summary.expiring_certificates_30d)} 项 30 天内到期`" trend="到期数取最新快照" trend-type="flat" tone="warning" :icon="ShieldCheck" />
          <StatCard label="域名购买" :value="money(summary.domain_purchase_expense)" :helper="`共管理 ${number(summary.managed_domains)} 个域名`" trend="存量取最新快照" trend-type="flat" :icon="Globe2" />
          <StatCard label="资源预算使用" :value="`${budgetUsage.toFixed(1)}%`" :helper="`年度预算 ${money(summary.annual_budget)}`" trend="区间支出/年度预算" trend-type="flat" tone="success" :icon="BadgeDollarSign" />
        </section>

        <section class="panel expense-panel">
        <div class="section-heading">
          <div><h2 class="section-title">项目费用汇总</h2><p class="section-subtitle">Project Expense Summary · 按当前预算使用率排序</p></div>
          <button class="secondary-button" @click="detailView = detailView === 'all' ? 'summary' : 'all'">{{ detailView === 'all' ? '收起列表' : `查看全部（${data.project_expense_total || 0}）` }}</button>
        </div>
        <div class="table-wrap">
          <table class="data-table expense-table">
            <thead><tr><th>项目名称</th><th>负责团队</th><th>费用类型</th><th>预算使用率</th><th>总成本（¥）</th></tr></thead>
            <tbody>
              <tr v-for="item in expenses" :key="item.name">
                <td>{{ item.name }}</td>
                <td>{{ item.team }}</td>
                <td><span class="category-chip">{{ item.category }}</span></td>
                <td>
                  <div class="budget-cell">
                    <div class="progress-track"><div class="progress-bar" :class="tone(item.budget_usage)" :style="{ width: `${Math.min(item.budget_usage, 100)}%` }" /></div>
                    <b class="data-value">{{ Number(item.budget_usage).toFixed(1) }}%</b>
                  </div>
                </td>
                <td class="data-value cost-value">{{ number(item.cost) }}</td>
              </tr>
            </tbody>
          </table>
          <div v-if="!expenses.length" class="empty-note">当前范围没有项目费用明细</div>
        </div>
      </section>

      <section class="panel composition-panel">
          <div class="section-heading">
            <div><h2 class="section-title">费用构成</h2><p class="section-subtitle">本周期总支出 {{ money(summary.total_expense) }}</p></div>
            <Banknote :size="19" class="primary-icon" />
          </div>
          <div class="composition-content">
            <div class="composition-ring" :style="ringStyle"><strong class="data-value">{{ (summary.total_expense / 10000 || 0).toFixed(1) }}</strong><small>万元</small></div>
            <div class="legend-list">
              <div><span><i class="cloud" />云资源</span><b class="data-value">{{ share(breakdown.cloud_resource).toFixed(1) }}%</b></div>
              <div><span><i class="project" />项目投入</span><b class="data-value">{{ share(breakdown.project_investment).toFixed(1) }}%</b></div>
              <div><span><i class="security" />安全服务</span><b class="data-value">{{ share(breakdown.security_service).toFixed(1) }}%</b></div>
              <div><span><i class="other" />其他</span><b class="data-value">{{ share(breakdown.other).toFixed(1) }}%</b></div>
            </div>
          </div>
      </section>
      </DataState>
    </div>
  </AppShell>
</template>

<style scoped>
.expense-table th:nth-child(4),
.expense-table td:nth-child(4) {
  width: 260px;
}

.category-chip {
  display: inline-flex;
  padding: 3px 8px;
  color: var(--text-soft);
  background: rgba(157, 176, 189, 0.06);
  border: 1px solid var(--border);
  border-radius: 4px;
  font-size: 10px;
}

.budget-cell {
  display: flex;
  align-items: center;
  gap: 10px;
}

.budget-cell .progress-track {
  flex: 1;
}

.budget-cell b {
  min-width: 34px;
  font-size: 10px;
}

.progress-bar.danger {
  background: var(--danger);
}

.progress-bar.warning {
  background: var(--warning);
}

.progress-bar.success {
  background: var(--success);
}

.cost-value {
  color: var(--text) !important;
  text-align: right;
}

.primary-icon {
  color: var(--primary);
}

.composition-content {
  display: grid;
  align-items: center;
  gap: 24px;
  grid-template-columns: auto 1fr;
}

.composition-ring {
  display: grid;
  width: 136px;
  height: 136px;
  align-content: center;
  background:
    radial-gradient(circle, var(--surface) 55%, transparent 57%),
    conic-gradient(var(--primary) 0 46%, var(--info) 46% 77%, var(--success) 77% 92%, var(--border-strong) 92% 100%);
  border-radius: 50%;
  text-align: center;
}

.composition-ring strong {
  font-size: 25px;
}

.composition-ring small {
  color: var(--text-muted);
  font-size: 9px;
}

.legend-list {
  display: grid;
}

.legend-list > div {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 9px 0;
  border-top: 1px solid var(--border);
}

.legend-list > div:first-child {
  border-top: 0;
}

.legend-list span {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  color: var(--text-soft);
  font-size: 10px;
}

.legend-list i {
  width: 8px;
  height: 8px;
  background: var(--primary);
  border-radius: 2px;
}

.legend-list i.project { background: var(--info); }
.legend-list i.security { background: var(--success); }
.legend-list i.other { background: var(--border-strong); }

.legend-list b {
  font-size: 10px;
}

@media (max-width: 760px) {
  .composition-content {
    grid-template-columns: 1fr;
    justify-items: center;
  }

  .legend-list {
    width: 100%;
  }
}

</style>
