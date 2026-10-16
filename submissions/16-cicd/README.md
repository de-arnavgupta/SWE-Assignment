# Session 16 — CI/CD Automation with GitHub Actions

**Student Name:** Arnav Gupta  
**Enrollment ID:** 24bcs10063  
**Batch / Program:** Software Engineering  
**Student Email:** arnav.24bcs10063@sst.scaler.com  
**Workflow File:** `.github/workflows/demo-cicd.yml`  
**Repository:** [SWE-Assignment](https://github.com/de-arnavgupta/SWE-Assignment)  

---

## 1. Core Principles: CI vs. CD

```text
┌───────────────────────────────────────────────┐
│              CONTINUOUS INTEGRATION (CI)       │
│                                               │
│  Developer Push ──► Lint & SAST ──► Pytest   │
└───────────────────────┬───────────────────────┘
                        ▼
┌───────────────────────────────────────────────┐
│             CONTINUOUS DELIVERY (CD)          │
│                                               │
│  Build Docker Image ──► Push GHCR ──► Deploy  │
└───────────────────────────────────────────────┘
```

| Dimension | Continuous Integration (CI) | Continuous Delivery (CD) / Deployment |
|---|---|---|
| **Primary Goal** | Detect bugs early and prevent broken code from integrating into `main`. | Ensure code in `main` is always packaged and deployable to production. |
| **Key Actions** | Static linting, unit tests, integration tests, dependency checks. | Container image building, tagging with Git commit SHA, publishing to registry, deploying manifests to Kubernetes. |
| **Trigger** | Every pull request and push to any branch. | Merges / direct pushes to `main` branch. |
| **Failure Policy** | **Build Fails Immediately**: Branch cannot be merged if any test fails. | Rollout aborted; previous healthy revision preserved. |

---

## 2. GitHub Actions Architectural Components

1. **Workflow:** The automated configurable process defined in `.github/workflows/*.yml`.
2. **Events:** Triggers that activate the workflow (e.g. `on: push`, `on: pull_request`, `on: workflow_dispatch`).
3. **Jobs:** A set of sequential steps executed on the same runner environment. Jobs run in parallel by default unless ordered via `needs: [job_name]`.
4. **Steps:** Individual tasks executing either shell commands (`run: ...`) or pre-built community actions (`uses: actions/checkout@v4`).
5. **Runners:** Virtual machines provisioned on-demand (`runs-on: ubuntu-latest`) executing GitHub Actions jobs in isolated sandboxes.
6. **Secrets:** Secure, encrypted vault variables (`${{ secrets.GITHUB_TOKEN }}`) injected securely at runtime without exposing plain text in logs.
7. **Artifacts:** Persistent files produced by a workflow (test coverage XML, built binaries) saved using `actions/upload-artifact@v4`.

---

## 3. Workflow Pipeline Structure (`demo-cicd.yml`)

- **Job 1 (`test`):**
  - Checkouts repository code.
  - Provisions Python 3.11 environment.
  - Installs `pytest` and `flake8`.
  - Enforces syntax gates with `flake8`.
  - Executes automated unit tests with `pytest -v`.
  - Uploads test cache artifacts.
- **Job 2 (`build-and-deliver`):**
  - Depends on `needs: test` (ensures zero broken code is ever containerized).
  - Initializes Docker Buildx.
  - Authenticates to GitHub Container Registry (`ghcr.io`).
  - Builds and tags the container image using the Git commit SHA (`${{ github.sha }}`).
