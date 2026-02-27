export class DifferentialPrivacy {
    private readonly EPSILON: number; // Privacy budget (lower is more private)
    private readonly DELTA: number;   // Failure probability (typically 1e-5 to 1e-9)

    constructor(epsilon: number = 0.1, delta: number = 1e-5) {
        this.EPSILON = epsilon;
        this.DELTA = delta;
    }

    /**
     * Laplace mechanism for numeric queries.
     * Adds noise to a numeric value based on its sensitivity.
     * 
     * @param value - The true value
     * @param sensitivity - The maximum amount any single user's data could change the value
     * @returns The value with Laplace noise added
     */
    laplaceMechanism(value: number, sensitivity: number): number {
        const scale = sensitivity / this.EPSILON;
        const noise = this.laplaceNoise(scale);
        return value + noise;
    }

    /**
     * Exponential mechanism for categorical queries.
     * Selects an option probabilistically, preferring options with higher scores.
     * 
     * @param options - Array of possible options
     * @param scoreFunction - Function that assigns a utility score to each option
     * @param maxScore - Maximum possible score difference caused by one user
     * @returns A selected option
     */
    exponentialMechanism<T>(
        options: T[],
        scoreFunction: (t: T) => number,
        maxScore: number
    ): T {
        if (options.length === 0) throw new Error("Options array cannot be empty.");

        const scores = options.map(scoreFunction);
        const probabilities = scores.map(s =>
            Math.exp((this.EPSILON * s) / (2 * maxScore))
        );

        const total = probabilities.reduce((a, b) => a + b, 0);
        const normalized = probabilities.map(p => p / total);

        return this.weightedRandom(options, normalized);
    }

    /**
     * Calculates the privacy cost of running multiple queries.
     * Uses the advanced composition theorem.
     * 
     * @param queries - Number of queries executed
     * @returns Total epsilon cost
     */
    compose(queries: number): number {
        return Math.sqrt(2 * queries * Math.log(1 / this.DELTA)) * this.EPSILON
            + queries * this.EPSILON * (Math.exp(this.EPSILON) - 1);
    }

    /**
     * Generates random noise following a Laplace distribution.
     * 
     * @param scale - The scale parameter (b) of the distribution
     * @returns A random number from the Laplace distribution
     */
    private laplaceNoise(scale: number): number {
        const u = Math.random() - 0.5;
        // Avoid domain errors for Math.log
        if (u === -0.5) return -Math.log(1) / scale; // effectively zero-ish context
        return -Math.sign(u) * Math.log(1 - 2 * Math.abs(u)) * scale;
    }

    /**
     * Selects an item from an array based on weighted probabilities.
     * 
     * @param items - Array of items to select from
     * @param weights - Array of probabilities adding up to 1
     * @returns The chosen item
     */
    private weightedRandom<T>(items: T[], weights: number[]): T {
        let r = Math.random();
        for (let i = 0; i < items.length; i++) {
            const weight = weights[i] ?? 0;
            if (r < weight) {
                return items[i] as T;
            }
            r -= weight;
        }
        return items[items.length - 1] as T;
    }
}
