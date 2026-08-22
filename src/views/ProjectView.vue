<script setup>
import { computed, ref } from 'vue'
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
  X,
} from '@lucide/vue'
import AppShell from '../components/AppShell.vue'
import DataProvenance from '../components/DataProvenance.vue'
import DataState from '../components/DataState.vue'
import DateRangeFilter from '../components/DateRangeFilter.vue'
import StatCard from '../components/StatCard.vue'
import { useOpsData } from '../composables/useOpsData'

const detailView = ref('summary')
const selectedKey = ref('')
const { data, meta, loading, error, empty, reload } = useOpsData('projects', () => ({ view: detailView.value }))
const summary = computed(() => data.value?.summary || {})
const incidents = computed(() => data.value?.incidents || [])
const tasks = computed(() => data.value?.tasks || [])
const releases = computed(() => data.value?.releases || {})
const selectedIncident = computed(() => incidents.value.find((item) => `${item.report_date}-${item.id}` === selectedKey.value))

const number = (value) => new Intl.NumberFormat('zh-CN').format(value || 0)
const percent = (value) => `${Number(value || 0).toFixed(1)}%`
const tone = (status = '') => (status.includes('完成') || status.includes('关闭') || status.includes('复盘') ? 'success' : 'warning')

function toggleAll() {
  detailView.value = detailView.value === 'all' ? 'summary' : 'all'
}

function openIncident(incident) {
  selectedKey.value = `${incident.report_date}-${incident.id}`
  if (detailView.value === 'all') reload()
  else detailView.value = 'all'
}
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
        <span class="status-pill success">项目接口已连接</span>
      </header>

      <DateRangeFilter />
      <DataProvenance :meta="meta" />

      <DataState :loading="loading" :error="error" :empty="empty" @retry="reload">
        <section class="metrics-grid">
          <StatCard label="Jira 清单总数量" :value="number(summary.jira_total)" :helper="`${number(summary.jira_completed)} 项已完成`" :trend="percent(summary.completion_rate)" :icon="ClipboardList" />
          <StatCard label="告警汇总数量" :value="number(summary.alert_total)" :helper="`${number(summary.alerts_processing)} 项处理中`" trend="区间发生量" trend-type="flat" tone="warning" :icon="BellRing" />
          <StatCard label="发板记录" :value="number(summary.release_total)" :helper="`成功率 ${percent(summary.release_success_rate)}`" :trend="`${number(summary.release_success)} 次成功`" :icon="Rocket" tone="success" />
          <StatCard label="变更记录" :value="number(summary.change_total)" :helper="`高风险变更 ${number(summary.high_risk_changes)} 项`" trend="区间发生量" trend-type="flat" :icon="History" />
        </section>

        <section class="split-grid">
        <article class="panel">
          <div class="section-heading">
            <div>
              <h2 class="section-title">RCA / 故障报告</h2>
              <p class="section-subtitle">按最近更新时间排序</p>
            </div>
            <button class="secondary-button" @click="toggleAll">{{ detailView === 'all' ? '收起列表' : `查看全部（${data.incident_total || 0}）` }}</button>
          </div>
          <div class="incident-list">
            <article v-for="incident in incidents" :key="`${incident.report_date}-${incident.id}`" class="incident-row">
              <span class="incident-icon"><AlertCircle :size="17" /></span>
              <div class="incident-main">
                <span class="incident-id data-value">#{{ incident.id }}</span>
                <strong>{{ incident.title }}</strong>
                <small>{{ incident.owner }}</small>
              </div>
              <span class="duration data-value"><TimerReset :size="13" />{{ incident.duration_minutes }} min</span>
              <span class="status-pill" :class="tone(incident.status)">{{ incident.status }}</span>
              <button class="row-link" aria-label="查询并查看故障报告详情" @click="openIncident(incident)"><ExternalLink :size="15" /></button>
            </article>
            <div v-if="!incidents.length" class="empty-note">当前范围没有 RCA / 故障报告明细</div>
          </div>
        </article>

        <article class="panel task-panel">
          <div class="section-heading">
            <div>
              <h2 class="section-title">季度任务 / 杂项任务</h2>
              <p class="section-subtitle">{{ data.task_total || 0 }} 类任务 · 当前显示 {{ tasks.length }} 类</p>
            </div>
            <GitPullRequestArrow :size="19" class="section-icon" />
          </div>
          <div class="task-list">
            <article v-for="task in tasks" :key="`${task.report_date}-${task.title}`" class="task-row">
              <div class="task-title">
                <span :class="tone(task.status)"><CheckCircle2 :size="15" /></span>
                <div><strong>{{ task.title }}</strong><small>{{ task.owner || '未指定负责人' }} · 截止 {{ task.due_date || '未设置' }}</small></div>
                <b class="task-count data-value">{{ task.count }} 项</b>
              </div>
            </article>
            <div v-if="!tasks.length" class="empty-note">当前范围没有季度/杂项任务明细</div>
          </div>
        </article>
      </section>

      <section class="panel release-panel">
        <div class="section-heading">
          <div><h2 class="section-title">本周期交付状态</h2><p class="section-subtitle">按环境统计部署结果</p></div>
        </div>
        <div class="release-grid">
          <div><span>生产环境</span><strong class="data-value">{{ number(releases.production) }}</strong><small>{{ number(releases.production_success) }} 成功 · {{ number(releases.production_rollback) }} 回滚</small></div>
          <div><span>预发布环境</span><strong class="data-value">{{ number(releases.staging) }}</strong><small>按业务日期汇总</small></div>
          <div><span>测试环境</span><strong class="data-value">{{ number(releases.test) }}</strong><small>{{ number(releases.test_verifying) }} 项验证中</small></div>
          <div><span>交付总数量</span><strong class="data-value">{{ number(releases.total) }}</strong><small>覆盖 3 个环境</small></div>
        </div>
      </section>
      </DataState>
    </div>

    <div v-if="selectedIncident" class="incident-modal-backdrop" @click.self="selectedKey = ''">
      <article class="incident-modal" role="dialog" aria-modal="true" aria-labelledby="incident-detail-title">
        <button class="modal-close" aria-label="关闭详情" @click="selectedKey = ''"><X :size="18" /></button>
        <p class="page-eyebrow">Incident detail</p>
        <h2 id="incident-detail-title">#{{ selectedIncident.id }} {{ selectedIncident.title }}</h2>
        <dl><div><dt>业务日期</dt><dd>{{ selectedIncident.report_date }}</dd></div><div><dt>负责团队</dt><dd>{{ selectedIncident.owner || '未提供' }}</dd></div><div><dt>处理状态</dt><dd>{{ selectedIncident.status }}</dd></div><div><dt>影响时长</dt><dd>{{ selectedIncident.duration_minutes }} 分钟</dd></div></dl>
      </article>
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

.incident-modal-backdrop {
  position: fixed;
  z-index: 60;
  display: grid;
  padding: 18px;
  background: rgba(1, 7, 12, 0.78);
  backdrop-filter: blur(6px);
  inset: 0;
  place-items: center;
}

.incident-modal {
  position: relative;
  width: min(100%, 560px);
  padding: 28px;
  background: var(--surface-strong);
  border: 1px solid var(--border-strong);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow);
}

.modal-close {
  position: absolute;
  display: grid;
  width: 34px;
  height: 34px;
  color: var(--text-muted);
  cursor: pointer;
  background: transparent;
  border: 0;
  border-radius: 6px;
  inset: 16px 16px auto auto;
  place-items: center;
}

.incident-modal h2 { margin: 0 44px 18px 0; font-size: 18px; }
.incident-modal dl { display: grid; gap: 1px; margin: 0; overflow: hidden; background: var(--border); border: 1px solid var(--border); border-radius: var(--radius-sm); }
.incident-modal dl > div { display: grid; grid-template-columns: 110px 1fr; padding: 11px 13px; background: var(--surface-soft); }
.incident-modal dt { color: var(--text-muted); font-size: 10px; }
.incident-modal dd { margin: 0; color: var(--text-soft); font-size: 11px; }

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
