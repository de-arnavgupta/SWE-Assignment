# AWS IAM — Identity & Access Management (Governance)

**Author:** Arnav Gupta (Roll: 24bcs10063)  
**Session:** Session 18 — Cloud Fundamentals  

---

## 1. What is AWS IAM?

AWS Identity and Access Management (IAM) is the central security control plane that regulates authentication (who you are) and authorization (what permissions you have) across all AWS services and resources.

---

## 2. Core IAM Building Blocks

- **IAM Users:** Persistent identity representing an individual person or service account requiring console or CLI/API access.
- **IAM Groups:** Collections of users sharing identical permission sets (e.g. `Developers`, `DevOpsAdmins`, `Auditors`).
- **IAM Roles:** Temporary identities that can be assumed by trusted entities (EC2 instances, Lambda functions, EKS ServiceAccounts, or external federated users via SAML/OIDC). Roles do not use long-term static passwords or access keys; AWS STS (Security Token Service) issues temporary credentials expiring within 1–12 hours.
- **IAM Policies:** Formal JSON documents explicitly declaring `Effect` (Allow/Deny), `Action` (e.g. `s3:GetObject`), `Resource` (e.g. `arn:aws:s3:::my-bucket/*`), and optional `Condition` clauses.

---

## 3. The Principle of Least Privilege & Best Practices

1. **Principle of Least Privilege:** Grant only the exact, minimal permissions required to complete the designated job function, and nothing more. Never attach wildcard `AdministratorAccess` to application workloads.
2. **Lock Down the Root User:** Enable MFA (Hardware/FIDO or Authenticator), lock away root access keys, and use root only for initial account bootstrapping.
3. **IAM Roles for Compute Workloads:** Never hardcode AWS Access Key ID and Secret Access Key inside EC2 instances, containers, or code repositories. Use IAM Instance Profiles and EKS IRSA (IAM Roles for Service Accounts).
4. **Enforce Multi-Factor Authentication (MFA):** Mandate MFA across all human IAM users and administrative roles.
5. **Rotate Access Credentials:** Implement automatic 90-day key rotation policies and monitor dormant credentials via AWS IAM Credential Reports.
