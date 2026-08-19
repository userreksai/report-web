<script setup>
import {
  AlertCircle,
  BellRing,
  CheckCircle2,
  ClipboardList,
  ExternalLink,
  GitPullRequestArrow,
  History,
  Rocket,
  TimerReset,
} from '@lucide/vue'
import AppShell from '../components/AppShell.vue'
import DateRangeFilter from '../components/DateRangeFilter.vue'
import StatCard from '../components/StatCard.vue'

const incidents = [
  { id: 'RCA-4091', title: '生产数据库集群同步延迟', owner: '数据库平台组', status: '分析中', tone: 'warning', duration: '65 min' },
  { id: 'RCA-4088', title: '峰值时段 API 网关延迟升高', owner: '平台工程组', status: '已复盘', tone: 'success', duration: '42 min' },
  { id: 'RCA-4082', title: 'Redis 缓存驱逐率异常', owner: '基础架构组', status: '已关闭', tone: 'success', duration: '18 min' },
  { id: 'RCA-4079', title: '海外节点健康检查波动', owner: '网络工程组', status: '跟进中', tone: 'warning', duration: '31 min' },
]

const tasks = [
  { title: '迁移旧版认证服务', owner: '王宁', count: 10, due: '08-22', tone: 'success' },
  { title: '更新 Q3 安全证书', owner: '李敏', count: 4, due: '08-26', tone: 'warning' },
  { title: 'IAM 角色与权限审计', owner: '赵强', count: 87, due: '08-30', tone: 'warning' },
  { title: '核心链路压测与基线更新', owner: '陈晓', count: 6, due: '08-20', tone: 'success' },
]
</script>

<template>
  <AppShell title="项目概览">
    <div class="page">
      <header class="page-heading">
        <div>
          <p class="page-eyebrow">Project Operations</p>
          <h1 class="page-title">项目概览</h1>
          <p class="page-description">统一追踪工作项、告警、发布、变更以及故障复盘进度。</p>
        </div>
        <span class="status-pill success">项目同步正常</span>
      </header>

      <DateRangeFilter />

      <section class="metrics-grid">
        <StatCard label="Jira 清单总数量" value="142" helper="98 项已完成" trend="12.6%" :icon="ClipboardList" />
        <StatCard label="告警汇总数量" value="12" helper="3 项处理中" trend="2 项" trend-type="down" tone="warning" :icon="BellRing" />
        <StatCard label="发板记录" value="34" helper="成功率 97.1%" trend="4 次" :icon="Rocket" tone="success" />
        <StatCard label="变更记录" value="89" helper="高风险变更 6 项" trend="8.4%" :icon="History" />
      </section>

      <section class="split-grid">
        <article class="panel">
          <div class="section-heading">
            <div>
              <h2 class="section-title">RCA / 故障报告</h2>
              <p class="section-subtitle">按最近更新时间排序</p>
            </div>
            <button class="secondary-button">查看全部</button>
          </div>
          <div class="incident-list">
            <article v-for="incident in incidents" :key="incident.id" class="incident-row">
              <span class="incident-icon"><AlertCircle :size="17" /></span>
              <div class="incident-main">
                <span class="incident-id data-value">#{{ incident.id }}</span>
                <strong>{{ incident.title }}</strong>
                <small>{{ incident.owner }}</small>
              </div>
              <span class="duration data-value"><TimerReset :size="13" />{{ incident.duration }}</span>
              <span class="status-pill" :class="incident.tone">{{ incident.status }}</span>
              <button class="row-link" aria-label="查看故障报告"><ExternalLink :size="15" /></button>
            </article>
          </div>
        </article>

        <article class="panel task-panel">
          <div class="section-heading">
            <div>
              <h2 class="section-title">季度任务 / 杂项任务</h2>
              <p class="section-subtitle">4 类任务 · 共 107 项</p>
            </div>
            <GitPullRequestArrow :size="19" class="section-icon" />
          </div>
          <div class="task-list">
            <article v-for="task in tasks" :key="task.title" class="task-row">
              <div class="task-title">
                <span :class="task.tone"><CheckCircle2 :size="15" /></span>
                <div><strong>{{ task.title }}</strong><small>{{ task.owner }} · 截止 {{ task.due }}</small></div>
                <b class="task-count data-value">{{ task.count }} 项</b>
              </div>
            </article>
          </div>
        </article>
      </section>

      <section class="panel release-panel">
        <div class="section-heading">
          <div><h2 class="section-title">本周期交付状态</h2><p class="section-subtitle">按环境统计部署结果</p></div>
        </div>
        <div class="release-grid">
          <div><span>生产环境</span><strong class="data-value">18</strong><small>17 成功 · 1 回滚</small></div>
          <div><span>预发布环境</span><strong class="data-value">41</strong><small>成功率 100%</small></div>
          <div><span>测试环境</span><strong class="data-value">96</strong><small>8 项验证中</small></div>
          <div><span>交付总数量</span><strong class="data-value">155</strong><small>覆盖 3 个环境</small></div>
        </div>
      </section>
    </div>
  </AppShell>
</template>

<style scoped>
.incident-list,
.task-list {
  display: grid;
}

.incident-row {
  display: grid;
  min-height: 72px;
  align-items: center;
  gap: 12px;
  border-top: 1px solid var(--border);
  grid-template-columns: auto minmax(0, 1fr) auto auto auto;
}

.incident-row:first-child {
  border-top: 0;
}

.incident-icon {
  display: grid;
  width: 32px;
  height: 32px;
  color: var(--warning);
  background: rgba(243, 182, 74, 0.08);
  border-radius: 7px;
  place-items: center;
}

.incident-main {
  display: grid;
  min-width: 0;
}

.incident-main strong {
  overflow: hidden;
  font-size: 12px;
  font-weight: 580;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.incident-main small {
  color: var(--text-muted);
  font-size: 10px;
}

.incident-id {
  color: var(--primary);
  font-size: 9px;
}

.duration {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  color: var(--text-muted);
  font-size: 9px;
}

.row-link {
  display: grid;
  width: 30px;
  height: 30px;
  padding: 0;
  color: var(--text-muted);
  cursor: pointer;
  background: transparent;
  border: 0;
  border-radius: 5px;
  place-items: center;
}

.row-link:hover {
  color: var(--primary);
  background: var(--primary-soft);
}

.section-icon {
  color: var(--primary);
}

.task-row {
  padding: 15px 0;
  border-top: 1px solid var(--border);
}

.task-row:first-child {
  padding-top: 0;
  border-top: 0;
}

.task-title {
  display: grid;
  align-items: center;
  gap: 9px;
  grid-template-columns: auto 1fr auto;
}

.task-count {
  color: var(--primary);
  font-size: 12px;
}

.task-title > span {
  display: grid;
  width: 28px;
  height: 28px;
  color: var(--success);
  background: rgba(49, 209, 139, 0.08);
  border-radius: 7px;
  place-items: center;
}

.task-title > span.warning {
  color: var(--warning);
  background: rgba(243, 182, 74, 0.08);
}

.task-title > div {
  display: grid;
}

.task-title strong {
  font-size: 12px;
}

.task-title small {
  color: var(--text-muted);
  font-size: 10px;
}

.task-title b {
  color: var(--primary);
  font-size: 11px;
}

.release-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1px;
  overflow: hidden;
  background: var(--border);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
}

.release-grid > div {
  display: grid;
  gap: 3px;
  padding: 16px;
  background: var(--surface-soft);
}

.release-grid span,
.release-grid small {
  color: var(--text-muted);
  font-size: 10px;
}

.release-grid strong {
  font-size: 22px;
}

@media (max-width: 820px) {
  .release-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 600px) {
  .incident-row {
    grid-template-columns: auto minmax(0, 1fr) auto;
  }

  .duration,
  .incident-row .status-pill {
    display: none;
  }
}
</style>
