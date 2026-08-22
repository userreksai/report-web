// 默认走前端服务的同域代理，HTTPS 页面不再直连只提供 HTTP 的 10010 端口。
const apiBase = (import.meta.env.VITE_API_BASE_URL || '/api/v1').replace(/\/$/, '')

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
