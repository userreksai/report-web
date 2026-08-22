import { computed, onBeforeUnmount, ref, watch } from 'vue'
import { dateRange } from '../state/dateRange'
import { getReport } from '../services/api'

export function useOpsData(endpoint, extraParams = () => ({})) {
  const data = ref(null)
  const meta = ref(null)
  const loading = ref(false)
  const error = ref('')
  let controller

  const empty = computed(() => !loading.value && !error.value && (meta.value?.record_count ?? 0) === 0)

  async function load() {
    controller?.abort()
    const requestController = new AbortController()
    controller = requestController
    loading.value = true
    error.value = ''
    data.value = null
    meta.value = null
    try {
      const response = await getReport(
        endpoint,
        {
          start_date: dateRange.start,
          end_date: dateRange.end,
          ...extraParams(),
        },
        requestController.signal,
      )
      data.value = response.data
      meta.value = response.meta
    } catch (requestError) {
      if (requestError.name !== 'AbortError') {
        error.value = requestError.message || '暂时无法获取数据'
      }
    } finally {
      if (!requestController.signal.aborted && controller === requestController) loading.value = false
    }
  }

  watch(
    () => [dateRange.revision, JSON.stringify(extraParams())],
    load,
    { immediate: true },
  )

  onBeforeUnmount(() => controller?.abort())

  return { data, meta, loading, error, empty, reload: load }
}
