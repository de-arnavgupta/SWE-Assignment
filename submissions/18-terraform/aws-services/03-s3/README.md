# AWS S3 — Simple Storage Service (Object Storage)

**Author:** Arnav Gupta (Roll: 24bcs10063)  
**Session:** Session 18 — Cloud Fundamentals  

---

## 1. What is Amazon S3?

Amazon Simple Storage Service (Amazon S3) is an industry-leading object storage service offering 99.999999999% (11 9's) data durability, virtually infinite scalability, and fine-grained data security for unstructured data (images, backups, static websites, logs, data lakes).

---

## 2. Core Concepts & Storage Architecture

- **Buckets:** Top-level containers for storing objects. Bucket names must be globally unique across all AWS accounts worldwide.
- **Objects:** The fundamental entities stored in S3, consisting of data bytes, a unique key (path string), and metadata (headers, content-type, timestamps).
- **Storage Classes & Tiering:**
  - *S3 Standard:* High-throughput, low-latency access for frequently queried data.
  - *S3 Intelligent-Tiering:* Automatically moves objects between frequent, infrequent, and archive access tiers based on access patterns without operational overhead.
  - *S3 Standard-IA (Infrequent Access):* Lower storage fee; nominal per-GB retrieval fee.
  - *S3 Glacier Flexible & Deep Archive:* Lowest-cost archive tiers for compliance data (retrievals in minutes to 12 hours).
- **Versioning:** Preserves multiple historical variants of an object within the same bucket. Protects against unintended user overwrites and malicious ransomware deletions.
- **Lifecycle Policies:** Automated declarative rules that transition aging objects to cheaper storage classes (e.g. Move to Glacier after 90 days; purge after 365 days).
- **Server-Side Encryption (SSE):**
  - *SSE-S3 (AES-256):* Default encryption managed automatically by S3.
  - *SSE-KMS:* Customer-managed keys enabling audit logging in AWS CloudTrail.
- **Bucket Policies & IAM Access Control:** JSON policy documents attached directly to the bucket enforcing TLS/HTTPS (`aws:SecureTransport`), IP restrictions, or cross-account delegation.
