import { test, expect } from '@playwright/test';

test.describe('Sovereign Institutional Plane - Phase 3 Verification', () => {

    test.beforeEach(async ({ page }) => {
        page.on('console', msg => console.log('BROWSER:', msg.text()));

        // 🏛️ SOVEREIGN BRIDGE: Bypass onboarding by mocking credentials
        await page.addInitScript(() => {
            window.localStorage.setItem('sovereign', JSON.stringify({
                id: 'did:age:test_identity',
                handle: 'antigravity_admin',
                profile: { displayName: 'Antigravity Architect' },
                verificationLevel: 3
            }));
            window.localStorage.setItem('onboarding_complete', 'true');
        });

        // Go to dashboard and wait for hydration
        await page.goto('http://localhost:5173/dashboard', { waitUntil: 'networkidle' });
    });

    test('Node Presence - One-Click Deploy Flow', async ({ page }) => {
        // Find Node Presence module (represented by 💎 icon or label)
        const presenceBlock = page.locator('text=Sovereign_Presence');
        await expect(presenceBlock).toBeVisible();

        // Select a role
        await page.click('text=Validator');

        // Initiate deployment sequence
        const deployBtn = page.locator('text=Execute_One-Click_Deploy');
        await expect(deployBtn).toBeVisible();
        await deployBtn.click();

        // Verify sync animation/status
        const syncingMsg = page.locator('text=Hyper_Synchronizing');
        await expect(syncingMsg).toBeVisible();

        // Wait for operational status (simulated 100% progress)
        await expect(page.locator('text=Node_Status: OPERATIONAL')).toBeVisible({ timeout: 10000 });
        await expect(page.locator('text=TFLOPS_Shared')).toBeVisible();
    });

    test('Sovereign Research - Mission Control', async ({ page }) => {
        const researchModule = page.locator('text=Sovereign_Research');
        await expect(researchModule).toBeVisible();

        // Check for active missions (use H2 to avoid ambiguity with sidebar list)
        await expect(page.locator('h2:has-text("Post-Quantum Privacy Vectors")')).toBeVisible();
        await expect(page.locator('span:has-text("LIBRARIAN")').first()).toBeVisible();

        // Interaction: Stake AGE
        const stakeBtn = page.locator('text=Stake_1,000_AGE_to_Mission');
        await expect(stakeBtn).toBeVisible();
        await stakeBtn.click();
    });

    test('Diplomacy Forge - Treaty Fabric', async ({ page }) => {
        const diplomacyModule = page.locator('text=Diplomacy_Forge');
        await expect(diplomacyModule).toBeVisible();

        // Check for jurisdiction nodes
        await expect(page.locator('text=Nagano_Shard')).toBeVisible();
        await expect(page.locator('text=Global Liquid State Accord')).toBeVisible();
    });

    test('Policy Fabricator - Law Wafer Bakery', async ({ page }) => {
        const policyModule = page.locator('text=Policy_Fabricator');
        await expect(policyModule).toBeVisible();

        // Check logic laboratory
        await expect(page.locator('text=Logic_Baking_Matrix')).toBeVisible();

        // Run Stress Simulation
        const simBtn = page.locator('text=Run_Stress_Test');
        await expect(simBtn).toBeVisible();
        await simBtn.click();

        await expect(page.locator('text=Fuzzing Invariants...')).toBeVisible();
        await expect(page.locator('text=Policy Integrity: 99.98%')).toBeVisible({ timeout: 10000 });
    });

    test('Somatic Bio-Mirror - Bio-Parity Sync', async ({ page }) => {
        const bioModule = page.locator('text=Somatic_Bio-Mirror');
        await expect(bioModule).toBeVisible();

        // Check vitals
        await expect(page.locator('text=Bio-Vigor')).toBeVisible();
        await expect(page.locator('text=Moral_Yield_Boost')).toBeVisible();
    });

    test('Sovereign Tokenomics - Equity Explorer', async ({ page }) => {
        const tokenomicsModule = page.locator('text=Age_Tokenomics');
        await expect(tokenomicsModule).toBeVisible();

        // Check tabs
        await page.click('text=SUPPLY');
        await expect(page.locator('text=Real-Time_Burn')).toBeVisible();

        await page.click('text=VE_AGE');
        await expect(page.locator('text=Vote-Escrowed_AGE')).toBeVisible();
    });

    test('Sovereign Comms - Kloak-inspired Nexus', async ({ page }) => {
        const commsModule = page.locator('text=Sovereign_Comms');
        await expect(commsModule).toBeVisible();

        // Check for secret key gate
        const keyBtn = page.locator('text=Import_Secret_Key');
        await expect(keyBtn).toBeVisible();
    });

});
