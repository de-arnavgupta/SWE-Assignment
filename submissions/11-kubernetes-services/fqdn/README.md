# Fully Qualified Domain Names (FQDN) in Kubernetes

**Author:** Arnav Gupta (Roll: 24bcs10063)  
**Session:** Session 11 — Kubernetes Networking  

---

## 1. What is an FQDN?

A Fully Qualified Domain Name (FQDN) is an unambiguous, complete domain address specifying its exact hierarchical location within the global Domain Name System (DNS) tree down to the root zone (represented by the trailing dot `.`).

---

## 2. Kubernetes Service DNS Naming Standard

Every Kubernetes Service automatically receives an internal FQDN structured as follows:

$$\text{<service-name>}.\text{<namespace>}.\text{svc}.\text{<cluster-domain>}$$

Where:
- `<service-name>`: Name of the Service object (e.g. `mentorsync-backend`).
- `<namespace>`: The namespace where the Service resides (e.g. `production` or `default`).
- `svc`: Identifies the object type as a Kubernetes Service.
- `<cluster-domain>`: The local cluster domain suffix, standardly `cluster.local`.

### Concrete Examples

| Calling Workload | Target Service | FQDN to Use | Notes |
|---|---|---|---|
| Pod in `production` | `api-svc` in `production` | `api-svc` or `api-svc.production` | Same namespace resolution via search domain |
| Pod in `monitoring` | `api-svc` in `production` | `api-svc.production.svc.cluster.local` | Cross-namespace call requiring full FQDN |
| Headless Pod-0 | `db-headless` in `database` | `db-0.db-headless.database.svc.cluster.local` | Individual stateful Pod direct A-record |

---

## 3. Resolving Mechanism Inside Pod Containers

When a container runs inside a Kubernetes Pod, `kubelet` automatically generates `/etc/resolv.conf`:

```text
nameserver 10.96.0.10
search production.svc.cluster.local svc.cluster.local cluster.local
options ndots:5
```

- **Search Domains:** When an application curls `http://api-svc:8080`, the DNS resolver tests the search prefixes sequentially:
  1. `api-svc.production.svc.cluster.local` (Matched immediately!)
- **`ndots:5`:** Any domain query with fewer than 5 dots is first evaluated against the local search domains before being forwarded to public root nameservers.
