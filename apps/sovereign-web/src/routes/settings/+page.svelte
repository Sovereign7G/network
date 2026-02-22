<script lang="ts">
    import { goto } from "$app/navigation";
    import { onMount } from "svelte";

    // Redirect to sovereign dashboard for now
    onMount(() => {
        goto("/dashboard/sovereign");
    });
</script>

<!-- This page intentionally left blank - redirecting -->
