import os
import re

def process_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    orig = content
    content = re.sub(r'\(manifold as any\)\.', 'manifold.', content)
    content = re.sub(r'\(telemetryStore as any\)\.', 'telemetryStore.', content)
    content = re.sub(r'\(telemetryStore\.vitals as any\)\.', 'telemetryStore.vitals.', content)
    content = re.sub(r'\(lll as any\)\.', 'lll.', content)
    content = re.sub(r'\(stablecoin as any\)\.', 'stablecoin.', content)
    content = re.sub(r'\(bridge as any\)\.', 'bridge.', content)
    content = re.sub(r'\(engineStats as any\)\.', 'engineStats.', content)
    content = re.sub(r'\(combo as any\)\.', 'combo.', content)
    content = re.sub(r'includes\(([^ ]+) as any\)', r'includes(\1)', content)
    content = re.sub(r'= tab as any', '= tab', content)
    content = re.sub(r'handleSave as any', 'handleSave', content)
    content = re.sub(r'null as any\b', 'null', content)
    content = re.sub(r'\] as any,', '],', content)
    content = re.sub(r'details: \{\} as any,', 'details: {} as any,', content) # Ignore for now, handled later if needed

    if content != orig:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed {path}")

for root, _, files in os.walk('src'):
    for file in files:
        if file.endswith('.svelte') or file.endswith('.ts'):
            process_file(os.path.join(root, file))
