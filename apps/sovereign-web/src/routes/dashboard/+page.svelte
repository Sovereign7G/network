<script lang="ts">
	import { onMount } from "svelte";
	import { fly } from "svelte/transition";
	import WorkspaceCanvas from "$lib/components/blocks/WorkspaceCanvas.svelte";
	import TemplateSelector from "$lib/components/workspace/TemplateSelector.svelte";
	import { vaultStore } from "$lib/stores/master-store";

	// Initial workspace state - citizens will rearrange this
	const initialColumns: any[] = [
		{
			id: "col-wealth",
			blocks: [
				{
					id: "block-wealth",
					type: "tile",
					content: {
						title: "Sovereign Treasury",
						value: "$48.76B",
						icon: "💰",
						variant: "primary",
					},
					schema: "wealth-tile",
				},
				{
					id: "block-resonance",
					type: "tile",
					content: {
						title: "Resonance",
						value: "98%",
						icon: "✨",
						variant: "success",
					},
					schema: "resonance-tile",
				},
			],
		},
		{
			id: "col-atlas",
			blocks: [
				{
					id: "block-atlas",
					type: "canvas",
					content: {
						title: "Living Atlas",
						canvasType: "network-topology",
						height: 300,
					},
					schema: "atlas-canvas",
				},
			],
		},
		{
			id: "col-nodes",
			blocks: [
				{
					id: "block-nodes",
					type: "tile",
					content: {
						title: "Active Nodes",
						value: "389,000",
						icon: "⚡",
						variant: "warning",
					},
					schema: "nodes-tile",
				},
				{
					id: "block-hearth",
					type: "tile",
					content: {
						title: "Hearth Memories",
						value: "47",
						icon: "🔥",
						variant: "danger",
					},
					schema: "hearth-tile",
				},
			],
		},
		{
			id: "col-activity",
			blocks: [
				{
					id: "block-activity",
					type: "table",
					content: {
						title: "Recent Activity",
						headers: ["Type", "Amount", "Time", "Status"],
						rows: [
							["Bridge", "5,000 USDC", "2 min ago", "completed"],
							["Stake", "1,200 SYND", "15 min ago", "active"],
							["Vote", "Proposal #12", "1 hour ago", "cast"],
						],
					},
					schema: "activity-table",
				},
			],
		},
	];

	let workspaceColumns = $state(initialColumns);

	let isLoading = $state(true);

	onMount(async () => {
		try {
			await vaultStore.loadVaultData();
		} catch (e) {
			console.warn("Store load skipped", e);
		}

		// Load saved workspace from localStorage
		const saved = localStorage.getItem("sovereign-workspace");
		if (saved) {
			try {
				workspaceColumns = JSON.parse(saved);
			} catch (e) {}
		}

		isLoading = false;
	});

	function handleWorkspaceChange(
		updatedColumns: { id: string; blocks: any[] }[],
	) {
		workspaceColumns = updatedColumns;
		localStorage.setItem(
			"sovereign-workspace",
			JSON.stringify(updatedColumns),
		);
	}

	function addNewColumn() {
		workspaceColumns = [
			...workspaceColumns,
			{
				id: `col-${Date.now()}`,
				blocks: [],
			},
		];
	}

	function handleTemplateSelect(columns: any[]) {
		workspaceColumns = columns;
		localStorage.setItem("sovereign-workspace", JSON.stringify(columns));
	}
</script>

<div class="dashboard-container" in:fly={{ y: 20, duration: 400 }}>
	{#if isLoading}
		<div class="loading-state">
			<div class="resonance-breath"></div>
			<p>Awakening the Cathedral...</p>
		</div>
	{:else}
		<TemplateSelector
			currentColumns={workspaceColumns}
			onSelect={handleTemplateSelect}
		/>

		<WorkspaceCanvas
			bind:columns={workspaceColumns}
			onLayoutChange={handleWorkspaceChange}
			tile={tileSnippet}
			canvas={canvasSnippet}
			table={tableSnippet}
		/>

		{#snippet tileSnippet(content: any)}
			<div class="wealth-tile">
				<span class="tile-icon">{content.icon}</span>
				<div class="tile-content">
					<h3>{content.title}</h3>
					<p class="tile-value">{content.value}</p>
				</div>
			</div>
		{/snippet}

		{#snippet canvasSnippet(content: any)}
			<div class="canvas-container" style="height: {content.height}px">
				<!-- Canvas component would render here -->
				<div class="canvas-placeholder">
					<span class="canvas-icon">🗺️</span>
					<span>{content.title}</span>
				</div>
			</div>
		{/snippet}

		{#snippet tableSnippet(content: any)}
			<div class="table-container">
				<h4>{content.title}</h4>
				<table>
					<thead>
						<tr>
							{#each content.headers || [] as header}
								<th>{header}</th>
							{/each}
						</tr>
					</thead>
					<tbody>
						{#each content.rows || [] as row}
							<tr>
								{#each row as cell}
									<td>{cell}</td>
								{/each}
							</tr>
						{/each}
					</tbody>
				</table>
			</div>
		{/snippet}

		<button class="add-column-btn" onclick={addNewColumn}>
			<span class="btn-icon">+</span>
			Add Column
		</button>
	{/if}
</div>

<style>
	.dashboard-container {
		min-height: 100vh;
		padding: 1rem;
		padding-bottom: 6rem;
	}

	.loading-state {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		height: 60vh;
		gap: 2rem;
	}

	.resonance-breath {
		width: 100px;
		height: 100px;
		background: radial-gradient(
			circle at 30% 50%,
			rgba(255, 215, 0, 0.3),
			transparent 70%
		);
		animation: breath 4s ease-in-out infinite;
		border-radius: 50%;
	}

	@keyframes breath {
		0%,
		100% {
			transform: scale(1);
			opacity: 0.5;
		}
		50% {
			transform: scale(1.1);
			opacity: 0.8;
		}
	}

	.wealth-tile {
		display: flex;
		align-items: center;
		gap: 1rem;
		padding: 1rem;
	}

	.tile-icon {
		font-size: 2rem;
	}

	.tile-content h3 {
		margin: 0 0 0.25rem;
		color: rgba(255, 255, 255, 0.7);
		font-size: 0.9rem;
	}

	.tile-value {
		margin: 0;
		font-size: 1.5rem;
		font-weight: bold;
		color: #ffd700;
	}

	.canvas-placeholder {
		width: 100%;
		height: 100%;
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		gap: 0.5rem;
		background: rgba(0, 0, 0, 0.3);
		border-radius: 16px;
		color: rgba(255, 255, 255, 0.5);
	}

	.canvas-icon {
		font-size: 2rem;
	}

	.table-container {
		padding: 1rem;
	}

	.table-container h4 {
		margin: 0 0 1rem;
		color: rgba(255, 255, 255, 0.7);
	}

	table {
		width: 100%;
		border-collapse: collapse;
	}

	th {
		text-align: left;
		padding: 0.5rem;
		color: rgba(255, 255, 255, 0.5);
		font-weight: normal;
		font-size: 0.8rem;
		border-bottom: 1px solid rgba(255, 215, 0, 0.2);
	}

	td {
		padding: 0.5rem;
		color: white;
		border-bottom: 1px solid rgba(255, 255, 255, 0.1);
	}

	.add-column-btn {
		position: fixed;
		bottom: 2rem;
		right: 2rem;
		display: flex;
		align-items: center;
		gap: 0.5rem;
		padding: 0.75rem 1.5rem;
		background: rgba(255, 215, 0, 0.1);
		border: 1px solid rgba(255, 215, 0, 0.3);
		border-radius: 100px;
		color: #ffd700;
		cursor: pointer;
		transition: all 0.3s ease;
		z-index: 100;
	}

	.add-column-btn:hover {
		background: #ffd700;
		color: #0a0a0f;
		transform: translateY(-2px);
	}

	.btn-icon {
		font-size: 1.2rem;
		font-weight: bold;
	}
</style>
