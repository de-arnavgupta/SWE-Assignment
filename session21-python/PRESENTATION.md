# MentorSync — Capstone Presentation Outline & Live Demo Script

**Presenter / Student:** Arnav Gupta  
**Enrollment ID:** 24bcs10063  
**Batch / Section:** Software Engineering  
**Application:** MentorSync (Office Hours & Peer Tutoring Booking Platform)  
**Target Repository:** [SWE-Assignment](https://github.com/de-arnavgupta/SWE-Assignment)  

---

## 1. Presentation Structure (5–7 Minute Walkthrough)

### Slide 1: Title & Problem Statement (0:00 - 1:00)
- **Problem:** University students struggle to discover faculty office hours and peer tutors; scheduling conflicts and double bookings cause missed academic support.
- **Solution:** MentorSync — a cloud-native, microservices-ready consultation platform providing real-time booking, slot synchronization, and containerized deployment.

### Slide 2: Full-Stack Architecture & Originality (1:00 - 2:00)
- **FastAPI Backend:** Asynchronous Python API, SQLAlchemy 2.0 ORM, Alembic migrations.
- **Domain Models:** `Mentor`, `Slot`, `Appointment` state machine.
- **React Frontend:** Responsive SPA with dark UI, live KPI cards, search/filter, and booking modal.
- **Originality Highlights:** Distinct academic consultation schema; double-booking validation; automatic slot release on appointment cancellation.

### Slide 3: Containerization & CI/CD DevSecOps (2:00 - 3:15)
- **Docker:** Non-root users (`appuser` UID 10001, `nginx`), multi-stage frontend build reducing image footprint by 80%.
- **GitHub Actions Pipeline:** Triggered on main push -> Pytest tests -> Frontend build -> Trivy container vulnerability scan -> GHCR image publish with Git commit SHA tags.

### Slide 4: Cloud Infrastructure & Kubernetes (3:15 - 4:15)
- **Terraform:** Declarative VPC (multi-AZ subnets, NAT gateway, route tables) and Amazon EKS cluster v1.30.
- **Helm Package Management:** Custom chart in `helm/mentorsync/` managing deployments, ClusterIP services, Ingress (`/` to frontend, `/api` to backend), and HPA.

### Slide 5: Observability & Resilience (4:15 - 5:00)
- **Prometheus:** Real-time scraping of `/metrics` endpoint.
- **Grafana Dashboard:** Visualizing throughput (req/sec), p95 latency, error status codes, and active Pod health.
- **Self-Healing:** Readiness and liveness probes; HPA autoscaling from 2 to 6 replicas under load.

---

## 2. Live Demo Sequence: Commit → Pipeline → Deployed Application

To fulfill the rubric requirement (*"commit a visible change, watch the pipeline run, see the deployment update"*), execute this exact verified workflow:

### Step 1: Make a Visible Code Change
Edit `frontend/src/main.jsx` to update the header subtitle or banner:
```jsx
// Change:
<p>Office Hours & Peer Tutoring Platform — DevOps Final Capstone</p>
// To:
<p>Office Hours & Peer Tutoring Platform — Version 1.1 Live Demo (Arnav Gupta)</p>
```

### Step 2: Commit and Push to Main
```bash
git add frontend/src/main.jsx
git commit -m "feat(ui): update banner subtitle for live presentation demo"
git push origin main
```

### Step 3: Observe GitHub Actions Green Pipeline Run
1. Open repository Actions tab: `https://github.com/de-arnavgupta/SWE-Assignment/actions`.
2. Watch the workflow execute:
   - `test-and-build`: Pytest runs clean -> Frontend compiles.
   - `security-scan-and-publish`: Docker build -> Trivy scan passes -> Image pushed to GHCR with new commit SHA.

### Step 4: Verify Updated Deployed Application
1. Refresh the application URL (or port-forward / Ingress host `http://localhost:3000` or `http://mentorsync.local`).
2. Point out the updated subtitle live on screen:
   `Office Hours & Peer Tutoring Platform — Version 1.1 Live Demo (Arnav Gupta)`
3. Demonstrate live slot booking:
   - Select an open slot for a mentor.
   - Enter student name `Arnav Gupta` and roll `24bcs10063`.
   - Submit booking: Verify appointment appears in the table with status `CONFIRMED`.
   - Click "✕ Cancel": Verify status changes to `CANCELLED` and the mentor's slot button flips back from "Booked" to "Book Slot" in real time.
