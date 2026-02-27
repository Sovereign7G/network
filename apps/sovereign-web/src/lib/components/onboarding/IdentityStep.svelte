<script lang="ts">
    let { data, onnext, onback } = $props();

    let formData = $state({
        displayName: "",
        handle: "",
        bio: "",
        interests: [] as string[],
        avatar: null as string | null,
    });

    let errors = $state({} as any);
    let avatarPreview = $state(null as string | null);
    let isGeneratingAvatar = $state(false);

    $effect(() => {
        formData.displayName = data.displayName || "";
        formData.handle = data.handle || "";
        formData.bio = data.bio || "";
        formData.interests = data.interests || [];
        formData.avatar = data.avatar || null;
        avatarPreview = data.avatar || null;
    });

    const INTEREST_OPTIONS = [
        "DeFi",
        "Governance",
        "AI",
        "Wellbeing",
        "Community",
        "Art",
        "Science",
        "Philosophy",
    ];

    function validateForm() {
        errors = {};

        if (!formData.displayName.trim()) {
            errors.displayName = "Name is required";
        }

        if (!formData.handle.trim()) {
            errors.handle = "Handle is required";
        } else if (!/^[a-zA-Z0-9_]+$/.test(formData.handle)) {
            errors.handle = "Only letters, numbers, and underscores";
        }

        return Object.keys(errors).length === 0;
    }

    function handleSubmit(e: Event) {
        e.preventDefault();
        if (validateForm()) {
            if (onnext) onnext(formData);
        }
    }

    function handleFileUpload(event: Event) {
        const target = event.target as HTMLInputElement;
        const file = target.files?.[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (e) => {
                const result = e.target?.result as string;
                avatarPreview = result;
                formData.avatar = result;
            };
            reader.readAsDataURL(file);
        }
    }

    function generateAvatar() {
        isGeneratingAvatar = true;

        // Simulate AI avatar generation
        setTimeout(() => {
            const colors = ["9370DB", "FF6B6B", "4ECDC4", "FFD700"];
            const color = colors[Math.floor(Math.random() * colors.length)];
            const initials =
                formData.displayName
                    .split(" ")
                    .map((n: string) => n[0])
                    .join("")
                    .toUpperCase()
                    .slice(0, 2) || "C";

            // Generate a simple SVG avatar
            const svg = `data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='100' height='100'%3E%3Crect width='100' height='100' fill='%23${color}'/%3E%3Ctext x='50' y='50' font-size='40' text-anchor='middle' dy='.3em' fill='white' font-family='Arial'%3E${initials}%3C/text%3E%3C/svg%3E`;

            avatarPreview = svg;
            formData.avatar = svg;
            isGeneratingAvatar = false;
        }, 1000);
    }

    function toggleInterest(interest: string) {
        if (formData.interests.includes(interest)) {
            formData.interests = formData.interests.filter(
                (i: string) => i !== interest,
            );
        } else {
            formData.interests = [...formData.interests, interest];
        }
    }
</script>

<div class="identity-step">
    <h2 class="step-title">Forge Your Identity</h2>
    <p class="step-subtitle">Your sovereign self awaits</p>

    <form class="identity-form" onsubmit={handleSubmit}>
        <!-- Avatar section -->
        <div class="avatar-section">
            <div class="avatar-container">
                {#if avatarPreview}
                    <img
                        src={avatarPreview}
                        alt="Avatar"
                        class="avatar-preview"
                    />
                {:else}
                    <div class="avatar-placeholder">
                        <span class="placeholder-icon">👤</span>
                    </div>
                {/if}

                <div class="avatar-actions">
                    <label class="avatar-upload" for="avatar-input">
                        <span class="upload-icon">📁</span>
                        <span>Upload</span>
                    </label>
                    <input
                        type="file"
                        id="avatar-input"
                        accept="image/*"
                        onchange={handleFileUpload}
                        hidden
                    />
                    <button
                        type="button"
                        class="avatar-generate"
                        onclick={generateAvatar}
                        disabled={isGeneratingAvatar}
                    >
                        <span class="generate-icon"
                            >{isGeneratingAvatar ? "⏳" : "✨"}</span
                        >
                        <span
                            >{isGeneratingAvatar
                                ? "Generating..."
                                : "Generate"}</span
                        >
                    </button>
                </div>
            </div>
        </div>

        <!-- Display Name -->
        <div class="form-group">
            <label for="displayName" class="form-label">
                Display Name <span class="required">*</span>
            </label>
            <input
                type="text"
                id="displayName"
                class="form-input"
                class:error={errors.displayName}
                bind:value={formData.displayName}
                placeholder="How should we address you?"
                maxlength="50"
            />
            {#if errors.displayName}
                <span class="error-message">{errors.displayName}</span>
            {/if}
            <span class="char-count">{formData.displayName.length}/50</span>
        </div>

        <!-- Handle -->
        <div class="form-group">
            <label for="handle" class="form-label">
                Sovereign Handle <span class="required">*</span>
            </label>
            <div class="handle-input-wrapper">
                <span class="handle-prefix">@</span>
                <input
                    type="text"
                    id="handle"
                    class="form-input handle-input"
                    class:error={errors.handle}
                    bind:value={formData.handle}
                    placeholder="sovereign_handle"
                    maxlength="30"
                />
            </div>
            {#if errors.handle}
                <span class="error-message">{errors.handle}</span>
            {/if}
            <span class="char-count">{formData.handle.length}/30</span>
        </div>

        <!-- Bio -->
        <div class="form-group">
            <label for="bio" class="form-label">Bio</label>
            <textarea
                id="bio"
                class="form-textarea"
                bind:value={formData.bio}
                placeholder="Tell us about your sovereign journey..."
                rows="3"
                maxlength="200"
            ></textarea>
            <span class="char-count">{formData.bio.length}/200</span>
        </div>

        <!-- Interests -->
        <div class="form-group">
            <span class="form-label" id="interests-label">Interests</span>
            <div
                class="interests-grid"
                role="group"
                aria-labelledby="interests-label"
            >
                {#each INTEREST_OPTIONS as interest}
                    <button
                        type="button"
                        class="interest-tag"
                        class:selected={formData.interests.includes(interest)}
                        onclick={() => toggleInterest(interest)}
                    >
                        {interest}
                    </button>
                {/each}
            </div>
        </div>

        <!-- Form actions -->
        <div class="form-actions">
            <button
                type="button"
                class="back-button"
                onclick={() => onback && onback()}
            >
                ← Back
            </button>
            <button type="submit" class="next-button"> Continue → </button>
        </div>
    </form>
</div>

<style>
    .identity-step {
        width: 100%;
        animation: fadeIn 0.5s;
        color: white;
    }

    .step-title {
        text-align: center;
        font-size: 2rem;
        margin: 0 0 0.5rem 0;
        background: linear-gradient(135deg, #9370db, #ff6b6b);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .step-subtitle {
        text-align: center;
        margin: 0 0 2rem 0;
        opacity: 0.7;
    }

    .avatar-section {
        display: flex;
        justify-content: center;
        margin-bottom: 2rem;
    }

    .avatar-container {
        text-align: center;
    }

    .avatar-preview,
    .avatar-placeholder {
        width: 100px;
        height: 100px;
        border-radius: 50%;
        margin-bottom: 1rem;
        border: 3px solid #9370db;
        box-shadow: 0 0 30px rgba(147, 112, 219, 0.3);
    }

    .avatar-preview {
        object-fit: cover;
    }

    .avatar-placeholder {
        background: linear-gradient(135deg, #9370db, #ff6b6b);
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .placeholder-icon {
        font-size: 3rem;
    }

    .avatar-actions {
        display: flex;
        gap: 1rem;
        justify-content: center;
    }

    .avatar-upload,
    .avatar-generate {
        padding: 0.5rem 1rem;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 2rem;
        color: white;
        cursor: pointer;
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        transition: all 0.2s;
    }

    .avatar-upload:hover,
    .avatar-generate:hover:not(:disabled) {
        background: rgba(147, 112, 219, 0.2);
        border-color: #9370db;
    }

    .avatar-generate:disabled {
        opacity: 0.5;
        cursor: not-allowed;
    }

    .form-group {
        margin-bottom: 1.5rem;
        position: relative;
    }

    .form-label {
        display: block;
        margin-bottom: 0.5rem;
        font-size: 0.9rem;
        opacity: 0.8;
    }

    .required {
        color: #ff6b6b;
    }

    .form-input,
    .form-textarea {
        box-sizing: border-box;
        width: 100%;
        padding: 0.75rem;
        background: rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 0.5rem;
        color: white;
        font-family: inherit;
        transition: all 0.2s;
    }

    .form-input:focus,
    .form-textarea:focus {
        outline: none;
        border-color: #9370db;
        box-shadow: 0 0 20px rgba(147, 112, 219, 0.2);
    }

    .form-input.error {
        border-color: #ff6b6b;
    }

    .handle-input-wrapper {
        display: flex;
        align-items: center;
    }

    .handle-prefix {
        padding: 0.75rem;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-right: none;
        border-radius: 0.5rem 0 0 0.5rem;
        opacity: 0.7;
    }

    .handle-input {
        border-radius: 0 0.5rem 0.5rem 0;
    }

    .error-message {
        position: absolute;
        bottom: -1.5rem;
        left: 0;
        color: #ff6b6b;
        font-size: 0.8rem;
    }

    .char-count {
        position: absolute;
        bottom: -1.5rem;
        right: 0;
        font-size: 0.8rem;
        opacity: 0.5;
    }

    .interests-grid {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
    }

    .interest-tag {
        padding: 0.5rem 1rem;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 2rem;
        color: white;
        cursor: pointer;
        transition: all 0.2s;
    }

    .interest-tag:hover {
        background: rgba(147, 112, 219, 0.2);
        border-color: #9370db;
    }

    .interest-tag.selected {
        background: #9370db;
        border-color: #9370db;
    }

    .form-actions {
        display: flex;
        gap: 1rem;
        margin-top: 2rem;
    }

    .back-button,
    .next-button {
        flex: 1;
        padding: 1rem;
        border: none;
        border-radius: 0.5rem;
        font-size: 1rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.2s;
    }

    .back-button {
        background: rgba(255, 255, 255, 0.05);
        color: white;
    }

    .back-button:hover {
        background: rgba(255, 255, 255, 0.1);
    }

    .next-button {
        background: linear-gradient(135deg, #9370db, #ff6b6b);
        color: white;
    }

    .next-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 20px rgba(147, 112, 219, 0.4);
    }
</style>
