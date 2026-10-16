# Session 6 — Docker Fundamentals: 6 Hello World Web Applications

**Student Name:** Arnav Gupta  
**Enrollment ID:** 24bcs10063  
**Batch / Program:** Software Engineering  
**Student Email:** arnav.24bcs10063@sst.scaler.com  
**Repository:** [SWE-Assignment](https://github.com/de-arnavgupta/SWE-Assignment)  

---

## 1. Application Inventory & Container Matrix

Every application has been created in its own dedicated, case-sensitive directory, equipped with custom application logic, Dockerfile, non-root security considerations, and tested endpoints.

| Application Folder | Technology Stack | Base Image | Container Port | Host Port | Verified Endpoint |
|---|---|---|---|---|---|
| `nodejs-app/` | Node.js 20 + Express | `node:20-alpine` | 3000 | 3001 | `http://localhost:3001/` |
| `python-app/` | Python 3.11 + Flask | `python:3.11-slim` | 5000 | 5001 | `http://localhost:5001/` |
| `java-app/` | Java 17 Temurin (JDK/JRE) | `eclipse-temurin:17-jre-alpine` | 8080 | 8081 | `http://localhost:8081/` |
| `Apache-app/` | Apache HTTP Server 2.4 | `httpd:2.4-alpine` | 80 | 8082 | `http://localhost:8082/` |
| `React-app/` | React 18 + Nginx Server | `nginx:alpine` | 80 | 8083 | `http://localhost:8083/` |
| `nginx-app/` | Nginx Web Server | `nginx:alpine` | 80 | 8084 | `http://localhost:8084/` |

---

## 2. Build & Execution Commands for Each Application

### 1. Node.js Application (`nodejs-app/`)
```bash
cd session6-7-docker/nodejs-app
docker build -t arnav-nodejs-app:1.0 .
docker run -d --name c-nodejs -p 3001:3000 arnav-nodejs-app:1.0
curl -i http://localhost:3001/
```
**Response:** `Hello World from Node.js Application! - Arnav Gupta (24bcs10063)`

### 2. Python Application (`python-app/`)
```bash
cd session6-7-docker/python-app
docker build -t arnav-python-app:1.0 .
docker run -d --name c-python -p 5001:5000 arnav-python-app:1.0
curl -i http://localhost:5001/
```
**Response:** `Hello World from Python Flask Application! - Arnav Gupta (24bcs10063)`

### 3. Java Application (`java-app/`)
```bash
cd session6-7-docker/java-app
docker build -t arnav-java-app:1.0 .
docker run -d --name c-java -p 8081:8080 arnav-java-app:1.0
curl -i http://localhost:8081/
```
**Response:** `Hello World from Java Application! - Arnav Gupta (24bcs10063)`

### 4. Apache Web Server (`Apache-app/`)
```bash
cd session6-7-docker/Apache-app
docker build -t arnav-apache-app:1.0 .
docker run -d --name c-apache -p 8082:80 arnav-apache-app:1.0
curl -i http://localhost:8082/
```
**Response:** `Hello World from Apache HTTP Server! - Arnav Gupta (24bcs10063)`

### 5. React Application (`React-app/`)
```bash
cd session6-7-docker/React-app
docker build -t arnav-react-app:1.0 .
docker run -d --name c-react -p 8083:80 arnav-react-app:1.0
curl -i http://localhost:8083/
```
**Response:** `Hello World from React Application! - Arnav Gupta (24bcs10063)`

### 6. Nginx Web Server (`nginx-app/`)
```bash
cd session6-7-docker/nginx-app
docker build -t arnav-nginx-app:1.0 .
docker run -d --name c-nginx -p 8084:80 arnav-nginx-app:1.0
curl -i http://localhost:8084/
```
**Response:** `Hello World from Nginx Web Server! - Arnav Gupta (24bcs10063)`

---

## 3. Scoped Cleanup

```bash
docker stop c-nodejs c-python c-java c-apache c-react c-nginx
docker rm c-nodejs c-python c-java c-apache c-react c-nginx
docker rmi arnav-nodejs-app:1.0 arnav-python-app:1.0 arnav-java-app:1.0 arnav-apache-app:1.0 arnav-react-app:1.0 arnav-nginx-app:1.0
```
