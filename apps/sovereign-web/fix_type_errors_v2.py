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

process_file('src/lib/stores/master-store.svelte.ts', [
    (r"side: 'BUY' \| 'SELL'", r"side: 'BID' | 'ASK'"),
    (r"points: \[\] as \{ id: string, label: string \}\[\]", r"points: [] as { id: string, label: string, region: string, scarcity: string, status: string, tps: number }[]")
])

process_file('src/lib/components/dashboard/SovereignTokenomics.svelte', [
    (r'const tabs = \["SUPPLY", "YIELD", "VE_AGE"\];', r'const tabs = ["SUPPLY", "YIELD", "VE_AGE"] as const;')
])

process_file('src/lib/components/dashboard/SovereignTelemetryLog.svelte', [
    (r'status: \["COHERENT", "SYNCING", "CAUSAL_TRACE"\]\[Math\.floor\(Math\.random\(\) \* 3\)\]', r'status: (["COHERENT", "SYNCING", "CAUSAL_TRACE"] as const)[Math.floor(Math.random() * 3)]')
])

process_file('src/lib/components/dashboard/SonicIndicator.svelte', [
    (r'window\.addEventListener\("extraction-saved", handleSave\);', r'window.addEventListener("extraction-saved", handleSave as EventListener);'),
    (r'window\.removeEventListener\("extraction-saved", handleSave\);', r'window.removeEventListener("extraction-saved", handleSave as EventListener);')
])
