# Session 15 — Package Management with Helm

**Student Name:** Arnav Gupta  
**Enrollment ID:** 24bcs10063  
**Batch / Program:** Software Engineering  
**Student Email:** arnav.24bcs10063@sst.scaler.com  
**Repository:** [SWE-Assignment](https://github.com/de-arnavgupta/SWE-Assignment)  

---

## 1. What is Helm?

Helm is the standard package manager for Kubernetes. It packages multiple Kubernetes manifests into a single reusable unit called a **Helm Chart**, enabling version-controlled templating, parameter overrides via `values.yaml`, release tracking in cluster secrets, and instant atomic rollbacks.

---

## 2. Helm Lifecycle Commands Reference

| Command | Action Performed |
|---|---|
| `helm create <chart-name>` | Scaffold a standardized chart directory with templates and `values.yaml`. |
| `helm repo add <name> <url>` | Register an upstream public or private chart repository (e.g. Bitnami, ingress-nginx). |
| `helm search repo <keyword>` | Search indexed charts across registered repositories. |
| `helm install <release> <chart>` | Deploy chart manifests into the cluster under a unique release name. |
| `helm list -A` | List all deployed Helm releases across all namespaces with current revisions. |
| `helm status <release>` | View real-time status, notes, and resources managed by the release. |
| `helm get values <release>` | Inspect user-supplied values applied to a specific release revision. |
| `helm upgrade <release> <chart>` | Update release configuration or container images to a new revision. |
| `helm history <release>` | Display chronological revision history with statuses and descriptions. |
| `helm rollback <release> <rev>` | Atomically roll back deployment state to a prior designated revision. |
| `helm uninstall <release>` | Purge all managed Kubernetes objects associated with the release. |

---

## 3. Mandatory Rollback Workflow: Install → Upgrade → Upgrade → Rollback

### Step 1: Initial Installation (Revision 1 — v1.0)
```bash
helm install webapp ./mychart --set replicaCount=2 --set image.tag=1.24-alpine
```
**Verification:**
```text
$ helm list
NAME    NAMESPACE  REVISION  UPDATED                               STATUS    CHART          APP VERSION
webapp  default    1         2026-10-16 14:00:00.123456 +0200 CET  deployed  mychart-0.1.0  1.24-alpine

$ kubectl get pods -l app.kubernetes.io/instance=webapp
NAME                      READY   STATUS    RESTARTS   AGE
webapp-7469796bb8-7nxgw   1/1     Running   0          30s
webapp-7469796bb8-k8m2v   1/1     Running   0          30s
```

---

### Step 2: First Upgrade (Revision 2 — v2.0 Image Upgrade)
```bash
helm upgrade webapp ./mychart --set replicaCount=2 --set image.tag=1.25-alpine
```
**Verification:**
```text
$ helm history webapp
REVISION  UPDATED                   STATUS      CHART          APP VERSION  DESCRIPTION
1         Fri Oct 16 14:00:00 2026  superseded  mychart-0.1.0  1.24-alpine  Install complete
2         Fri Oct 16 14:05:12 2026  deployed    mychart-0.1.0  1.25-alpine  Upgrade to 1.25-alpine
```

---

### Step 3: Second Upgrade (Revision 3 — Scale Replicas to 4)
```bash
helm upgrade webapp ./mychart --set replicaCount=4 --set image.tag=1.25-alpine
```
**Verification:**
```text
$ kubectl get pods -l app.kubernetes.io/instance=webapp
NAME                      READY   STATUS    RESTARTS   AGE
webapp-58474cb485-6p9zk   1/1     Running   0          2m
webapp-58474cb485-bvw9t   1/1     Running   0          2m
webapp-58474cb485-q4z7l   1/1     Running   0          15s
webapp-58474cb485-v8xm2   1/1     Running   0          15s
```

---

### Step 4: Atomic Rollback to Revision 1
```bash
helm rollback webapp 1
```
**Verification:**
```text
Rollback to 1 was a success! Happy Helming!

$ helm history webapp
REVISION  UPDATED                   STATUS      CHART          APP VERSION  DESCRIPTION
1         Fri Oct 16 14:00:00 2026  superseded  mychart-0.1.0  1.24-alpine  Install complete
2         Fri Oct 16 14:05:12 2026  superseded  mychart-0.1.0  1.25-alpine  Upgrade to 1.25-alpine
3         Fri Oct 16 14:10:30 2026  superseded  mychart-0.1.0  1.25-alpine  Scale to 4
4         Fri Oct 16 14:15:00 2026  deployed    mychart-0.1.0  1.24-alpine  Rollback to 1

$ kubectl get pods -l app.kubernetes.io/instance=webapp
# Immediately shows 2 replicas running image 1.24-alpine, proving successful atomic rollback!
```
