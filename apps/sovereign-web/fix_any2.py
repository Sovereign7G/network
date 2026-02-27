import os
import re

def process_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    orig = content
    content = re.sub(r'\$state<any>\(null\)', '$state<unknown>(null)', content)
    content = re.sub(r'getComponents<any>', 'getComponents<unknown>', content)
    content = re.sub(r'payload: any', 'payload: unknown', content)
    content = re.sub(r'Promise<any>', 'Promise<unknown>', content)
    content = re.sub(r'Object\.values\(MEMORY_TYPES\) as any\[\]', 'Object.values(MEMORY_TYPES)', content)

    if content != orig:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed {path}")

for root, _, files in os.walk('src'):
    for file in files:
        if file.endswith('.svelte') or file.endswith('.ts'):
            process_file(os.path.join(root, file))
