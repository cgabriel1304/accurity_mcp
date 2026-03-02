import express from 'express'
import { createProxyMiddleware } from 'http-proxy-middleware'
import { fileURLToPath } from 'url'
import { dirname, join } from 'path'

const __dirname = dirname(fileURLToPath(import.meta.url))

const PORT = parseInt(process.env.PORT || '3000', 10)
const HOST = process.env.HOST || '0.0.0.0'
const BACKEND_URL = process.env.BACKEND_URL || 'http://localhost:5000'

const app = express()

// Logging middleware — logs all requests with IP and response status
app.use((req, res, next) => {
  const startTime = Date.now()
  const ip = req.ip || req.connection.remoteAddress || 'unknown'

  // Log when response finishes (covers all response types: send, json, redirect, etc.)
  res.on('finish', () => {
    const duration = Date.now() - startTime
    const logMessage = `[${new Date().toISOString()}] ${req.method} ${req.path} | IP: ${ip} | Status: ${res.statusCode} | ${duration}ms\n`
    process.stdout.write(logMessage)
  })

  next()
})

// Proxy /api to Flask backend
// Using pathFilter (not app.use('/api', ...)) so the full /api/* path is
// preserved when forwarded to Flask — Express would otherwise strip the prefix.
app.use(
  createProxyMiddleware({
    pathFilter: '/api',
    target: BACKEND_URL,
    changeOrigin: true,
    proxyTimeout: 120_000,  // 2 min — allow time for LLM streaming responses
    timeout: 120_000,
    on: {
      error: (err, req, res) => {
        console.error(`[proxy] ${req.method} ${req.path} → ${err.code}: ${err.message}`)
        if (!res.headersSent) {
          res.status(502).json({ error: 'Flask backend unavailable', detail: err.message })
        }
      },
    },
  })
)

// Serve the Vite production build
const distDir = join(__dirname, 'dist')
app.use(express.static(distDir))
console.log(`Using static middleware to serve ${distDir}`)

// SPA fallback — all non-asset routes serve index.html
app.get('*', (_req, res) => {
  res.sendFile(join(distDir, 'index.html'))
})

app.listen(PORT, HOST, () => {
  console.log(`Frontend server listening on port http://${HOST}:${PORT}`)
  console.log(`Proxying /api to ${BACKEND_URL}`)
})
