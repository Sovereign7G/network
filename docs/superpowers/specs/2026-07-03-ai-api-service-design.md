# AI API Service Design Document (Verifiable Ledger & Billing Gateway)

This document describes the architecture, schemas, and components of the AI API Service built on top of the Sovereign 7G (S7G) Committee network.

---

## 🏛️ Architecture Overview

The system consists of two primary boundaries:
1. **FastAPI Gateway (Billing Boundary)**: Authenticates clients, manages credits/balances, logs usage, and proxies requests to the S7G committee. Runs a local SQLite database `billing.db`.
2. **S7G Committee (Consensus Boundary)**: PBFT-based consensus group of nodes. Reaches consensus on proposal requests, produces signatures, and writes blocks to the immutable ledger database `ledger.db`.

```
                        +------------------+
                        |      Client      |
                        +--------+---------+
                                 | (1) POST /v1/chat/completions (with API Key)
                                 v
                        +--------+---------+
                        | FastAPI Gateway  |<---+
                        |   (billing.db)   |    | (2) Authenticate key & check balance
                        +--------+---------+----+
                                 |
                                 | (3) POST /propose (payload, request_id)
                                 v
                        +--------+---------+
                        |  S7G Committee   |<---+
                        |   (ledger.db)    |    | (4) Run PBFT (pre-prepare, prepare, commit)
                        +--------+---------+----+
                                 |
                                 | (5) BFT response + signatures
                                 v
                        +--------+---------+
                        | FastAPI Gateway  |<---+
                        |   (billing.db)   |    | (6) Deduct credits & log usage
                        +--------+---------+----+
                                 |
                                 | (7) Response + provenance signatures
                                 v
                        +--------+---------+
                        |      Client      |
                        +------------------+
```

---

## 💾 Database Schema (`billing.db`)

The billing SQLite database will be initialized inside the gateway with the following tables:

```sql
-- Customers profile information
CREATE TABLE IF NOT EXISTS customers (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    created_at INTEGER NOT NULL
);

-- Active API Keys for authentication
CREATE TABLE IF NOT EXISTS api_keys (
    key TEXT PRIMARY KEY,
    customer_id TEXT NOT NULL,
    name TEXT NOT NULL,
    is_active INTEGER DEFAULT 1,
    created_at INTEGER NOT NULL,
    last_used_at INTEGER,
    FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE
);

-- Customer balances (credits in USD/tokens)
CREATE TABLE IF NOT EXISTS balances (
    customer_id TEXT PRIMARY KEY,
    credits REAL DEFAULT 0.0,
    updated_at INTEGER NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE
);

-- Immutable local log of token consumption per request
CREATE TABLE IF NOT EXISTS usage_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id TEXT NOT NULL,
    request_id TEXT UNIQUE NOT NULL,
    tokens_used INTEGER NOT NULL,
    cost REAL NOT NULL,
    timestamp INTEGER NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE
);

-- Customer invoice history
CREATE TABLE IF NOT EXISTS invoices (
    id TEXT PRIMARY KEY,
    customer_id TEXT NOT NULL,
    amount REAL NOT NULL,
    status TEXT CHECK(status IN ('pending', 'paid')) DEFAULT 'pending',
    created_at INTEGER NOT NULL,
    due_date INTEGER NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE
);
```

---

## 🔌 Components & Files

### 1. `gateway/models.py`
Defines Pydantic models for incoming requests, billing admin commands, and responses.
* `CustomerCreate`, `CustomerResponse`
* `CreditGrant`
* `CompletionRequest` (OpenAI compatible)
* `InvoiceResponse`

### 2. `gateway/billing.py`
Encapsulates all interaction with `billing.db` including user creation, key generation, balance checks, usage deduction, and invoice generation.

### 3. `gateway/s7g_client.py`
HTTP client to connect to S7G nodes. Handles routing the request to the committee and verifying the response signature.

### 4. `gateway/proxy.py`
The FastAPI application itself. Exposes endpoints:
* `POST /v1/chat/completions`: User-facing completions endpoint.
* `POST /admin/customers`: Admin endpoint to provision new accounts and grant credits.
* `GET /v1/billing/usage`: Customer usage analytics.
* `GET /v1/billing/invoices`: Customer invoice records.

---

## 🔍 Validation & Verification Plan
1. **Billing Database Setup Verification**: Ensure tables are correctly created.
2. **Key Authentication Tests**: Reject requests with invalid keys, inactive keys, or missing headers.
3. **Double-Spend & Credit Depletion Tests**: Ensure a user cannot make requests once credits are exhausted.
4. **End-to-End Test (E2E)**: Simulate a full loop proposing to a local S7G committee, updating credits, logging block hashes, and returning signed proof.
