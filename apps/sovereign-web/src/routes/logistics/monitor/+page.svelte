<script lang="ts">
    import { onMount } from "svelte";

    // Mock data for initial UI render
    let stats = {
        bountiesCreated: 150,
        bountiesAccepted: 142,
        deliveriesCompleted: 135,
        totalPaid: 405.0,
        avgDeliveryTime: 18,
        activeCouriers: 45,
        activeMerchants: 12,
    };

    let recentDeliveries: any[] = [
        {
            timestamp: Date.now() - 300000,
            origin: "Padaria Ibiri",
            destination: "Rua Augusta",
            reward: "3.00",
            courier: "joao_s",
        },
        {
            timestamp: Date.now() - 600000,
            origin: "Central Cafe",
            destination: "Avenida Paulista",
            reward: "4.50",
            courier: "maria_l",
        },
    ];
    let mapMarkers: any[] = [];

    onMount(() => {
        // Simulated websockets
        const interval = setInterval(() => {
            const d = {
                timestamp: Date.now(),
                origin: "Cafe SP",
                destination: "Pinheiros",
                reward: "3.50",
                courier: "random_" + Math.floor(Math.random() * 100),
            };
            recentDeliveries = [d, ...recentDeliveries].slice(0, 10);
            stats.deliveriesCompleted++;
            stats.totalPaid += 3.5;
        }, 15000);

        return () => clearInterval(interval);
    });
</script>

<div class="monitor">
    <header>
        <h1>🇧🇷 Logistics Monitor - São Paulo</h1>
        <div class="live-indicator">🔴 LIVE</div>
    </header>

    <div class="stats-grid">
        <div class="stat-card">
            <label>Entregas Hoje</label>
            <div class="value">{stats.deliveriesCompleted}</div>
        </div>

        <div class="stat-card">
            <label>Valor Total (USDC)</label>
            <div class="value">${stats.totalPaid.toFixed(2)}</div>
        </div>

        <div class="stat-card">
            <label>Tempo Médio</label>
            <div class="value">{stats.avgDeliveryTime} min</div>
        </div>

        <div class="stat-card">
            <label>Couriers Ativos</label>
            <div class="value">{stats.activeCouriers}</div>
        </div>
    </div>

    <div class="heatmap">
        <div class="map-placeholder">
            <p>📍 P2P Logistic Heatmap Active</p>
            <p class="map-sub">
                Tracking {stats.activeCouriers} couriers dynamically
            </p>
        </div>
    </div>

    <div class="recent">
        <h2>Entregas Recentes (Tempo Real)</h2>

        {#each recentDeliveries as d}
            <div class="delivery-item">
                <span class="time"
                    >{new Date(d.timestamp).toLocaleTimeString()}</span
                >
                <span class="route"
                    ><strong>{d.origin}</strong> ➔ {d.destination}</span
                >
                <span class="reward">${d.reward} USDC</span>
                <span class="courier">@{d.courier}</span>
            </div>
        {/each}
    </div>
</div>

<style>
    .monitor {
        max-width: 1000px;
        margin: 40px auto;
        padding: 20px;
        font-family: "Inter", sans-serif;
    }

    header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 24px;
        padding-bottom: 20px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }
    h1 {
        margin: 0;
        color: #fff;
        font-size: 24px;
    }
    .live-indicator {
        background: rgba(255, 68, 68, 0.2);
        color: #ff4444;
        padding: 6px 16px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 13px;
        text-transform: uppercase;
        animation: pulse 2s infinite;
    }

    @keyframes pulse {
        0% {
            opacity: 1;
        }
        50% {
            opacity: 0.5;
        }
        100% {
            opacity: 1;
        }
    }

    .stats-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 20px;
        margin-bottom: 30px;
    }

    .stat-card {
        background: #111;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        text-align: center;
    }
    .stat-card label {
        display: block;
        color: #888;
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 12px;
    }
    .stat-card .value {
        font-size: 32px;
        font-weight: bold;
        color: #4caf50;
        font-family: "Menlo", monospace;
    }

    .heatmap {
        background: #111;
        border-radius: 12px;
        height: 300px;
        margin-bottom: 30px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        overflow: hidden;
        position: relative;
    }
    .map-placeholder {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        background: #0a0a0a;
        color: #4caf50;
    }
    .map-sub {
        color: #666;
        font-size: 13px;
        margin-top: 8px;
    }

    .recent {
        background: #111;
        border-radius: 12px;
        padding: 24px;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    h2 {
        margin: 0 0 20px 0;
        font-size: 16px;
        color: #eee;
    }

    .delivery-item {
        display: flex;
        align-items: center;
        padding: 12px 0;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        font-size: 14px;
    }
    .delivery-item:last-child {
        border-bottom: none;
    }

    .time {
        color: #666;
        width: 100px;
        font-family: "Menlo", monospace;
    }
    .route {
        flex: 1;
        color: #ccc;
    }
    .reward {
        font-weight: bold;
        color: #4caf50;
        width: 120px;
        text-align: right;
        padding-right: 20px;
    }
    .courier {
        color: #888;
        width: 120px;
        text-align: right;
        font-family: "Menlo", monospace;
        font-size: 13px;
    }
</style>
