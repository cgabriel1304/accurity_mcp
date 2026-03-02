import { defineConfig, loadEnv } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig(({ mode }) => {
  // Load the .env file from the frontend directory (empty prefix = load all vars)
  const env = loadEnv(mode, process.cwd(), '')

  const port = parseInt(env.PORT || '3000', 10)
  const backendUrl = env.BACKEND_URL || 'http://localhost:5000'

  return {
    plugins: [react()],
    server: {
      port,
      proxy: {
        '/api': {
          target: backendUrl,
          changeOrigin: true,
        },
      },
    },
    build: {
      outDir: 'dist',
      emptyOutDir: true,
    },
  }
})
