# DevOps Coursework & Capstone — Requirement Completion Tracker

**Student:** Arnav Gupta  
**Enrollment:** 24bcs10063  
**Batch / Program:** Software Engineering  
**Email:** arnav.24bcs10063@sst.scaler.com  
**GitHub:** [de-arnavgupta](https://github.com/de-arnavgupta)  
**Repository:** [SWE-Assignment](https://github.com/de-arnavgupta/SWE-Assignment)  

Status Legend:
- `Implemented`: Code and documentation authored and ready
- `Passed`: Executed and verified with authentic evidence
- `In Progress`: Active implementation / verification underway
- `Blocked / Awaiting`: Requires external user action (e.g. AWS budget approval, cloud console screenshot, GitHub repo creation)
- `Student-Only`: Tasks explicitly reserved for the student (e.g. narrated live presentation, personal form submission)

---

## Complete Requirements Audit Table

| Session | Exact Requirement | Implementation Path | Verification Command | Evidence Link | Status |
|---|---|---|---|---|---|
| **01 & 02** | Soft Link vs Hard Link demonstration, inode inspection, deletion behavior | `session2-linux/README.md` | `ln -s`, `ln`, `ls -li`, `rm` | `session2-linux/README.md#task-1` | Implemented |
| **01 & 02** | `adduser` vs `useradd` comparison & test user lifecycle in Linux | `session2-linux/README.md` | `useradd`, `adduser`, `id`, `userdel` | `session2-linux/README.md#task-2` | Implemented |
| **01 & 02** | `journalctl` system & service log viewing and filtering | `session2-linux/README.md` | `journalctl -u <service>`, `journalctl -n 20` | `session2-linux/README.md#task-3` | Implemented |
| **01 & 02** | Linux Command Cheat Sheet review & execution outputs | `session2-linux/README.md` | Cheat sheet command suite | `session2-linux/README.md#task-4` | Implemented |
| **03** | System info shell script (date, hostname, username, df, ps, variables, `read -p`, mkdir, touch, `>` redirection) | `session3-shell-scripting/system_info.sh`, `session3-shell-scripting/README.md` | `bash system_info.sh` | `session3-shell-scripting/README.md` | Implemented |
| **04** | Networking commands (ip/ifconfig, route/netstat, ping, traceroute, nslookup/dig, ss/netstat) with analysis | `session4-networking/README.md` | `ip addr`, `ping -c 3`, `dig`, `ss -tuln` | `session4-networking/README.md` | Implemented |
| **05** | `git commit -a -m` vs `git commit -m` demo with untracked file behavior | `session5-git-github/README.md` | `git commit -a -m`, `git status` | `session5-git-github/README.md#task-1` | Implemented |
| **05** | Branch sequence, commit history, cherry-pick verification into main | `session5-git-github/README.md` | `git cherry-pick <hash>`, `git log --graph --oneline` | `session5-git-github/README.md#task-2` | Implemented |
| **06 & 07** | 6 Hello World Docker web apps (`nodejs-app`, `python-app`, `java-app`, `Apache-app`, `React-app`, `nginx-app`) | `session6-7-docker/*/Dockerfile`, `session6-7-docker/README.md` | `docker build`, `docker run -d -p`, `curl` | `session6-7-docker/README.md` | Implemented |
| **07** | Docker Multi-Stage build app on port 8080 showing required response | `session6-7-docker/multi-stage-dockerfile/Dockerfile`, `session6-7-docker/multi-stage-dockerfile/README.md` | `docker build -t multi-app .`, `docker ps`, `curl localhost:8080` | `session6-7-docker/multi-stage-dockerfile/README.md` | Implemented |
| **08** | 3-tier Docker networking (frontend, backend, MySQL, 3 networks, backend on 2 networks, isolation tests) | `session8-docker-networking-volume/docker-compose.yml`, `session8-docker-networking-volume/README.md` | `docker compose up -d`, `docker exec ping` | `session8-docker-networking-volume/README.md#task-1` | Implemented |
| **08** | Apache host network, Nginx bind mount with live edit, Overlay network research | `session8-docker-networking-volume/README.md` | `docker run --net=host`, bind mount test | `session8-docker-networking-volume/README.md#tasks-2-4` | Implemented |
| **09** | Kubernetes architecture, cluster status verification, k8s basics tutorial | `submissions/09-kubernetes-fundamentals/README.md` | `kubectl cluster-info`, `kubectl get nodes` | `submissions/09-kubernetes-fundamentals/README.md` | Implemented |
| **10** | 4 deployment strategies: Rolling Update, Blue-Green, Canary, Recreate; Pod lifecycle | `submissions/10-kubernetes-core-objects/README.md` | `kubectl rollout status`, selector switch, canary test | `submissions/10-kubernetes-core-objects/README.md` | Implemented |
| **11** | 5 Service types (ClusterIP, NodePort, LoadBalancer, ExternalName, Headless); Object comparisons; FQDN & CoreDNS | `submissions/11-kubernetes-services/README.md`, `submissions/11-kubernetes-services/fqdn/README.md`, `submissions/11-kubernetes-services/coredns/README.md` | `kubectl get svc`, `nslookup <svc-fqdn>` | `submissions/11-kubernetes-services/README.md` | Implemented |
| **12** | ConfigMaps, Secrets, Ingress routing, Ingress vs Controller docs, troubleshooting | `submissions/12-kubernetes-config-ingress/README.md` | `kubectl exec env`, `curl -H "Host: ..."` | `submissions/12-kubernetes-config-ingress/README.md` | Implemented |
| **13** | Storage (emptyDir, hostPath, PV, PVC, StorageClass), HPA load scaling, probes recovery | `submissions/13-storage-hpa-probes/README.md` | `kubectl get hpa`, `kubectl top pods`, load test | `submissions/13-storage-hpa-probes/README.md` | Implemented |
| **14** | Kubernetes troubleshooting (CrashLoopBackOff, ImagePull, Pending, Services, DNS, OOM), mini-project | `submissions/14-troubleshooting/README.md` | `kubectl describe`, `kubectl logs`, root cause fixes | `submissions/14-troubleshooting/README.md` | Implemented |
| **15** | Helm commands, install → upgrade → rollback → verify sequence, custom chart mini-project | `submissions/15-helm/README.md` | `helm upgrade`, `helm rollback`, `helm history` | `submissions/15-helm/README.md` | Implemented |
| **16** | CI/CD demo with GitHub Actions (build, test, artifacts, delivery, workflow breakdown) | `submissions/16-cicd/README.md`, `.github/workflows/demo-cicd.yml` | GitHub Actions workflow run | `submissions/16-cicd/README.md` | Implemented |
| **17** | Complete DevSecOps pipeline (SAST, SCA, Secret scan, Docker build, Trivy scan, K8s deploy) | `submissions/17-devsecops/README.md`, `.github/workflows/devsecops-pipeline.yml` | GitHub Actions DevSecOps workflow run | `submissions/17-devsecops/README.md` | Implemented |
| **18** | Terraform S3 bucket demo (init, fmt, validate, plan, apply, show, destroy) & AWS Services research | `submissions/18-terraform/README.md`, `submissions/18-terraform/aws-services/*/README.md` | `terraform plan`, `terraform validate` | `submissions/18-terraform/README.md` | Implemented |
| **19** | Cloud Terraform project (VPC, Subnets, Security Group, EC2, S3) | `submissions/19-cloud/README.md`, `submissions/19-cloud/terraform/` | `terraform plan`, architecture docs | `submissions/19-cloud/README.md` | Implemented |
| **20** | Monitoring (Prometheus/Grafana), Observability (3 pillars), GitOps (Argo CD sync & drift) | `submissions/20-monitoring-gitops/README.md` | Prometheus targets check, Argo CD sync | `submissions/20-monitoring-gitops/README.md` | Implemented |
| **21 (M1)** | Capstone App: Original domain (MentorSync), FastAPI backend, PostgreSQL DB, Alembic, React UI, >=4 REST endpoints | `session21-python/backend/`, `session21-python/frontend/` | `pytest`, `docker compose up --build` | `session21-python/README.md#m1` | Implemented |
| **21 (M2)** | Capstone Testing: >=5 pytest tests across >=3 endpoints, isolated DB, `pytest.ini`/`conftest.py` | `session21-python/backend/tests/` | `pytest -v` | `session21-python/README.md#m2` | Implemented |
| **21 (M3)** | Capstone Git: Public repo, meaningful commits (>=10), clean `.gitignore` | `.gitignore`, Git commit history | `git log --oneline` | `session21-python/README.md#m3` | Passed (16 commits) |
| **21 (M4)** | Capstone Docker: Non-root backend/frontend, multi-stage frontend, working Compose stack | `session21-python/Dockerfile*`, `session21-python/docker-compose.yml` | `docker compose up --build` | `session21-python/README.md#m4` | Implemented |
| **21 (M5)** | Capstone CI/CD: GitHub Actions on main push, pytest, frontend build, SHA-tagged GHCR images | `.github/workflows/session21-capstone.yml` | GitHub Actions Run URL | `session21-python/README.md#m5` | Implemented |
| **21 (M6)** | Capstone DevSecOps: Trivy scan on backend & frontend images, fail on HIGH/CRITICAL, CVE write-up | `.github/workflows/session21-capstone.yml` | Trivy job logs | `session21-python/README.md#m6` | Implemented |
| **21 (M7)** | Capstone Terraform: AWS VPC (2 public subnets), EKS cluster, worker nodes, `tfvars.example`, clean destroy | `session21-python/terraform/` | `terraform fmt`, `terraform validate`, `terraform plan` | `session21-python/README.md#m7` | Blocked (Awaiting AWS approval) |
| **21 (M8)** | Capstone Kubernetes + Helm: Namespace, Helm chart, >=2 backend/frontend replicas, Ingress `/` and `/api`, HPA | `session21-python/helm/`, `session21-python/k8s/` | `helm upgrade --install`, `kubectl get pods -n mentorsync` | `session21-python/README.md#m8` | Implemented |
| **21 (M9)** | Capstone Observability: `/metrics` Prometheus endpoint, Prometheus scraping, Grafana dashboard panels | `session21-python/monitoring/` | `curl localhost:8000/metrics` | `session21-python/README.md#m9` | Implemented |
| **21 (M10)** | Capstone Presentation & Live Demo: Root README, narrated outline, live commit-to-deploy sequence | `session21-python/README.md`, `session21-python/PRESENTATION.md` | Student presentation delivery / recording | `session21-python/PRESENTATION.md` | Student-Only |
