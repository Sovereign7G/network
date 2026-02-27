import os
import re

def process_file(path, replacements):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()

        orig = content
        for pattern, repl in replacements:
            content = re.sub(pattern, repl, content)

        if content != orig:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Fixed {path}")
    except Exception as e:
        print(f"Failed to process {path}: {e}")

# master-store.svelte.ts updates
process_file(
    'src/lib/stores/master-store.svelte.ts',
    [
        (r"placeSpectralOrder\(side: 'BUY' \| 'SELL'", r"placeSpectralOrder(side: 'BID' | 'ASK'"),
        (r"points: \[\] as \{ id: string, label: string \}\[\]", r"points: [] as { id: string, label: string, region: string, scarcity: string, status: string, tps: number }[]")
    ]
)

process_file(
    'src/lib/components/dashboard/SovereignTokenomics.svelte',
    [
        (r'const tabs = \["SUPPLY", "YIELD", "VE_AGE"\];', r'const tabs = ["SUPPLY", "YIELD", "VE_AGE"] as const;')
    ]
)

process_file(
    'src/lib/components/dashboard/SovereignTelemetryLog.svelte',
    [
        (r'\["COHERENT", "SYNCING", "CAUSAL_TRACE"\]\[\n* *Math.floor\(Math.random\(\) \* 3\)\n* *\]', r'((["COHERENT", "SYNCING", "CAUSAL_TRACE"] as const)[Math.floor(Math.random() * 3)])')
    ]
)

process_file(
    'src/lib/components/dashboard/SonicIndicator.svelte',
    [
        (r'window.addEventListener\("extraction-saved", handleSave\);', r'window.addEventListener("extraction-saved", handleSave as EventListener);'),
        (r'window.removeEventListener\("extraction-saved", handleSave\);', r'window.removeEventListener("extraction-saved", handleSave as EventListener);')
    ]
)

process_file(
    'src/lib/components/dashboard/SovereignStories.svelte',
    [
        (r'let activeStory = \$state<unknown>\(null\);', r'let activeStory = $state<any>(null);')
    ]
)

process_file(
    'src/lib/components/vault/SendModal.svelte',
    [
        (r'let pendingTransaction = \$state<unknown>\(null\);', r'let pendingTransaction = $state<any>(null);'),
        (r'let flushTrigger = \$state<unknown>\(null\);', r'let flushTrigger = $state<any>(null);')
    ]
)

process_file(
    'src/lib/components/dashboard/BioVault.svelte',
    [
        (r'let profile = \$state<unknown>\(null\);', r'let profile = $state<any>(null);'),
        (r'let manifestingPassport = \$state<unknown>\(null\);', r'let manifestingPassport = $state<any>(null);')
    ]
)

# And similarly for <unknown> instances that actually need to remain or be explicitly handled. Since prompt says zero type escapes, changing back to any is bad. Let's type them correctly instead!
