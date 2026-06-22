# 🏛️ AGE REPUBLIC: KNOWLEDGE ASSET (ERA 225.0)
## Identifier: `00_KNOWLEDGE/338_REPUBLIC_ANTIGRAVITY_ECOSYSTEM_WISDOM`
## Theme: Google Antigravity (Agy) Global Configurations, Path Rectifications & MCP Standards

---

> [!IMPORTANT]
> **SYSTEM COMPLIANCE & PATH WAYPOINT BLUEPRINT:**
> This knowledge manifest formalizes the global path corrections, syntactical constraints, and directory structures of the **Google Antigravity ("Agy")** ecosystem. It rectifies official documentation bugs regarding skill pathways, defines the precise JSON structures of `mcp_config.json`, and outlines automated relocation patterns for local agent tools.

---

## 🧭 I. The Problem Argument (Status Quo)

**Premise:** Previously, Google's Gemini CLI and other developer tools were developed independently and in parallel, leading to fragmented configuration standards and user friction.

**Evidence cited:**
> *"Previously these products were developed independently and in parallel. As a result they had different standards and approaches for configuration (such as MCP servers), and where to put things… like skills. This creates a certain amount of friction for users."*

**Specific pain points:**
- Duplicate configurations across tools.
- Skills working in one environment (CLI) but not another (IDE).
- Inconsistent MCP server configuration formats.
- Different locations for the same assets.

**Implicit Claim:** Fragmented tooling creates cognitive overhead and adoption barriers. Users should not have to configure MCP servers and skills multiple times for different tools in the same ecosystem.

---

## 🏛️ II. The Core Thesis (Solution)

**Proposition:** Google's Antigravity ("Agy") suite unifies configuration across CLI, IDE, and desktop agent manager through a **shared agent harness** and **centralized configuration hierarchy**.

**The Antigravity Suite components:**
| Component | Purpose |
| :--- | :--- |
| **Antigravity 2.0** | Desktop agent-first "builder" environment — no IDE, only agent manager |
| **Antigravity IDE** | VS Code-esque coding environment with agent harness |
| **Antigravity SDK** | Python SDK (`google.antigravity`) for programmatic access |
| **Antigravity CLI** | Go-based terminal CLI (replaces Gemini CLI) — faster, shared harness |

**The unification claim:** *"Now, in theory, we only need to configure in one place."*

---

## 🔬 III. The Configuration Architecture Arguments

### Argument A: Centralized `.gemini` Directory Structure
```
.gemini/
├── antigravity/           # (docs say skills go here — incorrect per testing)
├── antigravity-cli/
│   ├── brain/             # Conversations and artifacts
│   ├── mcp/               # Dynamically generated from shared MCP config
│   └── settings.json
├── antigravity-ide/
│   ├── brain/
│   ├── mcp/
│   └── plugins/           # Symlinked from global config
├── config/
│   ├── plugins/           # Global/shared plugins
│   ├── projects/          # Approved project folders
│   └── mcp_config.json    # Global/shared MCP config ← KEY
├── skills/                # Global/shared skills ← ACTUAL location
└── GEMINI.md
```

**Key discovery (documentation vs. reality):**
> *"At the time of writing, the official Antigravity documentation says that to configure skills 'globally', you need to put them here: `~/.gemini/antigravity/skills/<skill-folder>/`. But my experience is that this is incorrect."*

**Verified correct location:** `~/.gemini/skills/` — discovered via `/skills` command output showing "shared skills" location.

**Argument:** Documentation lags implementation. Empirical verification (running `/skills` in the CLI) is necessary to discover actual behavior. The shared skills location is the top-level skills folder, not the product-specific subfolder.

### Argument B: Two-Tier Skill Hierarchy

| Tier | Location | Scope |
| :--- | :--- | :--- |
| **Global skills** | `~/.gemini/antigravity-cli/skills` | CLI only |
| **Shared skills** | `~/.gemini/skills` | All Antigravity tools (CLI, IDE, desktop) |

**Argument:** Users need both product-specific skills (only relevant to CLI) and shared skills (useful across all surfaces). The two-tier hierarchy accommodates both without duplication.

### Argument C: Shared MCP Configuration
**Location:** `~/.gemini/config/mcp_config.json`

**Format changes from old Gemini CLI:**
| Old Format | New Format (Antigravity) |
| :--- | :--- |
| `httpUrl` | `serverUrl` |
| Top-level `timeout` parameter | Not supported (removed) |
| Inline comments allowed | Inline comments not supported |

**Local command servers:**
```json
"avtool": {
  "command": "mcp-avtool-go",
  "env": { "PROJECT_ID": "my-project" }
}
```

**Remote HTTP servers (new pattern):**
```json
"FirestoreMCP": {
  "serverUrl": "https://firestore.googleapis.com/mcp",
  "authProviderType": "google_credentials",
  "oauth": { "scopes": ["..."] }
}
```

**Argument:** The new format supports both local (command-based) and remote (HTTP-based) MCP servers, with native Google Cloud authentication patterns (`google_credentials`, OAuth scopes).

### Argument D: MCP Configuration is Shared Across All Tools
The shared `mcp_config.json` in `~/.gemini/config/` is correctly picked up by both CLI and IDE, eliminating duplicate configuration.

---

## 🚫 IV. The Anti-Arguments (What Antigravity Rejects)

| Rejected Practice | Antigravity Alternative |
| :--- | :--- |
| **Tool-specific configuration** | Shared `config/mcp_config.json` across all tools |
| **Skills in product-specific folders only** | Two-tier (global + shared) with `~/.gemini/skills/` for sharing |
| **Python-based CLI (slow startup)** | Go-based CLI (faster) |
| **Separate development of CLI and IDE** | Shared agent harness, common configuration |
| **Manual configuration of MCP servers per tool** | One configuration, automatically picked up |
| **Proprietary skill installation only** | Supports `npx skills add` (but requires relocation) |

---

## 🏛️ V. The Philosophical Core (Six Sentences)

1. **Configuration should be shared, not duplicated** — one `mcp_config.json` for CLI, IDE, and desktop.
2. **Documentation is not truth** — empirical verification (running `/skills`) reveals actual behavior.
3. **Skills should be portable across tools** — a skill installed once should work in CLI and IDE.
4. **Faster tooling matters** — Go-based CLI feels tangibly faster than Python-based predecessor.
5. **Abstraction skills fix ecosystem fragmentation** — if tools install to the wrong place, write a skill that fixes it.
6. **Day-one paper cuts are acceptable if the foundation is solid** — environment variable bugs will be fixed; the shared harness is here to stay.

---

## 🧠 VI. Lessons and Wisdom Extracted

### Lesson 1: Unification is a Feature, Not an Afterthought
Fragmented tooling creates real user friction. Unifying configuration across surfaces is not a nice-to-have — it is essential for a coherent developer experience.

### Lesson 2: Documentation vs. Reality — Always Verify
Documentation is often wrong, especially for new products. Run commands (`/skills`) to discover actual behavior. Trust empirical output over written docs.

### Lesson 3: The CLI's Own Output is the Best Documentation
The tool itself knows where its configuration lives. When in doubt, ask the tool. The `/skills` command output is authoritative.

### Lesson 4: Two-Tier is Better Than One
Some skills are only useful in the CLI (e.g., terminal-specific automation). Others are useful across all surfaces. A two-tier hierarchy accommodates both without forcing everything into one bucket.

### Lesson 5: Migration Requires Automation
When the ecosystem changes (new folder locations, new tools), do not expect users to manually migrate. Build automation — and if you build it as a skill, teach the agent to use it.

### Lesson 6: API Keys in Configs are a Security Risk
Hardcoding secrets into config files is bad practice. Environment variable support is not a nice-to-have — it is a security requirement. This bug needs fixing.

### Lesson 7: JSON Without Comments is Unfriendly
JSON's lack of comments has always been a problem. For configuration files, allow comments (JSON5, YAML, or explicit comment field support). Users need to document their configs.
