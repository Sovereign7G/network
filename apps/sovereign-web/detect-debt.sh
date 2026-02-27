#!/bin/bash
# detect-debt.sh - Run this weekly to track progress

echo "🏛️ Sovereign Technical Debt Detector"
echo "====================================="

# TypeScript errors
echo "🔴 TypeScript errors:"
npm run type-check 2>&1 | grep error | wc -l

# Svelte-check errors
echo "🔴 Svelte-check errors:"
npm run check 2>&1 | grep error | wc -l

# ESLint warnings
echo "🟡 ESLint warnings:"
npx eslint . --max-warnings=0 2>&1 | grep warning | wc -l

# A11y issues
echo "🟡 Accessibility issues:"
# Note: axe requires a running server, skipping or using a static check if possible
# For now, svelte-check covers many a11y issues
echo "Check svelte-check output for a11y warnings"

# Bundle size
echo "🔵 Bundle size:"
# npx vite-bundle-visualizer --output bundle-stats.html
echo "Run 'npx vite-bundle-visualizer' manually to check bundle size"

# Test coverage
echo "🧪 Test coverage:"
# npm run test:coverage | grep "All files"
echo "Configure test:coverage script in package.json"

echo "====================================="
echo "Run weekly to track progress to ZERO"
