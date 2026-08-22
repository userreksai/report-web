const defaultApiBase = import.meta.env.DEV
  ? '/api/v1'
  : `${window.location.protocol}//${window.location.hostname}:10010/api/v1`
const apiBase = (import.meta.env.VITE_API_BASE_URL || defaultApiBase).replace(/\/$/, '')

export async function getReport(endpoint, params = {}, signal) {
  const query = new URLSearchParams()
  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined && value !== null && value !== '') query.set(key, String(value))
  })
  const response = await fetch(`${apiBase}/${endpoint}?${query.toString()}`, {
    headers: { Accept: 'application/json' },
    signal,
  })
  const payload = await response.json().catch(() => null)
  if (!response.ok) {
    throw new Error(payload?.error?.message || `请求失败（HTTP ${response.status}）`)
  }
  return payload
}
