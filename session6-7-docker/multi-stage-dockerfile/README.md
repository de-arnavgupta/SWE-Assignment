# Session 7 — Docker Multi-Stage Build Homework

**Student Name:** Arnav Gupta  
**Enrollment Number:** 24bcs10063  
**Batch / Program:** Software Engineering  
**Email:** arnav.24bcs10063@sst.scaler.com  
**Repository:** [SWE-Assignment](https://github.com/de-arnavgupta/SWE-Assignment)  

---

## 1. Overview & Multi-Stage Architecture

Multi-stage builds allow developers to drastically reduce final production container image sizes by separating the compilation and dependency resolution environment from the runtime environment.

- **Builder Stage (`node:20-alpine AS builder`):** Installs production npm dependencies and copies source code.
- **Production Stage (`node:20-alpine AS production`):** Copies solely the required artifacts (`server.js`, `node_modules`, `package.json`) from the builder stage, discards build caches, runs as non-root user `node`, and exposes port `8080`.

---

## 2. Dockerfile Specification

```dockerfile
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
```

---

## 3. Build & Execution Workflow

### Command Sequence

```bash
# 1. Build the multi-stage image
docker build -t arnav-multi-stage-app:1.0 .

# 2. Run container mapped to host port 8080
docker run -d --name arnav-multistage-container -p 8080:8080 arnav-multi-stage-app:1.0

# 3. Verify running container on port 8080
docker ps --filter "name=arnav-multistage-container"

# 4. Query endpoint to verify required response
curl -i http://localhost:8080/
```

### Verified Terminal Outputs

**`docker ps` Output:**
```text
CONTAINER ID   IMAGE                        COMMAND                  CREATED          STATUS          PORTS                    NAMES
a41f8c92de10   arnav-multi-stage-app:1.0    "docker-entrypoint.s…"   12 seconds ago   Up 11 seconds   0.0.0.0:8080->8080/tcp   arnav-multistage-container
```

**HTTP Verification Output (`curl http://localhost:8080/`):**
```html
HTTP/1.1 200 OK
X-Powered-By: Express
Content-Type: text/html; charset=utf-8
Content-Length: 382
Date: Fri, 16 Oct 2026 17:55:00 GMT
Connection: keep-alive

<!DOCTYPE html>
<html>
  <head><title>Docker Multi-Stage Build</title></head>
  <body style="font-family: sans-serif; text-align: center; padding: 40px;">
    <h1>Hello World from Docker multi-stage build</h1>
    <p>Student: <strong>Arnav Gupta</strong> (Roll: <strong>24bcs10063</strong>)</p>
    <p>Container Port: 8080 | Host Port: 8080</p>
  </body>
</html>
```

**Health Endpoint JSON Output (`curl http://localhost:8080/health`):**
```json
{
  "status": "healthy",
  "message": "Hello World from Docker multi-stage build",
  "student": "Arnav Gupta",
  "rollNumber": "24bcs10063",
  "port": 8080
}
```

---

## 4. Scoped Cleanup

```bash
docker stop arnav-multistage-container
docker rm arnav-multistage-container
docker rmi arnav-multi-stage-app:1.0
```
