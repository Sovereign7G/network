import { browser } from "$app/environment";
            // @ts-ignore
import type { Suggestion, SuggestionType } from "$lib/types";

const STORAGE_KEY = "davinci-learning-profile";

interface UserJourney {
    joinedAt: number;
    transactionCount: number;
    voteCount: number;
    zkCount: number;
    milestones: string[];
}

interface UserPreferences {
    typeScores: Record<string, number>; // SuggestionType -> score (0-1)
    activeHours: Record<number, number>; // 0-23 -> activity weight (0-1)
    dismissedTopics: string[];
}

interface UserProfile {
    journey: UserJourney;
    preferences: UserPreferences;
    lastInteractionAt: number;
}

type InteractionAction = "seen" | "acted" | "dismissed" | "ignored";

interface UserInteraction {
    suggestionId: string;
    type: SuggestionType;
    action: InteractionAction;
    timestamp: number;
    source: string;
}

class LearningEngine {
    #profile = $state<UserProfile>({
        journey: {
            joinedAt: Date.now(),
            transactionCount: 0,
            voteCount: 0,
            zkCount: 0,
            milestones: []
        },
        preferences: {
            typeScores: {},
            activeHours: {},
            dismissedTopics: []
        },
        lastInteractionAt: Date.now()
    });

    constructor() {
        if (browser) {
            this.load();
        }
    }

    get profile() {
        return this.#profile;
    }

    private load() {
        const saved = localStorage.getItem(STORAGE_KEY);
        if (saved) {
            try {
                const data = JSON.parse(saved);
                this.#profile = { ...this.#profile, ...data };
            } catch (e) {
                console.error("Failed to load learning profile", e);
            }
        }
    }

    private save() {
        if (browser) {
            localStorage.setItem(STORAGE_KEY, JSON.stringify(this.#profile));
        }
    }

    trackInteraction(interaction: UserInteraction) {
        const { type, action, timestamp } = interaction;
        this.#profile.lastInteractionAt = timestamp;

        // 1. Update Type Preferences
        const currentScore = this.#profile.preferences.typeScores[type] ?? 0.5;
        let newScore = currentScore;

        switch (action) {
            case "acted":
                newScore += 0.2;
                break;
            case "dismissed":
                newScore -= 0.15;
                break;
            case "ignored":
                newScore -= 0.05;
                break;
            case "seen":
                // seen alone doesn't change score much unless ignored later
                break;
        }

        this.#profile.preferences.typeScores[type] = Math.max(0, Math.min(1, newScore));

        // Auto-archiving topics with very low scores
        if (newScore < 0.2 && !this.#profile.preferences.dismissedTopics.includes(type)) {
            this.#profile.preferences.dismissedTopics.push(type);
        } else if (newScore >= 0.2) {
            this.#profile.preferences.dismissedTopics = this.#profile.preferences.dismissedTopics.filter(t => t !== type);
        }

        // 2. Update Temporal Patterns
        const hour = new Date(timestamp).getHours();
        const currentHourWeight = this.#profile.preferences.activeHours[hour] ?? 0.1;
        let hourWeightDelta = 0;

        if (action === "acted") hourWeightDelta = 0.3;
        if (action === "seen") hourWeightDelta = 0.05;
        if (action === "dismissed") hourWeightDelta = -0.1;

        this.#profile.preferences.activeHours[hour] = Math.max(0, Math.min(1, currentHourWeight + hourWeightDelta));

        this.save();
    }

    // Helper for journey updates
    recordMilestone(milestoneId: string) {
        if (!this.#profile.journey.milestones.includes(milestoneId)) {
            this.#profile.journey.milestones.push(milestoneId);
            this.save();
        }
    }

    incrementActivity(type: "transaction" | "vote" | "zk") {
        if (type === "transaction") this.#profile.journey.transactionCount++;
        if (type === "vote") this.#profile.journey.voteCount++;
        if (type === "zk") this.#profile.journey.zkCount++;
        this.save();
    }

    get journeyStage(): "onboarding" | "explorer" | "active" | "power" | "sovereign" {
        const { transactionCount, voteCount, joinedAt } = this.#profile.journey;
        const daysActive = (Date.now() - joinedAt) / (1000 * 60 * 60 * 24);

        if (daysActive < 1) return "onboarding";
        if (transactionCount < 5) return "explorer";
        if (transactionCount < 20) return "active";
        if (voteCount < 1) return "power";
        return "sovereign";
    }

    shouldShowNow(): boolean {
        const hour = new Date().getHours();
        const hourWeight = this.#profile.preferences.activeHours[hour] ?? 0.5;
        // If we have some data about this hour, check if it's better than 0.3
        // For new users, it defaults to true
        return hourWeight > 0.2;
    }

    personalize(suggestions: Suggestion[]): Suggestion[] {
        return suggestions
            // @ts-ignore
            .filter(s => !this.#profile.preferences.dismissedTopics.includes(s.type))
            .map(s => {
                const pScore = this.calculatePersonalizedPriority(s);
                return { ...s, priority: pScore };
            })
            .sort((a, b) => b.priority - a.priority);
    }

    private calculatePersonalizedPriority(suggestion: Suggestion): number {
        let priority = suggestion.priority;

        // Boost based on type preference
        const typeScore = this.#profile.preferences.typeScores[suggestion.type] ?? 0.5;
            // @ts-ignore
        priority += (typeScore - 0.5) * 4; // Shift range [-2, +2]

        // Boost based on temporal relevance
        const hour = new Date().getHours();
        const hourWeight = this.#profile.preferences.activeHours[hour] ?? 0.1;
        priority += (hourWeight * 2); // Boost up to +2

        return Math.max(1, Math.min(10, priority));
    }

    reset() {
        this.#profile = {
            journey: {
                joinedAt: Date.now(),
                transactionCount: 0,
                voteCount: 0,
                zkCount: 0,
                milestones: []
            },
            preferences: {
                typeScores: {},
                activeHours: {},
                dismissedTopics: []
            },
            lastInteractionAt: Date.now()
        };
        this.save();
    }
}

export const learningEngine = new LearningEngine();
