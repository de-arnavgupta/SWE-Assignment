# AWS VPC — Virtual Private Cloud (Cloud Networking)

**Author:** Arnav Gupta (Roll: 24bcs10063)  
**Session:** Session 18 — Cloud Fundamentals  

---

## 1. What is an Amazon VPC?

Amazon Virtual Private Cloud (Amazon VPC) allows developers to provision a logically isolated, software-defined private virtual network in the AWS cloud with complete control over IP address ranges, subnets, route tables, and network gateways.

---

## 2. Core Architectural Components

- **CIDR Block:** Classless Inter-Domain Routing prefix defining the private IPv4 block for the VPC (e.g. `10.0.0.0/16` providing 65,536 private IP addresses).
- **Subnets:** Segments of a VPC's IP block mapped to a specific Availability Zone (AZ):
  - *Public Subnet:* Associated with a Route Table containing a default route to an **Internet Gateway** (`0.0.0.0/0 -> igw-xxxx`). Instances can receive public IPv4 addresses.
  - *Private Subnet:* Route table has **no direct route to an Internet Gateway**. Outbound internet traffic (for software patches) must traverse a **NAT Gateway** located in a public subnet.
- **Internet Gateway (IGW):** Horizontally scaled, redundant VPC component that enables communication between public subnet resources and the Internet via bidirectional 1-to-1 NAT.
- **NAT Gateway (Network Address Translation):** Managed service enabling instances in private subnets to initiate outbound connections to the Internet while preventing external inbound traffic from initiating connections to private instances.
- **Security Groups vs. Network ACLs (NACLs):**

| Dimension | Security Groups | Network Access Control Lists (NACLs) |
|---|---|---|
| **Operating Layer** | Instance / Elastic Network Interface (ENI) level. | Subnet boundary level. |
| **Statefulness** | **Stateful:** Inbound return traffic automatically permitted regardless of outbound rules. | **Stateless:** Inbound and outbound traffic evaluated independently; ephemeral ports must be opened explicitly. |
| **Rule Processing** | Evaluates all rules before making a decision. Default is implicit deny. | Evaluates numbered rules in strict ascending order (e.g. rule 100 before 200). First match wins. |
| **Deny Rules** | Allows only **ALLOW** rules; cannot create explicit deny rules. | Supports both explicit **ALLOW** and **DENY** rules. |
