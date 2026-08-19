<script setup>
import { computed, onBeforeUnmount, ref } from 'vue'
import { CalendarDays, Check, ChevronDown, RotateCcw, Search } from '@lucide/vue'

const emit = defineEmits(['search'])

const today = new Date()
const presets = [
  { label: '近 7 天', days: 7 },
  { label: '近 30 天', days: 30 },
  { label: '近 90 天', days: 90 },
  { label: '本月', month: true },
]

const open = ref(false)
const appliedStart = ref(shiftDate(today, -29))
const appliedEnd = ref(formatDate(today))
const draftStart = ref(appliedStart.value)
const draftEnd = ref(appliedEnd.value)
const activePreset = ref('近 30 天')
const feedback = ref(false)
let feedbackTimer

const displayRange = computed(() => `${toDisplay(appliedStart.value)} — ${toDisplay(appliedEnd.value)}`)

function formatDate(date) {
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  return `${year}-${month}-${day}`
}

function shiftDate(date, days) {
  const next = new Date(date)
  next.setDate(next.getDate() + days)
  return formatDate(next)
}

function toDisplay(value) {
  return value?.replaceAll('-', '.') || '未选择'
}

function usePreset(preset) {
  activePreset.value = preset.label
  draftEnd.value = formatDate(today)
  if (preset.month) {
    draftStart.value = formatDate(new Date(today.getFullYear(), today.getMonth(), 1))
  } else {
    draftStart.value = shiftDate(today, -(preset.days - 1))
  }
}

function reset() {
  activePreset.value = '近 30 天'
  draftStart.value = shiftDate(today, -29)
  draftEnd.value = formatDate(today)
}

function applyRange() {
  if (!draftStart.value || !draftEnd.value) return
  if (draftStart.value > draftEnd.value) {
    ;[draftStart.value, draftEnd.value] = [draftEnd.value, draftStart.value]
  }
  appliedStart.value = draftStart.value
  appliedEnd.value = draftEnd.value
  open.value = false
  feedback.value = true
  clearTimeout(feedbackTimer)
  feedbackTimer = setTimeout(() => (feedback.value = false), 1800)
  emit('search', { start: appliedStart.value, end: appliedEnd.value })
}

onBeforeUnmount(() => clearTimeout(feedbackTimer))
</script>

<template>
  <section class="date-filter" aria-label="时间筛选">
    <div class="filter-label">
      <span class="filter-icon"><CalendarDays :size="18" /></span>
      <span>
        <strong>时间范围</strong>
        <small>统一统计口径</small>
      </span>
    </div>

    <div class="preset-list" aria-label="快捷日期范围">
      <button
        v-for="preset in presets"
        :key="preset.label"
        :class="{ active: activePreset === preset.label }"
        @click="usePreset(preset)"
      >
        {{ preset.label }}
      </button>
    </div>

    <div class="picker-wrap">
      <button class="range-button" :aria-expanded="open" @click="open = !open">
        <CalendarDays :size="16" />
        <span>{{ displayRange }}</span>
        <ChevronDown :size="15" :class="{ rotated: open }" />
      </button>

      <div v-if="open" class="picker-popover">
        <div class="picker-heading">
          <div>
            <strong>选择日期范围</strong>
            <small>开始和结束日期均包含在统计内</small>
          </div>
          <button class="reset-button" @click="reset">
            <RotateCcw :size="14" />
            重置
          </button>
        </div>

        <div class="date-fields">
          <label>
            <span>开始日期</span>
            <input v-model="draftStart" type="date" :max="draftEnd" />
          </label>
          <span class="field-separator">至</span>
          <label>
            <span>结束日期</span>
            <input v-model="draftEnd" type="date" :min="draftStart" />
          </label>
        </div>

        <div class="picker-actions">
          <button class="secondary-button" @click="open = false">取消</button>
          <button class="primary-button" @click="applyRange">
            <Check :size="15" />
            应用范围
          </button>
        </div>
      </div>
    </div>

    <button class="search-button" @click="applyRange">
      <Check v-if="feedback" :size="16" />
      <Search v-else :size="16" />
      {{ feedback ? '已更新' : '查询' }}
    </button>
  </section>
</template>

<style scoped>
.date-filter {
  position: relative;
  z-index: 10;
  display: flex;
  min-height: 68px;
  align-items: center;
  gap: 18px;
  padding: 12px 14px;
  background: linear-gradient(90deg, rgba(16, 33, 49, 0.98), rgba(13, 29, 44, 0.98));
  border: 1px solid var(--border);
  border-radius: var(--radius);
}

.filter-label {
  display: flex;
  min-width: 142px;
  align-items: center;
  gap: 10px;
}

.filter-label > span:last-child {
  display: grid;
}

.filter-label strong {
  font-size: 12px;
}

.filter-label small {
  color: var(--text-muted);
  font-size: 10px;
}

.filter-icon {
  display: grid;
  width: 36px;
  height: 36px;
  color: var(--primary);
  background: var(--primary-soft);
  border: 1px solid rgba(22, 213, 217, 0.18);
  border-radius: 8px;
  place-items: center;
}

.preset-list {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 4px;
  background: rgba(3, 13, 22, 0.48);
  border: 1px solid var(--border);
  border-radius: 8px;
}

.preset-list button {
  min-height: 30px;
  padding: 0 10px;
  color: var(--text-muted);
  cursor: pointer;
  background: transparent;
  border: 0;
  border-radius: 5px;
  font-size: 11px;
  white-space: nowrap;
}

.preset-list button:hover,
.preset-list button.active {
  color: var(--text);
  background: var(--surface-hover);
}

.preset-list button.active {
  color: var(--primary);
}

.picker-wrap {
  position: relative;
  min-width: 250px;
  margin-left: auto;
}

.range-button {
  display: flex;
  width: 100%;
  min-height: 38px;
  align-items: center;
  gap: 9px;
  padding: 0 11px;
  color: var(--text-soft);
  cursor: pointer;
  background: var(--bg-deep);
  border: 1px solid var(--border-strong);
  border-radius: var(--radius-sm);
  font: 500 12px/1 var(--font-data);
}

.range-button:hover,
.range-button[aria-expanded='true'] {
  border-color: var(--primary);
}

.range-button span {
  flex: 1;
  text-align: left;
}

.range-button .rotated {
  transform: rotate(180deg);
}

.picker-popover {
  position: absolute;
  z-index: 30;
  width: 490px;
  padding: 18px;
  background: #102335;
  border: 1px solid var(--border-strong);
  border-radius: var(--radius);
  box-shadow: var(--shadow);
  inset: calc(100% + 8px) 0 auto auto;
}

.picker-heading,
.picker-actions {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.picker-heading > div {
  display: grid;
}

.picker-heading strong {
  font-size: 14px;
}

.picker-heading small {
  margin-top: 2px;
  color: var(--text-muted);
  font-size: 10px;
}

.reset-button {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 7px 8px;
  color: var(--text-muted);
  cursor: pointer;
  background: transparent;
  border: 0;
  border-radius: 5px;
  font-size: 11px;
}

.reset-button:hover {
  color: var(--primary);
  background: var(--primary-soft);
}

.date-fields {
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  align-items: end;
  gap: 10px;
  padding: 18px 0;
}

.date-fields label {
  display: grid;
  gap: 7px;
}

.date-fields label > span {
  color: var(--text-muted);
  font-size: 10px;
  font-weight: 650;
  letter-spacing: 0.04em;
}

.date-fields input {
  width: 100%;
  height: 40px;
  padding: 0 10px;
  color: var(--text);
  background: var(--bg-deep);
  border: 1px solid var(--border-strong);
  border-radius: var(--radius-sm);
  color-scheme: dark;
}

.date-fields input:focus {
  border-color: var(--primary);
  outline: none;
}

.field-separator {
  padding-bottom: 11px;
  color: var(--text-muted);
  font-size: 11px;
}

.picker-actions {
  justify-content: flex-end;
  padding-top: 14px;
  border-top: 1px solid var(--border);
}

.picker-actions button {
  gap: 7px;
  min-height: 36px;
}

.search-button {
  display: inline-flex;
  min-width: 84px;
  min-height: 38px;
  align-items: center;
  justify-content: center;
  gap: 7px;
  padding: 0 14px;
  color: #003337;
  cursor: pointer;
  background: var(--primary);
  border: 1px solid var(--primary);
  border-radius: var(--radius-sm);
  font-size: 12px;
  font-weight: 700;
}

@media (max-width: 1180px) {
  .preset-list {
    display: none;
  }
}

@media (max-width: 720px) {
  .date-filter {
    display: grid;
    grid-template-columns: 1fr auto;
    gap: 10px;
  }

  .filter-label {
    grid-column: 1 / -1;
  }

  .picker-wrap {
    width: 100%;
    min-width: 0;
    margin-left: 0;
  }

  .picker-popover {
    position: fixed;
    width: auto;
    inset: auto 12px 16px;
  }

  .date-fields {
    grid-template-columns: 1fr;
  }

  .field-separator {
    display: none;
  }
}
</style>
