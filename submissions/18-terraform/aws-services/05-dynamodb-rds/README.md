# AWS DynamoDB & RDS — Database Services in the Cloud

**Author:** Arnav Gupta (Roll: 24bcs10063)  
**Session:** Session 18 — Cloud Fundamentals  

---

## 1. Amazon DynamoDB (Serverless NoSQL Key-Value & Document DB)

### Overview & Architecture
Amazon DynamoDB is a fully managed, serverless, key-value and document database that delivers single-digit millisecond latency performance at any scale.

### Key Concepts:
- **Tables, Items, Attributes:** A Table is a collection of Items (rows); an Item is a collection of Attributes (columns). Unlike relational tables, items can have arbitrary schemas (schemaless).
- **Primary Keys:**
  - *Partition Key (HASH):* A single attribute hashed by internal partition routers to determine physical SSD storage allocation.
  - *Composite Key (HASH + RANGE / Sort Key):* Combines a partition key with a sort key (e.g. `UserId` [Hash] + `Timestamp` [Range]), enabling rich range queries (`begins_with`, `between`).
- **Secondary Indexes:**
  - *Global Secondary Index (GSI):* Index with a partition key and sort key that can differ from those on the base table.
  - *Local Secondary Index (LSI):* Same partition key as table, but different sort key.
- **Common Use Cases:** User session stores, gaming leaderboards, shopping carts, mobile IoT telemetry, high-velocity clickstream event streams.

---

## 2. Amazon RDS (Relational Database Service)

### Overview & Architecture
Amazon Relational Database Service (Amazon RDS) automates hardware provisioning, database setup, patching, automated daily backups, and point-in-time recovery for relational databases.

### Key Concepts:
- **Supported Engines:** PostgreSQL, MySQL, MariaDB, Oracle, Microsoft SQL Server, and cloud-native Amazon Aurora.
- **High Availability (Multi-AZ):** Synchronous physical replication across two independent Availability Zones. If the primary master instance suffers a hardware outage, RDS automatically triggers an automatic DNS failover to the standby replica within 60–120 seconds with zero data loss.
- **Read Replicas:** Asynchronous read-only replicas configured across same or cross-region AZs to scale read-heavy analytical workloads.
- **Security:** Network isolation inside private DB subnets, encryption at rest via AWS KMS (AES-256), SSL/TLS in-transit encryption, and IAM database authentication.
- **Common Use Cases:** Enterprise transactional workloads (OLTP), ERP systems, CRM applications, and structured e-commerce databases requiring strict ACID compliance.
