<script lang="ts">
    import { createQuery } from "@tanstack/svelte-query";

    const todosQuery = createQuery({
        queryKey: ["todos"],
        queryFn: () =>
            fetch("https://jsonplaceholder.typicode.com/todos?_limit=10").then(
                (res) => res.json(),
            ),
    });
</script>

<div class="todos-page">
    <h2>Todos (TanStack Demo)</h2>
    <p class="subtitle">
        Mocked live query showcasing automatic suspense and deduping logic
    </p>

    {#if $todosQuery.isPending}
        <div class="loading">Loading records from server...</div>
    {/if}

    {#if $todosQuery.isError}
        <div class="error">Error: {$todosQuery.error?.message}</div>
    {/if}

    <div class="todo-list">
        {#each $todosQuery.data || [] as todo (todo.id)}
            <div class="todo-item" class:completed={todo.completed}>
                <input type="checkbox" checked={todo.completed} readonly />
                <span class="text">{todo.title}</span>
            </div>
        {/each}
    </div>
</div>

<style>
    .todos-page {
        padding: 2rem;
        color: white;
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 1rem;
        max-width: 600px;
        margin: 0 auto;
    }
    h2 {
        margin: 0 0 0.5rem 0;
        color: #9370db;
    }
    .subtitle {
        color: rgba(255, 255, 255, 0.5);
        font-size: 0.9rem;
        margin-bottom: 2rem;
    }
    .loading {
        color: #4ecdc4;
        animation: pulse 1.5s infinite;
    }
    .error {
        color: #ff6b6b;
    }
    .todo-list {
        display: flex;
        flex-direction: column;
        gap: 0.75rem;
    }
    .todo-item {
        display: flex;
        align-items: center;
        gap: 1rem;
        padding: 1rem;
        background: rgba(0, 0, 0, 0.2);
        border-radius: 0.5rem;
        transition: all 0.2s;
    }
    .todo-item:hover {
        background: rgba(147, 112, 219, 0.1);
    }
    .todo-item.completed {
        opacity: 0.5;
    }
    .todo-item.completed .text {
        text-decoration: line-through;
    }
    input[type="checkbox"] {
        accent-color: #9370db;
        width: 1.2rem;
        height: 1.2rem;
    }
    @keyframes pulse {
        0%,
        100% {
            opacity: 1;
        }
        50% {
            opacity: 0.5;
        }
    }
</style>
