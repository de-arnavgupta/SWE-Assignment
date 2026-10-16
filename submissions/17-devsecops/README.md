# Session 17 — DevSecOps Pipeline & Security Gates

**Student Name:** Arnav Gupta  
**Enrollment ID:** 24bcs10063  
**Batch / Program:** Software Engineering  
**Student Email:** arnav.24bcs10063@sst.scaler.com  
**Workflow File:** `.github/workflows/devsecops-pipeline.yml`  
**Repository:** [SWE-Assignment](https://github.com/de-arnavgupta/SWE-Assignment)  

---

## 1. DevSecOps Paradigm: Shift-Left Security

DevSecOps shifts security checks from a post-release compliance audit to an automated, gate-driven developer workflow integrated directly into the CI/CD pipeline.

```text
Code Commit
    │
    ▼
[ Gate 1: Gitleaks ] ────────► Fails if API keys / tokens detected in Git tree
    │
    ▼
[ Gate 2: Bandit SAST ] ────► Fails on unsafe SQL concatenation, shell injections
    │
    ▼
[ Gate 3: pip-audit SCA ] ──► Fails if third-party libraries have known CVEs
    │
    ▼
[ Docker Build ]
    │
    ▼
[ Gate 4: Trivy Scan ] ─────► Fails on HIGH or CRITICAL base image / package CVEs
    │
    ▼
[ GHCR Publish & Deploy ] ──► Only images passing all 4 gates are published!
```

---

## 2. Security Tooling Breakdown

### 1. Secret Scanning (Gitleaks)
- **Role:** Scans git commits, branches, and staged files for regular expressions matching private keys, cloud provider secrets (AWS, GCP), JWT tokens, and connection strings.
- **Enforcement:** `continue-on-error: false` blocks any commit containing committed credentials from progressing through the pipeline.

### 2. Static Application Security Testing — SAST (Bandit)
- **Role:** Analyzes Python AST (Abstract Syntax Tree) without executing code. Detects SQL injections, hardcoded credentials, insecure deserialization (`pickle`), and unvetted shell subprocesses (`shell=True`).
- **Command:** `bandit -r ./session21-python/backend/app -ll -ii` (reports Medium and High severity issues).

### 3. Software Composition Analysis — SCA (`pip-audit`)
- **Role:** Scans all application dependencies in `requirements.txt` against the PyPI Advisory Database and Google OSV (Open Source Vulnerabilities) database.
- **Enforcement:** Blocks deployment if vulnerable libraries with known exploits are discovered before updating to patched versions.

### 4. Container Vulnerability Scanning (Aqua Security Trivy)
- **Role:** Deep inspection of container OS packages (Alpine/Debian musl/glibc) and language-specific runtime libraries.
- **Gate Specification:**
  ```yaml
  exit-code: '1'
  severity: 'CRITICAL,HIGH'
  ignore-unfixed: true
  ```
- **Rationale for `ignore-unfixed: true`:** Focuses enforcement strictly on actionable vulnerabilities where upstream maintainers have issued a patch, preventing false-positive pipeline deadlocks on theoretical or unpatched upstream bugs.

---

## 3. Explaining Scan Results & Security Caveats

> [!NOTE]
> **Why a 0-Vulnerability Clean Scan is NOT Proof of Absolute Security:**  
> A clean Trivy scan confirms that no *known, published CVEs* in public databases match the installed package versions. It does **not** guarantee the absence of zero-day vulnerabilities, business logic flaws (e.g. Broken Object Level Authorization - BOLA), runtime misconfigurations, or insider threat vectors. Security is a defense-in-depth practice requiring least privilege IAM, runtime WAF inspection, and ongoing observability.
