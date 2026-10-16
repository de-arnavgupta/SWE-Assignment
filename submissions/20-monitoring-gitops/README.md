# Session 20 — Monitoring, Observability & GitOps

**Student Name:** Arnav Gupta  
**Enrollment ID:** 24bcs10063  
**Batch / Program:** Software Engineering  
**Student Email:** arnav.24bcs10063@sst.scaler.com  
**Repository:** [SWE-Assignment](https://github.com/de-arnavgupta/SWE-Assignment)  

---

## 1. The Three Pillars of Observability

Observability is the degree to which the internal state of a complex distributed system can be inferred solely from its external telemetry outputs.

```text
               ┌────────────────────────┐
               │     OBSERVABILITY      │
               └───────────┬────────────┘
        ┌──────────────────┼──────────────────┐
        ▼                  ▼                  ▼
   [ METRICS ]          [ LOGS ]          [ TRACES ]
Aggregable numeric    Timestamped text    End-to-end request
timeseries (counters, records of discrete spans across microservices
gauges, histograms)   runtime events      (latency breakdowns)
e.g. Prometheus       e.g. Loki, ELK      e.g. OpenTelemetry, Jaeger
```

### Deep Dive Comparison

| Telemetry Pillar | Data Model | Primary Benefit | Standard Tooling | Kubernetes Implementation |
|---|---|---|---|---|
| **Metrics** | Numeric time-series ($(\text{timestamp}, \text{value})$ with key-value labels). | Low storage overhead; instant alerting on anomalies (e.g. HTTP 5xx rate spikes). | **Prometheus**, Datadog, InfluxDB. | Prometheus Server scraping `/metrics` endpoints via `ServiceMonitor` or annotations. |
| **Logs** | Structured JSON or semi-structured timestamped text events. | Contextual forensic debugging of why a specific error occurred. | **Grafana Loki**, Fluentbit, ELK Stack. | DaemonSet log collector reading `/var/log/pods/*/*.log` from worker nodes. |
| **Traces** | Directed Acyclic Graph (DAG) of Spans representing request journey across microservices. | Pinpoint exact service bottleneck causing high p99 response latency. | **OpenTelemetry**, Jaeger, Zipkin. | W3C `traceparent` headers propagated across HTTP/gRPC RPC calls. |

---

## 2. Prometheus Scraping & Application `/metrics`

The backend application instruments real-time metrics using `prometheus-client` / `prometheus-fastapi-instrumentator`:

```python
# Sample backend metric exposure
from prometheus_client import Counter, Histogram, generate_latest

REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP Requests', ['method', 'endpoint', 'status'])
REQUEST_LATENCY = Histogram('http_request_duration_seconds', 'HTTP Request Latency', ['endpoint'])
```

### Verified Metrics Output (`curl http://<backend>:8000/metrics`)
```text
# HELP http_requests_total Total HTTP Requests
# TYPE http_requests_total counter
http_requests_total{endpoint="/api/v1/mentors",method="GET",status="200"} 482.0
http_requests_total{endpoint="/api/v1/appointments",method="POST",status="201"} 34.0
http_requests_total{endpoint="/health",method="GET",status="200"} 1240.0

# HELP http_request_duration_seconds HTTP Request Latency
# TYPE http_request_duration_seconds histogram
http_request_duration_seconds_bucket{endpoint="/api/v1/mentors",le="0.05"} 470.0
http_request_duration_seconds_bucket{endpoint="/api/v1/mentors",le="0.1"} 480.0
http_request_duration_seconds_bucket{endpoint="/api/v1/mentors",le="+Inf"} 482.0
```

### Prometheus Target Status: `UP (1/1)`
Prometheus scrapes the application Pod endpoints every 15 seconds. On the Prometheus Targets dashboard (`http://localhost:9090/targets`), the target shows state **`UP`**, with zero scrape scrape errors.

---

## 3. GitOps Architecture with Argo CD

GitOps is an operational model where a Git repository serves as the **single source of truth** for declarative infrastructure and application deployments.

```text
[ Developer Commit ] ──► [ Git Repository: main ]
                                │
                                │ (Webhook / 3-minute poll)
                                ▼
                       [ Argo CD Controller ]
                                │
                ┌───────────────┴───────────────┐
                ▼                               ▼
       [ Desired State (Git) ]       [ Actual State (K8s Cluster) ]
                │                               │
                └────────── Diff Engine ────────┘
                                │
              Out-of-Sync Detected?
              ├── Auto-Sync Enabled ──► Reconcile Cluster State
              └── Manual Sync Mode  ──► Flag Out-of-Sync in UI
```

### Continuous Reconciliation & Self-Healing Workflow
1. **Desired State in Git:** `replicas: 2` in `helm/mentorsync/values.yaml`.
2. **Deliberate Out-of-Band Drift:** Operator manually modifies cluster directly:
   ```bash
   kubectl scale deployment mentorsync-backend --replicas=5
   ```
3. **Argo CD Detection:** Argo CD marks application status as `OutOfSync`.
4. **Self-Healing Action:** Because `selfHeal: true` is configured in the Argo CD `Application` CRD, the controller automatically executes corrective reconciliation, terminating the 3 unauthorized Pods and restoring replicas back to the desired Git commit state of `2`.
5. **Deployment Ownership Principle:** Production clusters should only be altered via Git commits reviewed through Pull Requests; direct imperative `kubectl apply` commands on production clusters violate traceability and are overwritten by GitOps reconciliation.
