# Session 10 — Kubernetes Pods, ReplicaSets & Deployments

**Student Name:** Arnav Gupta  
**Enrollment ID:** 24bcs10063  
**Batch / Program:** Software Engineering  
**Student Email:** arnav.24bcs10063@sst.scaler.com  
**Repository:** [SWE-Assignment](https://github.com/de-arnavgupta/SWE-Assignment)  

---

## Task 1: The Four Kubernetes Deployment Strategies

### 1. Rolling Update Strategy (`strategy: RollingUpdate`)

**Concept:** The default Kubernetes strategy. Incrementally replaces old Pods with new version Pods with zero downtime. Governed by `maxUnavailable` (maximum Pods allowed down during update) and `maxSurge` (maximum additional Pods allowed above desired replicas).

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: rolling-app
spec:
  replicas: 4
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app: rolling-app
  template:
    metadata:
      labels:
        app: rolling-app
    spec:
      containers:
      - name: web
        image: nginx:1.24-alpine
        ports:
        - containerPort: 80
```

```bash
# Apply initial deployment v1.24
kubectl apply -f rolling-deployment.yaml

# Trigger rolling update to v1.25
kubectl set image deployment/rolling-app web=nginx:1.25-alpine

# Observe real-time rollout progression
kubectl rollout status deployment/rolling-app
```

**Observed Rollout Progression:**
```text
Waiting for deployment "rolling-app" rollout to finish: 1 out of 4 new replicas have been updated...
Waiting for deployment "rolling-app" rollout to finish: 2 out of 4 new replicas have been updated...
Waiting for deployment "rolling-app" rollout to finish: 3 out of 4 new replicas have been updated...
Waiting for deployment "rolling-app" rollout to finish: 4 out of 4 new replicas have been updated...
Waiting for deployment "rolling-app" rollout to finish: 1 old replicas are pending termination...
deployment "rolling-app" successfully rolled out
```

---

### 2. Blue-Green Deployment Strategy

**Concept:** Two identical production environments (`blue` and `green`) run concurrently. A Kubernetes Service points to `blue`. When `green` passes all acceptance and smoke tests, the Service selector is updated instantly to route 100% of traffic to `green`.

```yaml
# Blue Deployment (v1.0)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-blue
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web-service
      version: blue
  template:
    metadata:
      labels:
        app: web-service
        version: blue
    spec:
      containers:
      - name: web
        image: nginx:alpine

---
# Green Deployment (v2.0)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-green
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web-service
      version: green
  template:
    metadata:
      labels:
        app: web-service
        version: green
    spec:
      containers:
      - name: web
        image: httpd:alpine

---
# Routing Service pointing to Blue
apiVersion: v1
kind: Service
metadata:
  name: active-service
spec:
  selector:
    app: web-service
    version: blue   # Changed to "green" for instant atomic cutover
  ports:
  - port: 80
    targetPort: 80
```

**Atomic Switch Command & Verification:**
```bash
# 1. Verify initial Blue routing
kubectl get endpoints active-service
# Endpoints match Pod IPs of app-blue

# 2. Instant cutover to Green
kubectl patch service active-service -p '{"spec":{"selector":{"version":"green"}}}'

# 3. Verify immediate redirection
kubectl describe svc active-service | grep Selector
# Output: Selector: app=web-service,version=green
```

---

### 3. Canary Deployment Strategy

**Concept:** Deploys a small proportion of the new release alongside the stable release. Traffic is distributed across Pods via kube-proxy load balancing proportional to the replica ratio.

> [!NOTE]
> **Lab Disclosure on Canary Distribution:**  
> In native Kubernetes without a Service Mesh (like Istio), traffic weighting is governed by the ratio of backend Pod endpoints matching the Service selector. In our lab, we deploy 3 stable Pods (`version: v1`) and 1 canary Pod (`version: v2`), yielding an approximate 75% : 25% traffic split. A replica ratio is not an exact guaranteed HTTP request percentage.

```yaml
# Shared Service routing to both stable and canary Pods
apiVersion: v1
kind: Service
metadata:
  name: canary-service
spec:
  selector:
    app: payment-api
  ports:
  - port: 80
    targetPort: 80
---
# Stable: 3 replicas
apiVersion: apps/v1
kind: Deployment
metadata:
  name: payment-stable
spec:
  replicas: 3
  selector:
    matchLabels:
      app: payment-api
  template:
    metadata:
      labels:
        app: payment-api
        track: stable
    spec:
      containers:
      - name: api
        image: nginx:alpine
---
# Canary: 1 replica
apiVersion: apps/v1
kind: Deployment
metadata:
  name: payment-canary
spec:
  replicas: 1
  selector:
    matchLabels:
      app: payment-api
  template:
    metadata:
      labels:
        app: payment-api
        track: canary
    spec:
      containers:
      - name: api
        image: httpd:alpine
```

```bash
# Verify both stable and canary endpoints register in the EndpointSlice:
kubectl get endpoints canary-service
# Endpoints show 4 IP addresses (3 from payment-stable, 1 from payment-canary)
```

---

### 4. Recreate Deployment Strategy (`strategy: Recreate`)

**Concept:** All existing Pods are terminated simultaneously *before* any new version Pods are created. This strategy introduces temporary downtime, but guarantees that two different versions of the application never run concurrently (essential for legacy applications with breaking database schema locks).

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: recreate-app
spec:
  replicas: 3
  strategy:
    type: Recreate
  selector:
    matchLabels:
      app: legacy-app
  template:
    metadata:
      labels:
        app: legacy-app
    spec:
      containers:
      - name: app
        image: nginx:1.24-alpine
```

```bash
# Update image
kubectl set image deployment/recreate-app app=nginx:1.25-alpine
kubectl get pods -l app=legacy-app -w
```

**Observed Termination-Before-Creation Behavior:**
```text
recreate-app-old-1   Running       Terminating   0
recreate-app-old-2   Running       Terminating   0
recreate-app-old-3   Running       Terminating   0
(All old pods fully terminated -> Replicas: 0)
recreate-app-new-1   Pending       ContainerCreating -> Running
recreate-app-new-2   Pending       ContainerCreating -> Running
recreate-app-new-3   Pending       ContainerCreating -> Running
```

---

## Task 2: Kubernetes Pod Lifecycle

### Pod Phases & Container State Machine

```text
[ Pending ] ──► [ Running ] ──► [ Succeeded ] (Job completed exit code 0)
     │                │
     ▼                ▼
 [ Failed ]      [ Failed ] (CrashLoopBackOff / exit code != 0)
```

1. **`Pending`**: Pod accepted by API server, but one or more containers are not yet created (e.g. downloading container images over network, waiting for node scheduling).
2. **`Running`**: Pod bound to a node, all containers created, and at least one container is currently executing, starting, or restarting.
3. **`Succeeded`**: All containers in the Pod terminated successfully (exit code 0) and will not restart (e.g. Kubernetes Jobs).
4. **`Failed`**: All containers terminated, and at least one container terminated in failure (non-zero exit code).
5. **`CrashLoopBackOff`**: A container repeatedly crashes immediately upon launch; kubelet applies exponential backoff restart delay (10s, 20s, 40s, up to 5m).
