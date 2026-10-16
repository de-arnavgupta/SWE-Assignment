# Session 14 — Kubernetes Troubleshooting Runbook

**Student Name:** Arnav Gupta  
**Enrollment ID:** 24bcs10063  
**Batch / Program:** Software Engineering  
**Student Email:** arnav.24bcs10063@sst.scaler.com  
**Repository:** [SWE-Assignment](https://github.com/de-arnavgupta/SWE-Assignment)  

---

## 1. Essential Diagnostic Toolset

| Diagnostic Command | Specific Troubleshooting Purpose |
|---|---|
| `kubectl get pods -o wide` | Identify node assignment, Pod IP, restart count, and current phase. |
| `kubectl describe pod <name>` | **Primary diagnostic tool**: Reveals exact lifecycle events, probe failures, scheduling errors, and image pull events. |
| `kubectl logs <name> --previous` | Inspect application stderr/stdout from a *crashed* container instance prior to restart. |
| `kubectl get events --sort-by='.metadata.creationTimestamp'` | Cluster-wide event timeline (scheduling, pulling, evictions, failures). |
| `kubectl top nodes` / `top pods` | Real-time CPU/Memory consumption vs requests/limits. |
| `kubectl exec -it <name> -- sh` | Live interactive inspection of environment variables, local filesystem, and network reachability. |

---

## 2. Common Scenarios: Root Cause Analysis & Solutions

### Scenario 1: `CrashLoopBackOff`
- **Symptom:** Pod starts, immediately crashes, restarts, and enters exponential backoff.
- **Investigation:**
  ```bash
  kubectl logs broken-pod --previous
  ```
  *Output:* `Fatal error: Database connection string DATABASE_URL is not set.`
- **Root Cause:** Application binary expected environment variable `DATABASE_URL` which was omitted from the PodSpec.
- **Solution & Verification:** Injected missing environment variable via `ConfigMapKeyRef`. Pod transitioned to `1/1 Running`.

---

### Scenario 2: `ImagePullBackOff` / `ErrImagePull`
- **Symptom:** Pod remains stuck in `ImagePullBackOff` with 0 restarts.
- **Investigation:**
  ```bash
  kubectl describe pod broken-image-pod | grep -A 5 Events
  ```
  *Output:* `Failed to pull image "ghcr.io/de-arnavgupta/private-app:v1": rpc error: code = Unknown desc = failed to pull and unpack image ... unauthorized`
- **Root Cause:** Container image hosted in private GHCR registry without `imagePullSecrets` configured in the namespace.
- **Solution:** Created docker-registry secret and attached `imagePullSecrets: [{name: ghcr-secret}]` in the PodSpec. Image pulled successfully.

---

### Scenario 3: `Pending` Pod (Unschedulable)
- **Symptom:** Pod remains in `Pending` indefinitely; no node assigned.
- **Investigation:**
  ```bash
  kubectl describe pod pending-pod | grep Events
  ```
  *Output:* `0/2 nodes are available: 2 Insufficient cpu.`
- **Root Cause:** Pod requested `cpu: "4000m"` (4 vCPUs) on a 2-node cluster with only 2 vCPUs per node.
- **Solution:** Scaled down `requests.cpu` to `250m`. `kube-scheduler` scheduled the Pod within 2 seconds.

---

### Scenario 4: Service Connectivity Failure (`Connection Refused`)
- **Symptom:** Upstream clients curling `http://backend-svc:8000` receive `Connection Refused`.
- **Investigation:**
  ```bash
  kubectl get endpoints backend-svc
  # Output: backend-svc   <none>
  kubectl get pods --show-labels
  ```
- **Root Cause:** Service `spec.selector` had `app: api-server`, while Deployment Pods had `app: backend-api`.
- **Solution:** Corrected selector in Service YAML to match `app: backend-api`. Endpoints immediately registered Pod IPs.

---

### Scenario 5: `OOMKilled` (Exit Code 137)
- **Symptom:** Pod crashes intermittently under peak traffic with `Exit Code 137`.
- **Investigation:**
  ```bash
  kubectl describe pod memory-leak-pod | grep -E "Last State|Reason|Exit Code"
  ```
  *Output:* `Reason: OOMKilled, Exit Code: 137`
- **Root Cause:** Container memory usage exceeded `limits.memory: "128Mi"`; kernel cgroup OOM killer terminated the process (SIGKILL = 128 + 9 = 137).
- **Solution:** Increased `limits.memory: "512Mi"` and patched memory leak in application caching layer.
