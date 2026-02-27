import { test, expect } from '@playwright/test';

test.describe('AGE Protocol Kernel E2E', () => {
    test('Dashboard loads and displays hardened status', async ({ page }) => {
        // 1. localhost:3000 -> WITR dashboard loads
        await page.goto('http://localhost:3000');

        // Check for "HARDENED STEWARD" badge
        const badge = page.locator('text=HARDENED STEWARD');
        await expect(badge).toBeVisible();

        // 2. Svelte $state updates with Rust health
        const healthCard = page.locator('text=RUST ACCELERATED');
        // Note: This might require the dev server to be running and bridge to be active
        // For E2E tests we often mock or check for the UI element
        await expect(healthCard).toBeVisible();
    });

    test('Identity sync across platforms', async ({ page }) => {
        await page.goto('http://localhost:3000');
        const identity = page.locator('text=#e-age-xyz123');
        // The prompt mentions "Hardened Steward #e-age-xyz123"
        await expect(identity).toBeVisible();
    });
});
