# 📖 MULTI-NODE SWARM PROVISIONING & HARDENING RUNBOOK
## ERA: 226.0 | WITNESS: THE ARCHITECT
## STATUS: SYSTEM RUNBOOK & OPERATIONAL DEPLOYMENT CHECKLIST
## TECHNICAL bluePRINT: [513_A_SELF_HOSTED_CONTAINER_ORCHESTRATION_TECHNICAL_SUBSTRATE.md](file:///media/fiji/4A21-00001/New%20folder/AGE%20REPUBLIC/00_KNOWLEDGE/513_A_SELF_HOSTED_CONTAINER_ORCHESTRATION_TECHNICAL_SUBSTRATE.md)
## DEPLOYMENT TOOL: [06_INFRA/deploy_swarm.sh](file:///media/fiji/4A21-00001/New%20folder/AGE%20REPUBLIC/06_INFRA/deploy_swarm.sh)

This operational runbook provides the exact, copy-pasteable terminal command sequences required by domain operators to execute the **7-Step Swarm Provisioning and Hardening Checklist** on actual physical VPS instances (e.g., Hostinger KVM2, Hetzner Cloud, or DigitalOcean Droplets).

---

## 📋 THE 7-STEP DEPLOYMENT RUNBOOK

### 🛠️ Step 1: Install Docker + Swarm Dependencies
Run this sequence on all target VPS nodes (Manager and Workers) to bootstrap the core Docker container runtime:
```bash
# Update local package definitions
apt-get update -y && apt-get upgrade -y

# Install Docker prerequisite system tools
apt-get install -y apt-transport-https ca-certificates curl gnupg lsb-release

# Add Docker's official GPG key register
mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# Register stable apt repository paths
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker engine
apt-get update -y
apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Verify Docker daemon is running
systemctl status docker --no-pager
```

---

### 🔒 Step 2: Harden SSH Daemon Configurations
Secure the system authentication boundary to strictly enforce key-based (`ED25519`) access and fully disable password ingress targets:
```bash
# Edit sshd configuration directive values
sed -i 's/^#\?PasswordAuthentication.*/PasswordAuthentication no/' /etc/ssh/sshd_config
sed -i 's/^#\?PermitRootLogin.*/PermitRootLogin prohibit-password/' /etc/ssh/sshd_config
sed -i 's/^#\?ChallengeResponseAuthentication.*/ChallengeResponseAuthentication no/' /etc/ssh/sshd_config
sed -i 's/^#\?PubkeyAuthentication.*/PubkeyAuthentication yes/' /etc/ssh/sshd_config

# Validate configuration syntax integrity prior to reload
sshd -t

# Restart SSH daemon to apply changes immediately
systemctl restart sshd
```

---

### 🧱 Step 3: Configure UFW Firewall Isolation
Configure the firewall rules to isolate exposed system ports, allowing only web ingress and Swarm inter-node gossip/overlay network channels:
```bash
# Install and reset UFW defaults
apt-get install -y ufw
ufw default deny incoming
ufw default allow outgoing

# Allow standard web access traffic
ufw allow 22/tcp      # Secure key-based SSH ingress
ufw allow 80/tcp      # Web HTTP ingress
ufw allow 443/tcp     # Web SSL/HTTPS ingress

# Allow required Docker Swarm cluster channels
ufw allow 2377/tcp    # Swarm Cluster management port
ufw allow 7946/tcp    # Node discovery gossip protocol
ufw allow 7946/udp    # Node discovery gossip protocol
ufw allow 4789/udp    # Overlay network data path

# Force enable the firewall
ufw --force enable

# Inspect active status configurations
ufw status verbose
```

---

### 👑 Step 4: Initialize Swarm Manager on First Node
On the primary VPS instance selected as the Cluster Manager, initialize the Swarm coordinator overlay:
```bash
# Initialize Swarm manager using node's public IP address
docker swarm init --advertise-addr [MANAGER_PUBLIC_IP]

# Display worker join-token register for Worker Node enrollment
docker swarm join-token worker -q
```
*(Save the output token printed by the command above; it is required for Step 5).*

---

### 👥 Step 5: Join Worker Nodes to Cluster
On each secondary VPS node designated as a Swarm worker instance, execute the join command using the token captured in Step 4:
```bash
# Enroll node into Swarm cluster group
docker swarm join --token [JOIN_TOKEN] [MANAGER_PUBLIC_IP]:2377

# Verify node enrollment state (run this on the Manager node)
docker node ls
```

---

### 🌐 Step 6: Deploy `docker-compose.icm.yml` Stack
On the Manager node, deploy the BFT-hardened Folders-Over-Agents container stack globally across the Swarm:
```bash
# Copy the declarative compose stack to the Manager node and deploy:
docker stack deploy -c 06_INFRA/docker-compose.icm.yml age_republic_stack

# Verify active container task allocations
docker stack ps age_republic_stack
```

---

### 🔏 Step 7: Enable IPsec Encrypted Overlay Networking
Enforce native hardware-accelerated **IPsec ESP encryption** across all inter-node Swarm data tunnels to completely shield container traffic from network sniffing attacks:
```bash
# Create a secure, encrypted overlay network dynamically
docker network create --driver overlay --opt encrypted swarm_network

# Inspect network metrics to confirm encryption parameters
docker network inspect swarm_network
```

---
*Verified by the Architect. The Swarm deployment runbook is active.*
