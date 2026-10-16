# Session 11 — Kubernetes Networking & Services

**Student Name:** Arnav Gupta  
**Enrollment ID:** 24bcs10063  
**Batch / Program:** Software Engineering  
**Student Email:** arnav.24bcs10063@sst.scaler.com  
**Repository:** [SWE-Assignment](https://github.com/de-arnavgupta/SWE-Assignment)  

---

## Task 1: The 5 Kubernetes Service Types

A Kubernetes Service is an abstract way to expose an application running on a set of Pods as a network service with a stable IP and DNS name, decoupling consumers from ephemeral Pod IP addresses.

### 1. `ClusterIP` (Default)
- **Scope:** Internal to the cluster only.
- **Mechanics:** `kube-proxy` provisions a virtual IP from the service-cluster-ip-range. Traffic is routed via iptables or IPVS to matching Pod IPs.
- **YAML & Test:**
  ```yaml
  apiVersion: v1
  kind: Service
  metadata:
    name: internal-api-svc
  spec:
    type: ClusterIP
    selector:
      app: api-backend
    ports:
    - port: 8080
      targetPort: 8080
  ```

### 2. `NodePort`
- **Scope:** Accessible externally via `<NodeIP>:<NodePort>`.
- **Mechanics:** Allocates a static port across every node in the cluster from the range `30000-32767`. Any node receiving traffic on this port automatically routes it to the target Service.
- **YAML:**
  ```yaml
  apiVersion: v1
  kind: Service
  metadata:
    name: web-nodeport-svc
  spec:
    type: NodePort
    selector:
      app: frontend
    ports:
    - port: 80
      targetPort: 80
      nodePort: 31080
  ```

### 3. `LoadBalancer`
- **Scope:** External public access via Cloud Provider Load Balancer (e.g. AWS NLB/ALB, GCP Cloud Load Balancing).
- **Technical Rigor Note:** In bare-metal or local Minikube without `minikube tunnel` or MetalLB, LoadBalancer services remain in `<pending>` status. A pending LoadBalancer or a local ClusterIP curl is not proof of external cloud load balancing.
- **YAML:**
  ```yaml
  apiVersion: v1
  kind: Service
  metadata:
    name: public-lb-svc
  spec:
    type: LoadBalancer
    selector:
      app: frontend
    ports:
    - port: 80
      targetPort: 80
  ```

### 4. `ExternalName`
- **Scope:** CNAME redirection to an external third-party domain outside the cluster.
- **Mechanics:** Does not define selectors or proxy traffic; CoreDNS returns a CNAME record directly pointing to the external hostname.
- **YAML:**
  ```yaml
  apiVersion: v1
  kind: Service
  metadata:
    name: stripe-gateway
  spec:
    type: ExternalName
    externalName: api.stripe.com
  ```

### 5. `Headless` (`clusterIP: None`)
- **Scope:** Direct Pod IP resolution without load balancing or proxying.
- **Mechanics:** CoreDNS returns A-records for all healthy individual Pod IPs matching the selector. Crucial for stateful distributed databases (Cassandra, Kafka, PostgreSQL master-replica).
- **YAML:**
  ```yaml
  apiVersion: v1
  kind: Service
  metadata:
    name: db-headless-svc
  spec:
    clusterIP: None
    selector:
      app: postgres
    ports:
    - port: 5432
      targetPort: 5432
  ```

---

## Task 2: Architectural Comparisons

### 1. Deployment vs. ReplicaSet

| Feature | ReplicaSet | Deployment |
|---|---|---|
| **Primary Purpose** | Maintains a stable set of identical replica Pods running at any given time. | Declarative management for Pods and ReplicaSets; handles rollouts, updates, and rollbacks. |
| **Pod Management** | Direct Pod creation/deletion based on selector count. | Higher-level manager that creates and orchestrates underlying ReplicaSets. |
| **Rolling Updates** | **Cannot** perform rolling updates. Updating pod template only affects future pods. | **Natively orchestrates zero-downtime rolling updates** by creating a new RS and scaling down old RS. |
| **History & Rollback** | Does not maintain rollout revision history. | Maintains revision history (`kubectl rollout undo deployment/<name>`). |
| **Best Practice** | Never create ReplicaSets directly in production. | **Always manage workloads via Deployments.** |

### 2. Deployment vs. DaemonSet vs. StatefulSet

| Dimension | Deployment | DaemonSet | StatefulSet |
|---|---|---|---|
| **Scheduling Target** | Scheduled arbitrarily across available nodes by `kube-scheduler`. | Runs **exactly one Pod copy on every node** (or filtered subset via nodeSelector). | Scheduled on nodes with predictable ordinal indices (`pod-0`, `pod-1`). |
| **Workload Type** | Stateless web services and APIs (e.g. Nginx, React, FastAPI). | Node-level daemon utilities (e.g. log collectors `Fluentbit`, monitoring `Prometheus Node Exporter`, network plugins `kube-proxy`). | Stateful clustered applications (e.g. PostgreSQL, Redis Cluster, Kafka, ZooKeeper). |
| **Storage Binding** | Pods share ephemeral volumes or independent stateless PVCs. | Usually mounts host filesystems (`hostPath` to `/var/log`). | Provisions dedicated, persistent, ordinal VolumeClaimTemplates (`pvc-data-pod-0`). |
| **Network Identity** | Pod names are random hashes; IP changes on replacement. | Pod names tied to node hostname. | Stable, predictable DNS hostnames (`db-0.db-headless.default.svc.cluster.local`). |

### 3. ReplicaSet vs. Service

- **ReplicaSet Responsibility:** Manages the **lifecycle and quantity** of Pods. Ensures desired count matches healthy running Pods.
- **Service Responsibility:** Manages **network access and discoverability**. Provides a permanent virtual IP and DNS name that load balances traffic across healthy Pods identified by label selectors.
- **Why a Service is Essential:** Pods in Kubernetes are ephemeral; they are created and destroyed frequently during updates, crashes, or node rescheduling, receiving a new dynamic private IP each time. Without a Service, upstream clients cannot reliably locate the application.

---

## Sub-Documentation Links

- [FQDN Complete Technical Guide](fqdn/README.md)
- [CoreDNS Discovery & Troubleshooting Guide](coredns/README.md)
