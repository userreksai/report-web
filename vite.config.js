import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    host: '0.0.0.0',
    port: 8888,
    strictPort: true,
    proxy: {
      '/api': 'http://127.0.0.1:10010',
    },
  },
  preview: {
    host: '0.0.0.0',
    port: 8888,
    strictPort: true,
  },
})
