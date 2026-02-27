<script lang="ts">
    import MarketplaceBrowser from "$lib/components/marketplace/MarketplaceBrowser.svelte";

    function handleInstall(e: CustomEvent) {
        const block = e.detail;
        alert(
            `${block.name} successfully installed to your workspace templates.`,
        );
    }
</script>

<svelte:head>
    <title>Sovereign Marketplace | AGE Protocol</title>
</svelte:head>

<MarketplaceBrowser oninstall={handleInstall} />
