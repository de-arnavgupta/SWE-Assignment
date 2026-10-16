# CoreDNS Architecture & Troubleshooting in Kubernetes

**Author:** Arnav Gupta (Roll: 24bcs10063)  
**Session:** Session 11 — Kubernetes Networking  

---

## 1. What is CoreDNS?

CoreDNS is a fast, flexible, pluggable DNS server written in Go that serves as the official default in-cluster DNS service for Kubernetes (replacing legacy `kube-dns`). It runs as a `Deployment` in the `kube-system` namespace.

---

## 2. Corefile Configuration Architecture

CoreDNS behavior is controlled declaratively via a `ConfigMap` named `coredns` in `kube-system`:

```text
.:53 {
    errors
    health {
       lameduck 5s
    }
    ready
    kubernetes cluster.local in-addr.arpa ip6.arpa {
       pods insecure
       fallthrough in-addr.arpa ip6.arpa
       ttl 30
    }
    prometheus :9153
    forward . /etc/resolv.conf
    cache 30
    loop
    reload
    loadbalance
}
```

### Plugin Responsibilities:
- **`kubernetes`**: Interfaces with the Kubernetes API to watch Services and EndpointSlices, dynamically responding to in-cluster DNS queries.
- **`forward . /etc/resolv.conf`**: Forwards all non-cluster queries (e.g. `google.com`) to the upstream DNS nameservers configured on the underlying worker node.
- **`cache 30`**: Caches resolved DNS responses for up to 30 seconds to minimize load on `kube-apiserver`.
- **`prometheus :9153`**: Exposes CoreDNS metrics (latency, query volume, cache hit ratios) on port 9153 for Prometheus scraping.

---

## 3. Systematic DNS Troubleshooting Runbook

When Pods report `Could not resolve host` errors, follow this exact step-by-step diagnostic workflow:

```bash
# 1. Verify CoreDNS Pods are Running in kube-system
kubectl get pods -n kube-system -l k8s-app=kube-dns

# 2. Check CoreDNS service IP and endpoints
kubectl get svc -n kube-system -l k8s-app=kube-dns
kubectl get endpoints -n kube-system -l k8s-app=kube-dns

# 3. Inspect CoreDNS live logs for lookup errors or upstream timeouts
kubectl logs -n kube-system -l k8s-app=kube-dns --tail=100

# 4. Launch an ephemeral debug container with network tools
kubectl run dns-test --rm -i --tty --image=busybox:1.28 -- nslookup kubernetes.default

# 5. Check if upstream forwarding is failing
kubectl run dns-test --rm -i --tty --image=busybox:1.28 -- nslookup google.com
```

### Common Root Causes & Solutions:
- **CrashLoopBackOff on CoreDNS:** Caused by DNS forwarding loops (detected by the `loop` plugin when node `/etc/resolv.conf` points back to CoreDNS). **Fix:** Configure upstream static resolvers (e.g. `8.8.8.8`) in node resolver configuration.
- **Firewall / NetworkPolicy Dropping Port 53:** Security groups or NetworkPolicies blocking UDP/TCP port 53 traffic between worker nodes and CoreDNS Pods. **Fix:** Ensure intra-cluster communication allows port 53 ingress/egress.
