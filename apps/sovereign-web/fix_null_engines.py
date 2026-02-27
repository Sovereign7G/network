import os
import re

def process_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    orig = content
    content = re.sub(r'browser \? new ([a-zA-Z0-9_]+)\(\) : null', r'new \1()', content)

    if content != orig:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed {path}")

for root, _, files in os.walk('src'):
    for file in files:
        if file.endswith('.svelte') or file.endswith('.ts'):
            process_file(os.path.join(root, file))
