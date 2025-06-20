import path from 'node:path'

import react from '@vitejs/plugin-react-swc'
import observerPlugin from 'mobx-react-observer/swc-plugin'
import { defineConfig } from 'vite'

export default defineConfig({
  plugins: [
    react({
      plugins: [
        observerPlugin(),
      ],
    }),
  ],
  resolve: {
    alias: {
      '@': path.resolve(import.meta.dirname, 'src'),
    },
  },
  server: {
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000/',
        changeOrigin: true,
      },
    },
  },
})
