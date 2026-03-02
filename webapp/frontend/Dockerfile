# Stage 1 — build the Vite app
FROM node:20-alpine AS builder

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci


COPY . .
RUN npm run build

# Stage 2 — serve with Express
FROM node:20-alpine

WORKDIR /app

# Install only production dependencies
COPY package.json package-lock.json ./
RUN npm ci --omit=dev

COPY server.js ./
COPY --from=builder /app/dist ./dist

ENV PORT=3000
ENV BACKEND_URL=http://localhost:5000

EXPOSE 3000

# In Docker, env vars come from docker-compose env_file + environment
# For local dev, use: npm run serve  (loads .env via --env-file)
CMD ["node", "server.js"]
