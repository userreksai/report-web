<script setup>
import { computed, ref } from 'vue'
import {
  ArrowRight,
  CheckCircle2,
  FileChartColumn,
  FileText,
  Layers3,
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
const { data, meta, loading, error, empty, reload } = useOpsData('monthly', () => ({ view: detailView.value }))
const summary = computed(() => data.value?.summary || {})
const reports = computed(() => data.value?.reports || [])
const compilation = computed(() => data.value?.latest_compilation || { progress: 0, steps: [] })
const selectedReport = computed(() => reports.value.find((report) => `${report.report_date}-${report.report_month}` === selectedKey.value))

const number = (value) => new Intl.NumberFormat('zh-CN', { maximumFractionDigits: 1 }).format(value || 0)
const monthLabel = (value = '') => value ? value.replace('-', '年') + '月' : '未标注月份'

function openReport(report) {
  selectedKey.value = `${report.report_date}-${report.report_month}`
  if (detailView.value === 'all') reload()
  else detailView.value = 'all'
}
</script>

<template>
  <AppShell title="杂项 · 月报">
    <div class="page">
      <header class="page-heading">
        <div>
          <p class="page-eyebrow">Monthly Reports</p>
          <h1 class="page-title">运维月报</h1>
          <p class="page-description">沉淀每月运维工作与资源变化，形成可追溯的运营记录。</p>
        </div>
      </header>

      <DateRangeFilter />
      <DataProvenance :meta="meta" />

      <DataState :loading="loading" :error="error" :empty="empty" @retry="reload">
        <section class="metrics-grid monthly-metrics">
          <StatCard label="范围内月报" :value="number(summary.report_count)" :helper="reports[0] ? `最新发布于 ${reports[0].report_date}` : '暂无发布记录'" trend="按生成日期统计" trend-type="flat" :icon="FileText" />
          <StatCard label="累计工作项" :value="number(summary.work_items)" :helper="`月均 ${number(summary.average_work_items)} 项`" trend="范围内月报汇总" trend-type="flat" :icon="Layers3" />
        </section>

        <section class="reports-layout">
        <article class="panel report-list-panel">
          <div class="section-heading">
            <div><h2 class="section-title">月报列表</h2><p class="section-subtitle">按生成日期倒序</p></div>
            <button class="secondary-button" @click="detailView = detailView === 'all' ? 'summary' : 'all'">{{ detailView === 'all' ? '收起列表' : `查看全部（${data.report_total || 0}）` }}</button>
          </div>

          <div v-if="reports.length" class="report-list">
            <article v-for="report in reports" :key="`${report.report_date}-${report.report_month}`" class="report-row">
              <span class="report-file"><FileChartColumn :size="20" /></span>
              <div class="report-main">
                <strong>{{ monthLabel(report.report_month) }}运维月报</strong>
                <p>{{ report.summary }}</p>
                <small>生成日期：{{ report.report_date }}</small>
              </div>
              <div class="report-stats">
                <span><small>工作项</small><b class="data-value">{{ number(report.work_items) }}</b></span>
              </div>
              <span class="status-pill" :class="report.status.includes('发布') || report.status.includes('归档') ? 'success' : 'warning'">{{ report.status }}</span>
              <button class="view-button" @click="openReport(report)">
                查看 <ArrowRight :size="15" />
              </button>
            </article>
          </div>
          <div v-else class="empty-note">当前时间范围暂无月报</div>
        </article>

        <aside class="report-side">
          <article class="panel completion-card">
            <div class="section-heading">
              <div><h2 class="section-title">最新编制进度</h2><p class="section-subtitle">取范围内最近一条记录</p></div>
              <span class="status-pill warning">{{ compilation.progress >= 100 ? '已完成' : '进行中' }}</span>
            </div>
            <div class="completion-ring" :style="{ background: `radial-gradient(circle, var(--surface) 57%, transparent 59%), conic-gradient(var(--primary) 0 ${compilation.progress}%, var(--border) ${compilation.progress}% 100%)` }"><strong class="data-value">{{ compilation.progress }}%</strong><small>已完成</small></div>
            <div class="check-list">
              <span v-for="step in compilation.steps" :key="step.name" :class="{ done: step.completed }"><CheckCircle2 v-if="step.completed" :size="15" /><span v-else class="pending-dot" />{{ step.name }}</span>
              <span v-if="!compilation.steps?.length">暂无编制步骤</span>
            </div>
          </article>

        </aside>
      </section>
      </DataState>
    </div>

    <div v-if="selectedReport" class="modal-backdrop" @click.self="selectedKey = ''">
      <article class="report-modal" role="dialog" aria-modal="true" aria-labelledby="report-title">
        <button class="modal-close" aria-label="关闭" @click="selectedKey = ''"><X :size="18" /></button>
        <span class="modal-icon"><FileChartColumn :size="24" /></span>
        <p class="page-eyebrow">Monthly Report</p>
        <h2 id="report-title">{{ monthLabel(selectedReport.report_month) }}运维月报</h2>
        <p class="modal-summary">{{ selectedReport.summary }}</p>
        <div class="modal-metrics">
          <div><small>工作项</small><strong class="data-value">{{ number(selectedReport.work_items) }}</strong></div>
        </div>
        <div class="modal-actions">
          <button class="secondary-button" @click="selectedKey = ''">关闭</button>
        </div>
      </article>
    </div>
  </AppShell>
</template>

<style scoped>
.monthly-metrics {
  grid-template-columns: repeat(2, minmax(0, 1fr));
}

.reports-layout {
  display: grid;
  align-items: start;
  gap: 16px;
  grid-template-columns: minmax(0, 1fr) 320px;
}

.year-select {
  display: flex;
  height: 36px;
  align-items: center;
  gap: 7px;
  padding: 0 9px;
  color: var(--text-muted);
  background: var(--bg-deep);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
}

.year-select select {
  color: var(--text-soft);
  background: transparent;
  border: 0;
  outline: 0;
}

.report-list {
  display: grid;
}

.report-row {
  display: grid;
  min-height: 112px;
  align-items: center;
  gap: 14px;
  padding: 16px 0;
  border-top: 1px solid var(--border);
  grid-template-columns: auto minmax(200px, 1fr) auto auto auto;
}

.report-row:first-child {
  border-top: 0;
}

.report-file {
  display: grid;
  width: 42px;
  height: 42px;
  color: var(--primary);
  background: var(--primary-soft);
  border: 1px solid rgba(22, 213, 217, 0.15);
  border-radius: 9px;
  place-items: center;
}

.report-main {
  min-width: 0;
}

.report-main strong {
  font-size: 13px;
}

.report-main p {
  display: -webkit-box;
  max-width: 560px;
  margin: 4px 0;
  overflow: hidden;
  color: var(--text-muted);
  font-size: 10px;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 1;
}

.report-main small {
  color: var(--text-muted);
  font-size: 9px;
}

.report-stats {
  display: flex;
  gap: 16px;
}

.report-stats > span {
  display: grid;
  min-width: 52px;
  text-align: right;
}

.report-stats small {
  color: var(--text-muted);
  font-size: 9px;
}

.report-stats b {
  font-size: 11px;
}

.view-button {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 7px 9px;
  color: var(--text-soft);
  cursor: pointer;
  background: transparent;
  border: 0;
  border-radius: 5px;
  font-size: 11px;
}

.view-button:hover {
  color: var(--primary);
  background: var(--primary-soft);
}

.report-side {
  display: grid;
  gap: 16px;
}

.completion-ring {
  display: grid;
  width: 146px;
  height: 146px;
  margin: 8px auto 24px;
  align-content: center;
  background:
    radial-gradient(circle, var(--surface) 57%, transparent 59%),
    conic-gradient(var(--primary) 0 74%, var(--border) 74% 100%);
  border-radius: 50%;
  text-align: center;
}

.completion-ring strong {
  font-size: 27px;
}

.completion-ring small {
  color: var(--text-muted);
  font-size: 9px;
}

.check-list {
  display: grid;
  gap: 12px;
}

.check-list > span {
  display: flex;
  align-items: center;
  gap: 8px;
  color: var(--text-muted);
  font-size: 10px;
}

.check-list > span.done {
  color: var(--text-soft);
}

.check-list svg {
  color: var(--success);
}

.pending-dot {
  width: 13px;
  height: 13px;
  border: 1px dashed var(--text-muted);
  border-radius: 50%;
}

.modal-backdrop {
  position: fixed;
  z-index: 60;
  display: grid;
  padding: 18px;
  background: rgba(1, 7, 12, 0.78);
  backdrop-filter: blur(6px);
  inset: 0;
  place-items: center;
}

.report-modal {
  position: relative;
  width: min(100%, 530px);
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

.modal-close:hover {
  color: var(--text);
  background: var(--surface-hover);
}

.modal-icon {
  display: grid;
  width: 48px;
  height: 48px;
  margin-bottom: 18px;
  color: var(--primary);
  background: var(--primary-soft);
  border-radius: 10px;
  place-items: center;
}

.report-modal h2 {
  margin: 0;
  font-size: 21px;
}

.modal-summary {
  margin: 10px 0 20px;
  color: var(--text-soft);
  line-height: 1.7;
}

.modal-metrics {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1px;
  overflow: hidden;
  background: var(--border);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
}

.modal-metrics > div {
  display: grid;
  gap: 4px;
  padding: 14px;
  background: var(--surface-soft);
}

.modal-metrics small {
  color: var(--text-muted);
  font-size: 9px;
}

.modal-metrics strong {
  font-size: 16px;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
  margin-top: 22px;
}

.modal-actions button {
  gap: 7px;
}

@media (max-width: 1200px) {
  .reports-layout {
    grid-template-columns: 1fr;
  }

}

@media (max-width: 800px) {
  .monthly-metrics {
    grid-template-columns: 1fr;
  }

  .report-row {
    grid-template-columns: auto minmax(0, 1fr) auto;
  }

  .report-stats,
  .report-row > .status-pill {
    display: none;
  }

  .report-side {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 520px) {
  .report-list-panel .section-heading {
    align-items: flex-start;
  }

  .report-row {
    grid-template-columns: auto 1fr;
  }

  .view-button {
    grid-column: 2;
    justify-self: start;
    padding-left: 0;
  }
}
</style>
