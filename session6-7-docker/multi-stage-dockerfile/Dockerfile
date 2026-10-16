# -------------------------
# Stage 1: Build & Dependencies
# -------------------------
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install --omit=dev
COPY . .

# -------------------------
# Stage 2: Minimal Production Runtime
# -------------------------
FROM node:20-alpine AS production
WORKDIR /app

# Run as non-root user
USER node

COPY --chown=node:node --from=builder /app/package*.json ./
COPY --chown=node:node --from=builder /app/node_modules ./node_modules
COPY --chown=node:node --from=builder /app/server.js ./server.js

ENV PORT=8080
EXPOSE 8080

CMD ["node", "server.js"]