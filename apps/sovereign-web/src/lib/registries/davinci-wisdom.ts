interface DaVinciQuote {
    text: string;
    context?: string;
}

interface DaVinciLesson {
    title: string;
    description: string;
    principle: string;
}

interface DecodedFragment {
    text: string;
    source: string;
    focus: string;
}

            // @ts-ignore
const DAVINCI_QUOTES: DaVinciQuote[] = [
    { text: "Learning never exhausts the mind." },
    { text: "Simplicity is the ultimate sophistication." },
    { text: "Knowing is not enough; we must apply. Being willing is not enough; we must do." },
    { text: "Art is never finished, only abandoned." },
    { text: "The greatest deception men suffer is from their own opinions." },
    { text: "Once you have tasted flight, you will forever walk the earth with your eyes turned skyward." },
    { text: "The noblest pleasure is the joy of understanding." },
    { text: "Iron rusts from disuse; inaction saps the vigour of the mind." },
    { text: "Study without desire spoils the memory, and it retains nothing that it takes in." },
    { text: "There are three classes of people: those who see, those who see when they are shown, and those who do not see." },
    { text: "People of accomplishment rarely sat back and let things happen to them. They went out and happened to things." }
];

export const DAVINCI_LESSONS: DaVinciLesson[] = [
    {
        title: "Relentless Curiosity",
        principle: "Curiosità",
        description: "An insatiably curious approach to life and an unrelenting quest for continuous learning."
    },
    {
        title: "Experimental Knowledge",
        principle: "Dimostrazione",
        description: "A commitment to test knowledge through experience, persistence, and a willingness to learn from mistakes."
    },
    {
        title: "Sensory Refinement",
        principle: "Sensazione",
        description: "The continual refinement of the senses, especially sight, as the means to enliven experience."
    },
    {
        title: "Embracing Ambiguity",
        principle: "Sfumato",
        description: "A willingness to embrace ambiguity, paradox, and uncertainty."
    },
    {
        title: "Whole-Brain Thinking",
        principle: "Arte/Scienza",
        description: "The development of the balance between science and art, logic and imagination."
    },
    {
        title: "Bodily Grace",
        principle: "Corporalità",
        description: "The cultivation of grace, ambidexterity, fitness, and poise."
    },
    {
        title: "Systemic Interconnection",
        principle: "Connessione",
        description: "A recognition and appreciation for the connectedness of all things and phenomena."
    }
];

export const DECODED_FRAGMENTS: DecodedFragment[] = [
    { text: "What is seen is not what is true.", source: "Spectral Analysis", focus: "Perception" },
    { text: "The hands speak louder than the mouths of men.", source: "Manual Decryption", focus: "Action" },
    { text: "The truth will rise when reason replaces faith.", source: "Causal Trace", focus: "Epistemology" },
    { text: "All faith fades when light reveals the hand of man.", source: "Photonic Audit", focus: "Transparency" },
    { text: "He who eats with truth will not betray himself.", source: "Manifold Synchrony", focus: "Integrity" },
    { text: "Strength without understanding is blind.", source: "Peter's Pillar", focus: "Knowledge" },
    { text: "To question is not sin, but the path to clarity.", source: "Thomas's Vector", focus: "Inquiry" },
    { text: "Those who hold power will bury truth beneath stone until the eyes of the future uncover it.", source: "Historical Audit", focus: "Power" },
    { text: "Truth belongs not to saints, but to those who seek it in silence.", source: "Jesus's Robe", focus: "Solitude" },
    { text: "Faith without reason is the sleep of truth, and those who wake shall see what was forbidden.", source: "Overarching Decrypt", focus: "Awakening" }
];

const CONTAINMENT_AXIOMS = [
            // @ts-ignore
    {
        title: "Aetherial Logic",
        tech: "WebAssembly",
        metaphor: "The Spark of Thought",
        description: "Lightweight, ephemeral, and sandboxed execution that transcends the earthly machine."
    },
    {
        title: "Institutional Vessel",
        tech: "Docker",
        metaphor: "The Stone Cathedral",
        description: "A robust, multi-layered environment providing structural integrity and earthly scale."
    },
    {
        title: "Better Together",
        tech: "Heterogeneous Harmony",
        metaphor: "The Masterpiece",
        description: "The seamless integration of ephemeral logic and robust structure to create sovereign manifestations."
    }
];

export const CONTEXT_ENGINEERING_AXIOMS = [
    {
        step: "PRD Extraction",
        title: "Feature Sovereignty",
        description: "Extracting complete functional requirements before a single line of code is manifested."
    },
    {
        step: "Design Substrate",
        title: "Structural Aesthetic",
        description: "Establishing a cohesive system of colors, typography, and spacing tokens (Style Guide)."
    },
    {
        step: "State Manifold",
        title: "Total Presence",
        description: "Explicitly defining the 4 Pillars of Presence: Empty, Loading, Data, and Error."
    },
    {
        step: "Contextual Refinement",
        title: "Clean Futurism",
        description: "Iterating through the Antigravity lens to achieve high-fidelity, high-converting sovereign interfaces."
    }
];

export const TYPOGRAPHIC_HARMONY_AXIOMS = [
    {
        title: "Frictionless Logic",
        concept: "Invisible Engineering",
        description: "A design only succeeds when it removes the friction between the message and the mind. If the viewer notices the mechanism, the flow has failed."
    },
    {
        title: "Causal Kerning",
        concept: "Precise Proportions",
        description: "The meticulous adjustment of space between individual elements to achieve a visceral feeling of 'Rightness'."
    },
    {
        title: "Optical Symmetry",
        concept: "Intentional Asymmetry",
        description: "Crafting a system that is mathematically imperfect to ensure it is transitionally perfect to the human eye."
    },
    {
        title: "Aesthetic Performance",
        concept: "Functional Beauty",
        description: "Aesthetics are not an garnish; they are the exhaust of a machine performing at peak efficiency."
    }
];

export const SOVEREIGN_ECOSYSTEM_AXIOMS = [
    {
        title: "The Fortress Paradigm",
        concept: "Governed Sovereignty",
        description: "Moving from a 'Wilderness' of unoptimized logic to a 'Fortress' of governed stability. Peace of mind is the ultimate user sovereignty."
    },
    {
        title: "Convergence Mastery",
        concept: "Dynamic Scaling",
        description: "A sovereign interface must be scale-agnostic, transitioning seamlessly between mobile touch and desktop-scale workstations."
    },
    {
        title: "Aetherial Transparency",
        concept: "Visual Auditing",
        description: "As systems become 'Fortresses,' they must provide high-fidelity visual audits to maintain the user's trust and authority."
    },
    {
        title: "Institutional Decoupling",
        concept: "De-Googling logic",
        description: "Eliminating mandatory corporate telemetry to ensure that the device remains a tool for the individual, not a vessel for the institution."
    }
];

export const NESTED_BOX_AXIOMS = [
    {
        title: "Hierarchical Decomposition",
        concept: "The Nested Box",
        description: "Every complex UI manifested in the manifold is merely a series of nested boxes. Mastery over the container is mastery over the vision."
    },
    {
        title: "Structural Sovereignty",
        concept: "Grid-First Logic",
        description: "Favor rigid Grids for expanding structural truth, and sequential Stacks for ephemeral flows. Never let the layout 'vibe' its way into existence."
    },
    {
        title: "Visual Blueprinting",
        concept: "The Color-Coded Protocol",
        description: "Before manifesting code, audit the hierarchy using the sacred colors: Red (Root), Green (Secondary), Blue (Primary Content), and Yellow (Inner Flow)."
    },
    {
        title: "Contextual Intelligence",
        concept: "Substrate Awareness",
        description: "Logic execution and AI orchestration are exponentially more powerful when grounded in an existing Design Substrate."
    }
];

export const REDIS_SOVEREIGNTY_AXIOMS = [
    {
        title: "Single-Threaded Governance",
        concept: "Atomic Manifest",
        description: "Processing commands in a strict, sequential order removes the friction of concurrency. Simplicity is the ultimate fortification."
    },
    {
        title: "In-Memory Sovereignty",
        concept: "The Speed of Thought",
        description: "By living entirely within the ephemeral memory of the machine, logic transcends the latency of the earthly disk."
    },
    {
        title: "Structured Efficiency",
        concept: "Logic-in-Place",
        description: "The system should not merely store data, but provide complex structures (Sets, Streams, Hashes) for efficient, in-situ logic execution."
    },
    {
        title: "Durability Trade-off",
        concept: "Ephemeral Focus",
        description: "Acknowledging that for peak performance, one must often choose between the speed of the spark and the permanence of the stone."
    }
];

export const DESIGN_ENGINEERING_AXIOMS = [
    {
        title: "The Taste Multiplier",
        concept: "Sovereign Discernment",
        description: "Taste is the ability to recognize what is 'right'. It is not innate, but forged through obsessive study and the act of building."
    },
    {
        title: "Closing the Quality Gap",
        concept: "Handoff Elimination",
        description: "Institutional quality dies in the handoff. Design Engineering ensures that the masterpiece survives the transition from vision to manifest code."
    },
    {
        title: "Human-Centric Performance",
        concept: "Visceral Polish",
        description: "Interfaces must not only be functional, but feel fast, human, and polished—moving beyond utility into a 'State of Grace'."
    },
    {
        title: "The Anti-Slop Directive",
        concept: "Intentionality Audit",
        description: "Upholding human oversight to prevent the manifestation of 'AI slop', ensuring every pixel reflects sovereign intent."
    }
];

export const VINTAGE_SOVEREIGNTY_AXIOMS = [
    {
        title: "Individual Sovereignty",
        concept: "The Cohesive Vision",
        description: "A product led by a single human mind possesses a 'soul' that committee-driven design cannot replicate. Defend the quirks of the individual."
    },
    {
        title: "The Patina Principle",
        concept: "Graceful Aging",
        description: "Materials and logic should be designed to grow more beautiful with wear, developing a patina of usage rather than merely becoming obsolete."
    },
    {
        title: "Intentional Idiosyncrasy",
        concept: "Human Slop",
        description: "Embrace the 'unnecessary' detail and the slightly 'odd' proportion. We gravitate towards these because they provide visceral proof of human labor."
    },
    {
        title: "Aesthetic Boldness",
        concept: "Chromatic Optimism",
        description: "Reject the sterility of neutrals. Use bold, expressive colors to signal that the manifest environment is alive and optimistic."
    }
];

export const ANIMATION_KINETIC_AXIOMS = [
    {
        title: "Kinetic Orchestration",
        concept: "@keyframes Sequencing",
        description: "Motion is not a byproduct; it is a manifest state. Use CSS keyframes to orchestrate complex, multi-stage sequences that breathe life into the substrate."
    },
    {
        title: "Compositor Sovereignty",
        concept: "Performance-First Motion",
        description: "Protect the main thread. Offload complex UI transitions to the compositor layer through native CSS animations to ensure zero-friction interaction."
    },
    {
        title: "The Velocity Curve",
        concept: "Intentional Easing",
        description: "Fluidity is forged in the curve. Mastering the timing function is essential for achieving a 'State of Grace' in transition logic."
    },
    {
        title: "Infinite Loop Manifest",
        concept: "Persistence of Motion",
        description: "For artifacts that reflect eternal logic, use infinite iteration counts to create a tireless, pulsing presence within the manifold."
    }
];

export const LOCAL_SOVEREIGNTY_AXIOMS = [
    {
        title: "Local-First Residency",
        concept: "Physical Sovereignty",
        description: "Your data is an extension of your mind; it must reside on your physical machine by default, immune to the fragility of the cloud."
    },
    {
        title: "Conflict-Free Integrity",
        concept: "CRDT Sync Protocol",
        description: "Consistency is achieved through mathematical certainty, not central authority. Replicas merge without the friction of data loss."
    },
    {
        title: "Networked Thought",
        concept: "Hierarchical Obsolescence",
        description: "The folder is a prison. Information manifests through bidirectional links and context-aware mentions, creating a living graph of logic."
    },
    {
        title: "Digital Bunker Protocol",
        concept: "Self-Hosted Persistence",
        description: "Sovereignty is the ability to operate in isolation. Support for Docker and open formats ensures your manifest survives the vendor's death."
    }
];
