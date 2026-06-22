# 🏛️ AGE REPUBLIC: KNOWLEDGE ASSET (ERA 225.0)
## Identifier: `00_KNOWLEDGE/335_J_REPUBLIC_CVE_LITE_CLI_WISDOM`
## Theme: OWASP CVE Lite CLI — Local-First Dependency Vulnerability Scanning for JS/TS Environments

---

> [!IMPORTANT]
> **SYSTEM COMPACT-SCANNER BLUEPRINT:**
> This knowledge manifest formalizes the operational principles, advisory integrations, and engineering strategies of **OWASP CVE Lite CLI** (maintained by Sonu Kapoor). It establishes standard designs for local lockfile parsing, offline advisory caching, transitive package remediation, and local AI assistant skill compilation.

---

## 🧭 I. The Problem Argument (Status Quo)

**Premise:** Dependency vulnerability scanning in JavaScript and TypeScript projects has long sat at the far end of the development pipeline, resulting in late feedback loops, developer friction, and delayed triage.

**The critique of pipeline-locked security scanners:**
- **Surfaced late:** Vulnerabilities are first surfaced during CI checks, hours or days after the code is written.
- **Cognitive backtrack:** Developers must work backward through large reports on pushed branches to locate direct vs. transitive parents.
- **Cloud dependence:** Traditional scanners require external accounts, continuous network connections, and pushing lockfiles to centralized SaaS platforms.

**Implicit Claim:** Security scanning must be shifted left directly to the developer's local terminal loop. Developers require a fast, offline-first tool to resolve vulnerability dependencies before code ever leaves their machine.

---

## 🏛️ II. The Core Thesis (Solution)

**Proposition:** **OWASP CVE Lite CLI** is a local-first, zero-cloud dependency vulnerability scanner that reads project lockfiles (npm, pnpm, Yarn, Bun), queries a local cached OSV database, and returns copy-and-paste package upgrade commands to close the feedback loop instantly.

**The Local CVE Lite CLI Loop:**
```
Local Lockfile → OSV Local Cache → Query Affected Version → Parse Direct/Transitive Parent → Output Clear Fix Commands
```

**Key Capabilities & Performance Marks:**
1. **Local-First Isolation:** Zero accounts, zero cloud platforms, and zero code leaving the local machine.
2. **Speed & Scale:** Ingests and indexes **217,000 advisory records in under 9 seconds** (9.9x speed increase over initial baseline).
3. **Air-Gap Capability:** Supports full pre-syncing of the Open Source Vulnerabilities database for offline scanning.
4. **AI Assistant Portability:** Auto-generates skill files for local coding assistants (Claude Code, Gemini CLI, Cursor) via the `install-skill` command.

---

## 🔬 III. The Technical Arguments (Architectural Decisions)

### Argument A: Shifting Left via Immediate Actionable Output
Unlike heavy enterprise reports, CVE Lite CLI translates vulnerabilities into direct, terminal-executable remediation commands:

```bash
# Recommended output for npm transitive upgrades
npm update <parent>
```

**Argument:** Surfaces which vulnerabilities are *direct*, which are *transitive*, which can be updated immediately within existing package ranges, and which require structural dependency version overrides.

### Argument B: OSV Data Mapping
The tool maps package lockfiles exclusively against the Google-backed **Open Source Vulnerabilities (OSV)** database schema rather than flat CVE indexes.
* **Why OSV:** Maps advisories cleanly to open-source package ecosystem tags (npm, pnpm, etc.) and affected version ranges, minimizing false positives.
* **Design Acknowledgment:** No single advisory source is treated as perfect. The CLI explicitly labels its findings as OSV-sourced to maintain total auditing transparency.

### Argument C: Flexible Integration and CI Boundaries
The tool avoids intrusive blocking during local development, opting for developer-directed integration paths:
- **Manual/Package CLI Runs:** Executed on-demand.
- **Git Hooks:** Wired directly into `.git/hooks/pre-push` or `pre-commit`.
- **Non-Zero CI Failures:** Triggers exit codes using the `--fail-on` flag based on severity thresholds, outputting standard **SARIF** formats for direct GitHub Code Scanning uploads.

---

## 🧠 IV. Lessons and Wisdom Extracted

### Lesson 1: Local-First is the Ultimate Security Boundary
Scanning without outbound network connections eliminates the risk of exposing lockfiles or package versions to malicious public listening agents.

### Lesson 2: Direct vs. Transitive Separation is Critical for Triage
Developers waste hours trying to update transitive dependencies that are locked inside strict parent parent ranges. A scanner should distinguish direct items from child packages and recommend parent upgrades.

### Lesson 3: High-Speed Offline Syncing Enables Scale
By optimizing SQLite/vector database ingestion down to 9 seconds for 217,000 rows, a tool makes offline, air-gapped security scanning a viable and friction-free daily developer check.

### Lesson 4: Skill Generation Bridges Security and AI Autonomy
Using `install-skill` to compile scan definitions directly for local agents (Claude Code, Cursor) allows autonomous entities to digest scans and automatically write safe package repair commits.
