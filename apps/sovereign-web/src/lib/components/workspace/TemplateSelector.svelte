<script lang="ts">
    import { onMount } from "svelte";
    import { workspacePersistence } from "$lib/services/workspace-persistence";
    import { fly } from "svelte/transition";

    export let onSelect: (columns: any[]) => void;
    export let currentColumns: any[] = [];

    let templates: any[] = [];
    let showNewTemplate = false;
    let newTemplateName = "";
    let newTemplateDesc = "";

    onMount(() => {
        templates = workspacePersistence.listTemplates();
    });

    function loadTemplate(template: any) {
        const columns = workspacePersistence.loadTemplate(template.id);
        if (columns && onSelect) {
            onSelect(columns);
        }
    }

    function saveCurrentAsTemplate() {
        if (newTemplateName && currentColumns.length > 0) {
            workspacePersistence.saveTemplate(
                newTemplateName,
                newTemplateDesc,
                currentColumns,
            );
            templates = workspacePersistence.listTemplates();
            showNewTemplate = false;
            newTemplateName = "";
            newTemplateDesc = "";
        }
    }
</script>

<div class="template-selector">
    <h3>Workspace Templates</h3>

    <div class="template-grid">
        {#each templates as template}
            <div class="template-card" on:click={() => loadTemplate(template)}>
                <h4>{template.name}</h4>
                <p>{template.description}</p>
                <div class="template-meta">
                    <span>Used {template.useCount} times</span>
                    <span
                        >{new Date(
                            template.lastUsed,
                        ).toLocaleDateString()}</span
                    >
                </div>
            </div>
        {/each}

        <button
            class="new-template-btn"
            on:click={() => (showNewTemplate = true)}
        >
            <span class="btn-icon">+</span>
            Save Current
        </button>
    </div>

    {#if showNewTemplate}
        <div
            class="new-template-modal"
            transition:fly={{ y: 20, duration: 200 }}
        >
            <h4>Save Workspace Template</h4>
            <input
                type="text"
                bind:value={newTemplateName}
                placeholder="Template name"
                class="template-input"
            />
            <textarea
                bind:value={newTemplateDesc}
                placeholder="Description"
                class="template-input"
                rows="3"
            ></textarea>
            <div class="modal-actions">
                <button
                    class="cancel-btn"
                    on:click={() => (showNewTemplate = false)}>Cancel</button
                >
                <button class="save-btn" on:click={saveCurrentAsTemplate}
                    >Save</button
                >
            </div>
        </div>
    {/if}
</div>

<style>
    .template-selector {
        padding: 1.5rem;
        background: rgba(20, 20, 30, 0.9);
        backdrop-filter: blur(25px);
        border: 1px solid rgba(255, 215, 0, 0.2);
        border-radius: 24px;
        margin: 2rem 0;
    }

    .template-selector h3 {
        margin-top: 0;
    }

    .template-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
        gap: 1rem;
        margin-top: 1rem;
    }

    .template-card {
        padding: 1rem;
        background: rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 215, 0, 0.1);
        border-radius: 12px;
        cursor: pointer;
        transition: all 0.2s ease;
    }

    .template-card:hover {
        border-color: #ffd700;
        transform: translateY(-2px);
    }

    .template-card h4 {
        margin: 0 0 0.5rem;
        color: white;
    }

    .template-card p {
        margin: 0 0 0.5rem;
        color: rgba(255, 255, 255, 0.5);
        font-size: 0.8rem;
    }

    .template-meta {
        display: flex;
        justify-content: space-between;
        color: rgba(255, 255, 255, 0.3);
        font-size: 0.7rem;
    }

    .new-template-btn {
        padding: 1rem;
        background: rgba(255, 215, 0, 0.1);
        border: 1px dashed rgba(255, 215, 0, 0.3);
        border-radius: 12px;
        color: #ffd700;
        cursor: pointer;
        transition: all 0.2s ease;
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 0.5rem;
    }

    .new-template-btn:hover {
        background: rgba(255, 215, 0, 0.2);
        border-style: solid;
    }

    .new-template-modal {
        margin-top: 1rem;
        padding: 1.5rem;
        background: rgba(0, 0, 0, 0.5);
        border-radius: 12px;
    }

    .template-input {
        width: 100%;
        padding: 0.75rem;
        margin: 0.5rem 0;
        background: rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 215, 0, 0.2);
        border-radius: 8px;
        color: white;
        box-sizing: border-box;
    }

    .modal-actions {
        display: flex;
        gap: 0.5rem;
        margin-top: 1rem;
    }

    .cancel-btn,
    .save-btn {
        flex: 1;
        padding: 0.75rem;
        border: none;
        border-radius: 8px;
        cursor: pointer;
    }

    .cancel-btn {
        background: rgba(255, 255, 255, 0.1);
        color: white;
    }

    .save-btn {
        background: #ffd700;
        color: #0a0a0f;
        font-weight: bold;
    }
</style>
