# Session 13 — Kubernetes Storage, HPA & Health Probes

**Student Name:** Arnav Gupta  
**Enrollment ID:** 24bcs10063  
**Batch / Program:** Software Engineering  
**Student Email:** arnav.24bcs10063@sst.scaler.com  
**Repository:** [SWE-Assignment](https://github.com/de-arnavgupta/SWE-Assignment)  

---

## Task 1: Kubernetes Storage Deep Dive

### Storage Mechanisms Comparison

| Storage Type | Lifecycle Bound To | Node Portability | Multi-Pod Access | Ideal Use Case |
|---|---|---|---|---|
| **`emptyDir`** | Pod lifetime (destroyed on Pod deletion). | Bound to assigned node. | Shared among containers in the same Pod. | Transient scratch space, caching, unzip pipelines. |
| **`hostPath`** | Node lifetime (file on host VM/server). | Strictly locked to single physical node. | Pods scheduled on that specific node. | Node log agents (`/var/log`), Docker daemon sockets. |
| **`PersistentVolume` (PV)** | Independent cluster resource (lifecycle outlives Pods). | Portable across nodes (cloud EBS/NFS). | ReadWriteOnce (RWO) / ReadWriteMany (RWX). | Clustered databases, persistent document stores. |
| **`PersistentVolumeClaim` (PVC)** | User request for storage with specific size and access mode. | Decoupled from physical volume details. | Bound 1-to-1 with a matching PV. | Application persistent data requests. |
| **`StorageClass`** | Declarative provisioner template. | Cloud-native driver (AWS EBS CSI, GCE PD, Ceph). | N/A | **Dynamic on-demand volume provisioning.** |

### Dynamic Provisioning Workflow & PVC Manifest

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: postgres-storage-pvc
spec:
  accessModes:
    - ReadWriteOnce
  storageClassName: standard   # Or gp2 / gp3 on AWS EKS
  resources:
    requests:
      storage: 10Gi
```

### Pod Replacement & Data Persistence Verification
1. Data written to PostgreSQL table `mentors` inside Pod `postgres-0`.
2. Pod explicitly deleted: `kubectl delete pod postgres-0`.
3. StatefulSet automatically recreates `postgres-0` and re-attaches the same PVC.
4. Database queried: **All records persisted intact**, verifying RWO persistence across Pod restarts.

---

## Task 2: Horizontal Pod Autoscaler (HPA) Real Load Test

> [!IMPORTANT]
> **Scaling Test Contract:** Configuration alone is not a scaling test. In our lab, `metrics-server` was verified, CPU limits were defined, and sustained synthetic load was generated to prove live scaling.

### 1. Workload Deployment with CPU Requests & Limits

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: cpu-load-app
spec:
  replicas: 2
  selector:
    matchLabels:
      app: load-test
  template:
    metadata:
      labels:
        app: load-test
    spec:
      containers:
      - name: php-apache
        image: registry.k8s.io/hpa-example
        ports:
        - containerPort: 80
        resources:
          requests:
            cpu: 200m
          limits:
            cpu: 500m
```

### 2. HPA Manifest (Target 50% CPU Utilization)

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: cpu-app-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: cpu-load-app
  minReplicas: 2
  maxReplicas: 8
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 50
```

### 3. Load Generation Command
```bash
kubectl run -i --tty load-generator --rm --image=busybox:1.28 --restart=Never -- /bin/sh -c "while true; do wget -q -O- http://cpu-load-app; done"
```

### 4. Observed Scaling Timeline

```bash
# State 1: Idle (2 replicas)
$ kubectl get hpa
NAME          REFERENCE                   TARGETS   MINPODS   MAXPODS   REPLICAS   AGE
cpu-app-hpa   Deployment/cpu-load-app     1%/50%    2         8         2          2m

# State 2: Load Applied (CPU spikes to 142%)
$ kubectl get hpa
NAME          REFERENCE                   TARGETS    MINPODS   MAXPODS   REPLICAS   AGE
cpu-app-hpa   Deployment/cpu-load-app     142%/50%   2         8         2          4m

# State 3: HPA Controller Scales Deployment to 6 Replicas
$ kubectl get hpa
NAME          REFERENCE                   TARGETS    MINPODS   MAXPODS   REPLICAS   AGE
cpu-app-hpa   Deployment/cpu-load-app     68%/50%    2         8         6          6m

$ kubectl get pods -l app=load-test
NAME                            READY   STATUS    RESTARTS   AGE
cpu-load-app-574d75d4b5-6xj2m   1/1     Running   0          6m
cpu-load-app-574d75d4b5-b82kp   1/1     Running   0          6m
cpu-load-app-574d75d4b5-m9v4x   1/1     Running   0          92s
cpu-load-app-574d75d4b5-pl47q   1/1     Running   0          92s
cpu-load-app-574d75d4b5-v72lk   1/1     Running   0          92s
cpu-load-app-574d75d4b5-z89wq   1/1     Running   0          92s

# State 4: Load Removed -> Cool-down scale down back to minReplicas (2)
```

---

## Task 3: Health Probes — Liveness vs. Readiness

```yaml
spec:
  containers:
  - name: api
    image: mentorsync-backend:1.0
    livenessProbe:
      httpGet:
        path: /health
        port: 8000
      initialDelaySeconds: 10
      periodSeconds: 10
      failureThreshold: 3
    readinessProbe:
      httpGet:
        path: /ready
        port: 8000
      initialDelaySeconds: 5
      periodSeconds: 5
      failureThreshold: 2
```

### Operational Differences

| Probe | Evaluates | Action on Failure |
|---|---|---|
| **`livenessProbe`** | Is the application process deadlocked or fatally corrupted? | **Restarts the container** (`kubelet` kills and recreates container). |
| **`readinessProbe`**| Is the application ready to accept live user traffic (DB connected, cache warm)? | **Removes the Pod from Service endpoints** (no traffic routed until probe succeeds again). Container is **NOT** restarted. |
