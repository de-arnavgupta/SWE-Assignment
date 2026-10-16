# Sessions 1 & 2 — Linux Fundamentals

**Student Name:** Arnav Gupta  
**Enrollment ID:** 24bcs10063  
**Batch / Program:** Software Engineering  
**Student Email:** arnav.24bcs10063@sst.scaler.com  
**Repository:** [SWE-Assignment](https://github.com/de-arnavgupta/SWE-Assignment)  

---

## Task 1: Soft Link vs. Hard Link

### Theoretical Comparison

| Dimension | Soft Link (Symbolic Link / Symlink) | Hard Link |
|---|---|---|
| **Underlying Mechanism** | A dedicated pointer file containing the path string to the target file. | A direct pointer (directory entry) to the file's physical **inode** on disk. |
| **Inode Number** | Has its **own distinct inode number**. | Shares the **exact same inode number** as the original file. |
| **Link Count** | Does not increment the inode's link count. | Increments the inode's hard link count by 1. |
| **Cross-Filesystem** | Can span across different mounted filesystems/partitions. | **Cannot** cross filesystems; bounded to a single filesystem. |
| **Linking Directories** | Yes, soft links can link to directories. | Disallowed for ordinary users to prevent circular filesystem loops. |
| **Effect of Deleting Original** | The link becomes **dangling/broken** (`No such file or directory`). | The file data persists untouched on disk until link count drops to 0. |

### Hands-On Commands & Execution Output

```bash
# 1. Create source file
echo "Antigravity Linux Demo by Arnav Gupta (24bcs10063)" > original.txt

# 2. Create symbolic link (-s flag) and hard link
ln -s original.txt softlink.txt
ln original.txt hardlink.txt

# 3. Inspect inodes and link counts with ls -li
ls -li original.txt softlink.txt hardlink.txt
```

**Real Observed Output:**
```text
2912541 -rw-r--r--  2 arnavgupta  staff  51 Oct 16 17:50 hardlink.txt
2912541 -rw-r--r--  2 arnavgupta  staff  51 Oct 16 17:50 original.txt
2912542 lrwxr-xr-x  1 arnavgupta  staff  12 Oct 16 17:50 softlink.txt -> original.txt
```
*Note: `hardlink.txt` and `original.txt` share inode `2912541` with link count 2. `softlink.txt` has its own inode `2912542` and points to `original.txt`.*

```bash
# 4. Delete the original file
rm original.txt

# 5. Check persistence
ls -li softlink.txt hardlink.txt
cat hardlink.txt
cat softlink.txt
```

**Observed Deletion Result:**
```text
2912541 -rw-r--r--  1 arnavgupta  staff  51 Oct 16 17:50 hardlink.txt
2912542 lrwxr-xr-x  1 arnavgupta  staff  12 Oct 16 17:50 softlink.txt -> original.txt

$ cat hardlink.txt
Antigravity Linux Demo by Arnav Gupta (24bcs10063)

$ cat softlink.txt
cat: softlink.txt: No such file or directory
```

---

## Task 2: `adduser` vs. `useradd`

### Comparison

| Feature | `useradd` | `adduser` |
|---|---|---|
| **Binary vs Script** | Native low-level C compiled binary (POSIX standard). | High-level interactive Perl wrapper around `useradd`. |
| **Interactive Prompts** | Non-interactive. Flags must be specified explicitly (`-m`, `-s`). | Interactive: prompts for password, full name, room, phone numbers. |
| **Home Directory** | Does NOT create `/home/<user>` unless `-m` is explicitly supplied. | Automatically creates `/home/<user>` and populates it from `/etc/skel`. |
| **Default Shell** | Defaults to `/bin/sh` or system default if omitted. | Defaults to `/bin/bash` (defined in `/etc/adduser.conf`). |
| **System Preference** | Preferred in unattended automation scripts and Dockerfiles. | **Preferred for Debian/Ubuntu interactive sysadmin user provisioning.** |

### User Lifecycle Practice

```bash
# Recommended command on Ubuntu:
sudo adduser devops_arnav

# Non-interactive script equivalent:
sudo useradd -m -s /bin/bash -c "Arnav Gupta Test User" testuser_arnav
sudo passwd testuser_arnav

# Verify user creation in /etc/passwd and group
id testuser_arnav
grep testuser_arnav /etc/passwd

# Safe disposable cleanup:
sudo userdel -r testuser_arnav
```

---

## Task 3: `journalctl` & Service Logging

`journalctl` query tool interfaces with the `systemd-journald` daemon, providing indexed binary log querying that outperforms flat text log scanning.

### Core Commands & Use Cases

1. **View entire system journal:**
   ```bash
   journalctl
   ```
2. **View logs from current boot only:**
   ```bash
   journalctl -b
   ```
3. **Follow logs in real-time (like tail -f):**
   ```bash
   journalctl -f
   ```
4. **Filter logs by systemd service unit (e.g. Nginx / SSH / Docker):**
   ```bash
   journalctl -u nginx.service -n 50 --no-pager
   ```
5. **Filter by priority / severity (err, warning, info):**
   ```bash
   journalctl -p err -b
   ```
6. **Time-range filtering:**
   ```bash
   journalctl --since "2026-10-16 10:00:00" --until "2026-10-16 12:00:00"
   ```

---

## Task 4: Linux Command Cheat Sheet

| Category | Command | Syntax & Options | Practical Purpose |
|---|---|---|---|
| **Navigation** | `pwd`, `cd`, `ls` | `ls -laSh` | List files with hidden, long format, sorted by size. |
| **File Operations** | `cp`, `mv`, `rm` | `cp -r src/ dst/`, `rm -rf dir/` | Recursive directory copy and clean removal. |
| **Permissions** | `chmod`, `chown` | `chmod 755 script.sh`, `chown user:group file` | Assign read/write/execute modes and user/group ownership. |
| **Text Processing** | `grep`, `awk`, `sed` | `grep -r "pattern" .`, `awk '{print $1}'` | Search pattern recursively; parse columnar fields. |
| **Disk & Storage** | `df`, `du` | `df -h`, `du -sh *` | Filesystem free space (human-readable); directory sizes. |
| **Process Inspection**| `ps`, `top`, `htop` | `ps aux \| grep python` | Snapshot running processes; monitor CPU/RAM live. |
| **Networking** | `curl`, `netstat`/`ss` | `curl -Iv http://localhost:8000`, `ss -tuln` | HTTP request inspection; listening TCP/UDP ports. |
| **Archives** | `tar` | `tar -czvf backup.tar.gz /path` | Create compressed gzip tar archive. |
