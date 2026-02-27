import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

console.log('🏛️ SOVEREIGN DAVINCI - FINAL FIX SCRIPT');
console.log('==========================================');

// Configuration
const SRC_DIR = './src';
const EXTENSIONS = ['.svelte', '.ts', '.js'];

// Counters
let filesFixed = 0;
let totalFixes = 0;

// 1. Fix unused variables by adding underscore prefix
function fixUnusedVariables(content, filePath) {
    let newContent = content;
    let fixes = 0;

    // Find unused variable declarations
    const unusedPattern = /let (\w+)(?:\s*:\s*[^;=]+)?\s*=[^;]*;?\s*\/\/?\s*(?:not used|unused)?/gi;
    const matches = content.match(unusedPattern);

    if (matches) {
        matches.forEach(match => {
            const varName = match.match(/let (\w+)/)?.[1];
            if (varName && !varName.startsWith('_')) {
                const underscoreVar = `_${varName}`;
                newContent = newContent.replace(new RegExp(`\\b${varName}\\b`, 'g'), underscoreVar);
                fixes++;
            }
        });
    }

    return { content: newContent, fixes };
}

// 2. Fix canvas element types
function fixCanvasTypes(content, filePath) {
    let newContent = content;
    let fixes = 0;

    // Fix canvas declaration
    if (content.includes('let canvas;') || content.includes('let canvas = null;')) {
        newContent = newContent.replace(
            /let canvas\s*[^;]*;/g,
            'let canvas: HTMLCanvasElement | null = null;'
        );
        fixes++;
    }

    // Fix ctx declaration
    if (content.includes('let ctx;') || content.includes('let ctx = null;')) {
        newContent = newContent.replace(
            /let ctx\s*[^;]*;/g,
            'let ctx: CanvasRenderingContext2D | null = null;'
        );
        fixes++;
    }

    // Fix getElementById for canvas
    newContent = newContent.replace(
        /document\.getElementById\(['"]([^'"]+)['"]\)/g,
        (match, id) => {
            if (id.includes('canvas') || content.includes('canvas') || content.includes('ctx')) {
                fixes++;
                return `document.getElementById('${id}') as HTMLCanvasElement | null`;
            }
            return match;
        }
    );

    // Add non-null assertion for ctx when we're sure it exists
    newContent = newContent.replace(
        /if\s*\(\s*!ctx\s*\)\s*return\s*;?\s*\n?\s*ctx\./g,
        'if (!ctx) return;\n        ctx!.'
    );

    return { content: newContent, fixes };
}

// 4. Fix event handler parameters
function fixEventParameters(content, filePath) {
    let newContent = content;
    let fixes = 0;

    // Fix onclick handlers
    newContent = newContent.replace(
        /onclick=\{\(([^)]*)\)\s*=>/g,
        (match, params) => {
            if (params.trim() === '') {
                fixes++;
                return 'onclick={() =>';
            }
            return match;
        }
    );

    // Fix onsubmit handlers
    newContent = newContent.replace(
        /onsubmit=\{\(([^)]*)\)\s*=>/g,
        (match, params) => {
            if (params.trim() === '') {
                fixes++;
                return 'onsubmit={(e) =>';
            }
            return match;
        }
    );

    // Add type to event parameters
    newContent = newContent.replace(
        /on([a-z]+)=\{\((\w+)\)\s*=>/g,
        (match, event, param) => {
            // only apply if the param has no type natively:
            if (!param.includes(':')) {
                fixes++;
                return `on${event}={(e: ${getEventType(event)}) =>`;
            }
            return match;
        }
    );

    return { content: newContent, fixes };
}

function getEventType(event) {
    const types = {
        'click': 'MouseEvent',
        'submit': 'SubmitEvent',
        'change': 'Event',
        'input': 'InputEvent',
        'keydown': 'KeyboardEvent',
        'keyup': 'KeyboardEvent',
        'mouseenter': 'MouseEvent',
        'mouseleave': 'MouseEvent',
        'mousemove': 'MouseEvent',
        'mousedown': 'MouseEvent',
        'mouseup': 'MouseEvent',
        'wheel': 'WheelEvent',
        'drag': 'DragEvent',
        'drop': 'DragEvent',
        'dragover': 'DragEvent',
        'focus': 'FocusEvent',
        'blur': 'FocusEvent'
    };
    return types[event] || 'Event';
}

// 5. Fix array type annotations
function fixArrayTypes(content, filePath) {
    let newContent = content;
    let fixes = 0;

    // Find arrays without type annotations
    const arrayPattern = /let (\w+)\s*=\s*\[\s*\]\s*;?/g;
    const matches = content.match(arrayPattern);

    if (matches) {
        matches.forEach(match => {
            const varName = match.match(/let (\w+)\s*=/)?.[1];
            if (varName) {
                // Try to infer type from usage (simplified)
                const usageMatch = content.match(new RegExp(`${varName}\\.push\\((\\{[^}]+\\}|[^)]+)\\)`));
                if (usageMatch) {
                    const value = usageMatch[1];
                    if (value.includes('{')) {
                        fixes++;
                        newContent = newContent.replace(
                            match,
                            `let ${varName}: any[] = [];`
                        );
                    } else if (value.match(/['"]/)) {
                        fixes++;
                        newContent = newContent.replace(
                            match,
                            `let ${varName}: string[] = [];`
                        );
                    } else if (value.match(/^\d+$/)) {
                        fixes++;
                        newContent = newContent.replace(
                            match,
                            `let ${varName}: number[] = [];`
                        );
                    }
                } else {
                    fixes++;
                    newContent = newContent.replace(
                        match,
                        `let ${varName}: any[] = [];`
                    );
                }
            }
        });
    }

    return { content: newContent, fixes };
}

// 6. Fix missing transition imports
function fixTransitionImports(content, filePath) {
    let newContent = content;
    let fixes = 0;

    if (content.includes('transition:') || content.includes('in:') || content.includes('out:')) {
        if (!content.includes('import {') || !content.includes('} from "svelte/transition"')) {
            const imports = [];
            if (content.includes('transition:fade')) imports.push('fade');
            if (content.includes('transition:fly')) imports.push('fly');
            if (content.includes('transition:scale')) imports.push('scale');
            if (content.includes('transition:slide')) imports.push('slide');
            if (content.includes('transition:blur')) imports.push('blur');
            if (content.includes('in:fade')) imports.push('fade');
            if (content.includes('in:fly')) imports.push('fly');
            if (content.includes('in:scale')) imports.push('scale');
            if (content.includes('in:slide')) imports.push('slide');
            if (content.includes('out:fade')) imports.push('fade');
            if (content.includes('out:fly')) imports.push('fly');
            if (content.includes('out:scale')) imports.push('scale');
            if (content.includes('out:slide')) imports.push('slide');

            if (imports.length > 0) {
                const uniqueImports = [...new Set(imports)];
                const importStatement = `import { ${uniqueImports.join(', ')} } from 'svelte/transition';`;

                if (content.includes('<script>')) {
                    newContent = newContent.replace(
                        '<script>',
                        `<script>\n    ${importStatement}`
                    );
                    fixes++;
                } else if (content.includes('<script lang="ts">')) {
                    newContent = newContent.replace(
                        '<script lang="ts">',
                        `<script lang="ts">\n    ${importStatement}`
                    );
                    fixes++;
                }
            }
        }
    }
    return { content: newContent, fixes };
}

// 7. Fix CSS compatibility
function fixCSS(content, filePath) {
    let newContent = content;
    let fixes = 0;
    if (filePath.endsWith('.svelte')) {
        const pattern = /-webkit-background-clip:\s*text\s*;/g;
        if (pattern.test(content) && !content.includes('background-clip: text;')) {
            newContent = newContent.replace(
                /(-webkit-background-clip:\s*text\s*;)/g,
                '$1\n        background-clip: text;'
            );
            fixes++;
        }
    }
    return { content: newContent, fixes };
}

// Additional fix for specific store values
function fixStoreSyntax(content) {
    let fixes = 0;
    let newContent = content;
    if (content.match(/\$sovereignStore/g)) {
        newContent = newContent.replace(/\$sovereignStore/g, 'sovereignStore.state');
        fixes++;
    }
    if (content.match(/\$vaultStore/g)) {
        newContent = newContent.replace(/\$vaultStore/g, 'vaultStore.state');
        fixes++;
    }
    if (content.match(/\$governanceStore/g)) {
        newContent = newContent.replace(/\$governanceStore/g, 'governanceStore.state');
        fixes++;
    }
    if (content.match(/\$hearthStore/g)) {
        newContent = newContent.replace(/\$hearthStore/g, 'hearthStore.state');
        fixes++;
    }
    return { content: newContent, fixes };
}


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

    let res = {content: content, fixes: 0}; // fixUnusedVariables(content, filePath);
    content = res.content; fileFixes += res.fixes;

    res = fixCanvasTypes(content, filePath);
    content = res.content; fileFixes += res.fixes;

    res = fixEventParameters(content, filePath);
    content = res.content; fileFixes += res.fixes;

    res = fixArrayTypes(content, filePath);
    content = res.content; fileFixes += res.fixes;

    res = fixTransitionImports(content, filePath);
    content = res.content; fileFixes += res.fixes;

    res = fixCSS(content, filePath);
    content = res.content; fileFixes += res.fixes;

    res = fixStoreSyntax(content);
    content = res.content; fileFixes += res.fixes;

    if (content !== originalContent) {
        fs.writeFileSync(filePath, content, 'utf8');
        console.log(`✅ Fixed issues in ${path.relative(SRC_DIR, filePath)}`);
        filesFixed++;
        totalFixes += fileFixes;
    }
}

processDirectory(SRC_DIR);
console.log(`\n📊 SUMMARY: Files fixed: ${filesFixed} | Total fixes applied: ${totalFixes}\n`);
