<script setup>
import { computed, ref } from 'vue'
import {
  ArrowRight,
  CalendarDays,
  CheckCircle2,
  Download,
  FileChartColumn,
  FileText,
  Gauge,
  Layers3,
  TrendingDown,
  X,
} from '@lucide/vue'
import AppShell from '../components/AppShell.vue'
import DateRangeFilter from '../components/DateRangeFilter.vue'
import StatCard from '../components/StatCard.vue'

const selectedYear = ref('2026')
const selectedReport = ref(null)

const reports = [
  { month: '2026年7月', date: '2026-08-01', status: '已发布', items: 486, incidents: 8, availability: '99.96%', summary: '核心系统稳定运行，完成海外 CDN 扩容和年度证书集中续期。' },
  { month: '2026年6月', date: '2026-07-02', status: '已发布', items: 452, incidents: 11, availability: '99.92%', summary: '完成数据库主从架构优化，慢 SQL 数量较上月下降 13%。' },
  { month: '2026年5月', date: '2026-06-01', status: '已发布', items: 431, incidents: 9, availability: '99.94%', summary: '重点推进权限治理和资源成本核查，关闭 18 项历史风险。' },
  { month: '2026年4月', date: '2026-05-06', status: '已发布', items: 398, incidents: 14, availability: '99.88%', summary: '完成核心服务春季容量评估，新增 6 项自动化巡检。' },
  { month: '2025年12月', date: '2026-01-05', status: '已归档', items: 520, incidents: 10, availability: '99.95%', summary: '完成年度收口及跨年保障，所有高风险变更均通过复盘。' },
]

const filteredReports = computed(() => reports.filter((report) => report.month.startsWith(selectedYear.value)))
</script>

<template>
  <AppShell title="杂项 · 月报">
    <div class="page">
      <header class="page-heading">
        <div>
          <p class="page-eyebrow">Monthly Reports</p>
          <h1 class="page-title">运维月报</h1>
          <p class="page-description">沉淀每月运维工作、稳定性、故障与资源变化，形成可追溯的运营记录。</p>
        </div>
        <button class="primary-button create-button"><FileChartColumn :size="16" />生成本月月报</button>
      </header>

      <DateRangeFilter />

      <section class="metrics-grid">
        <StatCard label="本年月报" value="7" helper="最新发布于 08-01" trend="全部按时" trend-type="flat" :icon="FileText" />
        <StatCard label="累计工作项" value="3,142" helper="月均 449 项" trend="8.6%" :icon="Layers3" />
        <StatCard label="平均可用性" value="99.94%" helper="高于年度目标" trend="0.03%" tone="success" :icon="Gauge" />
        <StatCard label="故障数量" value="68" helper="较去年同期减少 17%" trend="17%" trend-type="down" tone="success" :icon="TrendingDown" />
      </section>

      <section class="reports-layout">
        <article class="panel report-list-panel">
          <div class="section-heading">
            <div><h2 class="section-title">月报列表</h2><p class="section-subtitle">按生成日期倒序</p></div>
            <label class="year-select">
              <CalendarDays :size="15" />
              <select v-model="selectedYear" aria-label="选择年份">
                <option value="2026">2026 年</option>
                <option value="2025">2025 年</option>
              </select>
            </label>
          </div>

          <div v-if="filteredReports.length" class="report-list">
            <article v-for="report in filteredReports" :key="report.month" class="report-row">
              <span class="report-file"><FileChartColumn :size="20" /></span>
              <div class="report-main">
                <strong>{{ report.month }}运维月报</strong>
                <p>{{ report.summary }}</p>
                <small>生成日期：{{ report.date }}</small>
              </div>
              <div class="report-stats">
                <span><small>工作项</small><b class="data-value">{{ report.items }}</b></span>
                <span><small>故障</small><b class="data-value">{{ report.incidents }}</b></span>
                <span><small>可用性</small><b class="data-value">{{ report.availability }}</b></span>
              </div>
              <span class="status-pill success">{{ report.status }}</span>
              <button class="view-button" @click="selectedReport = report">
                查看 <ArrowRight :size="15" />
              </button>
            </article>
          </div>
          <div v-else class="empty-note">该年份暂无月报</div>
        </article>

        <aside class="report-side">
          <article class="panel completion-card">
            <div class="section-heading">
              <div><h2 class="section-title">本月编制进度</h2><p class="section-subtitle">2026年8月</p></div>
              <span class="status-pill warning">进行中</span>
            </div>
            <div class="completion-ring"><strong class="data-value">74%</strong><small>已完成</small></div>
            <div class="check-list">
              <span class="done"><CheckCircle2 :size="15" />项目数据汇总</span>
              <span class="done"><CheckCircle2 :size="15" />数据库质量统计</span>
              <span class="done"><CheckCircle2 :size="15" />安全审批统计</span>
              <span><span class="pending-dot" />资源费用核对</span>
              <span><span class="pending-dot" />管理摘要确认</span>
            </div>
          </article>

          <article class="panel archive-card">
            <span><Download :size="19" /></span>
            <div><strong>归档与导出</strong><p>支持 PDF 与数据附件打包下载</p></div>
            <button class="secondary-button">批量导出</button>
          </article>
        </aside>
      </section>
    </div>

    <div v-if="selectedReport" class="modal-backdrop" @click.self="selectedReport = null">
      <article class="report-modal" role="dialog" aria-modal="true" aria-labelledby="report-title">
        <button class="modal-close" aria-label="关闭" @click="selectedReport = null"><X :size="18" /></button>
        <span class="modal-icon"><FileChartColumn :size="24" /></span>
        <p class="page-eyebrow">Monthly Report</p>
        <h2 id="report-title">{{ selectedReport.month }}运维月报</h2>
        <p class="modal-summary">{{ selectedReport.summary }}</p>
        <div class="modal-metrics">
          <div><small>工作项</small><strong class="data-value">{{ selectedReport.items }}</strong></div>
          <div><small>故障</small><strong class="data-value">{{ selectedReport.incidents }}</strong></div>
          <div><small>可用性</small><strong class="data-value">{{ selectedReport.availability }}</strong></div>
        </div>
        <div class="modal-actions">
          <button class="secondary-button" @click="selectedReport = null">关闭</button>
          <button class="primary-button"><Download :size="15" />下载月报</button>
        </div>
      </article>
    </div>
  </AppShell>
</template>

<style scoped>
.create-button {
  gap: 8px;
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

.archive-card {
  display: grid;
  align-items: center;
  gap: 12px;
  grid-template-columns: auto 1fr;
}

.archive-card > span {
  display: grid;
  width: 38px;
  height: 38px;
  color: var(--primary);
  background: var(--primary-soft);
  border-radius: 8px;
  place-items: center;
}

.archive-card strong {
  font-size: 12px;
}

.archive-card p {
  margin: 2px 0 0;
  color: var(--text-muted);
  font-size: 9px;
}

.archive-card button {
  grid-column: 1 / -1;
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
  grid-template-columns: repeat(3, 1fr);
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

  .report-side {
    grid-template-columns: 1fr 1fr;
  }
}

@media (max-width: 800px) {
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
  .create-button {
    width: 100%;
    margin-top: 14px;
  }

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
