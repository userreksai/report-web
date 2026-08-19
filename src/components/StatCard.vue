<script setup>
import { ArrowDownRight, ArrowUpRight, Minus } from '@lucide/vue'

defineProps({
  label: { type: String, required: true },
  value: { type: [String, Number], required: true },
  helper: { type: String, default: '' },
  trend: { type: String, default: '' },
  trendType: { type: String, default: 'up' },
  icon: { type: [Object, Function], required: true },
  tone: { type: String, default: 'primary' },
})
</script>

<template>
  <article class="stat-card" :class="`tone-${tone}`">
    <div class="stat-topline">
      <span class="stat-icon"><component :is="icon" :size="19" /></span>
      <span v-if="trend" class="trend" :class="trendType">
        <ArrowUpRight v-if="trendType === 'up'" :size="13" />
        <ArrowDownRight v-else-if="trendType === 'down'" :size="13" />
        <Minus v-else :size="13" />
        {{ trend }}
      </span>
    </div>
    <p>{{ label }}</p>
    <strong class="data-value">{{ value }}</strong>
    <small>{{ helper }}</small>
  </article>
</template>

<style scoped>
.stat-card {
  min-width: 0;
  padding: 17px;
  background: linear-gradient(145deg, rgba(19, 37, 56, 0.96), rgba(13, 29, 44, 0.98));
  border: 1px solid var(--border);
  border-radius: var(--radius);
  box-shadow: 0 1px 0 rgba(255, 255, 255, 0.025) inset;
}

.stat-topline {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
}

.stat-icon {
  display: grid;
  width: 34px;
  height: 34px;
  color: var(--primary);
  background: var(--primary-soft);
  border-radius: 8px;
  place-items: center;
}

.trend {
  display: inline-flex;
  align-items: center;
  gap: 3px;
  font: 600 10px/1 var(--font-data);
}

.trend.up {
  color: var(--success);
}

.trend.down {
  color: var(--danger);
}

.trend.flat {
  color: var(--text-muted);
}

.stat-card p {
  margin: 14px 0 3px;
  color: var(--text-soft);
  font-size: 12px;
}

.stat-card > strong {
  display: block;
  overflow: hidden;
  font-size: clamp(22px, 2.6vw, 29px);
  line-height: 1.2;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.stat-card > small {
  display: block;
  min-height: 18px;
  margin-top: 7px;
  color: var(--text-muted);
  font-size: 10px;
}

.tone-success .stat-icon {
  color: var(--success);
  background: rgba(49, 209, 139, 0.09);
}

.tone-warning .stat-icon {
  color: var(--warning);
  background: rgba(243, 182, 74, 0.09);
}

.tone-danger .stat-icon {
  color: var(--danger);
  background: rgba(255, 107, 118, 0.09);
}
</style>
