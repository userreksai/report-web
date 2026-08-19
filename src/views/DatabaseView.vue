<script setup>
import {
  Activity,
  AlarmClock,
  ArchiveRestore,
  BadgeCheck,
  Boxes,
  CircleGauge,
  Database,
  FileClock,
  HardDrive,
  ServerCog,
  TriangleAlert,
} from '@lucide/vue'
import AppShell from '../components/AppShell.vue'
import DateRangeFilter from '../components/DateRangeFilter.vue'
import StatCard from '../components/StatCard.vue'

const instances = [
  { name: 'prod-mysql-primary', type: 'MySQL 8.0', region: '华东-1', qps: '2,842', load: 72, status: '正常' },
  { name: 'prod-pg-order', type: 'PostgreSQL 15', region: '华北-2', qps: '1,906', load: 61, status: '正常' },
  { name: 'analytics-clickhouse', type: 'ClickHouse 23', region: '华东-1', qps: '4,115', load: 86, status: '关注' },
  { name: 'cache-redis-cluster', type: 'Redis 7.0', region: '华南-1', qps: '9,632', load: 43, status: '正常' },
]

const slowSql = [
  { db: 'order_service', avg: '3.84s', count: 126, owner: '订单平台组' },
  { db: 'user_center', avg: '2.16s', count: 92, owner: '账号服务组' },
  { db: 'reporting', avg: '5.62s', count: 48, owner: '数据平台组' },
]
</script>

<template>
  <AppShell title="数据库管理">
    <div class="page">
      <header class="page-heading">
        <div>
          <p class="page-eyebrow">Database Operations</p>
          <h1 class="page-title">数据库管理</h1>
          <p class="page-description">追踪工单、慢 SQL、实例负载与备份情况，统一数据库运行质量视图。</p>
        </div>
        <span class="status-pill success">核心实例可用</span>
      </header>

      <DateRangeFilter />

      <section class="metrics-grid">
        <StatCard label="Archery 工单" value="24" helper="总计 86 项" trend="6 项" :icon="FileClock" />
        <StatCard label="生产慢 SQL" value="842" helper="较上周期减少 7.8%" trend="7.8%" trend-type="down" tone="warning" :icon="AlarmClock" />
        <StatCard label="数据库实例" value="37" helper="35 正常 · 2 关注" trend="99.94%" tone="success" :icon="Database" />
        <StatCard label="备份成功率" value="99.8%" helper="最近一次 03:20" trend="0.2%" tone="success" :icon="ArchiveRestore" />
      </section>

      <section class="panel health-panel">
        <div class="section-heading">
          <div><h2 class="section-title">核心实例运行状态</h2><p class="section-subtitle">近 5 分钟平均负载</p></div>
          <span class="status-pill success">4 / 4 在线</span>
        </div>
        <div class="instance-grid">
          <article v-for="instance in instances" :key="instance.name" class="instance-card">
            <div class="instance-heading">
              <span><HardDrive :size="17" /></span>
              <div><strong>{{ instance.name }}</strong><small>{{ instance.type }} · {{ instance.region }}</small></div>
              <span class="status-pill" :class="instance.status === '正常' ? 'success' : 'warning'">{{ instance.status }}</span>
            </div>
            <div class="instance-values">
              <span>实时 QPS <b class="data-value">{{ instance.qps }}</b></span>
              <span>负载 <b class="data-value">{{ instance.load }}%</b></span>
            </div>
            <div class="progress-track">
              <div class="progress-bar" :class="{ hot: instance.load > 80 }" :style="{ width: `${instance.load}%` }" />
            </div>
          </article>
        </div>
      </section>

      <section class="split-grid">
        <article class="panel">
          <div class="section-heading">
            <div><h2 class="section-title">慢 SQL 排行</h2><p class="section-subtitle">按累计影响时长排序</p></div>
            <TriangleAlert :size="19" class="warning-icon" />
          </div>
          <div class="slow-list">
            <article v-for="(item, index) in slowSql" :key="item.db" class="slow-row">
              <b class="rank data-value">0{{ index + 1 }}</b>
              <div><strong class="data-value">{{ item.db }}</strong><small>{{ item.owner }}</small></div>
              <span><small>平均耗时</small><b class="data-value">{{ item.avg }}</b></span>
              <span><small>调用次数</small><b class="data-value">{{ item.count }}</b></span>
            </article>
          </div>
        </article>

        <article class="panel">
          <div class="section-heading">
            <div><h2 class="section-title">数据库健康评分</h2><p class="section-subtitle">容量、性能、可用性综合评分</p></div>
            <BadgeCheck :size="19" class="success-icon" />
          </div>
          <div class="score-content">
            <div class="score-ring"><strong class="data-value">92</strong><small>健康</small></div>
            <div class="score-items">
              <div><span><Activity :size="15" />性能</span><b class="data-value">89</b></div>
              <div><span><Boxes :size="15" />容量</span><b class="data-value">86</b></div>
              <div><span><ServerCog :size="15" />可用性</span><b class="data-value">99</b></div>
              <div><span><CircleGauge :size="15" />备份</span><b class="data-value">96</b></div>
            </div>
          </div>
        </article>
      </section>
    </div>
  </AppShell>
</template>

<style scoped>
.instance-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
}

.instance-card {
  padding: 15px;
  background: rgba(5, 15, 25, 0.42);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
}

.instance-heading {
  display: grid;
  align-items: center;
  gap: 10px;
  grid-template-columns: auto 1fr auto;
}

.instance-heading > span:first-child {
  display: grid;
  width: 32px;
  height: 32px;
  color: var(--primary);
  background: var(--primary-soft);
  border-radius: 7px;
  place-items: center;
}

.instance-heading > div {
  display: grid;
  min-width: 0;
}

.instance-heading strong {
  overflow: hidden;
  font: 600 11px/1.4 var(--font-data);
  text-overflow: ellipsis;
  white-space: nowrap;
}

.instance-heading small {
  color: var(--text-muted);
  font-size: 9px;
}

.instance-values {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin: 17px 0 8px;
  color: var(--text-muted);
  font-size: 10px;
}

.instance-values b {
  margin-left: 5px;
  color: var(--text-soft);
}

.progress-bar.hot {
  background: linear-gradient(90deg, var(--warning), var(--danger));
}

.warning-icon {
  color: var(--warning);
}

.success-icon {
  color: var(--success);
}

.slow-list {
  display: grid;
}

.slow-row {
  display: grid;
  min-height: 64px;
  align-items: center;
  gap: 12px;
  border-top: 1px solid var(--border);
  grid-template-columns: auto 1fr auto auto;
}

.slow-row:first-child {
  border-top: 0;
}

.rank {
  color: var(--primary);
  font-size: 11px;
}

.slow-row > div,
.slow-row > span {
  display: grid;
}

.slow-row > div strong {
  font-size: 11px;
}

.slow-row small {
  color: var(--text-muted);
  font-size: 9px;
}

.slow-row > span b {
  color: var(--text-soft);
  font-size: 10px;
  text-align: right;
}

.score-content {
  display: grid;
  align-items: center;
  gap: 24px;
  grid-template-columns: auto 1fr;
}

.score-ring {
  display: grid;
  width: 138px;
  height: 138px;
  align-content: center;
  background:
    radial-gradient(circle at center, var(--surface) 57%, transparent 59%),
    conic-gradient(var(--primary) 0 92%, var(--border) 92% 100%);
  border-radius: 50%;
  text-align: center;
}

.score-ring strong {
  font-size: 32px;
}

.score-ring small {
  color: var(--success);
  font-size: 10px;
}

.score-items {
  display: grid;
}

.score-items > div {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 9px 0;
  border-top: 1px solid var(--border);
}

.score-items > div:first-child {
  border-top: 0;
}

.score-items span {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  color: var(--text-soft);
  font-size: 11px;
}

.score-items svg {
  color: var(--primary);
}

.score-items b {
  font-size: 11px;
}

@media (max-width: 760px) {
  .instance-grid {
    grid-template-columns: 1fr;
  }

  .score-content {
    grid-template-columns: 1fr;
    justify-items: center;
  }

  .score-items {
    width: 100%;
  }
}

@media (max-width: 520px) {
  .slow-row {
    grid-template-columns: auto 1fr auto;
  }

  .slow-row > span:last-child {
    display: none;
  }
}
</style>
