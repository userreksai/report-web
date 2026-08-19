<script setup>
import {
  Banknote,
  BadgeDollarSign,
  Boxes,
  CalendarClock,
  CircleDollarSign,
  CloudCog,
  Globe2,
  Network,
  ShieldCheck,
} from '@lucide/vue'
import AppShell from '../components/AppShell.vue'
import DateRangeFilter from '../components/DateRangeFilter.vue'
import StatCard from '../components/StatCard.vue'

const expenses = [
  { name: '核心数据库迁移', team: '基础设施部', category: '云资源', progress: 92, cost: '342,000', tone: 'danger' },
  { name: 'Nexus 前端重构', team: '研发一部', category: '研发项目', progress: 45, cost: '128,500', tone: 'primary' },
  { name: '年度安全审计', team: '安全合规部', category: '安全服务', progress: 15, cost: '45,000', tone: 'success' },
  { name: '海外 CDN 扩展', team: '网络工程部', category: '网络资源', progress: 68, cost: '210,800', tone: 'warning' },
  { name: '日志平台扩容', team: 'SRE 团队', category: '云资源', progress: 57, cost: '98,600', tone: 'primary' },
]

const renewals = [
  { name: '*.internal.example.com', type: 'SSL 证书', due: '14 天', price: '¥2,800', tone: 'danger' },
  { name: 'report.example.com', type: '域名', due: '28 天', price: '¥380', tone: 'warning' },
  { name: '海外 CDN 套餐', type: '云资源', due: '36 天', price: '¥18,600', tone: 'warning' },
  { name: '堡垒机服务', type: '安全服务', due: '62 天', price: '¥24,000', tone: 'success' },
]
</script>

<template>
  <AppShell title="资源管理">
    <div class="page">
      <header class="page-heading">
        <div>
          <p class="page-eyebrow">Resource & Cost</p>
          <h1 class="page-title">资源管理</h1>
          <p class="page-description">查看资产新增、续期提醒、预算消耗与项目费用，提前识别超支风险。</p>
        </div>
        <span class="status-pill warning">2 项即将到期</span>
      </header>

      <DateRangeFilter />

      <section class="metrics-grid">
        <StatCard label="费用续费" value="¥45,200" helper="本月预计支出" trend="6.8%" trend-type="down" :icon="CircleDollarSign" />
        <StatCard label="证书续期" value="14" helper="2 项 30 天内到期" trend="2 项" tone="warning" :icon="ShieldCheck" />
        <StatCard label="域名购买" value="¥8,450" helper="共管理 42 个域名" trend="3 个" :icon="Globe2" />
        <StatCard label="资源预算使用" value="68.4%" helper="年度预算 ¥2.8M" trend="4.2%" tone="success" :icon="BadgeDollarSign" />
      </section>

      <section class="panel expense-panel">
        <div class="section-heading">
          <div><h2 class="section-title">项目费用汇总</h2><p class="section-subtitle">Project Expense Summary · 按当前预算使用率排序</p></div>
          <button class="secondary-button">导出明细</button>
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
                    <div class="progress-track"><div class="progress-bar" :class="item.tone" :style="{ width: `${item.progress}%` }" /></div>
                    <b class="data-value">{{ item.progress }}%</b>
                  </div>
                </td>
                <td class="data-value cost-value">{{ item.cost }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <section class="split-grid resource-bottom">
        <article class="panel">
          <div class="section-heading">
            <div><h2 class="section-title">续期提醒</h2><p class="section-subtitle">未来 90 天内到期项目</p></div>
            <CalendarClock :size="19" class="warning-icon" />
          </div>
          <div class="renewal-list">
            <article v-for="item in renewals" :key="item.name" class="renewal-row">
              <span class="renewal-icon">
                <ShieldCheck v-if="item.type === 'SSL 证书'" :size="17" />
                <Globe2 v-else-if="item.type === '域名'" :size="17" />
                <CloudCog v-else-if="item.type === '云资源'" :size="17" />
                <Network v-else :size="17" />
              </span>
              <div><strong>{{ item.name }}</strong><small>{{ item.type }}</small></div>
              <span class="status-pill" :class="item.tone">{{ item.due }}</span>
              <b class="data-value">{{ item.price }}</b>
            </article>
          </div>
        </article>

        <article class="panel composition-panel">
          <div class="section-heading">
            <div><h2 class="section-title">费用构成</h2><p class="section-subtitle">本周期总支出 ¥824,900</p></div>
            <Banknote :size="19" class="primary-icon" />
          </div>
          <div class="composition-content">
            <div class="composition-ring"><strong class="data-value">82.5</strong><small>万元</small></div>
            <div class="legend-list">
              <div><span><i class="cloud" />云资源</span><b class="data-value">46%</b></div>
              <div><span><i class="project" />项目投入</span><b class="data-value">31%</b></div>
              <div><span><i class="security" />安全服务</span><b class="data-value">15%</b></div>
              <div><span><i class="other" />其他</span><b class="data-value">8%</b></div>
            </div>
          </div>
        </article>
      </section>
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

.warning-icon {
  color: var(--warning);
}

.primary-icon {
  color: var(--primary);
}

.renewal-list {
  display: grid;
}

.renewal-row {
  display: grid;
  min-height: 61px;
  align-items: center;
  gap: 11px;
  border-top: 1px solid var(--border);
  grid-template-columns: auto minmax(0, 1fr) auto auto;
}

.renewal-row:first-child {
  border-top: 0;
}

.renewal-icon {
  display: grid;
  width: 31px;
  height: 31px;
  color: var(--primary);
  background: var(--primary-soft);
  border-radius: 7px;
  place-items: center;
}

.renewal-row > div {
  display: grid;
  min-width: 0;
}

.renewal-row strong {
  overflow: hidden;
  font-size: 11px;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.renewal-row small {
  color: var(--text-muted);
  font-size: 9px;
}

.renewal-row > b {
  font-size: 10px;
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

@media (max-width: 520px) {
  .renewal-row {
    grid-template-columns: auto minmax(0, 1fr) auto;
  }

  .renewal-row .status-pill {
    display: none;
  }
}
</style>
