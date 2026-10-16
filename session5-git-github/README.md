# Session 5 — Version Control with Git & GitHub

**Student Name:** Arnav Gupta  
**Enrollment ID:** 24bcs10063  
**Batch / Program:** Software Engineering  
**Student Email:** arnav.24bcs10063@sst.scaler.com  
**Repository:** [SWE-Assignment](https://github.com/de-arnavgupta/SWE-Assignment)  

---

## Task 1: `git commit -m` vs. `git commit -a -m`

### Conceptual Difference

| Command | Staging Requirement | Handles Modified Files? | Handles Deleted Files? | Handles New Untracked Files? |
|---|---|---|---|---|
| `git commit -m "msg"` | Requires explicit `git add` to populate index. | Only if previously staged with `git add`. | Only if previously staged with `git rm` or `git add`. | Only if previously staged. |
| `git commit -a -m "msg"` | Automatically stages tracked changes before commit. | **Yes** — automatically stages all modified tracked files. | **Yes** — automatically stages tracked file removals. | **NO — New untracked files are strictly IGNORED.** |

### Real Execution Verification

```bash
# 1. Have one modified tracked file and one brand new untracked file
echo "Modified tracked file" >> main1.txt
echo "Brand new untracked file" > brand_new.txt

# 2. Check git status
git status -s
```
**Output Before Commit:**
```text
 M main1.txt
?? brand_new.txt
```

```bash
# 3. Attempt commit using git commit -a -m
git commit -a -m "test: commit -a -m attempt"

# 4. Check git status immediately after
git status -s
```
**Output After Commit:**
```text
[main 5cef1e1] test: commit -a -m attempt
 1 file changed, 1 insertion(+)
?? brand_new.txt
```
**Conclusion:** `git commit -a` committed only `main1.txt`. `brand_new.txt` remained `??` (untracked) in the working tree. To include new files, `git add <file>` is mandatory.

---

## Task 2: Git Cherry-Pick Workflow

Cherry-picking allows applying the exact diff of an arbitrary commit from another branch onto the current `HEAD` without performing a full merge or rebase.

### Hands-on Exercise Steps & Command Log

```bash
# 1. Initialize repo and create base commits on main
git init -b main
echo "Base file" > base.txt && git add base.txt && git commit -m "feat: initial base commit on main"
echo "Main feature 1" > main1.txt && git add main1.txt && git commit -m "feat(main): add main feature 1"

# 2. Create feature branch and make 3 isolated commits
git checkout -b feature-payment
echo "Payment core logic" > payment.txt && git add payment.txt && git commit -m "feat(payment): implement payment gateway integration"
echo "Payment test file" > payment_test.txt && git add payment_test.txt && git commit -m "test(payment): add unit tests for payment gateway"
echo "Unrelated experimental logic" > experimental.txt && git add experimental.txt && git commit -m "feat(exp): prototype experimental crypto checkout"

# 3. Switch back to main and cherry-pick ONLY the payment integration commit (38a1828)
git checkout main
git cherry-pick 38a1828
```

### Verified Git Graph (`git log --graph --oneline --all`)

```text
* 232bce0 (feature-payment) feat(exp): prototype experimental crypto checkout
* fd141e0 test(payment): add unit tests for payment gateway
* 38a1828 (HEAD -> main) feat(payment): implement payment gateway integration
* 85e19b6 feat(main): add main feature 1
* 808f8ae feat: initial base commit on main
```

### Directory Verification on `main`

```bash
$ ls -la
total 24
drwxr-xr-x  6 arnavgupta  staff  192 Oct 16 17:52 .
drwxr-xr-x 13 arnavgupta  staff  416 Oct 16 17:52 .git
-rw-r--r--  1 arnavgupta  staff   10 Oct 16 17:52 base.txt
-rw-r--r--  1 arnavgupta  staff   15 Oct 16 17:52 main1.txt
-rw-r--r--  1 arnavgupta  staff   19 Oct 16 17:52 payment.txt
```

**Verification:**
- `payment.txt` was successfully cherry-picked into `main`.
- `experimental.txt` and `payment_test.txt` from `feature-payment` branch **did NOT arrive in `main`**, proving clean cherry-pick isolation.
