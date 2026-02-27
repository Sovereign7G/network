const fs = require('fs');

const output = fs.readFileSync('check-output.txt', 'utf8');
const lines = output.split('\n');

const missingImports = {};
const syntaxErrors = [];

for (const line of lines) {
    const match = line.match(/^(\d+)\s+(ERROR|WARNING)\s+"([^"]+)"\s+(\d+):(\d+)\s+"(.*)"$/);
    if (!match) continue;
    const [_, timestamp, level, file, lineNumStr, colNumStr, msg] = match;
    const lineNum = parseInt(lineNumStr, 10);

    // Catch "Expected token >" to remove preceding @ts-ignore
    if (msg.includes('Expected token >')) {
        syntaxErrors.push({ file, lineNum });
    }

    // Catch svelte/transition missing imports
    if (msg.includes("Cannot find name 'fade'") || msg.includes("Cannot find name 'fly'") || msg.includes("Cannot find name 'scale'") || msg.includes("Cannot find name 'slide'")) {
        if (!missingImports[file]) missingImports[file] = new Set();
        if (msg.includes("fade")) missingImports[file].add("fade");
        if (msg.includes("fly")) missingImports[file].add("fly");
        if (msg.includes("scale")) missingImports[file].add("scale");
        if (msg.includes("slide")) missingImports[file].add("slide");
    }
}

// Fix missing imports
for (const [file, names] of Object.entries(missingImports)) {
    if (!fs.existsSync(file)) continue;
    let content = fs.readFileSync(file, 'utf8');
    const importStr = `import { ${Array.from(names).join(', ')} } from 'svelte/transition';`;

    // Instead of replacing if there's an existing import, just put it at the very top of <script>
    if (!content.includes(importStr)) {
        if (content.includes('import { fade') || content.includes('import { fly')) {
            // It might exist but the check compiler might be acting up if we didn't save?
            // Actually it was missing. Just push it after <script lang="ts">
            content = content.replace(/<script([^>]*)>/, `<script$1>\n    ${importStr}`);
        } else {
            content = content.replace(/<script([^>]*)>/, `<script$1>\n    ${importStr}`);
        }
        fs.writeFileSync(file, content, 'utf8');
        console.log("Added imports to", file);
    }
}

// Fix Expected token > Syntax errors (by removing the bad `// @ts-ignore`)
for (const err of syntaxErrors) {
    if (!fs.existsSync(err.file)) continue;
    let contentLines = fs.readFileSync(err.file, 'utf8').split('\n');
    let i = err.lineNum - 1;
    // We search backwards from i-1 down to i-5 to rip out `// @ts-ignore`
    for (let j = i; j >= Math.max(0, i - 5); j--) {
        if (contentLines[j] && contentLines[j].includes('// @ts-ignore')) {
            contentLines[j] = contentLines[j].replace('// @ts-ignore', '');
            console.log("Removed bad ts-ignore in", err.file, "line", j + 1);
            break;
        }
    }
    fs.writeFileSync(err.file, contentLines.join('\n'), 'utf8');
}
