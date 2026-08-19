import { createReadStream, existsSync, statSync } from 'node:fs'
import { createServer } from 'node:http'
import { extname, join, normalize } from 'node:path'
import { fileURLToPath } from 'node:url'

const root = join(fileURLToPath(new URL('.', import.meta.url)), 'dist')
const port = Number(process.env.PORT || 8888)

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

createServer((request, response) => {
  const pathname = decodeURIComponent(new URL(request.url, 'http://localhost').pathname)
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
})
