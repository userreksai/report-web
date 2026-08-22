<script setup>
import { AlarmClock, Database, FileClock } from '@lucide/vue'
import AppShell from '../components/AppShell.vue'
import DateRangeFilter from '../components/DateRangeFilter.vue'
</script>

<template>
  <AppShell title="数据库管理">
    <div class="page compact-page">
      <header class="page-heading">
        <div>
          <p class="page-eyebrow">Database Operations</p>
          <h1 class="page-title">数据库管理</h1>
          <p class="page-description">汇总 Archery 工单与慢 SQL 数量，快速查看数据库工作总量。</p>
        </div>
        <span class="status-pill success">数据汇总正常</span>
      </header>

      <DateRangeFilter />

      <section class="panel summary-panel">
        <div class="section-heading">
          <div>
            <h2 class="section-title">DBA 数据汇总</h2>
            <p class="section-subtitle">当前时间范围内的数据总量</p>
          </div>
          <Database :size="20" class="section-icon" />
        </div>

        <div class="database-summary-grid">
          <article class="summary-card">
            <span class="summary-icon"><FileClock :size="22" /></span>
            <div>
              <p>Archery 工单</p>
              <strong class="data-value">24</strong>
            </div>
          </article>

          <article class="summary-card">
            <span class="summary-icon warning"><AlarmClock :size="22" /></span>
            <div class="slow-summary">
              <p>慢 SQL（数量）</p>
              <strong class="data-value">1,402</strong>
              <span><small>生产</small><b class="data-value">842</b></span>
              <span><small>非生产</small><b class="data-value">560</b></span>
            </div>
          </article>
        </div>
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

.database-summary-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 14px;
}

.summary-card {
  display: grid;
  min-height: 178px;
  align-items: center;
  gap: 16px;
  padding: 22px;
  background: rgba(5, 15, 25, 0.42);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  grid-template-columns: auto 1fr;
}

.summary-icon {
  display: grid;
  width: 48px;
  height: 48px;
  color: var(--primary);
  background: var(--primary-soft);
  border-radius: 10px;
  place-items: center;
}

.summary-icon.warning {
  color: var(--warning);
  background: rgba(243, 182, 74, 0.09);
}

.summary-card p {
  margin: 0 0 5px;
  color: var(--text-soft);
  font-size: 12px;
}

.summary-card strong {
  display: block;
  font-size: 30px;
  line-height: 1.2;
}

.summary-card small {
  color: var(--text-muted);
  font-size: 10px;
}

.slow-summary {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 2px 18px;
}

.slow-summary > p,
.slow-summary > strong {
  grid-column: 1 / -1;
}

.slow-summary > span {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  margin-top: 10px;
  padding: 7px 10px;
  background: var(--surface-soft);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
}

.slow-summary > span b {
  font-size: 11px;
}

@media (max-width: 760px) {
  .database-summary-grid {
    grid-template-columns: 1fr;
  }

  .summary-card {
    min-height: 148px;
  }
}
</style>
