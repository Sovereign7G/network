<script lang="ts">
    import { onMount } from "svelte";
    import { createEventDispatcher } from "svelte";
    import { fly } from "svelte/transition";

    export let conversation = null;
    export let personality = null;

    const dispatch = createEventDispatcher();

    let messagesEnd;
    let inputValue = "";
    let isTyping = false;

    onMount(() => {
        scrollToBottom();
    });

    $: if (conversation) {
        scrollToBottom();
    }

    function scrollToBottom() {
        setTimeout(() => {
            if (messagesEnd) {
                messagesEnd.scrollIntoView({ behavior: "smooth" });
            }
        }, 100);
    }

    function handleSend(textValue = inputValue) {
        if (!textValue.trim()) return;

        dispatch("send", textValue);
        if (textValue === inputValue) {
            inputValue = "";
        }

        // Simulate typing
        isTyping = true;
        setTimeout(() => {
            isTyping = false;
            scrollToBottom();
        }, 1500);
    }

    function handleKeyDown(e) {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            handleSend();
        }
    }
</script>

<div class="chat-interface">
    {#if conversation}
        <!-- Chat header -->
        <div class="chat-header">
            <div
                class="personality-info"
                style="--personality-color: {personality?.color || '#9370DB'};"
            >
                <span class="personality-icon">{personality?.icon || "🤵"}</span
                >
                <div>
                    <span class="personality-name"
                        >{personality?.name || "Concierge"}</span
                    >
                    <span class="personality-desc"
                        >{personality?.description || "Your AI guide"}</span
                    >
                </div>
            </div>
            <span class="conversation-title">{conversation.title}</span>
        </div>

        <!-- Messages area -->
        <div class="messages-area">
            {#if conversation.messages && conversation.messages.length > 0}
                {#each conversation.messages as message (message.id)}
                    <div
                        class="message-wrapper"
                        class:user={message.role === "user"}
                        class:assistant={message.role === "assistant"}
                        in:fly={{ y: 10, duration: 300 }}
                    >
                        <div class="message-avatar">
                            {#if message.role === "user"}
                                <span class="avatar-icon">👤</span>
                            {:else}
                                <span
                                    class="avatar-icon"
                                    style="color: {personality?.color ||
                                        '#9370DB'};"
                                >
                                    {personality?.icon || "🤵"}
                                </span>
                            {/if}
                        </div>

                        <div class="message-content">
                            <div class="message-bubble">
                                <p class="message-text">{message.content}</p>

                                {#if message.suggestions && message.suggestions.length > 0}
                                    <div class="message-suggestions">
                                        {#each message.suggestions as suggestion}
                                            <button
                                                class="suggestion-chip"
                                                on:click={() =>
                                                    handleSend(suggestion.text)}
                                            >
                                                {suggestion.text}
                                            </button>
                                        {/each}
                                    </div>
                                {/if}
                            </div>

                            <span class="message-time">
                                {new Intl.DateTimeFormat("en-US", {
                                    hour: "2-digit",
                                    minute: "2-digit",
                                }).format(new Date(message.timestamp))}
                            </span>
                        </div>
                    </div>
                {/each}
            {:else}
                <div class="empty-chat">
                    <span class="empty-icon">💬</span>
                    <h3>Start a conversation</h3>
                    <p>Ask me about your Hearth, Vault, or Governance</p>
                </div>
            {/if}

            {#if isTyping}
                <div class="typing-indicator" in:fly={{ y: 10 }}>
                    <span class="typing-dot"></span>
                    <span class="typing-dot"></span>
                    <span class="typing-dot"></span>
                </div>
            {/if}

            <div bind:this={messagesEnd} />
        </div>

        <!-- Input area -->
        <div class="input-area">
            <textarea
                class="message-input"
                placeholder="Ask your Concierge..."
                bind:value={inputValue}
                on:keydown={handleKeyDown}
                rows="1"
            ></textarea>

            <button
                class="send-button"
                on:click={() => handleSend(inputValue)}
                disabled={!inputValue.trim() || isTyping}
            >
                <span class="send-icon">📤</span>
            </button>
        </div>
    {:else}
        <div class="no-conversation">
            <span class="empty-icon">💭</span>
            <h3>No conversation selected</h3>
            <p>Start a new conversation or select one from the sidebar</p>
            <button class="new-chat-btn" on:click={() => dispatch("new")}>
                New Conversation
            </button>
        </div>
    {/if}
</div>

<style>
    .chat-interface {
        height: 100%;
        display: flex;
        flex-direction: column;
        background: rgba(0, 0, 0, 0.2);
    }

    .chat-header {
        padding: 1rem 1.5rem;
        background: rgba(255, 255, 255, 0.02);
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .personality-info {
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }

    .personality-icon {
        font-size: 1.5rem;
        color: var(--personality-color);
    }

    .personality-name {
        display: block;
        font-weight: 600;
        font-size: 0.9rem;
    }

    .personality-desc {
        display: block;
        font-size: 0.7rem;
        opacity: 0.5;
    }

    .conversation-title {
        font-size: 0.9rem;
        opacity: 0.7;
    }

    .messages-area {
        flex: 1;
        overflow-y: auto;
        padding: 1.5rem;
        display: flex;
        flex-direction: column;
        gap: 1rem;
    }

    .message-wrapper {
        display: flex;
        gap: 1rem;
        max-width: 80%;
    }

    .message-wrapper.user {
        align-self: flex-end;
        flex-direction: row-reverse;
    }

    .message-wrapper.assistant {
        align-self: flex-start;
    }

    .message-avatar {
        width: 2.5rem;
        height: 2.5rem;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
    }

    .avatar-icon {
        font-size: 1.2rem;
    }

    .message-content {
        flex: 1;
    }

    .message-bubble {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 1rem;
        padding: 1rem;
        position: relative;
    }

    .user .message-bubble {
        background: rgba(147, 112, 219, 0.15);
        border: 1px solid rgba(147, 112, 219, 0.3);
    }

    .message-text {
        margin: 0;
        line-height: 1.5;
        white-space: pre-wrap;
    }

    .message-suggestions {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
        margin-top: 1rem;
    }

    .suggestion-chip {
        padding: 0.25rem 0.75rem;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 2rem;
        color: white;
        font-size: 0.8rem;
        cursor: pointer;
        transition: all 0.2s;
    }

    .suggestion-chip:hover {
        background: rgba(147, 112, 219, 0.2);
        border-color: #9370db;
    }

    .message-time {
        display: block;
        margin-top: 0.25rem;
        font-size: 0.6rem;
        opacity: 0.5;
        text-align: right;
    }

    .empty-chat {
        height: 100%;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        opacity: 0.5;
    }

    .empty-icon {
        font-size: 4rem;
        margin-bottom: 1rem;
    }

    .empty-chat h3 {
        margin: 0 0 0.5rem 0;
    }

    .empty-chat p {
        margin: 0;
    }

    .typing-indicator {
        display: flex;
        gap: 0.5rem;
        padding: 1rem;
        background: rgba(255, 255, 255, 0.02);
        border-radius: 2rem;
        align-self: flex-start;
        width: fit-content;
    }

    .typing-dot {
        width: 0.5rem;
        height: 0.5rem;
        background: #9370db;
        border-radius: 50%;
        animation: typing 1.4s infinite;
    }

    .typing-dot:nth-child(2) {
        animation-delay: 0.2s;
    }

    .typing-dot:nth-child(3) {
        animation-delay: 0.4s;
    }

    @keyframes typing {
        0%,
        60%,
        100% {
            transform: translateY(0);
        }
        30% {
            transform: translateY(-10px);
        }
    }

    .input-area {
        display: flex;
        gap: 1rem;
        padding: 1.5rem;
        background: rgba(255, 255, 255, 0.02);
        border-top: 1px solid rgba(255, 255, 255, 0.05);
    }

    .message-input {
        flex: 1;
        padding: 0.75rem;
        background: rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 1.5rem;
        color: white;
        font-family: inherit;
        resize: none;
        min-height: 2.5rem;
        max-height: 8rem;
    }

    .message-input:focus {
        outline: none;
        border-color: #9370db;
    }

    .send-button {
        width: 3rem;
        height: 3rem;
        background: linear-gradient(135deg, #9370db, #ff6b6b);
        border: none;
        border-radius: 50%;
        color: white;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.2s;
    }

    .send-button:hover:not(:disabled) {
        transform: scale(1.1);
        box-shadow: 0 0 20px rgba(147, 112, 219, 0.4);
    }

    .send-button:disabled {
        opacity: 0.5;
        cursor: not-allowed;
    }

    .send-icon {
        font-size: 1.2rem;
    }

    .no-conversation {
        height: 100%;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
    }

    .new-chat-btn {
        margin-top: 1rem;
        padding: 0.75rem 2rem;
        background: linear-gradient(135deg, #9370db, #ff6b6b);
        border: none;
        border-radius: 2rem;
        color: white;
        cursor: pointer;
        transition: all 0.2s;
    }

    .new-chat-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 20px rgba(147, 112, 219, 0.4);
    }
</style>
