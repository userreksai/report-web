<script setup>
import { BadgeCheck, ShieldCheck } from '@lucide/vue'
import AppShell from '../components/AppShell.vue'
import DateRangeFilter from '../components/DateRangeFilter.vue'
</script>

<template>
  <AppShell title="安全审批概览">
    <div class="page compact-page">
      <header class="page-heading">
        <div>
          <p class="page-eyebrow">Security Approval</p>
          <h1 class="page-title">安全审批</h1>
          <p class="page-description">查看指定时间范围内已完成的 Lark 安全审批数量。</p>
        </div>
        <span class="status-pill success">审批数据已同步</span>
      </header>

      <DateRangeFilter />

      <section class="panel approval-summary-panel">
        <div class="section-heading">
          <div>
            <h2 class="section-title">审批汇总</h2>
            <p class="section-subtitle">仅统计已完成审批</p>
          </div>
          <ShieldCheck :size="20" class="section-icon" />
        </div>

        <article class="approval-summary-card">
          <span class="approval-icon"><BadgeCheck :size="24" /></span>
          <div>
            <p>Lark 已完成审批数量</p>
            <strong class="data-value">12</strong>
            <small>项</small>
          </div>
          <span class="status-pill success">全部完成</span>
        </article>
      </section>
    </div>
  </AppShell>
</template>

<style scoped>
.compact-page {
  align-content: start;
}

.section-icon {
  color: var(--primary);
}

.approval-summary-card {
  display: grid;
  min-height: 162px;
  align-items: center;
  gap: 18px;
  padding: 24px;
  background: rgba(5, 15, 25, 0.42);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  grid-template-columns: auto 1fr auto;
}

.approval-icon {
  display: grid;
  width: 52px;
  height: 52px;
  color: var(--success);
  background: rgba(49, 209, 139, 0.09);
  border-radius: 11px;
  place-items: center;
}

.approval-summary-card > div {
  display: grid;
  align-items: baseline;
  grid-template-columns: auto auto;
  justify-content: start;
}

.approval-summary-card p {
  grid-column: 1 / -1;
  margin: 0 0 4px;
  color: var(--text-soft);
  font-size: 12px;
}

.approval-summary-card strong {
  font-size: 34px;
  line-height: 1.2;
}

.approval-summary-card small {
  margin-left: 7px;
  color: var(--text-muted);
  font-size: 11px;
}

@media (max-width: 600px) {
  .approval-summary-card {
    grid-template-columns: auto 1fr;
  }

  .approval-summary-card > .status-pill {
    grid-column: 1 / -1;
    justify-self: start;
  }
}
</style>
