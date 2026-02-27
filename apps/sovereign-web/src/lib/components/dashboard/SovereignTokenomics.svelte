<script lang="ts">
    import { onMount } from "svelte";
    import { fade, fly } from "svelte/transition";
    import { cubicOut } from "svelte/easing";
    import {
        Coins,
        TrendingUp,
        Activity,
        Flame,
        Lock,
        ArrowUpRight,
        BarChart3,
        Zap,
        ShieldCheck,
    } from "lucide-svelte";
    import { manifold } from "$lib/stores/master-store.svelte";

    const tokenomics = $derived(manifold.tokenomicsState);
    const veAge = $derived(manifold.veAgeState);
    const stablecoin = $derived(manifold.stablecoinState);
    const treasury = $derived(manifold.vaultState);

    type TabType = "SUPPLY" | "YIELD" | "VE_AGE";
    const tabs: TabType[] = ["SUPPLY", "YIELD", "VE_AGE"];
    let activeTab = $state<TabType>("SUPPLY");
    let burnRate = $state(124.5);
    let netEmission = $state(-42.1); // Deflationary flex

    onMount(() => {
        const interval = setInterval(() => {
            burnRate = 120 + Math.random() * 10;
            netEmission = -40 - Math.random() * 5;
        }, 3000);
        return () => clearInterval(interval);
    });
</script>

<div class="tokenomics-shell">
    <!-- Top HUD: Ecosystem Parity -->
    <header class="tokenomics-header">
        <div class="header-brand">
            <div class="logo-box">
                <Coins size={20} class="text-white" />
            </div>
            <div class="flex flex-col">
                <h2 class="title">Sovereign_Tokenomics</h2>
                <div class="flex items-center gap-2">
                    <span class="phase-label">DEFLATIONARY_PHASE</span>
                    <div class="phase-pulsar"></div>
                </div>
            </div>
        </div>

        <div class="header-telemetry">
            <div class="tel-block">
                <span class="tel-label">GLOBAL_REPUTATION_(RI)</span>
                <div class="flex items-center gap-1">
                    <TrendingUp size={10} class="text-emerald-400" />
                    <span class="tel-value text-emerald-400"
                        >{tokenomics.reputationIndex}</span
                    >
                </div>
            </div>
            <div class="tel-divider"></div>
            <div class="tel-block">
                <span class="tel-label">STABLE_PARITY</span>
                <span class="tel-value text-cyan-400"
                    >${stablecoin.parity.toFixed(4)}</span
                >
            </div>
        </div>
    </header>

    <!-- Navigation Tabs -->
    <nav class="tokenomics-nav">
        {#each tabs as tab}
            <button
                onclick={() => (activeTab = tab)}
                class="nav-btn"
                class:active={activeTab === tab}
            >
                <span>{tab}</span>
                {#if activeTab === tab}
                    <div class="nav-active-bar" in:fade></div>
                {/if}
            </button>
        {/each}
    </nav>

    <!-- Content Area -->
    <main class="tokenomics-body scrollbar-hide">
        {#if activeTab === "SUPPLY"}
            <div
                class="content-view"
                in:fly={{ y: 20, duration: 400, easing: cubicOut }}
            >
                <!-- Supply Visualization -->
                <div class="metrics-grid">
                    <section class="stat-vessel">
                        <header class="vessel-header">
                            <span class="vessel-label">CIRCULATING_SUPPLY</span>
                            <ArrowUpRight size={12} class="text-white/20" />
                        </header>
                        <div class="vessel-content">
                            <span class="v-value"
                                >{(tokenomics.ageCirculating / 1000000).toFixed(
                                    1,
                                )}M <small>AGE</small></span
                            >
                            <div class="progress-vessel">
                                <div
                                    class="progress-fill"
                                    style="width: {(tokenomics.ageCirculating /
                                        tokenomics.ageTotalSupply) *
                                        100}%"
                                ></div>
                            </div>
                            <span class="v-meta"
                                >{(
                                    (tokenomics.ageCirculating /
                                        tokenomics.ageTotalSupply) *
                                    100
                                ).toFixed(1)}% of Total</span
                            >
                        </div>
                    </section>

                    <section class="stat-vessel burn-tint">
                        <header class="vessel-header">
                            <span class="vessel-label">REAL-TIME_BURN</span>
                            <Flame size={12} class="text-rose-400" />
                        </header>
                        <div class="vessel-content">
                            <span class="v-value text-rose-400"
                                >-{burnRate.toFixed(1)}
                                <small>AGE/hr</small></span
                            >
                            <div class="emission-tag">
                                Net Emission: {netEmission.toFixed(1)}%
                            </div>
                        </div>
                    </section>
                </div>

                <!-- Market Cap Explorer -->
                <section class="valuation-vessel">
                    <header class="vessel-header">
                        <h3>Valuation_Topology</h3>
                        <BarChart3 size={12} class="text-white/20" />
                    </header>
                    <div class="topology-grid">
                        <div class="top-item">
                            <span class="top-label">MARKET_CAP</span>
                            <span class="top-value"
                                >${(tokenomics.marketCapUsd / 1000000).toFixed(
                                    0,
                                )}M</span
                            >
                        </div>
                        <div class="top-item">
                            <span class="top-label">FDV</span>
                            <span class="top-value text-white/40 italic"
                                >${(
                                    (tokenomics.ageTotalSupply *
                                        (tokenomics.marketCapUsd /
                                            tokenomics.ageCirculating)) /
                                    1000000
                                ).toFixed(0)}M</span
                            >
                        </div>
                        <div class="top-item">
                            <span class="top-label">ARI_INCENTIVE</span>
                            <span class="top-value text-emerald-400"
                                >{tokenomics.ariMultiplier.toFixed(2)}x</span
                            >
                        </div>
                    </div>
                </section>
            </div>
        {:else if activeTab === "YIELD"}
            <div
                class="content-view"
                in:fly={{ y: 20, duration: 400, easing: cubicOut }}
            >
                <header class="view-header">
                    <h3>Yield_Generation_Vectors</h3>
                </header>

                <div class="gauge-list">
                    {#each veAge.gauges as gauge}
                        <div class="gauge-item">
                            <div class="g-info">
                                <div class="g-icon">
                                    <Zap size={14} />
                                </div>
                                <div class="flex flex-col">
                                    <span class="g-name">{gauge.name}</span>
                                    <span class="g-label"
                                        >Active Incentives</span
                                    >
                                </div>
                            </div>
                            <div class="g-weight">
                                <span class="w-value"
                                    >{(gauge.weight * 100).toFixed(0)}%</span
                                >
                                <span class="w-label">WEIGHT</span>
                            </div>
                        </div>
                    {/each}
                </div>

                <!-- UCT Distribution -->
                <section class="dividend-vessel">
                    <div class="div-glow"></div>
                    <div class="div-content">
                        <header
                            class="flex items-center gap-2 text-emerald-400"
                        >
                            <Activity size={14} />
                            <span class="v-label">UCT_Universal_Dividend</span>
                        </header>
                        <div class="div-value">
                            {tokenomics.uctDailyDividend}
                            <small>CR / Cycle</small>
                        </div>
                        <p class="div-desc">
                            Distributed automatically to all verified identity
                            shards at the start of every cognitive epoch.
                        </p>
                    </div>
                </section>
            </div>
        {:else if activeTab === "VE_AGE"}
            <div
                class="content-view"
                in:fly={{ y: 20, duration: 400, easing: cubicOut }}
            >
                <!-- veAGE Locking Status -->
                <section class="lock-vessel">
                    <div class="lock-aura">
                        <Lock size={48} strokeWidth={1} />
                    </div>
                    <h3 class="lock-title">Vote-Escrowed_AGE</h3>
                    <p class="lock-subtitle">Governance Weight Multiplier</p>

                    <div class="lock-stats">
                        <div class="l-stat">
                            <span class="l-label">TOTAL_LOCKED</span>
                            <span class="l-value"
                                >{(veAge.totalLockedAge / 1000000).toFixed(
                                    1,
                                )}M</span
                            >
                        </div>
                        <div class="l-stat">
                            <span class="l-label">AVG_LOCK_TERM</span>
                            <span class="l-value"
                                >{veAge.averageLockTimeYears} yrs</span
                            >
                        </div>
                    </div>

                    <button class="lock-action-btn">
                        <span>Lock_AGE_for_Power</span>
                        <ArrowUpRight size={14} />
                    </button>
                </section>
            </div>
        {/if}
    </main>

    <!-- Security & Audit Footer -->
    <footer class="tokenomics-footer">
        <div class="footer-assurance">
            <ShieldCheck size={14} class="text-emerald-400" />
            <span class="audit-label">TREASURY_AUDIT: VERIFIED</span>
        </div>
        <div class="footer-meta">
            <span>Basel-IV_Compliant</span>
            <div class="meta-divider"></div>
            <span class="tvl"
                >TVL: ${(treasury.totalValueLockedUsd / 1000000).toFixed(
                    1,
                )}M</span
            >
        </div>
    </footer>
</div>

<style>
</style>
