# AWS EC2 — Elastic Compute Cloud (Compute Infrastructure)

**Author:** Arnav Gupta (Roll: 24bcs10063)  
**Session:** Session 18 — Cloud Fundamentals  

---

## 1. What is Amazon EC2?

Amazon Elastic Compute Cloud (EC2) provides resizable, on-demand virtual compute capacity (Virtual Machines) in the cloud. It eliminates upfront hardware investments, allowing rapid deployment of scalable server instances.

---

## 2. Core Technical Concepts

- **Amazon Machine Image (AMI):** Pre-configured template containing the operating system, kernel, device mappings, and software packages required to launch an instance (e.g. Amazon Linux 2023, Ubuntu 24.04, custom Golden AMIs).
- **Instance Families & Types:**
  - *General Purpose (`t3`, `t4g`, `m6i`):* Balanced CPU, memory, and networking.
  - *Compute Optimized (`c6i`, `c7g`):* High CPU-to-memory ratio for intensive batch processing, scientific modeling, and high-performance web servers.
  - *Memory Optimized (`r6i`, `r7g`):* High memory-to-CPU ratio for in-memory databases (Redis) and real-time big data analytics.
- **Key Pairs:** Asymmetric cryptographic keys (RSA or ED25519) used to securely SSH into Linux instances (`ssh -i key.pem ec2-user@<IP>`). AWS stores only the public key; the private key is held by the user.
- **Security Groups:** Stateful virtual firewalls operating at the hypervisor/NIC layer that regulate inbound and outbound traffic based on protocol, port range, and CIDR/security-group sources.
- **Elastic Block Store (EBS):** High-performance, durable block storage volumes attached over the network to a single EC2 instance (e.g. `gp3`, `io2`). Persists independently of instance lifecycle.
- **Public vs. Private IP:**
  - *Private IP:* Assigned via subnet DHCP; remains static throughout the instance lifecycle; accessible solely within the VPC.
  - *Public IP / Elastic IP (EIP):* Routable over the public Internet. Standard public IPs are released upon instance stop/start; Elastic IPs are static allocated IPv4 addresses.
- **Instance Lifecycle:** `Pending` ──► `Running` ──► `Stopping` ──► `Stopped` ──► `Terminated`.
