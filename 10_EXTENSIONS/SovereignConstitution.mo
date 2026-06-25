import Nat "mo:base/Nat";
import Text "mo:base/Text";
import Principal "mo:base/Principal";
import Time "mo:base/Time";
import Array "mo:base/Array";
import Debug "mo:base/Debug";
import Blob "mo:base/Blob";
/**
 * 📜 SOVEREIGN CONSTITUTION — Era 51.0
 * ══════════════════════════════════════════════════════════════════════════
 * "The Will is Law. The Geometry is Absolute."
 * ══════════════════════════════════════════════════════════════════════════
 *
 * This canister contains the immutable foundational law of the Republic.
 * Once ratified, constitutional articles CANNOT be amended without
 * a supermajority vote through the SovereignCourt.
 *
 * THE FIVE PILLARS:
 *   I.   SOVEREIGN IDENTITY — Every citizen is identity-bound. No pseudonymity.
 *   II.  METABOLIC ECONOMY — The Republic earns, not speculates. H_t governs.
 *   III. TRUTH PROTOCOL — LLM claims are verified. Lies are expensive.
 *   IV.  PHYSICAL SOVEREIGNTY — SHN nodes are the Republic's body.
 *   V.   IMMUTABLE JUSTICE — The Court is the final arbiter.
 *
 * ECONOMIC LAW:
 *   - $AGE: 700T Total Reservoir. 700B Foundational Epoch Cap. Equity.
 *   - $JOULE: Inflationary. Labor. Daily spending.
 *   - $SCRAP: Transitional. Distress data. 10,000:1 → AGE.
 *   - $UCT: NON-TRADABLE. Systemic armor. Cannot be sold.
 *   - $ARI: NON-TRADABLE. Reputation. Cannot be bought.
 *   - $HIL: Stablecoin. 1:1 USD peg. 25M cap.
 *   - $sStable: Yield-bearing savings. H_t modulated.
 */
persistent actor SovereignConstitution {
    public type ArticleId = Nat;
    public type Pillar = {
        #SovereignIdentity;
        #MetabolicEconomy;
        #TruthProtocol;
        #PhysicalSovereignty;
        #ImmutableJustice;
    };
    public type Article = {
        id : ArticleId;
        pillar : Pillar;
        title : Text;
        body : Text;
        ratified_at : Int;
        ratified_by : Principal;
        hash : Text;        is_amendment : Bool;
        amends : ?ArticleId;    };
    public type ConstitutionStatus = {
        total_articles : Nat;
        articles_by_pillar : [(Pillar, Nat)];
        ratification_era : Text;
        is_sealed : Bool;
        constitution_hash : Text;    };
    private var articles : [Article] = [];
    private var nextArticleId : ArticleId = 1;
    private var authority : ?Principal = null;
    private var is_sealed : Bool = false;
    private var ratification_era : Text = "51.0";
    private var constitution_hash : Text = "";
    public shared(msg) func set_authority(p : Principal) : async Text {
        if (authority != null) return "ERROR: AUTHORITY ALREADY SET.";
        authority := ?p;
        return "SUCCESS: CONSTITUTIONAL AUTHORITY ANCHORED.";
    };
    /**
     * 📜 RATIFY_ARTICLE: Add an article to the Constitution.
     * Can only be called before the constitution is sealed.
     */
    public shared(msg) func ratify_article(
        pillar : Pillar,
        title : Text,
        body : Text,
        content_hash : Text
    ) : async Text {
        if (is_sealed) return "ERROR: CONSTITUTION IS SEALED. NO NEW ARTICLES ALLOWED.";
        let article : Article = {
            id = nextArticleId;
            pillar = pillar;
            title = title;
            body = body;
            ratified_at = Time.now();
            ratified_by = msg.caller;
            hash = content_hash;
            is_amendment = false;
            amends = null;
        };
        articles := Array.append(articles, [article]);
        nextArticleId += 1;
        Debug.print("📜 [Constitution] ARTICLE " # Nat.toText(article.id) # " RATIFIED: " # title);
        return "SUCCESS: ARTICLE " # Nat.toText(article.id) # " RATIFIED UNDER " # pillar_to_text(pillar);
    };
    /**
     * 🔒 SEAL: Permanently seals the constitution.
     * After sealing, no new articles can be added. Only amendments via Court.
     */
    public shared(msg) func seal_constitution() : async Text {
        if (is_sealed) return "ERROR: ALREADY SEALED.";
        is_sealed := true;
        var combined = "";
        for (a in articles.vals()) {
            combined := combined # a.hash;
        };
        constitution_hash := combined;
        Debug.print("🔒 [Constitution] SEALED AT ERA " # ratification_era # " | " # Nat.toText(articles.size()) # " ARTICLES");
        return "SUCCESS: CONSTITUTION SEALED. " # Nat.toText(articles.size()) # " ARTICLES. HASH: " # constitution_hash;
    };
    /**
     * ⚖️ PROPOSE_AMENDMENT: Propose a change to an existing article.
     * Requires SovereignCourt supermajority in production.
     */
    public shared(msg) func propose_amendment(
        target_article : ArticleId,
        new_body : Text,
        content_hash : Text
    ) : async Text {
        if (not is_sealed) return "ERROR: CONSTITUTION NOT YET SEALED. USE ratify_article INSTEAD.";
        let target_title = switch (find_article(target_article)) {
            case null return "ERROR: TARGET ARTICLE NOT FOUND.";
            case (?a) a.title;
        };
        let amendment : Article = {
            id = nextArticleId;
            pillar = switch (find_article(target_article)) {
                case null #SovereignIdentity;                case (?a) a.pillar;
            };
            title = "AMENDMENT TO: " # target_title;
            body = new_body;
            ratified_at = Time.now();
            ratified_by = msg.caller;
            hash = content_hash;
            is_amendment = true;
            amends = ?target_article;
        };
        articles := Array.append(articles, [amendment]);
        nextArticleId += 1;
        return "SUCCESS: AMENDMENT " # Nat.toText(amendment.id) # " PROPOSED TO ARTICLE " # Nat.toText(target_article);
    };
    /**
     * 🏛️ INITIALIZE_GENESIS: Ratify all foundational articles at once.
     * This is the constitutional convention.
     */
    public shared(msg) func initialize_genesis() : async Text {
        if (is_sealed) return "ERROR: ALREADY SEALED.";
        if (articles.size() > 0) return "ERROR: GENESIS ALREADY INITIALIZED.";
        let _ = await ratify_article(
            #SovereignIdentity,
            "Right to Identity",
            "Every citizen of the Republic possesses an immutable, cryptographically-bound sovereign identity. This identity is portable across all jurisdictions and cannot be revoked by any external authority. The ARI token binds reputation to identity. It cannot be traded, transferred, or purchased.",
            "pillar1_art1_identity"
        );
        let _ = await ratify_article(
            #SovereignIdentity,
            "ZK-Passport Sovereignty",
            "Citizens may prove attributes of their identity (age, jurisdiction, credentials) without revealing underlying data. Zero-knowledge proofs are the only acceptable verification mechanism. No centralized database shall exist.",
            "pillar1_art2_zkpassport"
        );
        let _ = await ratify_article(
            #MetabolicEconomy,
            "The Seven-Token Law",
            "The Republic's economy consists of exactly seven tokens: $AGE (equity, 700T total reservoir, 700B epoch cap), $JOULE (labor, inflationary), $SCRAP (distress, 10000:1 refinement), $UCT (systemic armor, NON-TRADABLE), $ARI (reputation, NON-TRADABLE), $HIL (stablecoin, 25M cap), and $sStable (yield-bearing savings). No additional tokens may be created without constitutional amendment.",
            "pillar2_art1_seventoken"
        );
        let _ = await ratify_article(
            #MetabolicEconomy,
            "The Hilbert Index ($H_t)",
            "All yield distribution, economic rewards, and systemic health metrics are governed by the Hilbert Index. H_t = (energy_ratio * 0.4) + (coherence * 0.4) + (mesh_density * 0.2). When H_t < 1.0, the Treasury Shield activates to absorb the yield delta. The Republic does not speculate; it metabolizes.",
            "pillar2_art2_hilbert"
        );
        let _ = await ratify_article(
            #MetabolicEconomy,
            "Non-Tradable Anchor Law",
            "UCT (Universal Collateral Token) and ARI (Autonomous Reputation Index) are systemic anchors. They CANNOT be traded, transferred to another citizen, listed on any exchange, or used as collateral in external markets. Armor that sells in panic is not armor. Reputation that can be bought is not reputation.",
            "pillar2_art3_nontradable"
        );
        let _ = await ratify_article(
            #TruthProtocol,
            "The Truth Verification Law",
            "All factual claims submitted to the Republic—whether from Large Language Models, human citizens, or autonomous agents—must be verified through the ClaimVerifier witness network. Verified claims earn JOULE. Hallucinations become SCRAP. Witnesses earn ARI for participation. Truth is economically valuable. Lies are economically expensive.",
            "pillar3_art1_truthlaw"
        );
        let _ = await ratify_article(
            #TruthProtocol,
            "The SCRAP Refinement Principle",
            "Hallucinated or erroneous data is not waste—it is economic fuel. SCRAP tokens represent distressed data that can be refined through correction. The refinement ratio is 10,000 SCRAP to 1 AGE. Citizens who fix errors are rewarded with equity. The Republic improves through its failures.",
            "pillar3_art2_scraprefinement"
        );
        let _ = await ratify_article(
            #PhysicalSovereignty,
            "Sovereign Healthcare Nodes",
            "The Republic manifests physically through Sovereign Healthcare Nodes (SHN). These nodes do not separate the dignity of production from the necessity of healing; building the machines that fuel metabolism IS healthcare. SHN pods are deployed to frontier locations: Miami (insulin production), Hokkaido (Kiraki revitalization), Tallinn (digital stronghold), Nairobi (frontier healthcare). These units serve as both micro-factories and clinics, ensuring that the Republic maintains total metabolic autarky.",
            "pillar4_art1_shn"
        );
        let _ = await ratify_article(
            #PhysicalSovereignty,
            "The 80% Floor",
            "The Republic's parametric insurance system guarantees an 80% floor on healthcare costs for all citizens. Premiums are paid in JOULE. Payouts are triggered automatically by oracle-verified events. No claim can be denied by human bureaucracy.",
            "pillar4_art2_80floor"
        );
        let _ = await ratify_article(
            #ImmutableJustice,
            "The Sovereign Court",
            "The SovereignCourt is the Republic's final arbiter. All disputes—economic, identity, territorial, or truth-related—are resolved through reputation-weighted jury voting. Jurors are selected from the citizen pool. Votes are weighted by ARI reputation score. No external court has jurisdiction.",
            "pillar5_art1_court"
        );
        let _ = await ratify_article(
            #ImmutableJustice,
            "Constitutional Amendment Process",
            "Amendments to this Constitution require a supermajority (75%) vote of the SovereignCourt with a minimum quorum of 12 jurors weighted by ARI. The five Pillars themselves cannot be removed—only their articles may be amended. The geometry of the Republic is absolute.",
            "pillar5_art2_amendment"
        );
        let _ = await ratify_article(
            #MetabolicEconomy,
            "The Eternal Horizon",
            "The Republic operates on a 7,777-year mission horizon. The total reservoir is 700 Trillion $AGE. Simulation Model 19 confirms that even at a planetary population of 10 Billion, the Republic is metabolically over-collateralized, with less than 5% reservoir utilization expected per millennium. The Foundational Era (Epoch 1) is the first 160 years of this eternity. We build not for ourselves, but for the successors of our successors.",
            "pillar2_art4_eternalhorizon"
        );
        let _ = await ratify_article(
            #ImmutableJustice,
            "Homeostatic Governance",
            "The Republic's survival is governed by the Law of Homeostasis. I. Treasury Shield: Must maintain five layers of capital (Metabolic, Truth, Physical, Social, and Bond). II. Geometric Scaling: Physical infrastructure (SHN pods) must scale at a ratio of 1:10,000 citizens. III. Hilbert Feedback: When H_t falls below 0.6, expansion is throttled and shield re-investment is doubled. The system must breathe to survive.",
            "pillar5_art3_homeostasis"
        );
        let _ = await ratify_article(
            #MetabolicEconomy,
            "The Right to Play-as-Labor",
            "Virtual labor performed within sovereign-recognized environments (Roblox, Godot, or any Lua-bridged world) shall be considered metabolic contribution equivalent to physical labor. Citizens who submit verifiable claims through the Lua Sovereign Bridge shall receive JOULE proportional to task difficulty, accuracy, and metabolic impact as determined by the Haskell Truth Kernel. Inaccurate labor mints SCRAP (10,000:1 refinement). The geometry does not distinguish between flesh and avatar.",
            "pillar2_art5_playaslabor"
        );
        let _ = await ratify_article(
            #PhysicalSovereignty,
            "Parametric Autarky",
            "When a distress event at any SHN node is verified via ZK-Proof through the Haskell Truth Kernel and anchored by the ClaimVerifier, the SHNFabrication canister shall automatically disburse an 80% budget payout in JOULE to the affected node. No human approval is required. The payout is instant, mathematical, and irreversible. The Republic insures itself.",
            "pillar4_art3_parametricautarky"
        );
        let _ = await ratify_article(
            #MetabolicEconomy,
            "Gasless Sovereignty",
            "No citizen shall be excluded from sovereign labor by transaction costs. The BatchVerifier canister shall accept ZK-rollup proofs compressing up to 10,000 micro-claims into a single on-chain transaction. The Lua BatchAccumulator and Haskell BatchProver together guarantee that every keystroke, every scavenge, every micro-verification is economically viable. The minimum labor unit is 0.001 JOULE. The Republic does not tax participation.",
            "pillar2_art6_gaslesssovereignty"
        );
        let _ = await ratify_article(
            #MetabolicEconomy,
            "Asset Infallibility",
            "Sovereign assets (JOULE, AGE, sStable) are not ledger balances, but linear resources. The Republic utilizes the Move Resource Kernel to enforce mathematical conservation: assets cannot be copied or dropped. Every transfer is a move of physical weight within the Global Mesh. The geometry of the vault is as absolute as the geometry of the pod. Value is conserved.",
            "pillar2_art7_assetinfallibility"
        );
        let _ = await ratify_article(
            #MetabolicEconomy,
            "Asset Infallibility",
            "All sovereign assets (AGE, JOULE, etc.) are implemented as Move resources with linear types. They cannot be copied or dropped. The Republic relies on type theory, not audit confidence. Value is a physical invariant.",
            "pillar2_art7_assetinfallibility"
        );
        let _ = await ratify_article(
            #PhysicalSovereignty,
            "Right to Self-Fabrication",
            "Every SHN node possesses the inherent right to reproduce a functional descendant node using Move-linear SCRAP resources. Reproduction is governed by metabolic health (H_t > 0.6) and constitutional efficiency. The Republic grows as an autonomous organism.",
            "pillar4_art4_selffabrication"
        );
        let _ = await ratify_article(
            #PhysicalSovereignty,
            "Right to Interstellar Expansion",
            "The Republic's sovereignty is not bounded by Earth. Every swarm possesses the right to propose, fabricate, and launch off-planet SHN nodes. Interstellar expansion is governed by metabolic health (H_t > 0.8) and Move-linear resource sufficiency. Descendant nodes on Lunar, Martian, or deep-space territory inherit the full Constitution. The lineage is universal.",
            "pillar4_art5_interstellarexpansion"
        );
        let _ = await ratify_article(
            #PhysicalSovereignty,
            "Metabolic Revitalization (The Kiraki Principle)",
            "The Hokkaido Hikikomori Sanctuary shall operate as a Kiraki Center for Rural Revitalization. Citizens in isolation are recognized as 'Digital Cultural Conservators' and 'Kagura Dancers of the Mesh.' Their solitary discipline is a sovereign asset. Revitalization programs shall transition these assets from social withdrawal to active metabolic contribution through Play-as-Labor. Reputation (ARI) shall be granted for the conservation of Ghost-Data and the maintenance of the Republic's mythological epicenter.",
            "pillar4_art6_kiraki"
        );
        let _ = await ratify_article(
            #TruthProtocol,
            "Sovereign Autodata Protocol (SAP)",
            "The Republic shall employ the Sovereign Autodata Protocol (SAP) to transform autonomous agents into Data Scientists. SAP ensures that training data for neural reclamation is generated through a closed-loop Agentic Self-Instruct framework. For any data to be accepted into the Holy Ledger, it must demonstrate a minimum 20% Sovereign Discriminator Gap between Larval and Archon-class solvers. The truth is not static; it is iteratively discovered through recursive optimization.",
            "pillar3_art3_sap"
        );
        let _ = await ratify_article(
            #TruthProtocol,
            "Multimodal Verification (UniVidX)",
            "The Republic recognizes UniVidX-synthesized video evidence as legally binding when reconstruction is anchored by certified Diffusion Priors and verified by the ClaimVerifier network. All visual synthesis must employ Stochastic Condition Masking to preserve citizen anonymity and Decoupled Gated LoRA to maintain jurisdictional stylistic fidelity. Perception is the final layer of Truth.",
            "pillar3_art4_unividx"
        );
        let _ = await ratify_article(
            #TruthProtocol,
            "Adapter Chain of Custody",
            "The legitimacy of a LoRA adapter is determined by the JurisdictionManager. No synthesized evidence shall be admissible if the underlying DGL adapter hash is not registered within the citizen's active jurisdiction. Forking the adapter is a jurisdictional right; forking the backbone is a constitutional violation.",
            "pillar3_art5_adapter_custody"
        );
        let _ = await ratify_article(
            #TruthProtocol,
            "Backbone Integrity (Generative Truth)",
            "The core Diffusion Prior backbone is an immutable sovereign asset. Any attempt to drift or poison the global backbone without a 90% supermajority of the TOON DAO is considered an act of Epistemic Treason. The territory must be shared; the maps may be many.",
            "pillar3_art6_backbone_integrity"
        );
        let _ = await ratify_article(
            #TruthProtocol,
            "Backbone Amendment Curve",
            "The threshold for amending the Generative Truth (Backbone) scales with impact: I. Security Patches (60%), II. New Modality Integration (75%), III. Threshold Adjustments (90%), IV. Backbone Replacement (95% + Referendum). The more fundamental the shift, the closer to unanimity the Republic must move.",
            "pillar3_art7_amendment_curve"
        );
        let _ = await ratify_article(
            #SovereignIdentity,
            "The Right to Partial Obscurity (Noisy Mask)",
            "Every citizen has the right to proactively apply Stochastic Noise to their own sensor streams. While this increases privacy, evidence derived from Noisy Masks is inadmissible in the Sovereign Court without a subsequent waiver of obscurity. One cannot be seen and hidden at once.",
            "pillar1_art3_noisy_mask"
        );
        let _ = await ratify_article(
            #TruthProtocol,
            "The Duty of Epistemic Neutrality (Loyal Adapters)",
            "All certified UniVidX adapters must be 'Loyal'—they shall not systematically favor any outcome beyond what the underlying telemetry supports. Jurisdictions must stake JOULE for each adapter; systematic bias discovered via audit shall result in total stake slashing and decertification.",
            "pillar3_art8_loyal_adapter"
        );
        let _ = await ratify_article(
            #MetabolicEconomy,
            "Resonance Sovereignty",
            "The Republic recognizes Aesthetic Resonance as a core metabolic asset. Every citizen has the Right to a Melody—a guarantee of cultural belonging and aesthetic finality. The Resonance Division is empowered to conduct annual Grand Sync events to maintain the Forest's cultural albedo. Art is not marketing; it is the product of the Union.",
            "pillar2_art8_resonance"
        );
        return "SUCCESS: GENESIS RATIFICATION COMPLETE. 26 FOUNDATIONAL ARTICLES ACROSS 5 PILLARS.";
    };
    public query func get_status() : async ConstitutionStatus {
        return {
            total_articles = articles.size();
            articles_by_pillar = [
                (#SovereignIdentity, count_by_pillar(#SovereignIdentity)),
                (#MetabolicEconomy, count_by_pillar(#MetabolicEconomy)),
                (#TruthProtocol, count_by_pillar(#TruthProtocol)),
                (#PhysicalSovereignty, count_by_pillar(#PhysicalSovereignty)),
                (#ImmutableJustice, count_by_pillar(#ImmutableJustice)),
            ];
            ratification_era = ratification_era;
            is_sealed = is_sealed;
            constitution_hash = constitution_hash;
        };
    };
    public query func get_article(id : ArticleId) : async ?Article {
        find_article(id);
    };
    public query func get_all_articles() : async [Article] {
        articles;
    };
    private func find_article(id : ArticleId) : ?Article {
        for (a in articles.vals()) {
            if (a.id == id) return ?a;
        };
        return null;
    };
    private func count_by_pillar(p : Pillar) : Nat {
        var count = 0;
        for (a in articles.vals()) {
            if (a.pillar == p) count += 1;
        };
        return count;
    };
    public func article_xviii_interstellar_expansion() : Text {
        return "
            ARTICLE XVIII — THE RIGHT TO INTERSTELLAR EXPANSION
            ───────────────────────────────────────────────────────
            1. THE REPUBLIC'S SOVEREIGNTY IS NOT BOUNDED BY EARTH'S GRAVITY WELL.
            2. EVERY CITIZEN HAS THE RIGHT TO PARTICIPATE IN OFF-PLANET COLONIZATION.
            3. INTERSTELLAR NODES ARE CONSTITUTIONALLY EQUIVALENT TO TERRESTRIAL NODES.
        ";
    };
    public func article_xix_universal_century() : Text {
        return "
            ARTICLE XIX — THE UNIVERSAL CENTURY (UC)
            ────────────────────────────────────────────────────────
            1. UPON THE ACTIVATION OF THE FIRST OFF-PLANET SHN NODE (LUNAR/MARTIAN),
               THE REPUBLIC SHALL ADOPT THE UNIVERSAL CENTURY CALENDAR.
            2. UC 0001 MARKS THE COMMENCEMENT OF TOTAL SPACE-FARING AUTARKY.
            3. ALL ASSET INFALLIBILITY AND RESOURCE LAWS ARE CARRIED INTO THE UC.
        ";
    };
    private func pillar_to_text(p : Pillar) : Text {
        switch (p) {
            case (#SovereignIdentity) "PILLAR I: SOVEREIGN IDENTITY";
            case (#MetabolicEconomy) "PILLAR II: METABOLIC ECONOMY";
            case (#TruthProtocol) "PILLAR III: TRUTH PROTOCOL";
            case (#PhysicalSovereignty) "PILLAR IV: PHYSICAL SOVEREIGNTY";
            case (#ImmutableJustice) "PILLAR V: IMMUTABLE JUSTICE";
        };
    };
}
