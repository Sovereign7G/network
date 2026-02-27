<script lang="ts">
    import ProtocolHealth from "$lib/components/governance/ProtocolHealth.svelte";
    import ProposalAnalytics from "$lib/components/governance/ProposalAnalytics.svelte";
    import CitizenInsights from "$lib/components/governance/CitizenInsights.svelte";
    import TreasuryDashboard from "$lib/components/governance/TreasuryDashboard.svelte";
    import GovernanceSimulator from "$lib/components/governance/GovernanceSimulator.svelte";
</script>

<svelte:head>
    <title>Sovereign Cathedral - Governance Analytics Dashboard</title>
</svelte:head>

<div class="analytics-layout">
    <header class="page-header">
        <h1>Governance Analytics</h1>
        <p>Phase 5 Differential Privacy Insights and System Health</p>
    </header>

    <div class="analytics-grid">
        <div class="main-column">
            <ProtocolHealth />
            <GovernanceSimulator />
        </div>
        <div class="side-column">
            <TreasuryDashboard />
            <ProposalAnalytics />
            <CitizenInsights />
        </div>
    </div>
</div>

<style>
    .analytics-layout {
        padding: 2rem;
        height: 100vh;
        display: flex;
        flex-direction: column;
        overflow-y: auto;
    }
    .page-header {
        margin-bottom: 2rem;
    }
    .page-header h1 {
        font-size: 24px;
        font-weight: 900;
        text-transform: uppercase;
        color: white;
        letter-spacing: 0.1em;
    }
    .page-header p {
        font-size: 12px;
        color: rgba(255, 255, 255, 0.4);
        font-family: "JetBrains Mono", monospace;
    }
    .analytics-grid {
        display: grid;
        grid-template-columns: 2fr 1fr;
        gap: 2rem;
        flex: 1;
    }
    .main-column {
        display: flex;
        flex-direction: column;
        gap: 2rem;
    }
    .side-column {
        display: flex;
        flex-direction: column;
        gap: 2rem;
    }

    @media (max-width: 1024px) {
        .analytics-grid {
            grid-template-columns: 1fr;
        }
    }
</style>
