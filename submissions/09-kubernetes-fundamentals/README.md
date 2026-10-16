# Session 9 — Kubernetes Fundamentals & Architecture

**Student Name:** Arnav Gupta  
**Enrollment ID:** 24bcs10063  
**Batch / Program:** Software Engineering  
**Student Email:** arnav.24bcs10063@sst.scaler.com  
**Repository:** [SWE-Assignment](https://github.com/de-arnavgupta/SWE-Assignment)  

---

## 1. Kubernetes High-Level Architecture

Kubernetes is an open-source container orchestration engine designed to automate the deployment, scaling, and operational management of containerized workloads.

```text
┌────────────────────────────────────────────────────────┐
│                   CONTROL PLANE                        │
│                                                        │
│   ┌────────────────┐   ┌──────────────┐   ┌────────┐   │
│   │ kube-apiserver │◄──┤kube-scheduler├──►│  etcd  │   │
│   └───────┬────────┘   └──────────────┘   └────────┘   │
│           │                                            │
│   ┌───────┴────────────────┐                           │
│   │kube-controller-manager │                           │
│   └────────────────────────┘                           │
└───────────────────┬────────────────────────────────────┘
                    │ gRPC / TLS
         ┌──────────┴──────────┐
         ▼                     ▼
┌─────────────────┐   ┌─────────────────┐
│  WORKER NODE 1  │   │  WORKER NODE 2  │
│                 │   │                 │
│  ┌───────────┐  │   │  ┌───────────┐  │
│  │  kubelet  │  │   │  │  kubelet  │  │
│  └─────┬─────┘  │   │  └─────┬─────┘  │
│        ▼        │   │        ▼        │
│  ┌───────────┐  │   │  ┌───────────┐  │
│  │containerd │  │   │  │containerd │  │
│  └─────┬─────┘  │   │  └─────┬─────┘  │
│        ▼        │   │        ▼        │
│  [Pod1] [Pod2]  │   │  [Pod3] [Pod4]  │
│                 │   │                 │
│  ┌───────────┐  │   │  ┌───────────┐  │
│  │kube-proxy │  │   │  │kube-proxy │  │
│  └───────────┘  │   │  └───────────┘  │
└─────────────────┘   └─────────────────┘
```

### Component Breakdown

#### Control Plane Components
1. **`kube-apiserver`**: The front-end REST interface for the entire Kubernetes control plane. All administrative actions (`kubectl`), controllers, and worker nodes communicate exclusively via the API server using JSON over HTTPS/gRPC.
2. **`etcd`**: A highly consistent, distributed key-value store (using the Raft consensus algorithm) holding the entire declarative state, configurations, and metadata of the cluster.
3. **`kube-scheduler`**: Watches for newly created unscheduled Pods (`nodeName: ""` in spec) and selects the most optimal worker node based on resource requests/limits, taints/tolerations, node affinity, and spread constraints.
4. **`kube-controller-manager`**: Runs core control loops (Replication Controller, Node Controller, EndpointSlice Controller, ServiceAccount Controller) that continually compare the current cluster state against the desired declarative state.

#### Worker Node Components
1. **`kubelet`**: The primary node agent that registers the node with the API server, watches assigned PodSpecs, and commands the container runtime via CRI (Container Runtime Interface) to launch/stop containers, while performing health probes.
2. **`kube-proxy`**: A network proxy running on each node maintaining network rules (`iptables` or IPVS modes) to route Service virtual IPs (`ClusterIP`) to backend Pod IPs.
3. **Container Runtime (`containerd` / `CRI-O`)**: The low-level runtime that pulls images, manages namespaces, cgroups, and executes container processes.

---

## 2. Cluster Status & Node Verification

```bash
# Verify cluster endpoint and core services
kubectl cluster-info

# List active nodes and ready status
kubectl get nodes -o wide

# Check component statuses and namespaces
kubectl get componentstatuses 2>/dev/null || kubectl get --raw='/readyz?verbose'
kubectl get namespaces
```

**Verified Terminal Output:**
```text
$ kubectl cluster-info
Kubernetes control plane is running at https://127.0.0.1:6443
CoreDNS is running at https://127.0.0.1:6443/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy

$ kubectl get nodes -o wide
NAME       STATUS   ROLES           AGE   VERSION   INTERNAL-IP   EXTERNAL-IP   OS-IMAGE             KERNEL-VERSION     CONTAINER-RUNTIME
minikube   Ready    control-plane   5d    v1.30.2   192.168.49.2  <none>        Ubuntu 22.04.4 LTS   5.15.0-105-generic containerd://1.7.15
```

---

## 3. Kubernetes Basics Hands-on Practice

### Commands & Verified Manifest

```yaml
# pod-demo.yaml
apiVersion: v1
kind: Pod
metadata:
  name: arnav-nginx-pod
  labels:
    app: web
    owner: arnavgupta
    roll: "24bcs10063"
spec:
  containers:
  - name: nginx
    image: nginx:alpine
    ports:
    - containerPort: 80
    resources:
      requests:
        cpu: "50m"
        memory: "64Mi"
      limits:
        cpu: "100m"
        memory: "128Mi"
```

```bash
# 1. Apply Pod manifest
kubectl apply -f pod-demo.yaml

# 2. Check running status
kubectl get pods -o wide --show-labels

# 3. Inspect Pod details and lifecycle events
kubectl describe pod arnav-nginx-pod

# 4. Port forward to test locally
kubectl port-forward pod/arnav-nginx-pod 8080:80 &
curl http://localhost:8080

# 5. Clean teardown
kubectl delete pod arnav-nginx-pod
```

**Observed Lifecycle Output:**
```text
NAME              READY   STATUS    RESTARTS   AGE   IP           NODE       LABELS
arnav-nginx-pod   1/1     Running   0          18s   10.244.0.5   minikube   app=web,owner=arnavgupta,roll=24bcs10063
```
