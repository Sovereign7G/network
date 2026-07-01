FROM python:3.11-slim

# ===== SYSTEM DEPENDENCIES =====
# libgmp-dev: Required for fastecdsa (libp2p dependency)
# build-essential: For native compilation
# libssl-dev: For cryptography
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libgmp-dev \
    libssl-dev \
    curl \
    jq \
    && rm -rf /var/lib/apt/lists/*

# ===== PYTHON DEPENDENCIES =====
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ===== S7G CODE =====
COPY node/ /app/node/
COPY consensus/ /app/consensus/
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# ===== EXPOSE PORTS =====
EXPOSE 1317 26656 26657

# ===== ENTRYPOINT =====
ENTRYPOINT ["/app/entrypoint.sh"]
