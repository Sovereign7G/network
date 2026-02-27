import fs from 'fs';
import path from 'path';

const files = [
    "src/routes/onboarding/+page.svelte",
    "src/routes/send/+page.svelte",
    "src/routes/dashboard/+page.svelte",
    "src/routes/marketplace/+page.svelte",
    "src/lib/services/design-engineering-engine.svelte.ts",
    "src/lib/services/credential-service.ts",
    "src/lib/engines/suggestion-engine.svelte.ts",
    "src/lib/stores/sovereign-store.svelte.ts",
    "src/lib/stores/master-store.svelte.ts",
    "src/lib/services/agent-gateway.ts",
    "src/lib/auth/aal3.ts",
    "src/lib/nai/engine.svelte.ts",
    "src/routes/+layout.svelte",
    "src/lib/services/simulation-engine.svelte.ts",
    "src/lib/services/metabolic-engine.svelte.ts",
    "src/lib/stores/telemetry-store.svelte.ts",
    "src/lib/components/command/OmnipresentCommand.svelte",
    "src/lib/components/command/FloatingCommand.svelte",
    "src/lib/components/command/CommandPalette.svelte",
    "src/lib/components/infrastructure/NodeOnboarding.svelte",
    "src/lib/components/dashboard/ZVecPanel.svelte",
    "src/lib/components/layout/Header.svelte",
    "src/lib/components/marketplace/MarketplaceBrowser.svelte"
];

files.forEach(file => {
    const fullPath = path.resolve('/home/gt-07/Downloads/AGE PROTOCOL/apps/sovereign-web', file);
    if (fs.existsSync(fullPath)) {
        let content = fs.readFileSync(fullPath, 'utf-8');
        // Remove console.log statements. Handles multi-line sparingly.
        // This regex targets lines that only contain console.log or where console.log is a statement.
        const originalContent = content;
        content = content.replace(/^[ \t]*console\.log\(.*?\);?[ \t]*\r?\n/gm, '');
        // Also handle cases where it might be on the same line as other code (less common in this project)
        // or inside an arrow function without braces
        content = content.replace(/[ \t]+console\.log\(.*?\);?/g, '');

        if (content !== originalContent) {
            fs.writeFileSync(fullPath, content);
            console.log(`Removed logs from ${file}`);
        }
    } else {
        console.log(`File not found: ${file}`);
    }
});
