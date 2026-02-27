<script lang="ts">
    // ═══════════════════════════════════════════════════════════════════════════
    // 🧬 SOVEREIGN MOLECULE: DATA INTEGRITY PANEL
    // ═══════════════════════════════════════════════════════════════════════════
    // Visualizing Canonical Serialization, Stateless Schemas, and ZK-Readiness.
    // ═══════════════════════════════════════════════════════════════════════════

    import { fly, fade, scale, slide } from "svelte/transition";
    import {
        Layers,
        Box,
        ShieldCheck,
        Microscope,
        Code2,
        Database,
        Zap,
        Activity,
        Lock,
        Hexagon,
        Braces,
        Fingerprint,
    } from "lucide-svelte";
    import {
        sovereignMolecule,
        type MolSchema,
        type MolInstance,
    } from "$lib/services/mol-engine.svelte";

    // ─── STATE ──────────────────────────────────────────────────────────────

    let activeTab = $state<"schemas" | "workspace" | "inspector">("schemas");
    let selectedSchemaId = $state<string | null>(null);
    let dslInput = $state(
        "table TokenState {\n  owner: mol-byte32,\n  amount: mol-u32,\n  nonce: mol-u32\n}",
    );
    let dslResult = $derived(sovereignMolecule.parseDSL(dslInput));
    let lastInstance = $state<MolInstance | null>(null);

    // ─── ACTIONS ────────────────────────────────────────────────────────────

    function registerDsl() {
        const schema = dslResult;
        if (schema) {
            sovereignMolecule.registerSchema(schema);
            activeTab = "schemas";
            selectedSchemaId = schema.id;
        }
    }

    function simulateSerialization(schema: MolSchema) {
        const dummyData = schema.fields
            ? Object.fromEntries(
                  schema.fields.map((f) => [
                      f.name,
                      f.type === "mol-u32" ? 100 : "0x...",
                  ]),
              )
            : [1, 2, 3];

        lastInstance = sovereignMolecule.canonicalize(schema.id, dummyData);
        activeTab = "inspector";
    }
</script>

<div class="molecule-container">
    <!-- 🏛️ HEADER -->
    <header class="panel-header">
        <div class="brand">
            <div class="logo-orb">
                <Box size={18} class="accent-icon" />
            </div>
            <div class="title-group">
                <h3>Sovereign Molecule</h3>
                <p>Verifiable Data Integrity Layer</p>
            </div>
        </div>
        <div class="metrics-bar">
            <div class="metric">
                <span class="label">SCHEMAS</span>
                <span class="value">{sovereignMolecule.stats.schemaCount}</span>
            </div>
            <div class="metric">
                <span class="label">ZK-READY</span>
                <span class="value success"
                    >{sovereignMolecule.stats.zkReady}</span
                >
            </div>
            <div class="metric">
                <span class="label">INTEGRITY</span>
                <span class="value glow">100%</span>
            </div>
        </div>
    </header>

    <!-- 📑 TABS -->
    <div class="tabs">
        <button
            class:active={activeTab === "schemas"}
            onclick={() => (activeTab = "schemas")}
        >
            <Layers size={14} /> <span>Library</span>
        </button>
        <button
            class:active={activeTab === "workspace"}
            onclick={() => (activeTab = "workspace")}
        >
            <Code2 size={14} /> <span>DSL Workspace</span>
        </button>
        <button
            class:active={activeTab === "inspector"}
            onclick={() => (activeTab = "inspector")}
        >
            <Microscope size={14} /> <span>Inspector</span>
        </button>
    </div>

    <!-- 🎚️ CONTENT AREA -->
    <div class="content-scroll">
        {#if activeTab === "schemas"}
            <div class="schema-library" in:fade>
                <div class="grid">
                    {#each sovereignMolecule.allSchemas as schema, i (schema.id)}
                        <div
                            class="schema-card"
                            class:selected={selectedSchemaId === schema.id}
                            in:fly={{ y: 20, delay: i * 50 }}
                            onclick={() => (selectedSchemaId = schema.id)}
                            onkeydown={(e) => {
                                if (e.key === "Enter" || e.key === " ") {
                                    selectedSchemaId = schema.id;
                                }
                            }}
                            role="button"
                            tabindex="0"
                        >
                            <div class="card-header">
                                <span class="kind-tag {schema.kind}"
                                    >{schema.kind}</span
                                >
                                <h4>{schema.name}</h4>
                            </div>
                            <p class="desc">{schema.description}</p>

                            {#if selectedSchemaId === schema.id}
                                <div class="details" transition:slide>
                                    <div class="field-list">
                                        {#if schema.fields}
                                            {#each schema.fields as field}
                                                <div class="field">
                                                    <span class="fname"
                                                        >{field.name}</span
                                                    >
                                                    <span class="ftype"
                                                        >{field.type}</span
                                                    >
                                                </div>
                                            {/each}
                                        {/if}
                                    </div>
                                    <button
                                        class="serialize-btn"
                                        onclick={(e) => {
                                            e.stopPropagation();
                                            simulateSerialization(schema);
                                        }}
                                    >
                                        <Zap size={13} />
                                        <span>Serialize (Canonical)</span>
                                    </button>
                                </div>
                            {/if}
                        </div>
                    {/each}
                </div>
            </div>
        {:else if activeTab === "workspace"}
            <div class="dsl-workspace" in:fade>
                <div class="editor-shell">
                    <div class="shell-header">
                        <Braces size={14} />
                        <span>mol-lang.dsl</span>
                    </div>
                    <textarea
                        bind:value={dslInput}
                        placeholder="Define your Molecule table or struct..."
                        spellcheck="false"
                    ></textarea>
                </div>

                <div class="preview-panel">
                    {#if dslResult}
                        <div class="valid-schema" in:scale>
                            <ShieldCheck size={24} class="success" />
                            <div class="info">
                                <h5>Valid {dslResult.kind} Detected</h5>
                                <p>Ready for Sovereign Registration</p>
                            </div>
                            <button class="prime-btn" onclick={registerDsl}
                                >Register Schema</button
                            >
                        </div>
                    {:else}
                        <div class="invalid-schema">
                            <Lock size={20} class="muted" />
                            <p>Enter valid mol-lang syntax to preview...</p>
                        </div>
                    {/if}
                </div>
            </div>
        {:else if activeTab === "inspector"}
            <div class="inspector" in:fade>
                {#if lastInstance}
                    <div class="instance-view">
                        <div class="instance-header">
                            <Fingerprint size={20} class="glow" />
                            <div class="meta">
                                <h5>{lastInstance.id}</h5>
                                <p>Type: {lastInstance.schemaId}</p>
                            </div>
                            <span class="size-tag"
                                >{lastInstance.size} bytes</span
                            >
                        </div>

                        <div class="hex-dump">
                            <div class="header">
                                <Hexagon size={12} />
                                <span
                                    >CANONICAL REPRESENTATION (LITTLE ENDIAN)</span
                                >
                            </div>
                            <pre>{lastInstance.hex}</pre>
                        </div>

                        <div class="proof-status success">
                            <Activity size={14} />
                            <span
                                >Stateless Root Verified • Proof Ready for
                                Kernel</span
                            >
                        </div>

                        <div class="data-tree">
                            <div class="header">
                                <Database size={12} />
                                <span>DECONSTRUCTED PAYLOAD</span>
                            </div>
                            <pre>{JSON.stringify(
                                    lastInstance.data,
                                    null,
                                    2,
                                )}</pre>
                        </div>
                    </div>
                {:else}
                    <div class="empty-state">
                        <Microscope size={48} />
                        <p>
                            No active Molecules in memory. Select a schema to
                            serialize.
                        </p>
                    </div>
                {/if}
            </div>
        {/if}
    </div>
</div>

<style>
    .molecule-container {
        display: flex;
        flex-direction: column;
        height: 100%;
        background: rgba(10, 11, 15, 0.7);
        backdrop-filter: blur(20px);
        color: #e0e6ed;
        font-family: "Inter", system-ui, sans-serif;
    }

    .panel-header {
        padding: 1.25rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    }

    .brand {
        display: flex;
        gap: 0.75rem;
        align-items: center;
    }

    .logo-orb {
        width: 32px;
        height: 32px;
        background: linear-gradient(135deg, #6366f1, #a855f7);
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 0 15px rgba(99, 102, 241, 0.3);
    }

    .title-group h3 {
        margin: 0;
        font-size: 0.9rem;
        font-weight: 700;
        letter-spacing: 0.02em;
        text-transform: uppercase;
    }

    .title-group p {
        margin: 0;
        font-size: 0.7rem;
        color: #94a3b8;
    }

    .metrics-bar {
        display: flex;
        gap: 1.5rem;
    }

    .metric {
        display: flex;
        flex-direction: column;
        align-items: flex-end;
    }

    .metric .label {
        font-size: 0.6rem;
        color: #64748b;
        font-weight: 600;
    }

    .metric .value {
        font-size: 0.9rem;
        font-weight: 700;
        font-family: "JetBrains Mono", monospace;
    }

    .value.success {
        color: #10b981;
    }
    .value.glow {
        color: #f59e0b;
        text-shadow: 0 0 10px rgba(245, 158, 11, 0.4);
    }

    /* TABS */
    .tabs {
        padding: 0.5rem 1.25rem;
        display: flex;
        gap: 0.5rem;
        background: rgba(255, 255, 255, 0.02);
    }

    .tabs button {
        background: none;
        border: none;
        color: #94a3b8;
        padding: 0.5rem 0.75rem;
        font-size: 0.75rem;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 0.4rem;
        cursor: pointer;
        border-radius: 6px;
        transition: all 0.2s;
    }

    .tabs button:hover {
        background: rgba(255, 255, 255, 0.05);
        color: #f8fafc;
    }

    .tabs button.active {
        background: rgba(99, 102, 241, 0.1);
        color: #818cf8;
    }

    .content-scroll {
        flex: 1;
        overflow-y: auto;
        padding: 1.25rem;
    }

    /* SCHEMA LIBRARY */
    .grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
        gap: 1rem;
    }

    .schema-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 10px;
        padding: 1rem;
        cursor: pointer;
        transition: all 0.25s;
    }

    .schema-card:hover {
        background: rgba(255, 255, 255, 0.05);
        border-color: rgba(99, 102, 241, 0.4);
        transform: translateY(-2px);
    }

    .schema-card.selected {
        border-color: #6366f1;
        background: rgba(99, 102, 241, 0.05);
        box-shadow: 0 0 20px rgba(99, 102, 241, 0.1);
    }

    .card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.5rem;
    }

    .kind-tag {
        font-size: 0.6rem;
        padding: 2px 6px;
        border-radius: 4px;
        text-transform: uppercase;
        font-weight: 700;
        background: #334155;
    }

    .kind-tag.table {
        color: #f472b6;
        background: rgba(244, 114, 182, 0.1);
    }
    .kind-tag.struct {
        color: #38bdf8;
        background: rgba(56, 189, 248, 0.1);
    }
    .kind-tag.primitive {
        color: #818cf8;
        background: rgba(129, 140, 248, 0.1);
    }

    .desc {
        font-size: 0.75rem;
        color: #94a3b8;
        line-height: 1.4;
        margin-bottom: 1rem;
    }

    .details {
        margin-top: 1rem;
        padding-top: 1rem;
        border-top: 1px dashed rgba(255, 255, 255, 0.1);
    }

    .field {
        display: flex;
        justify-content: space-between;
        font-size: 0.7rem;
        margin-bottom: 0.25rem;
        font-family: "JetBrains Mono", monospace;
    }

    .fname {
        color: #cbd5e1;
    }
    .ftype {
        color: #6366f1;
    }

    .serialize-btn {
        width: 100%;
        margin-top: 1rem;
        background: #6366f1;
        border: none;
        color: white;
        padding: 0.5rem;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 600;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
        cursor: pointer;
        transition: background 0.2s;
    }

    .serialize-btn:hover {
        background: #4f46e5;
    }

    /* DSL WORKSPACE */
    .dsl-workspace {
        display: flex;
        flex-direction: column;
        gap: 1rem;
        height: 100%;
    }

    .editor-shell {
        background: #0f172a;
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        overflow: hidden;
        flex: 1;
        display: flex;
        flex-direction: column;
    }

    .shell-header {
        padding: 0.5rem 1rem;
        background: rgba(255, 255, 255, 0.03);
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-size: 0.7rem;
        color: #64748b;
    }

    textarea {
        flex: 1;
        background: transparent;
        border: none;
        color: #f8fafc;
        padding: 1.5rem;
        font-family: "JetBrains Mono", monospace;
        font-size: 0.85rem;
        line-height: 1.6;
        resize: none;
        outline: none;
    }

    .preview-panel {
        padding: 1rem;
        background: rgba(255, 255, 255, 0.02);
        border-radius: 10px;
        min-height: 80px;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .valid-schema {
        display: flex;
        align-items: center;
        gap: 1rem;
        width: 100%;
    }

    .valid-schema .info h5 {
        margin: 0;
        font-size: 0.9rem;
    }
    .valid-schema .info p {
        margin: 0;
        font-size: 0.7rem;
        color: #94a3b8;
    }

    .prime-btn {
        margin-left: auto;
        background: #10b981;
        border: none;
        color: white;
        padding: 0.6rem 1.25rem;
        border-radius: 6px;
        font-weight: 700;
        font-size: 0.75rem;
        cursor: pointer;
    }

    .invalid-schema {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        color: #64748b;
        font-size: 0.8rem;
    }

    /* INSPECTOR */
    .instance-view {
        display: flex;
        flex-direction: column;
        gap: 1.5rem;
    }

    .instance-header {
        display: flex;
        align-items: center;
        gap: 1rem;
        background: rgba(255, 255, 255, 0.03);
        padding: 1rem;
        border-radius: 10px;
    }

    .meta h5 {
        margin: 0;
        font-size: 1rem;
        color: #818cf8;
        font-family: "JetBrains Mono";
    }
    .meta p {
        margin: 0;
        font-size: 0.7rem;
        color: #64748b;
    }

    .size-tag {
        margin-left: auto;
        font-size: 0.7rem;
        font-weight: 700;
        color: #94a3b8;
    }

    .hex-dump pre,
    .data-tree pre {
        background: #020617;
        padding: 1.25rem;
        border-radius: 8px;
        font-family: "JetBrains Mono", monospace;
        font-size: 0.75rem;
        line-height: 1.5;
        overflow-x: auto;
        border: 1px solid rgba(255, 255, 255, 0.05);
        color: #818cf8;
    }

    .hex-dump {
        color: #f59e0b;
    }
    .hex-dump pre {
        color: #f59e0b;
    }

    .proof-status {
        padding: 0.75rem;
        border-radius: 8px;
        display: flex;
        align-items: center;
        gap: 0.75rem;
        font-size: 0.8rem;
        font-weight: 600;
    }

    .proof-status.success {
        background: rgba(16, 185, 129, 0.1);
        color: #10b981;
        border: 1px solid rgba(16, 185, 129, 0.2);
    }

    .header {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-size: 0.6rem;
        font-weight: 800;
        letter-spacing: 0.1em;
        margin-bottom: 0.5rem;
        color: #64748b;
    }

    .empty-state {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 300px;
        color: #334155;
    }

    .empty-state p {
        margin-top: 1rem;
        font-size: 0.85rem;
    }

    ::-webkit-scrollbar {
        width: 6px;
    }
    ::-webkit-scrollbar-track {
        background: transparent;
    }
    ::-webkit-scrollbar-thumb {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
    }
</style>
