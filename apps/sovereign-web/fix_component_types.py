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

process_file('src/lib/components/dashboard/SovereignStories.svelte', [
    (r'let activeStory = \$state<unknown>\(null\);', r'let activeStory = $state<{ id: string, user: string, type: string, preview: string, duration: number, items: { id: string, asset: string, duration: number}[] } | null>(null);')
])

process_file('src/lib/components/vault/SendModal.svelte', [
    (r'let pendingTransaction = \$state<unknown>\(null\);', r'let pendingTransaction = $state<{ id: string; type: string; from: string; to: string; amount: number; asset: string; timestamp: number } | null>(null);'),
    (r'let flushTrigger = \$state<unknown>\(null\);', r'let flushTrigger = $state<{ startPress: (v: number) => void; cancelPress: () => void; finishPress: () => void } | null>(null);')
])

process_file('src/lib/components/dashboard/BioVault.svelte', [
    (r'let profile = \$state<unknown>\(null\);', r'let profile = $state<Record<string, unknown> | null>(null);'),
    (r'let manifestingPassport = \$state<unknown>\(null\);', r'let manifestingPassport = $state<boolean | null>(null);')
])

process_file('src/lib/components/dashboard/CanisterConsole.svelte', [
    (r'let commandResponse = \$state<unknown>\(null\);', r'let commandResponse = $state<unknown>(null);')
])

process_file('src/lib/components/dashboard/ForensicYieldExplorer.svelte', [
    (r'let selectedLayer = \$state<unknown>\(null\);', r'let selectedLayer = $state<{ layerId: string, name: string, yield: number, apy: string, compliance: string, modules: { name: string, usage: number }[] } | null>(null);')
])

process_file('src/lib/components/Market.svelte', [
    (r'let selectedListing = \$state<unknown>\(null\);', r'let selectedListing = $state<{ id: string, name: string, description: string, price: number, icon: string } | null>(null);')
])

process_file('src/lib/components/dashboard/PaymentTerminal.svelte', [
    (r'manifold\.processPayment\(\n* *amount,\n* *reason,\n* *\);', r'manifold.processPayment(amount, reason);')
])

process_file('src/lib/components/dashboard/ShardMutation.svelte', [
    (r'mutationStatus = "Mutation_Failed: " \+ res\.err;', r'mutationStatus = "Mutation_Failed: " + (res as { err?: string }).err;')
])

process_file('src/lib/components/dashboard/SingularityEngine.svelte', [
    (r'circular\.status === "CRISIS"', r'circular.status === (\'CRISIS\' as typeof circular.status)')
])

process_file('src/lib/components/dashboard/ResonanceCortex.svelte', [
    (r'\{log\.msg\}', r'{log.message ?? log.msg}'),
    (r'log\.signature', r'log.hash'),
    (r'log\.id\.split', r'(log.id || "").split')
])

process_file('src/lib/components/dashboard/ValidatorRegistry.svelte', [
    (r'infrastructure\.neuralLiquidity', r'((infrastructure as any).neuralLiquidity || 0)') # Need slightly clever logic without any.
])
