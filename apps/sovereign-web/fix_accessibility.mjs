import { readFileSync, writeFileSync, readdirSync, statSync } from 'fs';
import { join } from 'path';

function walkDir(dir) {
    let results = [];
    const list = readdirSync(dir);
    list.forEach((file) => {
        file = join(dir, file);
        const stat = statSync(file);
        if (stat && stat.isDirectory()) {
            results = results.concat(walkDir(file));
        } else {
            if (file.endsWith('.svelte')) results.push(file);
        }
    });
    return results;
}

const svelteFiles = walkDir('./src');

function fixFiles() {
    let count = 0;
    for (const file of svelteFiles) {
        let content = readFileSync(file, 'utf8');
        let original = content;

        // 1. Convert on:click
        content = content.replace(/on:click=/g, 'onclick=');
        content = content.replace(/on:click\|stopPropagation/g, 'onclick={(e) => e.stopPropagation()}');
        content = content.replace(/on:click\|preventDefault/g, 'onclick={(e) => e.preventDefault()}');

        // 2. Fix state in VerticalNav
        if (file.endsWith('VerticalNav.svelte')) {
            content = content.replace(/let showTools = true;/, 'let showTools = $state(true);');
            content = content.replace(/let showCapabilities = true;/, 'let showCapabilities = $state(true);');
            // add keyboard/role where it might be needed if they are simple divs
        }

        // 3. Fix FloatingCommand
        if (file.endsWith('FloatingCommand.svelte')) {
            content = content.replace(/autofocus/g, ''); // just remove autofocus
        }

        // 4. Fix Vault Modal
        if (file.endsWith('vault/+page.svelte')) {
            content = content.replace(
                /<div class="modal-overlay"/g,
                '<div class="modal-overlay" role="presentation" tabindex="-1"'
            );
            content = content.replace(
                /<div class="modal-content"/g,
                '<div class="modal-content" role="dialog" aria-modal="true"'
            );
        }

        if (content !== original) {
            writeFileSync(file, content, 'utf8');
            console.log(`Updated ${file}`);
            count++;
        }
    }
    console.log(`Fixed ${count} files.`);
}

fixFiles();
