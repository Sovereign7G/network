import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

console.log('🏛️ SOVEREIGN DAVINCI - FINAL FIX SCRIPT');
console.log('==========================================');

// Configuration
const SRC_DIR = path.join(__dirname, 'src');
const EXTENSIONS = ['.svelte', '.ts', '.js'];

// Counters
let filesFixed = 0;
let totalFixes = 0;

function processDirectory(dir) {
    const files = fs.readdirSync(dir);

    files.forEach(file => {
        const fullPath = path.join(dir, file);
        const stat = fs.statSync(fullPath);

        if (stat.isDirectory() && !file.includes('node_modules') && !file.startsWith('.')) {
            processDirectory(fullPath);
        } else if (EXTENSIONS.includes(path.extname(file))) {
            processFile(fullPath);
        }
    });
}

function processFile(filePath) {
    let content = fs.readFileSync(filePath, 'utf8');
    let originalContent = content;
    let fileFixes = 0;

    // Fix Canvas types
    if (content.match(/let canvas(\s*:?\s*[^;]*);/) && !content.includes('HTMLCanvasElement')) {
        content = content.replace(/let canvas(\s*:?\s*[^;]*);/g, 'let canvas: HTMLCanvasElement | null = null;');
        fileFixes++;
    }
    if (content.match(/let canvasCtx(\s*:?\s*[^;]*);/) && !content.includes('CanvasRenderingContext2D')) {
        content = content.replace(/let canvasCtx(\s*:?\s*[^;]*);/g, 'let canvasCtx: CanvasRenderingContext2D | null = null;');
        fileFixes++;
    }
    if (content.match(/let ctx(\s*:?\s*[^;]*);/) && !content.includes('CanvasRenderingContext2D')) {
        content = content.replace(/let ctx(\s*:?\s*[^;]*);/g, 'let ctx: CanvasRenderingContext2D | null = null;');
        fileFixes++;
    }

    // Event params
    if (content.includes('onclick={(')) {
        content = content.replace(/onclick=\{\(([^):]*)\)\s*=>/g, (match, param) => {
            if (param.trim() === '') return 'onclick={() =>';
            return `onclick={(e: MouseEvent) =>`;
        });
        fileFixes++;
    }

    if (content.includes('onsubmit={(')) {
        content = content.replace(/onsubmit=\{\(([^):]*)\)\s*=>/g, (match, param) => {
            if (param.trim() === '') return 'onsubmit={(e: Event) =>';
            return `onsubmit={(e: Event) =>`;
        });
        fileFixes++;
    }

    // CSS Compat
    if (content.match(/-webkit-background-clip:\s*text;/)) {
        if (!content.match(/background-clip:\s*text;/)) {
            content = content.replace(/-webkit-background-clip:\s*text;/g, '-webkit-background-clip: text;\n        background-clip: text;');
            fileFixes++;
        }
    }

    // Add array typings
    if (content.match(/let (\w+)\s*=\s*\[\s*\]\s*;/g)) {
        content = content.replace(/let (\w+)\s*=\s*\[\s*\]\s*;/g, (match, varName) => {
            return `let ${varName}: any[] = [];`;
        });
        fileFixes++;
    }

    if (content !== originalContent) {
        fs.writeFileSync(filePath, content, 'utf8');
        filesFixed++;
        totalFixes += fileFixes;
    }
}

console.log('\n🔍 Scanning for files to fix...\n');
processDirectory(SRC_DIR);

console.log(`\n📊 SUMMARY:`);
console.log(`   Files fixed: ${filesFixed}`);
console.log(`   Total possible fixes applied: ${totalFixes}`);
console.log(`   Run 'npx svelte-check' to see remaining issues\n`);
