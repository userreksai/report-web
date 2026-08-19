<script setup>
import {
  BadgeCheck,
  CircleAlert,
  Clock3,
  FileCheck2,
  Fingerprint,
  KeyRound,
  ScanSearch,
  ShieldAlert,
  ShieldCheck,
  UserRoundCheck,
} from '@lucide/vue'
import AppShell from '../components/AppShell.vue'
import DateRangeFilter from '../components/DateRangeFilter.vue'
import StatCard from '../components/StatCard.vue'

const approvals = [
  { id: 'SEC-20260819-041', type: '生产权限申请', applicant: '陈晓', system: '支付中心', time: '15:42', status: '待审批', tone: 'warning' },
  { id: 'SEC-20260819-038', type: '数据导出审批', applicant: '王宁', system: '数据平台', time: '14:18', status: '已通过', tone: 'success' },
  { id: 'SEC-20260819-032', type: '临时账号申请', applicant: '李敏', system: '堡垒机', time: '11:05', status: '已通过', tone: 'success' },
  { id: 'SEC-20260818-126', type: '高危命令审批', applicant: '赵强', system: '容器平台', time: '昨天 18:30', status: '已驳回', tone: 'danger' },
  { id: 'SEC-20260818-119', type: '外部访问申请', applicant: '周桐', system: '工单中心', time: '昨天 16:24', status: '待审批', tone: 'warning' },
]

const risks = [
  { name: '弱口令 / 凭据风险', count: 7, percent: 58, tone: 'danger' },
  { name: '权限范围过大', count: 3, percent: 25, tone: 'warning' },
  { name: '证书临近到期', count: 2, percent: 17, tone: 'primary' },
]
</script>

<template>
  <AppShell title="安全审批概览">
    <div class="page">
      <header class="page-heading">
        <div>
          <p class="page-eyebrow">Security & Compliance</p>
          <h1 class="page-title">安全审批概览</h1>
          <p class="page-description">集中查看审批效率、权限风险与合规状态，减少安全事项积压。</p>
        </div>
        <span class="status-pill success">合规基线正常</span>
      </header>

      <DateRangeFilter />

      <section class="metrics-grid">
        <StatCard label="Lark 审批数量" value="126" helper="本周期全部申请" trend="16.7%" :icon="FileCheck2" />
        <StatCard label="待审批" value="12" helper="3 项已超过 4 小时" trend="2 项" trend-type="down" tone="warning" :icon="Clock3" />
        <StatCard label="平均审批时长" value="1.8h" helper="目标小于 2 小时" trend="0.4h" trend-type="down" tone="success" :icon="UserRoundCheck" />
        <StatCard label="安全风险项" value="12" helper="高风险 2 项" trend="3 项" trend-type="down" tone="danger" :icon="ShieldAlert" />
      </section>

      <section class="split-grid security-grid">
        <article class="panel approval-panel">
          <div class="section-heading">
            <div><h2 class="section-title">最新审批</h2><p class="section-subtitle">按申请时间倒序</p></div>
            <button class="secondary-button">进入审批中心</button>
          </div>
          <div class="table-wrap">
            <table class="data-table approval-table">
              <thead><tr><th>审批编号 / 类型</th><th>申请人</th><th>所属系统</th><th>申请时间</th><th>状态</th></tr></thead>
              <tbody>
                <tr v-for="item in approvals" :key="item.id">
                  <td><span class="approval-id data-value">{{ item.id }}</span><strong>{{ item.type }}</strong></td>
                  <td>{{ item.applicant }}</td>
                  <td>{{ item.system }}</td>
                  <td class="data-value">{{ item.time }}</td>
                  <td><span class="status-pill" :class="item.tone">{{ item.status }}</span></td>
                </tr>
              </tbody>
            </table>
          </div>
        </article>

        <article class="panel risk-panel">
          <div class="section-heading">
            <div><h2 class="section-title">风险分布</h2><p class="section-subtitle">当前未关闭的风险项</p></div>
            <ScanSearch :size="19" class="warning-icon" />
          </div>
          <div class="risk-total">
            <div class="risk-ring"><strong class="data-value">12</strong><small>待整改</small></div>
            <div><strong>风险可控</strong><p>较上周期减少 3 项</p><span class="status-pill success">下降 20%</span></div>
          </div>
          <div class="risk-list">
            <article v-for="risk in risks" :key="risk.name">
              <div><span>{{ risk.name }}</span><b class="data-value">{{ risk.count }}</b></div>
              <div class="progress-track"><div class="progress-bar" :class="risk.tone" :style="{ width: `${risk.percent}%` }" /></div>
            </article>
          </div>
        </article>
      </section>

      <section class="two-columns">
        <article class="panel compact-summary">
          <span class="summary-icon"><Fingerprint :size="20" /></span>
          <div><small>权限复核覆盖率</small><strong class="data-value">96.4%</strong><p>1,284 个账号已完成复核</p></div>
          <BadgeCheck :size="22" class="success-icon" />
        </article>
        <article class="panel compact-summary">
          <span class="summary-icon"><KeyRound :size="20" /></span>
          <div><small>凭据轮换完成率</small><strong class="data-value">88.7%</strong><p>16 个服务凭据待轮换</p></div>
          <CircleAlert :size="22" class="warning-icon" />
        </article>
      </section>
    </div>
  </AppShell>
</template>

<style scoped>
.security-grid {
  grid-template-columns: minmax(0, 1.5fr) minmax(310px, 0.5fr);
}

.approval-id {
  display: block;
  color: var(--primary);
  font-size: 9px;
}

.approval-table td:first-child strong {
  display: block;
  margin-top: 2px;
  font-size: 11px;
}

.approval-table td:nth-child(4) {
  font-size: 10px;
}

.warning-icon {
  color: var(--warning);
}

.success-icon {
  color: var(--success);
}

.risk-total {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 20px;
}

.risk-ring {
  display: grid;
  width: 112px;
  height: 112px;
  flex: 0 0 auto;
  align-content: center;
  background:
    radial-gradient(circle, var(--surface) 56%, transparent 58%),
    conic-gradient(var(--danger) 0 18%, var(--warning) 18% 66%, var(--primary) 66% 100%);
  border-radius: 50%;
  text-align: center;
}

.risk-ring strong {
  font-size: 26px;
}

.risk-ring small {
  color: var(--text-muted);
  font-size: 9px;
}

.risk-total > div:last-child > strong {
  font-size: 13px;
}

.risk-total p {
  margin: 3px 0 10px;
  color: var(--text-muted);
  font-size: 10px;
}

.risk-list {
  display: grid;
  gap: 16px;
}

.risk-list article > div:first-child {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 7px;
  color: var(--text-soft);
  font-size: 10px;
}

.risk-list b {
  color: var(--text);
}

.progress-bar.danger {
  background: var(--danger);
}

.progress-bar.warning {
  background: var(--warning);
}

.compact-summary {
  display: grid;
  align-items: center;
  gap: 15px;
  grid-template-columns: auto 1fr auto;
}

.summary-icon {
  display: grid;
  width: 42px;
  height: 42px;
  color: var(--primary);
  background: var(--primary-soft);
  border-radius: 9px;
  place-items: center;
}

.compact-summary > div {
  display: grid;
}

.compact-summary small,
.compact-summary p {
  color: var(--text-muted);
  font-size: 10px;
}

.compact-summary strong {
  margin: 2px 0;
  font-size: 20px;
}

.compact-summary p {
  margin: 0;
}

@media (max-width: 1100px) {
  .security-grid {
    grid-template-columns: 1fr;
  }
}
</style>
