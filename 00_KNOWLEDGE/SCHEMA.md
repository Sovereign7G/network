# Open Knowledge Format (OKF) Bundle Schema

## 🏛️ Domain
Shared persistent institutional memory for the Sovereign OS ecosystem, bridging Odysseus and Hermes.

## 📝 Conventions
- **Filename convention**: lowercase with hyphens, alphanumeric only, no spaces. e.g., `res-gpu-market-trends.md`.
- **Frontmatter requirement**: Every OKF concept/markdown file **MUST** start with a valid YAML frontmatter block containing `type`, `title`, `created`, and `updated`.
- **Wikilinks**: Use `[[wikilinks]]` for referencing other concept files. Every concept file must target at least 2 other files to avoid orphans.
- **Auto-Commit**: All manual and agent edits are tracked via automated git commit triggers.

---

## 🗂️ Frontmatter Schemas

### 1. `TelemetryReport`
- **Path**: `telemetry/`
- **Fields**:
  - `status`: SUCCESS | FAILURE | WARNING
  - `node_id`: ID of the reporting server/node
  - `metrics`: key-value metrics map
  - `errors`: array of error log messages

### 2. `ResearchFinding`
- **Path**: `research/`
- **Fields**:
  - `tags`: array of tags from taxonomy
  - `sources`: array of raw paths cited
  - `confidence`: high | medium | low
  - `contested`: boolean flag indicating unresolved contradictions
  - `contradictions`: list of conflicting pages

### 3. `ModelComparison`
- **Path**: `comparisons/`
- **Fields**:
  - `test_id`: comparison run ID
  - `baseline_model`: model ID acting as baseline
  - `candidate_model`: model ID being evaluated
  - `metrics`: map of latency, cost, and throughput metrics
  - `preferred_model`: the recommended model ID

### 4. `EmailDraft`
- **Path**: `inbox/`
- **Fields**:
  - `status`: DRAFT | APPROVED | SENT | ARCHIVED
  - `priority`: high | medium | low
  - `recipient`: email address
  - `subject`: subject line
  - `assigned_agent`: daemon profile ID
  - `approved_by`: human controller ID or empty

### 5. `SystemConfig`
- **Path**: `system/`
- **Fields**:
  - `hardware_family`: e.g. NVIDIA DGX Spark, RTX 4090
  - `memory_size_gb`: integer capacity
  - `quantization_target`: target weight bit-width (e.g. fp4, int8)
  - `recommended_routing`: primary/fallback routing map

### 6. `ChatSession`
- **Path**: `sessions/`
- **Fields**:
  - `session_id`: UUID of the session
  - `summary`: text block summarizing conversation
  - `checkpoints`: list of checkpoint commit hashes

---

## 🏷️ Tag Taxonomy
- **Hardware/Models**: `model`, `architecture`, `benchmark`, `hardware`, `gpu`, `tpu`
- **Logistics/Processors**: `email`, `calendar`, `contacts`, `triage`, `remittance`, `ledger`
- **Geopolitical Nodes**: `asean`, `central-asia`, `east-asia`, `sovereignty`
- **Operations**: `telemetry`, `cron`, `simulation`, `attestation`
