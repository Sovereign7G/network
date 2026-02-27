const defaultWorkspaceColumns = [
    {
        id: "col-intelligence",
        blocks: [
            { id: "block-code-intel", type: "code_intel", content: { title: "Code_Intelligence_Manifold" } },
            { id: "block-research", type: "research", content: { title: "Autonomous_Research_Control" } },
            { id: "block-opencode", type: "opencode", content: { title: "Sovereign_OpenCode_Matrix" } },
        ],
    },
    {
        id: "col-governance",
        blocks: [
            { id: "block-manifold", type: "manifold", content: { title: "Protocol_State_Manifold" } },
            { id: "block-court", type: "governance", content: { title: "Kernel_Governance_Court" } },
            { id: "block-policy", type: "policy", content: { title: "Governance_Logic_Forge" } },
            { id: "block-diplomacy", type: "diplomacy", content: { title: "Institutional_Trust_Topology" } },
        ],
    },
    {
        id: "col-operations",
        blocks: [
            { id: "block-superapp", type: "superapp", content: { title: "Sovereign_SuperApp_Terminal" } },
            { id: "block-resonance", type: "gauge", content: { title: "Systemic_Resonance_HUD" } },
            { id: "block-presence", type: "presence", content: { title: "Global_Node_Presence" } },
            { id: "block-comms", type: "comms", content: { title: "Sovereign_Intelligence_Manifold" } },
        ],
    },
    {
        id: "col-resource",
        blocks: [
            { id: "block-tokenomics", type: "tokenomics", content: { title: "Protocol_Asset_Plane" } },
            { id: "block-biomirror", type: "biomirror", content: { title: "Biological_Resonance_HUD" } },
            { id: "block-phygital", type: "phygital", content: { title: "Phygital_Asset_Tracker" } },
        ],
    },
    {
        id: "col-substrate",
        blocks: [
            { id: "block-trace", type: "trace", content: { title: "Substrate_Trace_Loom", canisterId: "ryjl3-tyaaa-aaaaa-aaaba-cai" } },
            { id: "block-audit", type: "audit", content: { title: "AdJoint_Institutional_Auditor" } },
        ],
    }
];
const basicWorkspaceColumns = [
    {
        id: "col-core",
        blocks: [
            { id: "block-superapp", type: "superapp", content: { title: "Sovereign_SuperApp_Terminal" } },
            { id: "block-resonance", type: "gauge", content: { title: "Systemic_Resonance_HUD" } },
        ],
    },
    {
        id: "col-vault",
        blocks: [
            { id: "block-tokenomics", type: "tokenomics", content: { title: "Portfolio_Overview" } },
            { id: "block-hearth", type: "hearth", content: { title: "Recent_Memories" } },
        ],
    },
    {
        id: "col-governance",
        blocks: [
            { id: "block-court", type: "governance", content: { title: "Community_Governance" } },
        ],
    }
];
