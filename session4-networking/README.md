# Session 4 — Networking Fundamentals & Diagnostics

**Student Name:** Arnav Gupta  
**Enrollment ID:** 24bcs10063  
**Batch / Program:** Software Engineering  
**Student Email:** arnav.24bcs10063@sst.scaler.com  
**Repository:** [SWE-Assignment](https://github.com/de-arnavgupta/SWE-Assignment)  

---

## 1. Network Interfaces & IP Addressing

### Commands: `ip addr` (Linux) / `ifconfig` (macOS / BSD)

```bash
# Linux
ip -brief addr show
# macOS / Unix
ifconfig lo0
```

**Real Execution Output:**
```text
lo0: flags=8049<UP,LOOPBACK,RUNNING,MULTICAST> mtu 16384
	options=1203<RXCSUM,TXCSUM,TXSTATUS,SW_TIMESTAMP>
	inet 127.0.0.1 netmask 0xff000000 
	inet6 ::1 prefixlen 128 
	inet6 fe80::1%lo0 prefixlen 64 scopeid 0x1 
	nd6 options=201<PERFORMNUD,DAD>
```

**Technical Explanation:**
- **Interface Naming:** `lo0` represents the local loopback interface. On Linux physical hosts, Ethernet is named `eth0` or predictable names like `enp3s0`; on macOS it is typically `en0` (Wi-Fi/Ethernet).
- **IP & Netmask:** `inet 127.0.0.1 netmask 0xff000000` (`127.0.0.1/8`) reserves the entire class A loopback block. Network packets sent to this IP bypass the physical Network Interface Card (NIC) hardware and are immediately re-routed by the kernel IP stack back to the local host.
- **IPv6:** `::1/128` represents the IPv6 loopback address; `fe80::1%lo0` represents the link-local unicast address.

---

## 2. Routing Tables & Gateway Resolution

### Commands: `ip route show` (Linux) / `netstat -rn` (macOS / Unix)

```bash
netstat -rn
```

**Real Execution Output:**
```text
Routing tables

Internet:
Destination        Gateway            Flags               Netif Expire
default            10.20.48.1         UGScg                 en0       
10.20.48/20        link#12            UCS                   en0      !
10.20.48.1/32      link#12            UCS                   en0      !
10.20.48.1         0:0:5e:0:1:e       UHLWIir               en0   1170
```

**Technical Explanation:**
- **Default Route (`0.0.0.0/0` or `default`):** Matches any outbound traffic not explicitly defined in more specific subnet routing entries.
- **Gateway (`10.20.48.1`):** The next-hop Layer 3 router responsible for forwarding packets outside the local subnet (`10.20.48.0/20`).
- **Flags:**
  - `U`: Route is Up and operational.
  - `G`: Gateway route (requires Layer 2 ARP resolution of the gateway's MAC address `00:00:5e:00:01:0e`).
  - `S`: Static or dynamically configured route.
  - `c`: Cloned route.

---

## 3. Domain Name System (DNS) Resolution

### Commands: `dig`, `nslookup`, `host`

```bash
# Query A-records using dig
dig +noall +answer google.com @8.8.8.8

# Inspect complete DNS resolution with nslookup
nslookup google.com
```

**Typical Verified Output:**
```text
Server:		8.8.8.8
Address:	8.8.8.8#53

Non-authoritative answer:
Name:	google.com
Address: 142.250.190.46
Name:	google.com
Address: 2a00:1450:4009:822::200e
```

**Technical Explanation:**
- **Port 53:** DNS standard queries use UDP port 53 for fast query-response resolution, falling back to TCP port 53 when response payload exceeds 512 bytes (EDNS0 allows up to 4096 bytes over UDP).
- **Resolver Order:** Resolution follows `/etc/resolv.conf` (or `systemd-resolved` / macOS mDNSResponder) before sending outbound recursive queries to upstream nameservers.
- **A vs AAAA Records:** A records map domain names to IPv4 addresses; AAAA records map domains to 128-bit IPv6 addresses.

---

## 4. Socket Inspection & Listening Ports

### Commands: `ss -tuln` (Linux) / `netstat -an | grep LISTEN` (macOS / Unix)

```bash
# Linux modern socket statistics
ss -tuln

# Universal Unix socket state
netstat -an | grep LISTEN | head -n 5
```

**Technical Explanation:**
- **Flags:**
  - `-t`: Filter TCP sockets.
  - `-u`: Filter UDP sockets.
  - `-l`: Show only sockets currently in `LISTEN` state.
  - `-n`: Display raw numerical port and IP addresses instead of resolving protocol names.
- **Port Binding Semantics:**
  - `0.0.0.0:8000`: Application listens on all available IPv4 interfaces (accessible remotely via LAN/WAN IP).
  - `127.0.0.1:8000`: Application binds strictly to the loopback interface (accessible only from the local machine, preventing external exposure).
  - `:::8000`: Sockets bound to dual-stack IPv6 wildcards.

---

## 5. Connectivity Testing & The "Blocked Ping" Fallacy

### Diagnostic Command Suite

```bash
# 1. ICMP probe (ping)
ping -c 3 8.8.8.8

# 2. Path analysis (traceroute)
traceroute -q 1 -w 1 8.8.8.8

# 3. Layer 7 application check (curl)
curl -Iv https://www.google.com
```

### Critical DevOps Diagnostic Principle: Blocked Ping != Network Outage

> [!IMPORTANT]
> **Why ICMP Ping Blocking Must Never Be Equated to a Network Failure:**
> 1. **ICMP Protocol Filtering:** `ping` uses the Internet Control Message Protocol (ICMP type 8 Echo Request / type 0 Echo Reply). Many corporate firewalls, AWS Security Groups, and modern cloud providers intentionally drop inbound ICMP packets to prevent reconnaissance and DDoS amplification.
> 2. **Independent Layer Operation:** Dropped ICMP packets only demonstrate that the target host or intermediate edge security gateway drops Layer 3/4 control traffic.
> 3. **Application Verification:** If `curl -I https://example.com` or `nc -zv example.com 443` successfully completes a TCP three-way handshake and TLS negotiation on port 443, full internet connectivity and application service availability are 100% operational, despite `ping example.com` failing with 100% packet loss.
