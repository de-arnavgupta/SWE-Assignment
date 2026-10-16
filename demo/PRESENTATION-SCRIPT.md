# MentorSync — Capstone Presentation & Video Walkthrough Script
## Complete Spoken Guide & Screen Recording Runbook

**Presenter:** Arnav Gupta  
**Enrollment:** 24bcs10063  
**Target Video Duration:** 6 — 8 minutes  
**Format:** Screen recording with voiceover (MP4)  
**File Destination:** `demo/presentation.mp4`

---

### Video Walkthrough Order & Timeline

| Section | Topic | Duration | Screen Content to Show |
|---|---|---|---|
| **Part 1** | PPT Slides Presentation | ~2:00 min | Presentation slide deck (`demo/presentation-slides.md` or exported slides) |
| **Part 2** | Codebase Walkthrough | ~1:00 min | VS Code / IDE: Folder layout, `main.py`, `models.py`, `conftest.py`, `Dockerfile` |
| **Part 3** | CI/CD Pipeline in Action | ~1:00 min | GitHub Actions: Push trigger, live workflow run, green checks, GHCR packages |
| **Part 4** | Terraform Infrastructure | ~1:00 min | Terminal `terraform plan` output & AWS Console / Architecture diagram |
| **Part 5** | GitOps with Argo CD | ~0:45 min | Argo CD dashboard showing `mentorsync` application in `Synced` & `Healthy` state |
| **Part 6** | Kubernetes Cluster State | ~0:45 min | Terminal: `kubectl get pods,svc,ingress,hpa -n mentorsync` showing all running |
| **Part 7** | Observability (Prometheus & Grafana) | ~1:00 min | Prometheus Targets (`UP`), `curl /metrics`, and Grafana dashboard panels |

---

## Detailed Spoken Script (Word-for-Word Walkthrough)

### [0:00 - 2:00] Part 1: PPT Slides & Project Overview
> **Screen:** Display Slide 1 of your presentation.

**Spoken:**
> "Hello everyone, my name is Arnav Gupta, enrollment number 24bcs10063. Today, I am presenting my DevSecOps Capstone Project: **MentorSync**—a cloud-native office hours and peer tutoring platform.
>
> In universities, booking office hours with professors, teaching assistants, or peer tutors is often uncoordinated and managed across ad-hoc email threads or spreadsheets. This frequently leads to scheduling conflicts, accidental double-bookings, and abandoned slots when appointments get cancelled.
>
> MentorSync solves this with a deterministic booking engine that features dynamic slot creation, concurrency-locked reservations to eliminate double-booking, and automated slot reclamation whenever an appointment is cancelled.
>
> Moving to our technology stack: the backend is powered by Python 3.12, FastAPI, and SQLAlchemy 2.0 with PostgreSQL 16 as our relational database, managed via version-controlled Alembic migrations. The frontend is a responsive React 18 single-page application built with Vite. Our testing harness uses Pytest with an in-memory SQLite fixture for rapid, zero-dependency test runs.
>
> Our architecture follows cloud-native best practices: clients connect through an Ingress controller which routes traffic to our frontend static Nginx pods and backend FastAPI pods. The backend is configured with Horizontal Pod Autoscaling from 2 to 6 replicas, and both containers run as unprivileged, non-root users. The backend exposes Prometheus metrics that are scraped and visualized in real-time in Grafana. Let's now dive into the live walkthrough."

---

### [2:00 - 3:00] Part 2: Codebase Walkthrough
> **Screen:** Open VS Code showing the repository root.

**Spoken:**
> "Here is our repository structure. In `session21-python/backend/app/`, we have our modular backend application:
> - `main.py` defines our 8 REST endpoints for mentors, slots, bookings, and statistics, alongside `/health`, `/ready`, and Prometheus instrumentation.
> - `models.py` defines our SQLAlchemy relational entities: Mentors, Slots, and Appointments with foreign key constraints.
> - `schemas.py` uses Pydantic v2 for strict request validation and email format verification.
> - In `backend/tests/`, we have `conftest.py` setting up an isolated SQLite in-memory test database, and `test_mentorsync_api.py` with 10 comprehensive test cases covering happy paths, edge cases, double-booking prevention, and status transitions.
> - Our `Dockerfile` in both backend and frontend use hardened, multi-stage builds running under unprivileged user IDs, specifically UID 10001 for our backend."

---

### [3:00 - 4:00] Part 3: CI/CD Pipeline & GitHub Actions
> **Screen:** Open GitHub repository `https://github.com/de-arnavgupta/SWE-Assignment/actions`.

**Spoken:**
> "Next, let's look at our automated CI/CD pipeline defined in `.github/workflows/session21-capstone.yml`. 
>
> On every push to the `main` branch, GitHub Actions executes two gated jobs:
> 1. First, **Backend Tests & Frontend Build Gate**: It installs dependencies, runs Flake8 linting, executes all 10 Pytest test cases, and compiles the React production bundle using Vite.
> 2. Second, **Docker Build, Trivy Gate & GHCR Publish**: It builds our container images using Docker Buildx and passes them through an Aqua Security Trivy vulnerability scan. The pipeline is strictly configured to fail if any unfixed HIGH or CRITICAL vulnerabilities are detected.
>
> Here in the Actions dashboard, you can see our workflow runs have completed with 100% green status. The resulting container images are published to the GitHub Container Registry with immutable Git commit SHA tags."

---

### [4:00 - 5:00] Part 4: Terraform Infrastructure as Code
> **Screen:** Open terminal in `session21-python/terraform/` or show terminal output of `terraform plan`.

**Spoken:**
> "Turning to our infrastructure as code, located in `session21-python/terraform/`, we have declared our cloud architecture using Terraform:
> - `vpc.tf` provisions an AWS Virtual Private Cloud spanning two Availability Zones with public and private subnets, an Internet Gateway, and NAT Gateway.
> - `eks.tf` provisions our AWS EKS Kubernetes cluster running version 1.30, backed by an IAM OIDC provider and a managed node group utilizing `t3.medium` instances.
> - All parameters are externalized in `variables.tf` and accompanied by a safe `terraform.tfvars.example` file to guarantee no cloud credentials or secrets are ever tracked in Git.
> - Running `terraform plan` confirms our execution plan is clean, validated, and ready to provision with zero drift."

---

### [5:00 - 5:45] Part 5: GitOps Deployment with Argo CD
> **Screen:** Open Argo CD web UI or display Argo CD application manifest in `session21-python/gitops/`.

**Spoken:**
> "For continuous deployment, we employ a declarative GitOps model using Argo CD.
> - Argo CD tracks our Helm chart in Git and synchronizes it continuously against our Kubernetes cluster.
> - As shown in the Argo CD application topology, all resources—Deployments, Services, Ingress, and HPA—are in a `Synced` and `Healthy` state. If any configuration drift occurs in the cluster, Argo CD automatically detects and remediates it back to the Git source of truth."

---

### [5:45 - 6:30] Part 6: Kubernetes Cluster State
> **Screen:** Terminal running `kubectl` commands against the cluster.

**Spoken:**
> "Let's inspect our live Kubernetes cluster state by running:
> ```bash
> kubectl get all -n mentorsync
> ```
> Notice that:
> - We have 2 backend pod replicas and 2 frontend pod replicas running in healthy status.
> - Our backend and frontend are exposed via internal ClusterIP services.
> - Our Horizontal Pod Autoscaler is monitoring backend CPU usage with a target of 60%, configured to scale up to 6 replicas under load.
> - The Ingress resource routes external HTTP traffic on port 80 to our frontend for `/` and our API service for `/api`."

---

### [6:30 - 7:30] Part 7: Observability (Prometheus & Grafana) & Conclusion
> **Screen:** Open Prometheus Targets page, then switch to Grafana Dashboard.

**Spoken:**
> "Finally, let's examine our full observability stack:
> - In Prometheus, visiting `/targets` confirms that our `mentorsync-backend` ServiceMonitor target is in the `UP` state, scraping metrics every 15 seconds.
> - Querying `curl http://localhost:8000/metrics` returns standard Prometheus formatted telemetry including HTTP request counters, request latency histograms, and Python runtime metrics.
> - In our pre-configured Grafana dashboard, we have real-time visibility into incoming request rate, 95th percentile latency, HTTP status code distribution (monitoring for 4xx and 5xx anomalies), and active pod memory/CPU utilization.
>
> In conclusion, MentorSync demonstrates a full-lifecycle, production-ready DevSecOps implementation—from clean modular Python/React application code and automated Pytest gates, to Trivy vulnerability scanning, Terraform AWS provisioning, Helm orchestration, GitOps delivery, and full-stack observability.
>
> Thank you for your time!"
