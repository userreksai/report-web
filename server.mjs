import { createReadStream, existsSync, statSync } from 'node:fs'
import { createServer, request as httpRequest } from 'node:http'
import { request as httpsRequest } from 'node:https'
import { extname, join, normalize } from 'node:path'
import { fileURLToPath } from 'node:url'

const root = join(fileURLToPath(new URL('.', import.meta.url)), 'dist')
const port = Number(process.env.PORT || 8888)
const apiOrigin = new URL(process.env.REPORT_API_ORIGIN || 'http://127.0.0.1:10010')
const apiRequest = apiOrigin.protocol === 'https:' ? httpsRequest : httpRequest

if (!['http:', 'https:'].includes(apiOrigin.protocol)) {
  console.error('REPORT_API_ORIGIN 只支持 http:// 或 https:// 地址')
  process.exit(1)
}

const mimeTypes = {
  '.css': 'text/css; charset=utf-8',
  '.html': 'text/html; charset=utf-8',
  '.ico': 'image/x-icon',
  '.js': 'text/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.png': 'image/png',
  '.svg': 'image/svg+xml',
  '.webp': 'image/webp',
  '.woff2': 'font/woff2',
}

if (!existsSync(join(root, 'index.html'))) {
  console.error('dist/index.html 不存在，请先执行 npm run build')
  process.exit(1)
}

function proxyApi(request, response) {
  const target = new URL(request.url, apiOrigin)
  const headers = { ...request.headers, host: apiOrigin.host }
  delete headers.connection

  const upstreamRequest = apiRequest(
    target,
    {
      method: request.method,
      headers,
    },
    (upstreamResponse) => {
      const responseHeaders = { ...upstreamResponse.headers }
      delete responseHeaders.connection
      delete responseHeaders['keep-alive']
      delete responseHeaders['proxy-authenticate']
      delete responseHeaders['proxy-authorization']
      delete responseHeaders.te
      delete responseHeaders.trailer
      delete responseHeaders['transfer-encoding']
      delete responseHeaders.upgrade
      response.writeHead(upstreamResponse.statusCode || 502, responseHeaders)
      upstreamResponse.pipe(response)
    },
  )

  upstreamRequest.setTimeout(30_000, () => {
    upstreamRequest.destroy(new Error('后端接口响应超时'))
  })
  upstreamRequest.on('error', (error) => {
    console.error(`接口代理失败：${request.method} ${request.url} - ${error.message}`)
    if (response.headersSent) {
      response.destroy(error)
      return
    }
    response.writeHead(502, {
      'Cache-Control': 'no-store',
      'Content-Type': 'application/json; charset=utf-8',
    })
    response.end(JSON.stringify({ error: { message: '后端服务暂时不可用' } }))
  })
  request.pipe(upstreamRequest)
}

createServer((request, response) => {
  const pathname = decodeURIComponent(new URL(request.url, 'http://localhost').pathname)
  if (pathname === '/api' || pathname.startsWith('/api/')) {
    proxyApi(request, response)
    return
  }

  const safePath = normalize(pathname).replace(/^(\.\.(\/|\\|$))+/, '')
  let filePath = join(root, safePath)

  if (!existsSync(filePath) || statSync(filePath).isDirectory()) {
    filePath = join(root, 'index.html')
  }

  const extension = extname(filePath)
  response.setHeader('Content-Type', mimeTypes[extension] || 'application/octet-stream')
  response.setHeader(
    'Cache-Control',
    extension === '.html' ? 'no-cache' : 'public, max-age=31536000, immutable',
  )
  createReadStream(filePath).pipe(response)
}).listen(port, '0.0.0.0', () => {
  console.log(`运维报告中心已启动：http://0.0.0.0:${port}`)
  console.log(`接口代理：/api -> ${apiOrigin.origin}`)
})
