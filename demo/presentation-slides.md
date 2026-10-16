# MentorSync — DevSecOps Capstone Presentation
## Office Hours & Peer Tutoring Platform

**Student:** Arnav Gupta  
**Enrollment:** 24bcs10063  
**Program:** Software Engineering  
**Course:** DevOps & DevSecOps Engineering  
**Submission Date:** October 2026  

---

## Slide 1: Project Overview & Problem Statement

### The Problem
- University office hours and academic tutoring bookings are plagued by fragmentation.
- Students and mentors rely on ad-hoc email chains, spreadsheets, and calendar links.
- Key operational issues:
  - Scheduling conflicts and accidental double-bookings.
  - No automated slot reclamation when sessions are cancelled.
  - Lack of visibility into mentor availability across academic departments.

### The Solution: MentorSync
- A cloud-native, deterministic consultation booking platform.
- Real-time availability search, conflict-free booking transaction guarantees, and automated slot recycling.
- Built from the ground up to demonstrate a full production DevSecOps lifecycle.

---

## Slide 2: Technology Stack & Architectural Decisions

| Layer | Component | Architectural Rationale |
|---|---|---|
| **Backend** | Python 3.12 + FastAPI + Uvicorn | Asynchronous performance, native OpenAPI documentation, strict Pydantic v2 data validation. |
| **Database** | PostgreSQL 16 + SQLAlchemy 2.0 | Relational integrity, ACID transaction guarantees, and declarative model mapping. |
| **Migrations** | Alembic | Version-controlled database schema evolution matching Git commits. |
| **Frontend** | React 18 + Vite 5 + CSS3 | High-performance single-page app (SPA), modular component hierarchy, rapid build cycles. |
| **Testing** | Pytest 8.3 + In-Memory SQLite | Isolated unit and integration testing without runtime database dependencies. |
| **Containers** | Docker (Alpine / Slim) | Minimal attack surface, multi-stage builds, non-root user execution (`UID 10001`). |

---

## Slide 3: End-to-End System Architecture

```text
[ React 18 SPA (Vite) ]
          │ HTTP / Ingress (Port 80)
          ▼
[ Kubernetes Ingress-Nginx Controller ]
          ├─► /    ──► [ Frontend Service (Nginx 1.27) ] ──► Pod Replicas (2)
          └─► /api ──► [ Backend Service (FastAPI) ]     ──► Pod Replicas (2-6 HPA)
                              │
                    ┌─────────┴─────────┐
                    ▼                   ▼
           [ PostgreSQL 16 DB ]   [ Prometheus /metrics ]
           (PVC / StatefulSet)     └──► Scraped by Prometheus
                                        └──► Visualized in Grafana
```

---

## Slide 4: Automated Testing Strategy (Pytest)

- **Decoupled Test Environment:**
  - `backend/tests/conftest.py` spins up an in-memory SQLite database (`sqlite:///:memory:`) using `StaticPool`.
  - Zero external network or PostgreSQL service container required during testing.
- **Test Suite Coverage (10 Test Cases):**
  1. `test_health_check`: Student identity and service status.
  2. `test_readiness_check`: Database connectivity verification.
  3. `test_create_mentor_success`: Mentor schema validation and DB persistence.
  4. `test_create_mentor_duplicate_email`: HTTP 400 on duplicate registrations.
  5. `test_create_mentor_validation_error`: Pydantic email syntax rejection.
  6. `test_list_and_filter_mentors`: Search query and department filtering.
  7. `test_create_and_validate_slot`: Chronological validation (`end_time > start_time`).
  8. `test_book_appointment_and_prevent_double_booking`: Concurrency lock on booked slots.
  9. `test_appointment_status_transition_and_slot_release`: Verifies automatic slot freeing on cancellation.
  10. `test_stats_summary_endpoint`: Real-time KPI aggregation.

---

## Slide 5: CI/CD Pipeline & GitHub Actions Automation

- **Trigger:** Automatic execution on every `git push` to `main`.
- **Workflow Architecture (`session21-capstone.yml`):**
  - **Job 1: Test & Build Gate**
    - Code checkout (`actions/checkout@v4`).
    - Python 3.12 environment setup with pip cache.
    - Flake8 syntax and linting checks.
    - Pytest execution: 10/10 tests must pass before proceeding.
    - Node.js 20 setup and Vite production bundle build.
  - **Job 2: Security Scan & GHCR Publish**
    - Docker Buildx setup (`docker/setup-buildx-action@v3`).
    - Build backend and frontend container images.
    - Aqua Security Trivy scan on both images (failing on HIGH or CRITICAL CVEs).
    - Authentication to GitHub Container Registry (`ghcr.io`).
    - Publish immutable SHA-tagged images:
      - `ghcr.io/de-arnavgupta/mentorsync-backend:<sha>`
      - `ghcr.io/de-arnavgupta/mentorsync-frontend:<sha>`

---

## Slide 6: DevSecOps & Security Hardening

- **Shift-Left Security Philosophy:**
  - Security gates embedded directly inside the pull request / push lifecycle.
- **Trivy Vulnerability Scanning:**
  - Scans base OS libraries and Python/Node packages against known CVE databases.
  - Enforces policy: zero unpatched HIGH or CRITICAL vulnerabilities allowed into production.
- **Container Hardening:**
  - Non-root user execution: Backend runs as `appuser` (`UID 10001`); Frontend runs as unprivileged `nginx`.
  - Multi-stage build in frontend leaves dev tools, compilers, and source files out of the production image.
- **Secret Management:**
  - `.gitignore` strictly protects `.env`, `*.tfstate`, and cloud tokens.
  - Ingress and database credentials injected dynamically via Kubernetes Secrets.

---

## Slide 7: Infrastructure as Code (Terraform on AWS)

- **Modular Infrastructure Definition (`terraform/`):**
  - `vpc.tf`: Multi-AZ VPC across 2 Availability Zones (`us-east-1a`, `us-east-1b`) with public/private subnets, Internet Gateway, and NAT Gateway.
  - `eks.tf`: Managed Kubernetes cluster (v1.30) with IAM OIDC provider.
  - `variables.tf` & `terraform.tfvars.example`: Parameterized sizing with default `t3.medium` worker nodes.
- **Idempotency & Lifecycle Safety:**
  - Safe lifecycle destruction via `terraform destroy` preventing accidental cloud expenditure.

---

## Slide 8: Kubernetes Orchestration & Helm Packaging

- **Production Helm Chart (`helm/mentorsync/`):**
  - Parameterized templates for Deployments, Services, Ingress, and Autoscaling.
- **High Availability & Zero Downtime:**
  - Backend: 2 replicas with RollingUpdate strategy.
  - Frontend: 2 replicas for load distribution.
- **Horizontal Pod Autoscaling (HPA):**
  - Dynamic scaling from 2 to 6 backend pods when target CPU exceeds 60%.
- **Single Entry Point Routing:**
  - Ingress Controller routes `/` to Frontend static server and `/api` to Backend REST API.
- **Self-Healing Probes:**
  - Liveness probe (`/health`) restarts stalled pods.
  - Readiness probe (`/ready`) removes unhealthy pods from traffic distribution until DB reconnects.

---

## Slide 9: Observability — Metrics, Logs & Traces

- **Metrics Instrumentation:**
  - `prometheus-fastapi-instrumentator` exposes native Prometheus format metrics on `/metrics`.
  - Metrics collected: HTTP request count, error rates (4xx, 5xx), request duration histogram, and memory usage.
- **Prometheus Scraping:**
  - `ServiceMonitor` polls `/metrics` every 15 seconds.
  - Service targets verified in `UP` status in Prometheus web console.
- **Grafana Dashboard Visualization:**
  - Real-time KPI panels for throughput, p95 latency, error spikes, and pod status.
- **GitOps Continuous Delivery (Argo CD):**
  - Declarative GitOps synchronization detecting drift between Git repository manifests and live cluster state.

---

## Slide 10: Key Learnings & Future Enhancements

### Key Learnings
1. **Decoupled Testing is Essential:** Using in-memory SQLite fixtures enabled ultra-fast CI/CD gates without database startup latency.
2. **Shift-Left Security:** Automated Trivy container scans catch vulnerable dependencies before images are published.
3. **Infrastructure as Code Hygiene:** Strict variable templating and cost-conscious architecture prevent unexpected cloud expenses.

### Future Roadmap
- Implement JWT-based Role-Based Access Control (RBAC) for Admin / Mentor / Student portals.
- Add Google Calendar & Outlook calendar bi-directional synchronization.
- Implement OpenTelemetry distributed tracing across microservices.
