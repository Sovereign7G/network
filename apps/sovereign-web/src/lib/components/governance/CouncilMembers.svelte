<script lang="ts">
    export let members = [];
</script>

<div class="council-members">
    {#each members as member}
        <div class="member-card">
            <div class="member-avatar">
                {#if member.avatar}
                    <img src={member.avatar} alt={member.name} />
                {:else}
                    <span class="avatar-placeholder">
                        {member.name
                            .split(" ")
                            .map((n) => n[0])
                            .join("")}
                    </span>
                {/if}
            </div>

            <div class="member-info">
                <div class="member-header">
                    <span class="member-name">{member.name}</span>
                    <span class="member-role">{member.role}</span>
                </div>

                <div class="member-stats">
                    <div class="stat">
                        <span class="stat-label">Voting Power</span>
                        <span class="stat-value">{member.votingPower}</span>
                    </div>
                    <div class="stat">
                        <span class="stat-label">Proposals</span>
                        <span class="stat-value">{member.proposalsCreated}</span
                        >
                    </div>
                    <div class="stat">
                        <span class="stat-label">Participation</span>
                        <span class="stat-value"
                            >{member.participationRate}%</span
                        >
                    </div>
                </div>
            </div>
        </div>
    {/each}
</div>

<style>
    .council-members {
        display: flex;
        flex-direction: column;
        gap: 0.75rem;
    }

    .member-card {
        display: flex;
        align-items: center;
        gap: 1rem;
        padding: 0.75rem;
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 0.75rem;
        transition: all 0.2s;
    }

    .member-card:hover {
        background: rgba(147, 112, 219, 0.05);
        border-color: #9370db;
    }

    .member-avatar {
        width: 3rem;
        height: 3rem;
        border-radius: 50%;
        overflow: hidden;
        background: linear-gradient(135deg, #9370db, #ff6b6b);
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
    }

    .avatar-placeholder {
        color: white;
        font-weight: 600;
        font-size: 0.9rem;
    }

    .member-avatar img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }

    .member-info {
        flex: 1;
    }

    .member-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.5rem;
    }

    .member-name {
        font-weight: 600;
        font-size: 0.9rem;
    }

    .member-role {
        font-size: 0.7rem;
        padding: 0.2rem 0.5rem;
        background: rgba(147, 112, 219, 0.2);
        border-radius: 1rem;
        color: #9370db;
    }

    .member-stats {
        display: flex;
        gap: 1rem;
        font-size: 0.8rem;
    }

    .stat {
        display: flex;
        align-items: center;
        gap: 0.25rem;
    }

    .stat-label {
        opacity: 0.5;
    }

    .stat-value {
        color: #9370db;
        font-weight: 600;
    }
</style>
