# Session 12 — Kubernetes Ingress, ConfigMaps & Secrets

**Student Name:** Arnav Gupta  
**Enrollment ID:** 24bcs10063  
**Batch / Program:** Software Engineering  
**Student Email:** arnav.24bcs10063@sst.scaler.com  
**Repository:** [SWE-Assignment](https://github.com/de-arnavgupta/SWE-Assignment)  

---

## Task 1: ConfigMap Hands-on Implementation

ConfigMaps allow decoupling configuration artifacts from container image binaries, enabling environment-agnostic portable workloads.

```yaml
# configmap-demo.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  APP_ENV: "production"
  LOG_LEVEL: "info"
  MAX_CONNECTIONS: "150"
  app.properties: |
    cache.ttl=3600
    feature.dark_mode=true
---
apiVersion: v1
kind: Pod
metadata:
  name: config-demo-pod
spec:
  containers:
  - name: test-app
    image: alpine:latest
    command: ["sh", "-c", "echo Env: $APP_ENV; cat /config/app.properties; sleep 3600"]
    env:
    - name: APP_ENV
      valueFrom:
        configMapKeyRef:
          name: app-config
          key: APP_ENV
    volumeMounts:
    - name: config-vol
      mountPath: /config
  volumes:
  - name: config-vol
    configMap:
      name: app-config
```

### Verification Commands & Output
```bash
kubectl apply -f configmap-demo.yaml
kubectl logs config-demo-pod
```
**Output:**
```text
Env: production
cache.ttl=3600
feature.dark_mode=true
```

---

## Task 2: Kubernetes Secrets & Security Policy

Secrets store sensitive credentials (API tokens, database passwords, TLS certificates). Values are base64-encoded in API manifests and injected into memory (`tmpfs` ramdisk mounts) inside Pods.

```yaml
# secret-demo.yaml
apiVersion: v1
kind: Secret
metadata:
  name: db-credentials
type: Opaque
stringData:
  DB_PASSWORD: "SuperSecureDevOpsPassword2026!"
  DB_USER: "arnav_admin"
---
apiVersion: v1
kind: Pod
metadata:
  name: secret-demo-pod
spec:
  containers:
  - name: secure-app
    image: alpine:latest
    command: ["sh", "-c", "echo 'Secret verified in container memory'; sleep 3600"]
    env:
    - name: DATABASE_PASSWORD
      valueFrom:
        secretKeyRef:
          name: db-credentials
          key: DB_PASSWORD
```

### Academic & Enterprise Security Rule: Never Commit Secrets to Git!
> [!CAUTION]
> **Why Kubernetes Secrets Must Never Be Committed to Version Control:**
> Standard Kubernetes Secret YAML files are only **base64 encoded, NOT encrypted**. Anyone with read access to the Git repository can run `echo "c3VwZXI=" | base64 -d` to extract plain-text credentials. In professional production systems:
> 1. Use **External Secrets Operator** (ESO) or HashiCorp Vault.
> 2. Use **Sealed Secrets** (asymmetric encryption where only the cluster's private key can decrypt).
> 3. Use cloud KMS secret managers (AWS Secrets Manager / GCP Secret Manager).

---

## Task 3: Ingress Routing Configuration

An Ingress manages external HTTP/HTTPS routing into cluster Services based on hostnames and URL request paths.

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: web-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /$2
spec:
  rules:
  - host: app.local
    http:
      paths:
      - path: /()(.*)
        pathType: Prefix
        backend:
          service:
            name: frontend-service
            port:
              number: 80
      - path: /api(/|$)(.*)
        pathType: Prefix
        backend:
          service:
            name: backend-service
            port:
              number: 8000
```

### Route Testing via Ingress
```bash
# Test frontend route
curl -H "Host: app.local" http://<INGRESS_IP>/
# Returns React/HTML Frontend

# Test backend API route
curl -H "Host: app.local" http://<INGRESS_IP>/api/health
# Returns {"status":"healthy"}
```

---

## Task 4: Ingress vs. Ingress Controller

| Dimension | Ingress (Resource) | Ingress Controller (Daemon / Pod) |
|---|---|---|
| **What is it?** | A declarative Kubernetes API object (`kind: Ingress`). | The active reverse-proxy software (Pod) running inside the cluster. |
| **Role** | Specifies the desired routing rules (hosts, paths, TLS certs, target services). | Continuously watches the Kubernetes API for Ingress objects and translates them into live proxy configurations. |
| **Execution** | Pure metadata; by itself, **does nothing without a controller**. | Actually intercepts network traffic and routes HTTP/S requests to Pod endpoints. |
| **Popular Implementations** | Standard Kubernetes API specification. | **Ingress-NGINX**, **Traefik**, **AWS Load Balancer Controller (ALB)**, **HAProxy**. |

---

## Task 5: Troubleshooting Scenarios & Fixes

### Scenario: Ingress Returns `503 Service Temporarily Unavailable`
1. **Diagnosis:** `kubectl describe ingress web-ingress` shows valid rules, but browser returns HTTP 503.
2. **Investigation:**
   ```bash
   kubectl get svc backend-service
   kubectl get endpoints backend-service
   # Output: <none> (No backend endpoints registered!)
   ```
3. **Root Cause:** Service selector (`app: backend`) did not match Pod labels (`app: api-backend`).
4. **Fix:** Patched Service selector to match Pod labels:
   ```bash
   kubectl patch svc backend-service -p '{"spec":{"selector":{"app":"api-backend"}}}'
   ```
5. **Verification:** `kubectl get endpoints backend-service` populated with Pod IPs. Ingress curl immediately returned HTTP 200 OK.
