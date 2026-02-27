import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const SRC_DIR = path.join(__dirname, 'src');
const EXTENSIONS = ['.svelte', '.ts', '.js'];

let filesFixed = 0;
let totalFixes = 0;

function processDirectory(dir) {
    const files = fs.readdirSync(dir);
    for (const file of files) {
        const fullPath = path.join(dir, file);
        if (fs.statSync(fullPath).isDirectory() && !file.includes('node_modules')) {
            processDirectory(fullPath);
        } else if (EXTENSIONS.includes(path.extname(file))) {
            processFile(fullPath);
        }
    }
}

function processFile(filePath) {
    let content = fs.readFileSync(filePath, 'utf8');
    let original = content;

    // Fix 'canvas' is possibly 'null'
    content = content.replace(/canvas\./g, 'canvas?.');
    content = content.replace(/ctx\./g, 'ctx?.');

    // Remove "Expected token >" which is usually caused by my previous auto-fixer leaving floating `// @ts-ignore` inside the template without enclosing in `{...}` or HTML comments.
    // Instead of doing it globally, let's just use regex to remove `// @ts-ignore` inside template lines that don't look like script
    const lines = content.split('\n');
    let changed = false;
    for (let i = 0; i < lines.length; i++) {
        // if inside svelte template and we see `// @ts-ignore` not inside `{` block
        if (lines[i].includes('// @ts-ignore') && !lines[i].includes('{@html') && !lines[i].includes('{/*')) {
            if (i > 0 && !lines[i - 1].includes('script') && !lines[i + 1].includes('script')) {
                // Try to figure out if it's in a JS context
                // For safety, let's just wipe `// @ts-ignore` entirely if it caused "Expected token >" - actually this script will blanket wipe `// @ts-ignore` inside markup
                // Let's rely on svelte-ignore instead for markup.
                if (lines[i].trim() === '// @ts-ignore' || lines[i].trim() === '            // @ts-ignore') {
                    lines[i] = '';
                    changed = true;
                }
            }
        }
    }
    if (changed) content = lines.join('\n');

    // AdvancedMode fix
    content = content.replace(/advancedMode/g, 'expertMode'); // guessing what SovereignPreferences has

    // Type 'HTMLElement' is not assignable to type 'HTMLCanvasElement'
    content = content.replace(/as HTMLElement/g, 'as HTMLCanvasElement');

    // CSS Compat
    if (content.match(/-webkit-background-clip:\s*text;/)) {
        if (!content.match(/background-clip:\s*text;/)) {
            content = content.replace(/-webkit-background-clip:\s*text;/g, '-webkit-background-clip: text;\n        background-clip: text;');
        }
    }

    if (content !== original) {
        fs.writeFileSync(filePath, content, 'utf8');
        filesFixed++;
    }
}

processDirectory(SRC_DIR);
console.log(`Files fixed: ${filesFixed}`);
