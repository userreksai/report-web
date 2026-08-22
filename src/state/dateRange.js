import { reactive } from 'vue'

const storageKey = 'ops-report-date-range'

export function formatLocalDate(date) {
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  return `${year}-${month}-${day}`
}

function shiftDate(date, days) {
  const next = new Date(date)
  next.setDate(next.getDate() + days)
  return formatLocalDate(next)
}

function defaultRange() {
  const today = new Date()
  return {
    start: shiftDate(today, -29),
    end: formatLocalDate(today),
    preset: '近 30 天',
  }
}

function restoreRange() {
  const fallback = defaultRange()
  try {
    const saved = JSON.parse(sessionStorage.getItem(storageKey))
    if (/^\d{4}-\d{2}-\d{2}$/.test(saved?.start) && /^\d{4}-\d{2}-\d{2}$/.test(saved?.end)) {
      return { start: saved.start, end: saved.end, preset: saved.preset || '' }
    }
  } catch {
    // 无效的会话数据直接使用默认时间范围。
  }
  return fallback
}

const restored = restoreRange()

export const dateRange = reactive({
  ...restored,
  revision: 0,
})

function persist() {
  sessionStorage.setItem(
    storageKey,
    JSON.stringify({ start: dateRange.start, end: dateRange.end, preset: dateRange.preset }),
  )
}

export function applyDateRange(start, end, preset = '') {
  if (!start || !end) return false
  const [normalizedStart, normalizedEnd] = start <= end ? [start, end] : [end, start]
  dateRange.start = normalizedStart
  dateRange.end = normalizedEnd
  dateRange.preset = preset
  dateRange.revision += 1
  persist()
  return true
}

export function applyPreset(label) {
  const today = new Date()
  const end = formatLocalDate(today)
  if (label === '本月') {
    return applyDateRange(formatLocalDate(new Date(today.getFullYear(), today.getMonth(), 1)), end, label)
  }
  const days = { '近 7 天': 7, '近 30 天': 30, '近 90 天': 90 }[label]
  if (!days) return false
  return applyDateRange(shiftDate(today, -(days - 1)), end, label)
}

export function refreshDateRange() {
  dateRange.revision += 1
}
