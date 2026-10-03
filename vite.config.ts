import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// the preview tooling hands out a port through PORT; 5173 otherwise
const env = (globalThis as { process?: { env: Record<string, string | undefined> } }).process?.env ?? {}

export default defineConfig({
  plugins: [react()],
  server: { port: Number(env.PORT) || 5173, strictPort: false },
  build: {
    target: 'es2022',
    chunkSizeWarningLimit: 1200,
  },
})
