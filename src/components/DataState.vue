<script setup>
import { CircleAlert, DatabaseZap, LoaderCircle, RotateCcw } from '@lucide/vue'

defineProps({
  loading: Boolean,
  error: { type: String, default: '' },
  empty: Boolean,
})

defineEmits(['retry'])
</script>

<template>
  <section v-if="loading" class="query-state panel" aria-live="polite">
    <LoaderCircle :size="24" class="state-spinner" />
    <strong>正在查询当前时间范围</strong>
    <span>正在汇总数据，请稍候…</span>
  </section>
  <section v-else-if="error" class="query-state error-state panel" role="alert">
    <CircleAlert :size="24" />
    <strong>数据加载失败</strong>
    <span>{{ error }}</span>
    <button class="secondary-button" @click="$emit('retry')"><RotateCcw :size="15" />重新查询</button>
  </section>
  <section v-else-if="empty" class="query-state panel" aria-live="polite">
    <DatabaseZap :size="24" />
    <strong>当前时间范围暂无数据</strong>
    <span>可切换时间范围，或请数据提供部门确认是否已完成上报。</span>
  </section>
  <slot v-else />
</template>

<style scoped>
.query-state {
  display: grid;
  min-height: 220px;
  place-items: center;
  align-content: center;
  gap: 8px;
  color: var(--text-muted);
  text-align: center;
}

.query-state strong {
  color: var(--text);
  font-size: 14px;
}

.query-state span {
  max-width: 520px;
  font-size: 11px;
}

.query-state > svg {
  color: var(--primary);
}

.query-state.error-state > svg {
  color: var(--danger);
}

.query-state .secondary-button {
  gap: 7px;
  margin-top: 7px;
}

.state-spinner {
  animation: spin 0.9s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>
