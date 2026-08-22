<script setup>
import { computed } from 'vue'
import { Clock3, Info, RadioTower } from '@lucide/vue'

const props = defineProps({
  meta: { type: Object, default: null },
})

const updatedAt = computed(() => formatTimestamp(props.meta?.updated_at))
const sourceUpdatedAt = computed(() => formatTimestamp(props.meta?.source_updated_at))
const sources = computed(() => props.meta?.sources?.join('、') || '暂无已上报的数据源')

function formatTimestamp(value) {
  if (!value) return '暂无'
  const date = new Date(value)
  if (Number.isNaN(date.getTime())) return value
  return new Intl.DateTimeFormat('zh-CN', {
    year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false,
  }).format(date)
}
</script>

<template>
  <aside v-if="meta" class="data-provenance">
    <span><Clock3 :size="14" /><b>数据更新时间</b>{{ updatedAt }}</span>
    <span><RadioTower :size="14" /><b>数据来源</b>{{ sources }}</span>
    <span class="methodology" :title="meta.methodology"><Info :size="14" /><b>统计口径</b>{{ meta.methodology }}</span>
    <small v-if="sourceUpdatedAt !== '暂无'">源系统最新时间：{{ sourceUpdatedAt }} · {{ meta.timezone }}</small>
  </aside>
</template>

<style scoped>
.data-provenance {
  display: grid;
  grid-template-columns: auto auto minmax(260px, 1fr);
  gap: 7px 18px;
  padding: 10px 13px;
  color: var(--text-muted);
  background: rgba(5, 15, 25, 0.38);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  font-size: 10px;
}

.data-provenance span {
  display: flex;
  min-width: 0;
  align-items: center;
  gap: 6px;
}

.data-provenance svg {
  flex: 0 0 auto;
  color: var(--primary);
}

.data-provenance b {
  color: var(--text-soft);
  font-weight: 600;
  white-space: nowrap;
}

.methodology {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.data-provenance small {
  grid-column: 1 / -1;
  color: var(--text-muted);
  font-size: 9px;
}

@media (max-width: 900px) {
  .data-provenance { grid-template-columns: 1fr; }
  .data-provenance small { grid-column: auto; }
  .methodology { white-space: normal; }
}
</style>
