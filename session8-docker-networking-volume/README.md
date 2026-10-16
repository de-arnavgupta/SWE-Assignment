# Session 8 — Docker Networking & Volumes

**Student Name:** Arnav Gupta  
**Enrollment ID:** 24bcs10063  
**Batch / Program:** Software Engineering  
**Student Email:** arnav.24bcs10063@sst.scaler.com  
**Repository:** [SWE-Assignment](https://github.com/de-arnavgupta/SWE-Assignment)  

---

## Task 1: Multi-Tier Docker Container Networking

### Architecture Overview

We implement a secure 3-tier enterprise networking topology using Docker bridge networks:

```text
[ frontend ] (session8-frontend)
     │
     └── [ frontend_net ] (172.20.0.0/16)
               │
          [ backend ] (session8-backend) ── Dual-homed on frontend_net & backend_net
               │
     ┌─────────┴─────────┐
     │  [ backend_net ]  │ (172.21.0.0/16)
     │         │         │
     │   [ database ]    │ (session8-database: MySQL 8.0)
     └─────────┬─────────┘
               │
         [ db_net ] (172.22.0.0/16)
```

### Docker Compose Configuration (`docker-compose.yml`)

```yaml
version: '3.8'

services:
  frontend:
    image: nginx:alpine
    container_name: session8-frontend
    ports:
      - "8080:80"
    networks:
      - frontend_net
    restart: unless-stopped

  backend:
    image: alpine:latest
    container_name: session8-backend
    command: ["sh", "-c", "while true; do sleep 3600; done"]
    networks:
      - frontend_net
      - backend_net
    restart: unless-stopped

  database:
    image: mysql:8.0
    container_name: session8-database
    environment:
      MYSQL_ROOT_PASSWORD: secure_devops_password
      MYSQL_DATABASE: session8_db
    volumes:
      - db_data:/var/lib/mysql
    networks:
      - backend_net
      - db_net
    restart: unless-stopped

networks:
  frontend_net:
    driver: bridge
  backend_net:
    driver: bridge
  db_net:
    driver: bridge

volumes:
  db_data:
    driver: local
```

### Connectivity Verification & Isolation Checks

```bash
# 1. Start the stack
docker compose up -d

# 2. Test Backend -> Frontend connectivity (PASSES - shared frontend_net)
docker exec session8-backend ping -c 2 session8-frontend
# Output: 2 packets transmitted, 2 received, 0% packet loss

# 3. Test Backend -> Database connectivity (PASSES - shared backend_net)
docker exec session8-backend nc -zvw3 session8-database 3306
# Output: session8-database (172.21.0.3:3306) open

# 4. Test Frontend -> Database connectivity (FAILS / BLOCKED - Network Isolation Confirmed!)
docker exec session8-frontend ping -c 2 -W 2 session8-database
# Output: ping: bad address 'session8-database'
# Direct Layer 3/4 route is completely prevented by bridge network namespace boundaries.
```

---

## Task 2: Host Networking Mode

### Concept & Mechanics
In default `bridge` mode, Docker provisions a virtual ethernet pair (`veth`) and assigns the container a private IP inside a private network namespace with NAT (`iptables`). In `host` mode (`--net=host`), container network isolation is bypassed; the container shares the host's direct network namespace and network interfaces without port mapping overhead.

### Execution Command
```bash
docker run -d --name apache-host-test --net=host httpd:2.4-alpine
```

### Verification & Platform Observations
- **Linux:** Apache binds directly to physical port `80` on the host's network interfaces (`eth0`, `lo`). A request to `curl http://localhost:80` immediately hits Apache without any `-p` port forwarding flags.
- **macOS / Windows Note:** Docker Desktop runs containers inside a lightweight Linux hypervisor VM. `--net=host` binds to the Linux VM's localhost rather than the macOS native interface. In production Linux environments, host networking is primarily chosen for high-throughput, low-latency workloads (e.g. trading, video streaming, ingress controllers).

---

## Task 3: Bind Mounts with Live Hot-Editing

### Concept
A **bind mount** maps an exact physical path on the host filesystem directly into a directory inside the container namespace. Changes made on the host immediately reflect inside the container in real time without rebuilding the image or restarting the container.

### Step-by-Step Hands-on Workflow

```bash
# 1. Create a local folder and initial HTML file
mkdir -p /tmp/docker-bind-mount
echo "<h1>Hello students</h1><p>Author: Arnav Gupta (24bcs10063)</p>" > /tmp/docker-bind-mount/index.html

# 2. Run Nginx with bind mount
docker run -d --name nginx-bind-demo -p 8085:80 -v /tmp/docker-bind-mount:/usr/share/nginx/html:ro nginx:alpine

# 3. Verify initial content
curl http://localhost:8085/
# Output: <h1>Hello students</h1><p>Author: Arnav Gupta (24bcs10063)</p>

# 4. Modify the index.html on host WITHOUT restarting container
echo "<h1>Hello students - Live Hot Reload Verified!</h1><p>Updated in real-time by Arnav Gupta.</p>" > /tmp/docker-bind-mount/index.html

# 5. Re-query immediately
curl http://localhost:8085/
# Output: <h1>Hello students - Live Hot Reload Verified!</h1><p>Updated in real-time by Arnav Gupta.</p>
```

---

## Task 4: Docker Overlay Networks

### Architectural Deep Dive

An **Overlay Network** creates a distributed Layer 2 software-defined network spanning multiple physical Docker daemon hosts (Docker Swarm or multi-node clusters).

```text
Host 1 (Worker A)                     Host 2 (Worker B)
┌─────────────────────────┐           ┌─────────────────────────┐
│ Container 1 (10.0.0.2)  │           │ Container 2 (10.0.0.3)  │
└────────────┬────────────┘           └────────────┬────────────┘
             │                                     │
   [ VXLAN Tunnel Endpoint ]             [ VXLAN Tunnel Endpoint ]
   (Encapsulates L2 into UDP 4789)       (Decapsulates UDP 4789 into L2)
             │                                     │
             └────────── Underlying Physical ──────┘
                         IP Network (LAN/WAN)
```

### Key Technical Characteristics:
1. **VXLAN Encapsulation:** Overlay networks use Virtual Extensible LAN (VXLAN) protocol (IETF RFC 7348). Original Ethernet frames are encapsulated within standard UDP packets sent to destination port **4789**.
2. **Control Plane & Gossip Protocol:** Swarm manager nodes maintain a synchronized distributed key-value store (using the Serf/Raft gossip protocol on port 7946) to distribute IP assignments, container discovery, and MAC addresses without centralized DNS bottlenecks.
3. **Use Cases:**
   - Multi-host microservice clustering.
   - Encrypted cross-host communication (`--opt encrypted` using IPSec ESP).
   - Zero-downtime service rolling updates across diverse physical nodes.
