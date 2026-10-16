# Session 18 — Terraform & Infrastructure as Code (IaC)

**Student Name:** Arnav Gupta  
**Enrollment ID:** 24bcs10063  
**Batch / Program:** Software Engineering  
**Student Email:** arnav.24bcs10063@sst.scaler.com  
**Repository:** [SWE-Assignment](https://github.com/de-arnavgupta/SWE-Assignment)  

---

## 1. Session Overview

Session 18 bridges declarative cloud infrastructure automation using HashiCorp Terraform with in-depth research into core Amazon Web Services (AWS) architectural building blocks.

---

## 2. Deliverables Index

### Task 1: Terraform S3 Bucket Hands-on Demo
- **Directory:** [`terraform-s3-demo/`](terraform-s3-demo/)
- **Documentation & Plan Output:** [`terraform-s3-demo/README.md`](terraform-s3-demo/README.md)
- **Key Modules:**
  - `provider.tf`: Configures AWS provider `~> 5.0` with standard enterprise tagging.
  - `main.tf`: Provisions an encrypted, versioned, private S3 bucket with random suffix.
  - `variables.tf` & `outputs.tf`: Clean input variables and exported attributes.
  - `terraform.tfvars.example`: Safe example variables template without committed secrets.

### Task 2: AWS Services Technical Research Modules
- **01. IAM (Governance & Security):** [`aws-services/01-iam/README.md`](aws-services/01-iam/README.md)
- **02. EC2 (Compute Infrastructure):** [`aws-services/02-ec2/README.md`](aws-services/02-ec2/README.md)
- **03. S3 (Object Storage & Lifecycle):** [`aws-services/03-s3/README.md`](aws-services/03-s3/README.md)
- **04. VPC (Cloud Networking & Subnets):** [`aws-services/04-vpc/README.md`](aws-services/04-vpc/README.md)
- **05. DynamoDB & RDS (Database Services):** [`aws-services/05-dynamodb-rds/README.md`](aws-services/05-dynamodb-rds/README.md)
