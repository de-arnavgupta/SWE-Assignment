# Session 19 — End-to-End Cloud Infrastructure with Terraform

**Student Name:** Arnav Gupta  
**Enrollment ID:** 24bcs10063  
**Batch / Program:** Software Engineering  
**Student Email:** arnav.24bcs10063@sst.scaler.com  
**Terraform Code Location:** `submissions/19-cloud/terraform/`  
**Repository:** [SWE-Assignment](https://github.com/de-arnavgupta/SWE-Assignment)  

---

## 1. Cloud Architecture

```text
AWS Cloud Region: us-east-1
┌─────────────────────────────────────────────────────────────┐
│ Custom VPC: 10.0.0.0/16                                      │
│                                                             │
│   Internet Gateway (devops-igw-arnav)                        │
│   ┌───────────────────────────────────────────────────────┐ │
│   │ Public Route Table (0.0.0.0/0 -> IGW)                 │ │
│   └───────┬───────────────────────────────────────────────┘ │
│           │                                                 │
│     ┌─────┴─────────────────────┐                           │
│     ▼                           ▼                           │
│  [ Public Subnet 1 ]         [ Public Subnet 2 ]            │
│  (10.0.1.0/24 - us-east-1a)  (10.0.2.0/24 - us-east-1b)     │
│     │                                                       │
│     ▼                                                       │
│  [ EC2 Instance: t3.micro ]                                 │
│  (Ubuntu 22.04 LTS + Nginx)                                 │
│  Security Group: Ingress 80 (HTTP), 22 (SSH)                │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
                 [ Encrypted S3 App Bucket ]
                 (devops-app-data-arnavgupta-*)
                 SSE-S3 (AES256) + Versioning Enabled
```

---

## 2. Terraform Modules & Resources

1. **`provider.tf`:** Declares AWS provider `~> 5.0` with enterprise-standard default tags (`Project`, `Owner: Arnav Gupta`, `StudentId: 24bcs10063`, `ManagedBy: Terraform`).
2. **`vpc.tf`:** Creates `aws_vpc` with DNS hostnames enabled, `aws_internet_gateway`, two multi-AZ public `aws_subnet` resources, route table, and subnet route table associations.
3. **`security_groups.tf`:** Stateful security group allowing port 80 (HTTP) to world, port 22 (SSH) restricted to admin CIDR, and all outbound egress.
4. **`ec2.tf`:** Ubuntu 22.04 LTS `t3.micro` instance bootstrapped with automated `user_data` installing and starting Nginx web server with custom HTML response.
5. **`s3.tf`:** Private S3 bucket with random suffix, `AES256` default encryption, versioning, and AWS Public Access Block.
6. **`outputs.tf`:** Exports `vpc_id`, `public_subnet_ids`, `ec2_public_ip`, and `s3_bucket_name`.

---

## 3. Plan & Verification Execution Output

```bash
cd submissions/19-cloud/terraform
terraform init
terraform plan
```

**Plan Output Preview:**
```text
Plan: 10 to add, 0 to change, 0 to destroy.

Changes to Outputs:
  + ec2_instance_id   = (known after apply)
  + ec2_public_ip     = (known after apply)
  + public_subnet_ids = [
      + (known after apply),
      + (known after apply),
    ]
  + s3_bucket_name    = (known after apply)
  + vpc_id            = (known after apply)
```

### Clean Teardown Guarantee
All provisioned lab resources are tracked within Terraform state and destroyed completely via `terraform destroy -auto-approve` upon evaluation completion, ensuring zero orphan cloud costs.
