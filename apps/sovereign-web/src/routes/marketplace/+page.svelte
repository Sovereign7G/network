<script lang="ts">
    import MarketplaceBrowser from "$lib/components/marketplace/MarketplaceBrowser.svelte";

    function handleInstall(e: CustomEvent) {
        const block = e.detail;
        console.log(`Installing block: ${block.name}`);
        alert(
            `${block.name} successfully installed to your workspace templates.`,
        );
    }
</script>

<svelte:head>
    <title>Sovereign Marketplace | AGE Protocol</title>
</svelte:head>

<MarketplaceBrowser on:install={handleInstall} />
