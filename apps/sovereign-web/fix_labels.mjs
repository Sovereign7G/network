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

function fixLabels() {
    let count = 0;
    for (const file of svelteFiles) {
        let content = readFileSync(file, 'utf8');
        let original = content;

        // Fix labels that simply wrap text without `for`
        // Example: <label>Recipient</label>\s*<input ... bind:value={something} ... />

        // Manual replacements:
        if (file.endsWith('send/+page.svelte')) {
            content = content.replace(/<label>Recipient<\/label>/g, '<label for="send-recipient">Recipient</label>');
            content = content.replace(/<input\s+type="text"\s+placeholder="0x\.\.\."\s+bind:value={recipient}/g, '<input id="send-recipient" aria-required="true" type="text" placeholder="0x..." bind:value={recipient}');

            content = content.replace(/<label>Amount<\/label>/g, '<label for="send-amount">Amount</label>');
            content = content.replace(/<input\s+type="number"\s+placeholder="0\.00"\s+bind:value={amount}/g, '<input id="send-amount" aria-required="true" type="number" placeholder="0.00" bind:value={amount}');

            content = content.replace(/<label>Asset<\/label>/g, '<label for="send-asset">Asset</label>');
            content = content.replace(/<select bind:value={asset} class="glass-select">/g, '<select id="send-asset" bind:value={asset} class="glass-select">');
        }

        if (file.endsWith('logistics/monitor/+page.svelte')) {
            content = content.replace(/<label>Entregas Hoje<\/label>/g, '<label for="logistics-entregas">Entregas Hoje</label>');
            content = content.replace(/<div class="value">{stats\.deliveriesCompleted}<\/div>/g, '<div id="logistics-entregas" class="value" role="group">{stats.deliveriesCompleted}</div>');

            content = content.replace(/<label>Valor Total \(USDC\)<\/label>/g, '<label for="logistics-valor">Valor Total (USDC)</label>');
            content = content.replace(/<div class="value">\${stats\.totalPaid\.toFixed\(2\)}<\/div>/g, '<div id="logistics-valor" class="value" role="group">${stats.totalPaid.toFixed(2)}</div>');

            content = content.replace(/<label>Tempo Médio<\/label>/g, '<label for="logistics-tempo">Tempo Médio</label>');
            content = content.replace(/<div class="value">{stats\.avgDeliveryTime} min<\/div>/g, '<div id="logistics-tempo" class="value" role="group">{stats.avgDeliveryTime} min</div>');

            content = content.replace(/<label>Couriers Ativos<\/label>/g, '<label for="logistics-couriers">Couriers Ativos</label>');
            content = content.replace(/<div class="value">{stats\.activeCouriers}<\/div>/g, '<div id="logistics-couriers" class="value" role="group">{stats.activeCouriers}</div>');

            // Remove rogue label from stats cards - they are just display values not forms, but user wants labels fixed
        }

        if (file.endsWith('governance/circuit-breaker/+page.svelte')) {
            content = content.replace(/<label>Current<\/label>\s*<div class="value">/g, '<label for="cb-cur">Current</label><div id="cb-cur" class="value" role="group">');
            content = content.replace(/<label>Limit<\/label>\s*<div class="value">/g, '<label for="cb-limit">Limit</label><div id="cb-limit" class="value" role="group">');
            content = content.replace(/<label>Remaining<\/label>\s*<div class="value">/g, '<label for="cb-rem">Remaining</label><div id="cb-rem" class="value" role="group">');
        }

        if (file.endsWith('Services.svelte')) {
            // Fix clickable divs. The file has <div class="glass-panel p-12 group ... onclick={() => initiateSignature(e.label)}
            content = content.replace(
                /<div\s*class="glass-panel p-12 group hover:border-white\/10 transition-all cursor-pointer relative overflow-hidden"\s*onclick={\(\) => initiateSignature\(e\.label\)}/g,
                '<button class="glass-panel p-12 group hover:border-white/10 transition-all cursor-pointer relative overflow-hidden" style="all: unset; display: block; width: 100%; box-sizing: border-box;" onclick={() => initiateSignature(e.label)} onkeydown={(evt) => evt.key === \'Enter\' && initiateSignature(e.label)} aria-label={`Initiate signature for ${e.label}`}'
            );
            content = content.replace(/<\/div>\s*<!-- Background Elements -->/g, '</button><!-- Background Elements -->');
        }

        if (file.endsWith('TemplateSelector.svelte')) {
            content = content.replace(
                /<div class="template-card" onclick={\(\) => loadTemplate\(template\)}>/g,
                '<button class="template-card" style="all: unset; display: block; cursor: pointer; width: 100%; box-sizing: border-box;" onclick={() => loadTemplate(template)} onkeydown={(e) => e.key === \'Enter\' && loadTemplate(template)} aria-label={`Load template: ${template.name}`}>'
            );
            // Assuming template cards have a closing div directly after the text
            content = content.replace(/<p>{template\.description}<\/p>\s*<\/div>/g, '<p>{template.description}</p></button>');
        }

        if (file.endsWith('WorkspaceCanvas.svelte')) {
            // drop zones
            content = content.replace(
                /class="drop-zone"/g,
                'class="drop-zone" role="region" aria-label="Drop zone"'
            );
            content = content.replace(
                /class="canvas-column"/g,
                'class="canvas-column" role="region" aria-label="Workspace column"'
            );
        }

        if (file.endsWith('ChatInterface.svelte')) {
            content = content.replace(/<div bind:this={messagesEnd} \/>/g, '<div bind:this={messagesEnd}></div>');
        }

        if (file.endsWith('hearth/MemoryCard.svelte')) {
            content = content.replace(
                /<div\s*class="memory-card"/g,
                '<div tabindex="0" class="memory-card" role="button" onkeydown={(e) => e.key === \'Enter\' && (isExpanded = !isExpanded)}'
            );
        }

        if (file.endsWith('AppLayout.svelte')) {
            // remove export let resonance = 98;
            content = content.replace(/export let resonance = 98;/g, '');
        }

        if (content !== original) {
            writeFileSync(file, content, 'utf8');
            console.log(`Updated ${file}`);
            count++;
        }
    }
    console.log(`Fixed ${count} files.`);
}

fixLabels();
