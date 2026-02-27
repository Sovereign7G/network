<script lang="ts">
	import { onMount } from "svelte";
	import { goto } from "$app/navigation";
	import { page } from "$app/stores";
	import { browser } from "$app/environment";
	import { QueryClient, QueryClientProvider } from "@tanstack/svelte-query";
	import {
		sovereignStore,
		systemHealth,
		vaultStore,
	} from "$lib/stores/master-store";
	import AppLayout from "$lib/components/layout/AppLayout.svelte";
	import VisualOverlay from "$lib/components/VisualOverlay.svelte";
	import SonicIndicator from "$lib/components/dashboard/SonicIndicator.svelte";
	import "../../../../packages/age-cleanroom/src/styles/stealth-mode.css";

	let mounted = false;

	const queryClient = new QueryClient({
		defaultOptions: {
			queries: { enabled: browser }, // Disable SSR queries
		},
	});

	import { cleanRoomActive } from "../../../../packages/age-cleanroom/src/store/clean-room-store";

	onMount(() => {
		mounted = true;
		sovereignStore.updateLastActive();

		// 🏛️ SOVEREIGN BRIDGE: Initialize data from backend
		const init = async () => {
			try {
				await Promise.all([
					vaultStore.loadVaultData(),
					sovereignStore.loadSovereignData(),
				]);
			} catch (error) {
				console.error("❌ Failed to sync Cathedral stores:", error);
			}
		};
		init();

		// Sync Clean Room body class
		const unsubClean = cleanRoomActive.subscribe((active: boolean) => {
			if (browser) {
				if (active) document.body.classList.add("clean-room-active");
				else document.body.classList.remove("clean-room-active");
			}
		});

		// Check if user is onboarded
		const sovereign = localStorage.getItem("sovereign");
		if (!sovereign && $page.url.pathname !== "/onboarding") {
			goto("/onboarding");
		}

		return () => {
			unsubClean();
		};
	});

	$: isQuietMode = $systemHealth?.quietMode || false;
</script>

<svelte:head>
	<title>AGE Protocol · Sovereign OS</title>
	<meta name="viewport" content="width=device-width, initial-scale=1.0" />
	<meta name="theme-color" content="#9370DB" />
</svelte:head>

<QueryClientProvider client={queryClient}>
	<div class="app" class:quiet-mode={isQuietMode} class:mounted>
		<!-- Visual overlay effects (AR/HUD) -->
		<VisualOverlay />

		{#if mounted}
			<AppLayout>
				<slot />
			</AppLayout>
		{/if}

		<!-- Sensory Feedback -->
		<SonicIndicator />
	</div>
</QueryClientProvider>

<style>
	.app {
		min-height: 100vh;
		background: radial-gradient(
				circle at 20% 30%,
				rgba(147, 112, 219, 0.15),
				transparent 40%
			),
			radial-gradient(
				circle at 80% 70%,
				rgba(255, 107, 107, 0.1),
				transparent 40%
			),
			#0a0a0a;
		color: white;
		font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
			Oxygen, Ubuntu, Cantarell, "Open Sans", "Helvetica Neue", sans-serif;
		transition: all 0.3s;
	}

	.app.quiet-mode {
		filter: brightness(0.9) saturate(0.8);
		transition: filter 0.5s;
	}

	.app.mounted {
		animation: fadeIn 0.5s;
	}

	@keyframes fadeIn {
		from {
			opacity: 0;
		}
		to {
			opacity: 1;
		}
	}
</style>
