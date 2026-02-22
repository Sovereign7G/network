<script lang="ts">
	import {
		Shield,
		Zap,
		Activity,
		Globe,
		Cpu,
		Camera,
		ArrowRight,
		ChevronDown,
		User,
		Vote,
		Car,
		DollarSign,
		Layers,
		Fingerprint,
		ChevronRight,
		Star,
		Apple,
		Coffee,
		Ticket,
		Droplets,
		PhoneCall,
		Plus,
	} from "lucide-svelte";
	import { onMount } from "svelte";
	import { fade, fly, slide } from "svelte/transition";
	import LivingMap from "$lib/components/map/LivingMap.svelte";
	import Onboarding from "$lib/components/Onboarding.svelte";
	import Security from "$lib/components/Security.svelte";
	import Tutorial from "$lib/components/Tutorial.svelte";
	import Vault from "$lib/components/Vault.svelte";
	import Market from "$lib/components/Market.svelte";
	import Profile from "$lib/components/Profile.svelte";
	import Governance from "$lib/components/Governance.svelte";
	import Services from "$lib/components/Services.svelte";
	import { authStatus, hasSeenTutorial } from "$lib/stores/auth.js";
	import { naiEngine } from "$lib/nai/engine.svelte";
	import type { AmbientComponent } from "$lib/nai/types";

	let mounted = $state(false);
	let scrollY = $state(0);
	let showProfile = $state(false);
	let showSpecs = $state(false);
	let currentView = $state("home"); // "home", "vault", "market", "profile", "governance"

	// 🧠 NAI: Global Atmosphere
	let ambientMood = $derived(
		naiEngine.getComponents<AmbientComponent>("ambient")[0] || {
			mood: "STABLE",
			baseColor: "#06b6d4",
		},
	);

	onMount(() => {
		mounted = true;
	});

	const features = [
		{
			title: "Assets",
			description:
				"Secure, zero-knowledge management for your digital wealth.",
			icon: DollarSign,
			color: "text-neon-cyan",
		},
		{
			title: "Network",
			description:
				"Decentralized identity and causal resonance for verified citizens.",
			icon: Globe,
			color: "text-plasma-purple",
		},
		{
			title: "Prosperity",
			description:
				"Algorithmic life services and prosperity streams hardcoded into the substrate.",
			icon: Activity,
			color: "text-neon-amber",
		},
		{
			title: "Hardening",
			description:
				"Sovereign forensic audits and real-time causal tracing.",
			icon: Shield,
			color: "text-aurora-green",
		},
	];
</script>

<svelte:window bind:scrollY />

{#if $authStatus === "onboarding"}
	<Onboarding />
{:else if $authStatus === "security"}
	<Security />
{:else}
	{#if !$hasSeenTutorial}
		<Tutorial />
	{/if}

	<div
		class="relative min-h-screen overflow-x-hidden bg-[#050505] text-white"
	>
		<!-- Background Effects -->
		<div class="fixed inset-0 pointer-events-none z-0">
			<!-- Visual Guard: Backdrop blur to prevent background burn -->
			<div
				class="absolute inset-0 bg-black/60 backdrop-blur-[60px] z-10"
			></div>

			<div
				class="absolute top-[-10%] left-[-10%] w-[45%] h-[45%] rounded-full blur-[140px] transition-all duration-1000 z-0"
				style="background-color: {ambientMood.baseColor}20"
			></div>
			<div
				class="absolute bottom-[-10%] right-[-10%] w-[45%] h-[45%] rounded-full blur-[140px] transition-all duration-1000 z-0"
				style="background-color: {ambientMood.baseColor}15"
			></div>
		</div>

		<!-- Navigation -->
		<nav
			class="fixed top-0 left-0 right-0 z-50 border-b border-white/5 backdrop-blur-md bg-black/20"
		>
			<div
				class="max-w-7xl mx-auto px-6 h-20 flex items-center justify-between"
			>
				<div class="flex items-center space-x-2">
					<div
						class="w-8 h-8 bg-cyan-400/20 border border-cyan-400 flex items-center justify-center rounded-lg shadow-[0_0_15px_rgba(0,242,255,0.3)]"
					>
						<div
							class="w-4 h-4 bg-cyan-400 rounded-sm animate-pulse"
						></div>
					</div>
					<span
						class="text-xl font-black tracking-tighter uppercase italic"
						>AGE<span class="text-cyan-400"> PROTOCOL</span></span
					>
				</div>

				<div
					class="hidden md:flex items-center space-x-6 text-[11px] font-semibold tracking-wider text-white/40"
				>
					<button
						onclick={() => (currentView = "home")}
						class="hover:text-white transition-colors {currentView ===
						'home'
							? 'text-white'
							: ''}">HUB</button
					>
					<button
						onclick={() => (currentView = "vault")}
						class="hover:text-white transition-colors {currentView ===
						'vault'
							? 'text-cyan-400'
							: ''}">ASSETS</button
					>
					<button
						onclick={() => (currentView = "market")}
						class="hover:text-white transition-colors {currentView ===
						'market'
							? 'text-emerald-400'
							: ''}">MARKET</button
					>
					<button
						onclick={() => (currentView = "governance")}
						class="hover:text-white transition-colors {currentView ===
						'governance'
							? 'text-cyan-400'
							: ''}">DECISIONS</button
					>
					<button
						onclick={() => (currentView = "services")}
						class="hover:text-white transition-colors {currentView ===
						'services'
							? 'text-amber-400'
							: ''}">LIFE</button
					>
					<a
						href="/dashboard"
						class="px-4 py-2 bg-white/5 border border-white/10 text-white hover:bg-white/10 transition-all rounded-lg"
						>ORCHESTRATE</a
					>
				</div>
			</div>
		</nav>

		{#if currentView === "home"}
			<!-- Hero Section -->
			<section
				class="relative pt-32 pb-20 px-6 min-h-screen flex flex-col justify-center items-center text-center overflow-hidden"
			>
				{#if mounted}
					<div in:fade={{ duration: 1500 }} class="relative z-10">
						<div
							class="inline-flex items-center space-x-2 px-3 py-1 rounded-full border border-white/10 bg-white/5 mb-8"
						>
							<div
								class="w-2 h-2 rounded-full bg-emerald-400 animate-ping"
							></div>
							<span
								class="text-[10px] font-black tracking-widest text-white/60"
								>MAINNET ACTIVE // NETWORK STABILIZED</span
							>
						</div>

						<h1
							in:fly={{ y: 20, duration: 1000 }}
							class="text-6xl md:text-9xl font-black tracking-tighter leading-none uppercase italic mb-8 premium-gradient-text"
						>
							CIVILIZATION<br />
							<span class="text-cyan-400">REMASTERED</span>
						</h1>

						<p
							class="max-w-2xl mx-auto text-lg text-white/60 leading-relaxed mb-12 italic"
						>
							The AGE Protocol: An institutional substrate for the
							next digital nation. Wealth is hardcoded. Identity
							is sovereign.
						</p>

						<div
							class="flex flex-col md:flex-row items-center justify-center gap-6 mb-20"
						>
							<button
								onclick={() => (currentView = "vault")}
								class="action-button group relative overflow-hidden transition-all shadow-[0_0_30px_rgba(254,93,41,0.3)]"
							>
								<span
									class="relative z-10 flex items-center gap-2"
								>
									OPEN ARSENAL <ArrowRight
										size={20}
										class="group-hover:translate-x-1 transition-transform"
									/>
								</span>
							</button>
						</div>
					</div>
				{/if}
			</section>

			<!-- Bento Features Grid -->
			<section id="features" class="py-32 px-6 max-w-7xl mx-auto">
				<div class="mb-20">
					<div
						class="text-cyan-400 text-[10px] font-black tracking-[0.4em] uppercase mb-4"
					>
						Core Architecture
					</div>
					<h2
						class="text-4xl md:text-6xl font-black italic tracking-tighter uppercase leading-none"
					>
						INSTITUTIONAL<br />SUBSTRATE
					</h2>
				</div>

				<div class="grid grid-cols-1 lg:grid-cols-3 gap-8 items-start">
					<div class="lg:col-span-2">
						<div class="grid grid-cols-1 md:grid-cols-2 gap-6">
							{#each features as feature}
								{@const Icon = feature.icon}
								<div
									class="glass-panel p-8 group hover:border-white/20 transition-all"
								>
									<div
										class="p-4 rounded-2xl bg-white/5 w-fit mb-8 group-hover:scale-110 transition-transform {feature.color}"
									>
										<Icon size={24} />
									</div>
									<h3
										class="text-xl font-black italic uppercase tracking-tight mb-4"
									>
										{feature.title}
									</h3>
									<p
										class="text-white/60 text-sm leading-relaxed mb-8"
									>
										{feature.description}
									</p>
								</div>
							{/each}
						</div>
					</div>
					<div class="lg:col-span-1 h-full min-h-[600px]">
						<LivingMap
							title="GLOBAL SUBSTRATE"
							subtitle="Institutional Mesh Active"
						/>
					</div>
				</div>
			</section>
		{:else if currentView === "vault"}
			<div class="pt-32">
				<Vault />
			</div>
		{:else if currentView === "market"}
			<div class="pt-32">
				<Market />
			</div>
		{:else if currentView === "profile"}
			<div class="pt-32">
				<Profile />
			</div>
		{:else if currentView === "governance"}
			<div class="pt-32">
				<Governance />
			</div>
		{:else if currentView === "services"}
			<div class="pt-32">
				<Services />
			</div>
		{/if}

		<!-- Footer -->
		<footer class="py-20 border-t border-white/5 bg-black/40 relative z-10">
			<div class="max-w-7xl mx-auto px-6">
				<div
					class="pt-10 flex flex-col md:flex-row justify-between items-center text-[10px] font-black text-white/20 uppercase tracking-widest gap-6"
				>
					<span>© 2026 AGE PROTOCOL MANIFOLD</span>
					<div class="flex space-x-8">
						<a
							href="/terms"
							class="hover:text-white transition-colors">Terms</a
						>
						<a
							href="/privacy"
							class="hover:text-white transition-colors"
							>Privacy</a
						>
						<a
							href="/legal"
							class="hover:text-white transition-colors"
							>Compliance</a
						>
					</div>
				</div>
			</div>
		</footer>
	</div>
{/if}
