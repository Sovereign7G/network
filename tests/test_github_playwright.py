#!/usr/bin/env python3
"""Playwright smoke test for S7G GitHub repo validation.
Uses playwright installed in /tmp/pw-venv.

Usage:
    source /tmp/pw-venv/bin/activate && python3 tests/test_github_playwright.py
"""
import subprocess, sys, os

# Use the venv's python
VENV_PYTHON = "/tmp/pw-venv/bin/python3"
assert os.path.exists(VENV_PYTHON), "Run install first: python3 -m venv /tmp/pw-venv && source /tmp/pw-venv/bin/activate && pip install playwright && python3 -m playwright install chromium"

TEST_SCRIPT = r'''
import asyncio
from playwright.async_api import async_playwright

REPO_URL = "https://github.com/Sovereign7G/network"
CHECKS = []
def check(name, passed, detail=""):
    status = "✅" if passed else "❌"
    CHECKS.append((status, name, detail))

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        print(f"Navigating to {REPO_URL}...")
        await page.goto(REPO_URL, wait_until="networkidle", timeout=30000)
        
        title = await page.title()
        check("Page loads", True, title[:80])
        check("Title has Sovereign 7G", "Sovereign 7G" in title or "Sovereign7G" in title)
        
        body = await page.inner_text("body")
        
        check("Description mentions EU AI Act", "EU AI Act" in body)
        check("Description mentions GENIUS Act", "GENIUS" in body)
        check("SDK v2.4 mentioned", "SDK v2.4" in body)
        check("Canister ID visible", "iemx3" in body)
        check("Security section readable", "Access controls" in body or "red-team" in body)
        check("Quick Start commands", "pip install" in body)
        check("LICENSE mentioned", "MIT" in body)
        check("ElizaOS actions listed", "S7G_GET_LIQUIDITY" in body)
        check("EU AI Act article matrix", "Art 50" in body or "Art 12" in body)
        check("Python code example", "DepinClient" in body)
        check("Self-verification commands", "verify_audit_integrity" in body)
        check("Reserve command present", "get_reserve_state" in body)
        
        # Check no internal artifacts visible
        check("No 00_KNOWLEDGE in tree", "00_KNOWLEDGE" not in body)
        
        await browser.close()
    
    print(f"\n{'=' * 55}")
    passed = sum(1 for s, _, _ in CHECKS if s == "✅")
    total = len(CHECKS)
    print(f"RESULTS: {passed}/{total} checks passed")
    print(f"{'=' * 55}")
    for status, name, detail in CHECKS:
        print(f"  {status} {name}")
    sys.exit(0 if passed == total else 1)

asyncio.run(main())
'''

result = subprocess.run([VENV_PYTHON, "-c", TEST_SCRIPT], capture_output=True, text=True, timeout=60)
print(result.stdout)
if result.stderr:
    print("STDERR:", result.stderr[:500])
sys.exit(result.returncode)
