<script lang="ts">
    import { onMount } from "svelte";

    import { Globe, Compass, Layers } from "lucide-svelte";

    let canvas: HTMLCanvasElement;
    let ctx: CanvasRenderingContext2D;
    let width = 0;
    let height = 0;
    let animationFrame: number;

    interface Shard {
        id: string;
        x: number;
        y: number;
        color: string;
        pulse?: number;
    }

    interface Ribbon {
        from: string;
        to: string;
        trust: number;
    }

    interface SentimentParticle {
        x: number;
        y: number;
        vx: number;
        vy: number;
        sentiment: number; // 0 to 1
    }

    import { naiEngine } from "$lib/nai/engine.svelte";
    import type { AmbientComponent } from "$lib/nai/types";

    interface Props {
        shards?: Shard[];
        ribbons?: Ribbon[];
        title?: string;
        subtitle?: string;
    }

    let {
        shards = [
            { id: "CORE", x: 0.5, y: 0.5, color: "#FDB813" },
            { id: "IC-ALPHA", x: 0.25, y: 0.35, color: "#00F3FF" },
            { id: "IC-BETA", x: 0.75, y: 0.45, color: "#0A84FF" },
            { id: "SHARD-088", x: 0.35, y: 0.75, color: "#ffaa00" },
            { id: "SHARD-042", x: 0.65, y: 0.25, color: "#a855f7" },
        ],
        ribbons = [
            { from: "CORE", to: "IC-ALPHA", trust: 0.95 },
            { from: "CORE", to: "IC-BETA", trust: 0.92 },
            { from: "IC-ALPHA", to: "SHARD-088", trust: 0.88 },
            { from: "IC-BETA", to: "SHARD-042", trust: 0.75 },
            { from: "SHARD-088", to: "SHARD-042", trust: 0.65 },
        ],
        title = "Living Map",
        subtitle = "Phase Space: Recursive",
    }: Props = $props();

    let sentimentParticles: SentimentParticle[] = [];

    // 🧠 NAI: Reactive Atmosphere
    let ambientMood = $derived(
        naiEngine.getComponents<AmbientComponent>("ambient")[0] || {
            mood: "STABLE",
            baseColor: "#00f2ff",
        },
    );

    function initSentiment() {
        sentimentParticles = Array(60) // Reduced from 100 to minimize noise
            .fill(null)
            .map(() => ({
                x: Math.random(),
                y: Math.random(),
                vx: (Math.random() - 0.5) * 0.001,
                vy: (Math.random() - 0.5) * 0.001,
                sentiment: Math.random(),
            }));
    }

    let time = $state(0);

    function draw() {
        if (!ctx) return;

        // 🧠 NAI: Dynamic Animation Resonance
        const intensity = ambientMood.intensity ?? 0.5;
        const turbulence = ambientMood.turbulence ?? 0.0;
        const speedMultiplier =
            (ambientMood.mood === "CHAOTIC" ? 3 : 1) * (1 + turbulence * 2);

        time += 0.01 * speedMultiplier;

        ctx.clearRect(0, 0, width, height);

        // Calculate jittered positions for shards based on turbulence
        const jitteredShards = shards.map((s) => ({
            ...s,
            jx: s.x * width + (Math.random() - 0.5) * 20 * turbulence,
            jy: s.y * height + (Math.random() - 0.5) * 20 * turbulence,
        }));

        // Draw Ribbons (Trust Edges)
        ribbons.forEach((link) => {
            const start = jitteredShards.find((s) => s.id === link.from)!;
            const end = jitteredShards.find((s) => s.id === link.to)!;

            const x1 = start.jx;
            const y1 = start.jy;
            const x2 = end.jx;
            const y2 = end.jy;

            // Base line
            ctx.beginPath();
            ctx.moveTo(x1, y1);
            ctx.lineTo(x2, y2);
            const baseAlpha = Math.floor(intensity * 0.1 * link.trust * 255) // Reduced from 0.2
                .toString(16)
                .padStart(2, "0");
            ctx.strokeStyle = `${ambientMood.baseColor}${baseAlpha}`;
            ctx.lineWidth = 1 + link.trust * 3;
            ctx.stroke();

            // Glow with resonance pulse
            const resonance = Math.sin(time * 2) * 0.2 * intensity;
            ctx.beginPath();
            ctx.moveTo(x1, y1);
            ctx.lineTo(x2, y2);
            ctx.strokeStyle = `${ambientMood.baseColor}0d`;
            ctx.shadowBlur = (10 + resonance * 30) * link.trust;
            ctx.shadowColor = ambientMood.baseColor;
            ctx.lineWidth = 10 * link.trust;
            ctx.stroke();
            ctx.shadowBlur = 0;

            // Photonic Pulse
            const pulsePos = (time + link.from.length * 0.13) % 1.0;
            const px = x1 + (x2 - x1) * pulsePos;
            const py = y1 + (y2 - y1) * pulsePos;

            ctx.beginPath();
            ctx.arc(px, py, 2 + link.trust * 2, 0, Math.PI * 2);
            ctx.fillStyle =
                link.trust > 0.9 ? "#FDB813" : ambientMood.baseColor;
            ctx.fill();

            // Pulse Glow
            ctx.beginPath();
            ctx.arc(px, py, (6 + link.trust * 4) * intensity, 0, Math.PI * 2);
            ctx.fillStyle =
                link.trust > 0.9
                    ? "rgba(253, 184, 19, 0.2)"
                    : `${ambientMood.baseColor}33`;
            ctx.fill();
        });

        // Draw Shards (Nodes)
        jitteredShards.forEach((shard) => {
            const x = shard.jx;
            const y = shard.jy;
            const pulse =
                (1 + Math.sin(time * 2 + shard.id.length) * 0.1) *
                (1 + turbulence);

            // Outer Glow
            const gradient = ctx.createRadialGradient(
                x,
                y,
                0,
                x,
                y,
                20 * pulse * intensity,
            );
            gradient.addColorStop(
                0,
                `${shard.color}${Math.floor(0.2 * intensity * 255)
                    .toString(16)
                    .padStart(2, "0")}`,
            );
            gradient.addColorStop(1, "transparent");
            ctx.fillStyle = gradient;
            ctx.beginPath();
            ctx.arc(x, y, 20 * pulse * intensity, 0, Math.PI * 2);
            ctx.fill();

            // Core
            ctx.beginPath();
            ctx.arc(x, y, 4, 0, Math.PI * 2);
            ctx.fillStyle = shard.color;
            ctx.fill();

            // Ring
            ctx.beginPath();
            ctx.arc(x, y, 8 * pulse, 0, Math.PI * 2);
            ctx.strokeStyle = `${shard.color}88`;
            ctx.lineWidth = 1;
            ctx.stroke();

            // Label
            ctx.fillStyle = `rgba(255, 255, 255, ${0.3 + 0.3 * intensity})`;
            ctx.font = "8px 'IBM Plex Mono', monospace";
            ctx.textAlign = "center";
            ctx.fillText(shard.id, x, y + 24);
        });

        // Draw Sentiment Cloud (10M Voices Simulation)
        sentimentParticles.forEach((p) => {
            p.x += p.vx;
            p.y += p.vy;
            if (p.x < 0 || p.x > 1) p.vx *= -1;
            if (p.y < 0 || p.y > 1) p.vy *= -1;

            const px = p.x * width;
            const py = p.y * height;
            const size = 1 + Math.sin(time * 5 + p.x * 100) * 0.5;

            ctx.beginPath();
            ctx.arc(px, py, size, 0, Math.PI * 2);
            ctx.fillStyle =
                p.sentiment > 0.6
                    ? `rgba(0, 242, 255, 0.08)` // Reduced from 0.15
                    : `rgba(168, 85, 247, 0.08)`;
            ctx.fill();
        });

        animationFrame = requestAnimationFrame(draw);
    }

    onMount(() => {
        ctx = canvas.getContext("2d")!;
        const resize = () => {
            width = canvas.clientWidth;
            height = canvas.clientHeight;
            canvas.width = width * window.devicePixelRatio;
            canvas.height = height * window.devicePixelRatio;
            ctx.scale(window.devicePixelRatio, window.devicePixelRatio);
        };
        resize();
        initSentiment();
        window.addEventListener("resize", resize);
        draw();

        return () => {
            cancelAnimationFrame(animationFrame);
            window.removeEventListener("resize", resize);
        };
    });
</script>

<div
    class="relative w-full h-full min-h-[400px] glass-panel bg-black/80 overflow-hidden group"
>
    <canvas bind:this={canvas} class="w-full h-full"></canvas>

    <div class="absolute top-6 left-6 flex items-center gap-3">
        <div class="p-2 bg-neon-cyan/10 border border-neon-cyan/20 rounded-lg">
            <Globe size={16} class="text-neon-cyan" />
        </div>
        <div>
            <h3 class="text-xs font-black mono-font tracking-widest uppercase">
                {title}
            </h3>
            <p class="text-[8px] mono-font text-white/40 uppercase">
                {subtitle}
            </p>
        </div>
    </div>

    <div class="absolute bottom-6 left-6 flex items-center gap-6">
        <div class="flex flex-col gap-1">
            <span
                class="text-[8px] font-black text-white/30 uppercase tracking-tighter"
                >Coherence</span
            >
            <div class="flex items-center gap-2">
                <div class="h-1 w-12 bg-white/5 rounded-full overflow-hidden">
                    <div class="h-full bg-neon-cyan" style="width: 94%"></div>
                </div>
                <span class="text-[10px] mono-font text-neon-cyan">94.2%</span>
            </div>
        </div>
        <div class="flex flex-col gap-1">
            <span
                class="text-[8px] font-black text-white/30 uppercase tracking-tighter"
                >Resonance</span
            >
            <div class="flex items-center gap-2">
                <div class="h-1 w-12 bg-white/5 rounded-full overflow-hidden">
                    <div class="h-full bg-purple-400" style="width: 82%"></div>
                </div>
                <span class="text-[10px] mono-font text-purple-400">82.1%</span>
            </div>
        </div>
    </div>

    <div class="absolute top-6 right-6 space-y-2">
        <button
            class="flex items-center gap-2 px-3 py-1.5 bg-white/5 border border-white/10 rounded-full hover:bg-white/10 transition-all"
        >
            <Compass size={12} class="text-white/60" />
            <span
                class="text-[9px] font-black mono-font uppercase tracking-widest text-white/60"
                >Center View</span
            >
        </button>
        <button
            class="flex items-center gap-2 px-3 py-1.5 bg-white/5 border border-white/10 rounded-full hover:bg-white/10 transition-all"
        >
            <Layers size={12} class="text-white/60" />
            <span
                class="text-[9px] font-black mono-font uppercase tracking-widest text-white/60"
                >Toggle Layers</span
            >
        </button>
    </div>
</div>

<style>
    canvas {
        display: block;
    }
</style>
