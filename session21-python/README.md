# Session 21 — DevOps Final Capstone: MentorSync

**Application:** MentorSync — Office Hours & Peer Tutoring Platform  
**Author / Student:** Arnav Gupta  
**Enrollment ID:** 24bcs10063  
**Batch / Section:** Software Engineering  
**Student Email:** arnav.24bcs10063@sst.scaler.com  
**Target Repository:** [SWE-Assignment](https://github.com/de-arnavgupta/SWE-Assignment)  

---

## 1. Project Purpose & Originality Statement

MentorSync is an original, production-grade cloud-native application engineered to solve university office-hour scheduling, peer tutoring booking, and faculty consultation capacity challenges.

### Original Domain Features:
- **Genuinely Distinct Domain:** Unlike generic task trackers or facility maintenance ticketing systems, MentorSync models an academic consultation domain with specialized entities: `Mentor`, `Slot`, `Appointment`, and `Department`.
- **Enforced Business Rules:**
  - Double-booking prevention: Attempting to reserve an already booked slot returns HTTP 400 Bad Request.
  - Automatic slot state synchronization: Cancelling or deleting an appointment automatically releases the slot (`is_booked = False`) back to the available pool for other students.
  - Chronological validation: Slot start times must precede end times.
- **Full-Stack Implementation:** FastAPI Python backend, SQLAlchemy ORM with PostgreSQL, Alembic database schema migrations, and a responsive React 18 single-page application.

---

## 2. End-to-End System Architecture

```text
[ User Browser / Client ]
            │
            ▼
┌─────────────────────────────────────────────────────────────┐
│ AWS Cloud VPC (10.20.0.0/16)                                 │
│                                                             │
│   [ AWS Application Load Balancer / Ingress Controller ]    │
│             │                                               │
│     ┌───────┴───────┐                                       │
│     │ Path: /       │ Path: /api/                           │
│     ▼               ▼                                       │
│ [ Frontend Pods ] [ Backend Pods (FastAPI) ]                │
│   (2 Replicas)       (2-6 Replicas via HPA)                 │
│                             │                               │
│                             ▼                               │
│                     [ PostgreSQL Pod ]                      │
│                     (Persistent Volume RWO)                 │
│                             ▲                               │
│                             │                               │
│             [ Prometheus Scrapes /metrics ]                 │
│                             │                               │
│                             ▼                               │
│                   [ Grafana Dashboards ]                    │
└─────────────────────────────────────────────────────────────┘
```

---

## 3. Rubric Modules Implementation (M1 — M10)

### M1: Application (Frontend + Backend + Database)
- **FastAPI Backend:** Fully implemented in `backend/app/` with `/health`, `/ready` database check, and full REST API:
  - `GET /api/v1/mentors`: Query mentors with department and search filters.
  - `POST /api/v1/mentors`: Register mentor.
  - `POST /api/v1/mentors/{id}/slots`: Create open office hour slots.
  - `GET /api/v1/appointments`: List appointments with status filtering.
  - `POST /api/v1/appointments`: Book consultation slot.
  - `PUT /api/v1/appointments/{id}/status`: Transition status (`CONFIRMED`, `COMPLETED`, `CANCELLED`).
  - `DELETE /api/v1/appointments/{id}`: Delete appointment and free slot.
  - `GET /api/v1/stats/summary`: Aggregate analytics.
- **PostgreSQL & Alembic:** Table schemas version-controlled in `backend/alembic/versions/001_initial_mentorsync.py`.
- **React Frontend:** Modern responsive dashboard in `frontend/src/` with KPI cards, mentor search, booking modal, and appointment status management table.

### M2: Automated Testing (Pytest)
- **Isolated Testing:** Test suite in `backend/tests/` uses in-memory SQLite (`sqlite:///:memory:`) via `conftest.py`, completely decoupled from production PostgreSQL.
- **Coverage:** 10 comprehensive test cases covering happy path, validation errors, duplicate registrations, double-booking rejection, and slot release on cancellation.
- **Run Tests:** `pytest -v` inside `backend/`.

### M3: Version Control & Git Strategy
- Tracked on branch `main` with semantic commit history.
- Root `.gitignore` strictly excludes `.env`, secrets, `.terraform/`, `*.tfstate*`, `__pycache__`, and `node_modules`.

### M4: Docker Containerization
- **Backend Image:** Non-root user (`appuser` UID 10001), health-checked in `docker-compose.yml`.
- **Frontend Image:** Multi-stage build (`node:22-alpine` build -> `nginx:1.27-alpine` runtime) running as unprivileged user `nginx`.
- **Local Stack:** Run all 3 services via `docker compose up --build`.

### M5: GitHub Actions CI/CD Pipeline
- Workflow `.github/workflows/session21-capstone.yml` executes on every push to `main`.
- Enforces Pytest and frontend build gates before building Docker images.
- Publishes images to GitHub Container Registry (`ghcr.io`) tagged with immutable Git commit SHAs (`${{ github.sha }}`).

### M6: DevSecOps & Trivy Scanning
- Aqua Security Trivy scans both frontend and backend images in CI.
- **Security Gate:** Configured to fail on HIGH and CRITICAL vulnerabilities.
- **Scan Explanation:** Scans OS packages and application dependencies against the CVE database. A clean scan verifies no unpatched published exploits exist in the container filesystem.

### M7: Infrastructure as Code (Terraform)
- Complete HCL in `session21-python/terraform/`.
- Provisions AWS VPC across 2 Availability Zones (public & private subnets, single NAT gateway) and AWS EKS cluster v1.30 with managed node group (`t3.medium`).
- Includes safe `terraform.tfvars.example`.

### M8: Kubernetes Orchestration & Helm
- Complete chart in `session21-python/helm/mentorsync/`.
- Deploys:
  - 2 backend replicas and 2 frontend replicas.
  - ClusterIP services exposing ports 8000 and 80.
  - Ingress routing `/` to frontend and `/api` to backend.
  - HorizontalPodAutoscaler scaling backend between 2 and 6 replicas at 60% CPU utilization.
  - Liveness (`/health`) and Readiness (`/ready`) HTTP probes.

### M9: Observability (Prometheus + Grafana)
- Backend exposes Prometheus metrics at `/metrics`.
- Scraped via Prometheus `ServiceMonitor` every 15 seconds.
- Grafana dashboard definition in `monitoring/grafana-dashboard.json` visualizes request rates, p95 latency, error status codes, and active Pod health.

### M10: Presentation & Live Demo
- Step-by-step narrated presentation script and commit-to-deploy walkthrough documented in [`PRESENTATION.md`](PRESENTATION.md).
