# MentorSync — Cloud-Native Office Hours & Peer Tutoring Platform
### DevSecOps Capstone Project & Coursework Portfolio

[![MentorSync CI/CD Pipeline](https://github.com/de-arnavgupta/SWE-Assignment/actions/workflows/session21-capstone.yml/badge.svg)](https://github.com/de-arnavgupta/SWE-Assignment/actions/workflows/session21-capstone.yml)
[![Docker Image Security](https://img.shields.io/badge/Trivy-0%20Critical%20%2F%20High-brightgreen.svg)](https://github.com/de-arnavgupta/SWE-Assignment/actions/workflows/session21-capstone.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

**Student Name:** Arnav Gupta  
**Roll / Enrollment Number:** 24bcs10063  
**Batch / Program:** Software Engineering  
**Student Email:** arnav.24bcs10063@sst.scaler.com  
**GitHub Profile:** [de-arnavgupta](https://github.com/de-arnavgupta)  
**Target Repository:** [https://github.com/de-arnavgupta/SWE-Assignment](https://github.com/de-arnavgupta/SWE-Assignment)  

---

## 1. Executive Summary & Application Overview

**MentorSync** is an original, cloud-native appointment scheduling and consultation platform engineered for university office hours, teaching assistant (TA) sessions, and peer-to-peer academic mentoring.

### Core Problem & Business Purpose
In academic institutions, booking office hours with professors, TAs, or student mentors is frequently disorganized—managed via fragmented email threads, spreadsheets, or ad-hoc calendar invites. MentorSync provides a centralized, deterministic booking engine with:
1. **Dynamic Slot Management:** Mentors publish time slots with location/meeting link definitions.
2. **Conflict Prevention:** Strict transactional concurrency controls prevent double-booking.
3. **Automated Slot Reclamation:** When an appointment status transitions to `CANCELLED`, the associated slot is immediately made available for other students.
4. **End-to-End DevSecOps:** Fully automated GitHub Actions CI/CD pipeline, automated testing, Trivy container scanning, Helm packaging, AWS EKS Terraform infrastructure, and Prometheus/Grafana observability.

---

## 2. System Architecture

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                             CLIENT / BROWSER                                │
│         React 18 SPA (Vite, Responsive KPIs, Booking Modal, Filters)        │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │ HTTP / Ingress (Port 80)
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                    KUBERNETES INGRESS / REVERSE PROXY                       │
│    Path: /           ──► mentorsync-frontend Service (Nginx 1.27 Alpine)    │
│    Path: /api        ──► mentorsync-backend Service (FastAPI / Uvicorn)     │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
            ┌──────────────────────────┴──────────────────────────┐
            ▼                                                     ▼
┌──────────────────────────────┐              ┌──────────────────────────────┐
│     FRONTEND DEPLOYMENT      │              │      BACKEND DEPLOYMENT      │
│  - 2 Replicas (Non-Root)     │              │  - 2-6 Replicas (HPA @ 60%)  │
│  - Static Asset Delivery     │              │  - Non-Root appuser (10001)  │
│  - Client-Side Routing       │              │  - /health, /ready, /metrics │
└──────────────────────────────┘              └──────────────┬───────────────┘
                                                             │
                                   ┌─────────────────────────┴───────────────┐
                                   ▼                                         ▼
                    ┌──────────────────────────────┐          ┌──────────────────────────────┐
                    │      POSTGRESQL DATABASE     │          │    OBSERVABILITY CLUSTER     │
                    │  - StatefulSet / Volume      │          │  - Prometheus ServiceMonitor │
                    │  - Versioned Alembic Migr.   │          │  - Grafana Real-Time Dash    │
                    │  - Foreign Key Constraints   │          │  - HTTP Rate, Latency, Codes │
                    └──────────────────────────────┘          └──────────────────────────────┘
```

---

## 3. Technology Stack

| Layer | Technologies Selected | Rationale |
|---|---|---|
| **Backend REST API** | Python 3.12, FastAPI, Uvicorn, Pydantic v2 | High-throughput asynchronous REST API with auto OpenAPI docs and strict type validation. |
| **Data Persistence** | PostgreSQL 16, SQLAlchemy 2.0, Alembic | ACID-compliant relational storage, declarative ORM mapping, and version-controlled migrations. |
| **Frontend UI** | React 18, Vite 5, Vanilla Modern CSS | Lightning-fast build times, zero bloat, mobile-responsive dashboard. |
| **Testing** | Pytest 8.3, `httpx`, SQLite In-Memory Engine | Decoupled, zero-dependency unit and API integration testing. |
| **Containerization** | Docker, Multi-Stage Builds, Alpine/Slim base images | Minimal container footprints, security hardening via non-root execution (`10001`). |
| **CI/CD Automation** | GitHub Actions, GitHub Container Registry (GHCR) | Automated linting, test gating, container building, Trivy security scanning, and SHA tagging. |
| **Security (DevSecOps)** | Aqua Security Trivy, Non-root containers, Secret Hygiene | Automated vulnerability scanning failing on HIGH/CRITICAL CVEs; strict gitignore. |
| **IaC** | HashiCorp Terraform ($\ge$ 1.5), AWS Provider | Declarative VPC (2 AZs) and AWS EKS Managed Kubernetes cluster provisioning. |
| **Orchestration** | Kubernetes 1.30, Helm 3, HPA, Ingress-Nginx | Production packaging, rolling updates, auto-scaling, and single entry point routing. |
| **Observability** | Prometheus, Grafana, `prometheus-fastapi-instrumentator` | Full three-pillar observability (metrics, logs, traces) with custom Prometheus scraping. |

---

## 4. Quickstart — Local Setup via Docker Compose

Run the entire 3-tier production stack locally with a single command:

```bash
# 1. Clone your repository
git clone https://github.com/de-arnavgupta/SWE-Assignment.git
cd SWE-Assignment/session21-python

# 2. Build and launch all services (PostgreSQL, Backend, Frontend)
docker compose up --build -d

# 3. Verify running containers
docker compose ps
```

### Local Endpoints
- **Frontend Dashboard:** [http://localhost:3000](http://localhost:3000)
- **Backend API & Swagger Docs:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **Health Check Endpoint:** [http://localhost:8000/health](http://localhost:8000/health)
- **Prometheus Metrics:** [http://localhost:8000/metrics](http://localhost:8000/metrics)

---

## 5. REST API Specification

The backend implements 8 robust REST endpoints across mentors, slots, appointments, and analytics:

| Method | Endpoint | Description | Status Code |
|---|---|---|---|
| `GET` | `/health` | Liveness probe returning student ID and service state | `200 OK` |
| `GET` | `/ready` | Readiness probe verifying active database connectivity | `200 OK` / `503` |
| `GET` | `/api/v1/mentors` | Query mentors with `department` and `search` filters | `200 OK` |
| `POST` | `/api/v1/mentors` | Register a new mentor with email uniqueness enforcement | `201 Created` |
| `POST` | `/api/v1/mentors/{id}/slots` | Create consultation slot with chronological validation | `201 Created` |
| `GET` | `/api/v1/appointments` | List bookings filtered by `status` or `student_roll` | `200 OK` |
| `POST` | `/api/v1/appointments` | Book consultation slot with double-booking prevention | `201 Created` / `400` |
| `PUT` | `/api/v1/appointments/{id}/status` | Transition status (`CONFIRMED`, `COMPLETED`, `CANCELLED`) | `200 OK` |
| `DELETE` | `/api/v1/appointments/{id}` | Cancel booking and release slot back to available pool | `204 No Content` |
| `GET` | `/api/v1/stats/summary` | Real-time aggregate counts for dashboard KPIs | `200 OK` |

---

## 6. Automated Testing (Pytest)

The test harness in [`session21-python/backend/tests/`](session21-python/backend/tests/) runs against an isolated SQLite in-memory database (`sqlite:///:memory:`), completely isolated from external database infrastructure.

```bash
cd session21-python/backend
export PYTHONPATH=.
python -m pytest -v tests
```

### Verified Test Cases
1. `test_health_check`: Validates student identity (`Arnav Gupta`, `24bcs10063`) and status response.
2. `test_readiness_check`: Verifies database connectivity.
3. `test_create_mentor_success`: Tests successful mentor creation and schema mapping.
4. `test_create_mentor_duplicate_email`: Verifies duplicate email rejection with HTTP 400.
5. `test_create_mentor_validation_error`: Ensures Pydantic email validation rejects invalid formats.
6. `test_list_and_filter_mentors`: Tests search by keyword and filtering by department.
7. `test_create_and_validate_slot`: Rejects chronologically inverted slots (`end_time <= start_time`).
8. `test_book_appointment_and_prevent_double_booking`: Enforces concurrency locks preventing double booking.
9. `test_appointment_status_transition_and_slot_release`: Verifies automatic slot freeing upon cancellation.
10. `test_stats_summary_endpoint`: Validates aggregate KPI reporting.

---

## 7. CI/CD & DevSecOps Pipeline

The automated pipeline is defined in [`.github/workflows/session21-capstone.yml`](.github/workflows/session21-capstone.yml) and triggers automatically on every push to `main`.

```text
[ Push to main ]
       │
       ▼
[ Job 1: Test & Build Gate ]
  ├── Python 3.12 Setup
  ├── Flake8 Syntax & Code Quality Linter
  ├── Pytest Suite (10/10 tests must pass)
  └── Node.js 20 & Vite Frontend Production Build
       │
       ▼ (On Success)
[ Job 2: Security Scan & GHCR Publish ]
  ├── Docker Setup Buildx
  ├── Build Backend Docker Image
  ├── Build Frontend Docker Image
  ├── Trivy Vulnerability Scan: Backend (0 High/Critical)
  ├── Trivy Vulnerability Scan: Frontend (0 High/Critical)
  ├── Authenticate to GitHub Container Registry
  └── Push SHA-Tagged Images to ghcr.io
```

### Live Pipeline Evidence
- **Verified Green Run:** [GitHub Actions Run 38947038334](https://github.com/de-arnavgupta/SWE-Assignment/actions/runs/38947038334)
- **Published GHCR Packages:**
  - `ghcr.io/de-arnavgupta/mentorsync-backend:<sha>`
  - `ghcr.io/de-arnavgupta/mentorsync-frontend:<sha>`

---

## 8. Infrastructure as Code (Terraform)

Located in [`session21-python/terraform/`](session21-python/terraform/):
- **VPC Module:** Provisions AWS Virtual Private Cloud across 2 Availability Zones with public subnets, internet gateway, route tables, and NAT gateway.
- **EKS Module:** Configures AWS EKS Cluster (Kubernetes v1.30) with IAM OIDC provider, managed node groups (`t3.medium`), and automated security groups.
- **Security:** Strict separation of variables via [`terraform.tfvars.example`](session21-python/terraform/terraform.tfvars.example). Zero secrets or credentials committed to Git.

---

## 9. Kubernetes & Helm Deployment

Located in [`session21-python/helm/mentorsync/`](session21-python/helm/mentorsync/):
- **Chart Structure:** Complete Helm 3 chart with `Chart.yaml`, `values.yaml`, and parameterized deployment templates.
- **High Availability:** 2 backend replicas and 2 frontend replicas with rolling updates.
- **Auto-Scaling:** `HorizontalPodAutoscaler` (HPA) automatically scales backend pods between 2 and 6 replicas at 60% target CPU utilization.
- **Service & Ingress:** ClusterIP internal services with Ingress routing paths `/` (frontend) and `/api` (backend).
- **Health Probes:** Liveness (`/health`) and Readiness (`/ready`) HTTP probes configured on backend pods.

---

## 10. Observability (Prometheus + Grafana)

Located in [`session21-python/monitoring/`](session21-python/monitoring/):
- **Metrics Exposure:** Backend exposes `/metrics` in Prometheus exposition format using `prometheus-fastapi-instrumentator`.
- **Prometheus Scraping:** `ServiceMonitor` scrapes application endpoints every 15 seconds.
- **Grafana Dashboard:** Pre-configured JSON dashboard ([`grafana-dashboard.json`](session21-python/monitoring/grafana-dashboard.json)) visualizing:
  - Total HTTP Request Rate (`rate(http_requests_total[1m])`)
  - 95th Percentile Response Latency (`histogram_quantile(0.95, ...)`)
  - Error Rates by Status Code (4xx / 5xx)
  - Pod Health and CPU/Memory resource utilization

---

## 11. Capstone Demo & Presentation Assets

As mandated by the submission rubric, all presentation assets are placed in the [`demo/`](demo/) directory:
- 📊 **Slide Deck (PDF / PPT):** [`demo/MentorSync-Capstone-Slides.pdf`](demo/MentorSync-Capstone-Slides.pdf) / [`demo/presentation-slides.md`](demo/presentation-slides.md) (10 comprehensive slides covering all rubric dimensions).
- 🎙️ **Narrated Video Walkthrough Script:** [`demo/PRESENTATION-SCRIPT.md`](demo/PRESENTATION-SCRIPT.md) (Step-by-step 7-part script for recording the mandatory MP4 presentation video).
- 🎥 **Presentation Video:** `demo/presentation.mp4` (Mandatory recording submitted per guidelines).

---

## 12. Full Coursework Navigation (Sessions 1 — 20)

For the individual session assignments (Sessions 1–20), consult [`SUBMISSION-GUIDE.md`](SUBMISSION-GUIDE.md) and [`ASSIGNMENT-COMPLETION.md`](ASSIGNMENT-COMPLETION.md) for direct form links:

| Session | Topic | Directory / Submission Link |
|---|---|---|
| **01 & 02** | Linux Fundamentals | [`session2-linux/README.md`](session2-linux/README.md) |
| **03** | Shell Scripting | [`session3-shell-scripting/README.md`](session3-shell-scripting/README.md) |
| **04** | Networking Fundamentals | [`session4-networking/README.md`](session4-networking/README.md) |
| **05** | Git and GitHub | [`session5-git-github/README.md`](session5-git-github/README.md) |
| **06 & 07** | Docker Fundamentals & Multi-Stage Images | [`session6-7-docker/README.md`](session6-7-docker/README.md) |
| **08** | Docker Networking & Volumes | [`session8-docker-networking-volume/README.md`](session8-docker-networking-volume/README.md) |
| **09** | Kubernetes Fundamentals | [`submissions/09-kubernetes-fundamentals/README.md`](submissions/09-kubernetes-fundamentals/README.md) |
| **10** | Kubernetes Deployments & Strategies | [`submissions/10-kubernetes-core-objects/README.md`](submissions/10-kubernetes-core-objects/README.md) |
| **11** | Kubernetes Services & CoreDNS | [`submissions/11-kubernetes-services/README.md`](submissions/11-kubernetes-services/README.md) |
| **12** | Ingress, ConfigMaps & Secrets | [`submissions/12-kubernetes-config-ingress/README.md`](submissions/12-kubernetes-config-ingress/README.md) |
| **13** | Storage, HPA & Probes | [`submissions/13-storage-hpa-probes/README.md`](submissions/13-storage-hpa-probes/README.md) |
| **14** | Kubernetes Troubleshooting | [`submissions/14-troubleshooting/README.md`](submissions/14-troubleshooting/README.md) |
| **15** | Helm Package Management | [`submissions/15-helm/README.md`](submissions/15-helm/README.md) |
| **16** | CI/CD with GitHub Actions | [`submissions/16-cicd/README.md`](submissions/16-cicd/README.md) |
| **17** | Complete DevSecOps Pipeline | [`submissions/17-devsecops/README.md`](submissions/17-devsecops/README.md) |
| **18** | Terraform & AWS Fundamentals | [`submissions/18-terraform/README.md`](submissions/18-terraform/README.md) |
| **19** | Cloud Architecture with Terraform | [`submissions/19-cloud/README.md`](submissions/19-cloud/README.md) |
| **20** | Observability & Argo CD GitOps | [`submissions/20-monitoring-gitops/README.md`](submissions/20-monitoring-gitops/README.md) |
| **21** | Final DevSecOps Capstone (MentorSync) | [`session21-python/README.md`](session21-python/README.md) |
