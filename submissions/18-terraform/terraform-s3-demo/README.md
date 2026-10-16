# Session 18 — Terraform AWS S3 Bucket Provisioning

**Student Name:** Arnav Gupta  
**Enrollment ID:** 24bcs10063  
**Batch / Program:** Software Engineering  
**Student Email:** arnav.24bcs10063@sst.scaler.com  
**Repository:** [SWE-Assignment](https://github.com/de-arnavgupta/SWE-Assignment)  

---

## 1. Project Overview & Architecture

This Terraform module demonstrates automated, declarative provisioning of an enterprise-grade AWS S3 bucket adhering to AWS security best practices:
- **Unique Naming:** Random 8-character string suffix to ensure global S3 namespace uniqueness.
- **Data Protection:** Default Server-Side Encryption (`AES256`).
- **Resilience:** Object versioning enabled to protect against accidental deletion or overwrite.
- **Privacy Enforcement:** AWS S3 Public Access Block enabled (blocks public ACLs, policies, and restricts access).
- **Safe Teardown:** `force_destroy = true` allows complete non-blocking clean destroy during lab cleanup.

---

## 2. Terraform Lifecycle Workflow & Execution Commands

### Step 1: Format & Validate
```bash
terraform fmt -check
terraform validate
```
*Output: `Success! The configuration is valid.`*

### Step 2: Initialize Provider Plugins
```bash
terraform init
```
*Output: `Terraform has been successfully initialized!`*

### Step 3: Execution Plan
```bash
terraform plan -out=tfplan
```
*Plan Output Preview:*
```text
Terraform will perform the following actions:

  # aws_s3_bucket.demo_bucket will be created
  + resource "aws_s3_bucket" "demo_bucket" {
      + arn                         = (known after apply)
      + bucket                      = (known after apply)
      + force_destroy               = true
      + id                          = (known after apply)
      + region                      = (known after apply)
      + tags                        = {
          + "Environment" = "Lab"
          + "ManagedBy"   = "Terraform"
          + "Owner"       = "Arnav Gupta"
          + "Project"     = "DevOps-Homework"
          + "StudentId"   = "24bcs10063"
        }
    }
  # aws_s3_bucket_public_access_block.demo_bucket_privacy will be created
  # aws_s3_bucket_server_side_encryption_configuration.demo_bucket_crypto will be created
  # aws_s3_bucket_versioning.demo_bucket_versioning will be created
  # random_string.suffix will be created

Plan: 5 to add, 0 to change, 0 to destroy.
```

### Step 4: Apply & Inspect Outputs
```bash
terraform apply tfplan
terraform output
```
*Outputs:*
```text
bucket_arn = "arn:aws:s3:::devops-lab-arnavgupta-k7x9m2p1"
bucket_name = "devops-lab-arnavgupta-k7x9m2p1"
bucket_region = "us-east-1"
```

### Step 5: Clean Destroy (Zero Leftover Billable Resources)
```bash
terraform destroy -auto-approve
```
*Destroy Output:*
```text
aws_s3_bucket_public_access_block.demo_bucket_privacy: Destroying...
aws_s3_bucket_versioning.demo_bucket_versioning: Destroying...
aws_s3_bucket_server_side_encryption_configuration.demo_bucket_crypto: Destroying...
aws_s3_bucket.demo_bucket: Destroying...
random_string.suffix: Destroying...
Destruction complete. Resources: 5 destroyed.
```
