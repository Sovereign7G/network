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

process_file('src/lib/components/dashboard/SonicIndicator.svelte', [
    (r'telemetryStore\.vitals\.systemic\?\.resonance \?\? 98', r'telemetryStore.vitals.resonance'),
    (r'telemetryStore\.vitals\.systemic\?\.resonance', r'telemetryStore.vitals.resonance')
])

process_file('src/lib/components/dashboard/NavyMap.svelte', [
    (r'telemetryStore\.resonance', r'telemetryStore.vitals.resonance')
])

process_file('src/lib/components/vault/SendModal.svelte', [
    (r'let flushTrigger = \$state<\{ startPress: \(v: number\) => void; cancelPress: \(\) => void; finishPress: \(\) => void \} \| null>\(null\);', r'let flushTrigger = $state<ReturnType<typeof import("./FlushHold.svelte").default> | null>(null);')
])
