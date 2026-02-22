<script lang="ts">
  const tiers = [
    {
      name: "SOVEREIGN",
      price: "$29",
      hilbertPrice: "25",
      interval: "mo",
      features: [
        "Rust gates + WITR",
        "Standard Resilience",
        "5 active canisters",
      ],
      buttonText: "STAKE ℍ",
      highlight: false,
    },
    {
      name: "INSTITUTIONAL",
      price: "$299",
      hilbertPrice: "250",
      interval: "mo",
      features: [
        "CausalGPT + Timeline",
        "Slow-drip blocking",
        "Unlimited canisters",
      ],
      buttonText: "STAKE ℍ",
      highlight: true,
    },
    {
      name: "MULTIVERSAL",
      price: "$2,999",
      hilbertPrice: "2500",
      interval: "mo",
      features: [
        "ZK Preflight proofs",
        "Physical Sovereignty",
        "Hardware attestation",
      ],
      buttonText: "STAKE ℍ",
    },
    {
      name: "STUDIO",
      price: "$9,999",
      hilbertPrice: "8500",
      interval: "mo",
      features: [
        "HOLLY-1 Mesh Access",
        "VOX-1 Vocal Lineage",
        "Global Shard Nodes",
        "Narrative Integrity",
      ],
      buttonText: "STAKE ℍ",
      highlight: false,
    },
  ];
</script>

<div
  class="min-h-screen bg-slate-950 text-white font-sans selection:bg-cyan-500/30"
>
  <div class="max-w-7xl mx-auto px-6 py-24">
    <div class="text-center mb-16">
      <h1
        class="text-5xl md:text-7xl font-bold mb-6 tracking-tight bg-gradient-to-r from-cyan-400 via-blue-500 to-indigo-600 bg-clip-text text-transparent"
      >
        Enterprise Pricing
      </h1>
      <p class="text-xl text-slate-400 max-w-2xl mx-auto">
        Sovereign compute infrastructure for the next generation of autonomous
        generative economics.
      </p>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
      {#each tiers as tier}
        <div class="relative group">
          {#if tier.highlight}
            <div
              class="absolute -inset-0.5 bg-gradient-to-r from-cyan-500 to-blue-600 rounded-2xl blur opacity-30 group-hover:opacity-100 transition duration-1000 group-hover:duration-200"
            ></div>
          {/if}
          <div
            class="relative flex flex-col h-full bg-slate-900/50 backdrop-blur-xl border {tier.highlight
              ? 'border-cyan-500/50'
              : 'border-slate-800'} rounded-2xl p-8 hover:bg-slate-900/80 transition-all duration-300"
          >
            <h3
              class="text-sm font-semibold tracking-widest text-cyan-500 uppercase mb-4"
            >
              {tier.name}
            </h3>
            <div class="flex flex-col mb-8">
              <div class="flex items-baseline">
                <span class="text-4xl font-bold">{tier.price}</span>
                <span class="text-slate-500 ml-2">/{tier.interval}</span>
              </div>
              <div class="flex items-baseline mt-1">
                <span class="text-2xl font-bold text-cyan-400"
                  >{tier.hilbertPrice} ℍ</span
                >
                <span
                  class="text-slate-500 text-[10px] ml-2 font-black uppercase tracking-widest"
                  >Sovereignty Rate</span
                >
              </div>
            </div>

            <ul class="flex-grow space-y-4 mb-8 text-slate-300">
              {#each tier.features as feature}
                <li class="flex items-start">
                  <svg
                    class="w-5 h-5 text-cyan-500 mt-1 mr-3 flex-shrink-0"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M5 13l4 4L19 7"
                    />
                  </svg>
                  {feature}
                </li>
              {/each}
            </ul>

            <button
              class="w-full py-4 px-6 rounded-xl font-semibold transition-all duration-300
              {tier.highlight
                ? 'bg-gradient-to-r from-cyan-500 to-blue-600 text-white hover:shadow-lg hover:shadow-cyan-500/25 active:scale-[0.98]'
                : 'bg-slate-800 text-slate-100 hover:bg-slate-700 active:scale-[0.98]'}"
            >
              {tier.buttonText}
            </button>

            {#if tier.buttonText.includes("Trial")}
              <p class="text-center text-xs text-slate-500 mt-4 italic">
                Paid Day 15 if not cancelled
              </p>
            {/if}
          </div>
        </div>
      {/each}
    </div>

    <div class="mt-24 text-center">
      <div
        class="inline-flex items-center space-x-2 bg-slate-900 border border-slate-800 rounded-full px-4 py-2 text-sm text-slate-400"
      >
        <span class="w-2 h-2 bg-green-500 rounded-full animate-pulse"></span>
        <span
          >Status: AGE PROTOCOL = sovereign computing unicorn trajectory.</span
        >
      </div>
    </div>
  </div>
</div>

<style>
  :global(body) {
    background-color: #020617; /* Tailwind slate-950 */
    margin: 0;
  }
</style>
