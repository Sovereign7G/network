import fs from 'fs';

const log = fs.readFileSync('prune.log', 'utf-8');
const lines = log.split('\n').filter(l => l.trim().length > 0);

for (const line of lines) {
    // Format: "file/path.ts:123 - ExportName (used in module)"
    const match = line.match(/^([^:]+):(\d+)\s+-\s+([\w]+)/);
    if (!match) continue;

    const file = match[1];
    const lineNum = parseInt(match[2], 10) - 1; // 0-indexed
    const exportName = match[3];

    if (file.startsWith('src/routes/') && (file.endsWith('+page.ts') || file.endsWith('+layout.ts') || file.endsWith('+server.ts') || file.endsWith('+page.server.ts'))) {
        console.log(`Skipping SvelteKit route file: ${file}`);
        continue;
    }

    if (exportName === 'default') {
        // Be careful with default exports
        console.log(`Skipping default export in ${file}`);
        continue;
    }

    if (!fs.existsSync(file)) {
        console.log(`File not found: ${file}`);
        continue;
    }

    const content = fs.readFileSync(file, 'utf-8');
    const fileLines = content.split('\n');

    // We should search around the lineNum because sometimes ts-prune line numbers are slightly off
    let found = false;
    for (let i = Math.max(0, lineNum - 2); i <= Math.min(fileLines.length - 1, lineNum + 2); i++) {
        let targetLine = fileLines[i];
        if (targetLine && targetLine.match(/\bexport\b/)) {
            // If it's an export list like `export { ... }`, skip for now
            if (targetLine.includes('export {')) continue;

            fileLines[i] = targetLine.replace(/export\s+/, '');
            fs.writeFileSync(file, fileLines.join('\n'));
            console.log(`Fixed: ${file} at line ${i + 1} (${exportName})`);
            found = true;
            break;
        }
    }

    if (!found) {
        console.log(`Warning: 'export' not found around line ${lineNum + 1} of ${file} for ${exportName}`);
    }
}
