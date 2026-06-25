"""BrowserAgent — web automation for the S7G agent swarm.
Wraps Playwright (headless Chromium) into an agent that other
S7G agents can delegate browser tasks to.

Usage:
    from agents.browser_agent import BrowserAgent
    agent = BrowserAgent()
    result = agent.run("navigate", url="https://example.com")
    result = agent.run("snapshot")
    result = agent.run("click", selector="button#submit")

Requirements:
    source /tmp/pw-venv/bin/activate  # Playwright + Chromium installed here
"""
import asyncio, json, os, subprocess
from datetime import datetime
from typing import Optional, Any

VENV_PYTHON = "/tmp/pw-venv/bin/python3"

# ── Core Browser Agent ─────────────────────────────────────────────

class BrowserAgent:
    """Browser automation agent using Playwright.

    Each method returns dict: {"ok": bool, "result": ..., "error": ...}
    """

    def __init__(self, name: str = "browser-agent"):
        self.name = name
        self._page = None
        self._browser = None
        self._playwright = None
        self._snapshot = ""

    def _ensure_async(self):
        """Lazy-import and ensure async context exists."""
        if self._page is not None:
            return
        # We use subprocess to call Playwright Python in a fresh process
        # to avoid async/await complexity in the sync agent swarm
        pass

    def _call_playwright(self, script: str) -> dict:
        """Run a Playwright Python script in a subprocess and return result."""
        result = subprocess.run(
            [VENV_PYTHON, "-c", script],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode != 0:
            return {"ok": False, "error": result.stderr.strip()[:500]}
        try:
            return json.loads(result.stdout)
        except json.JSONDecodeError:
            return {"ok": True, "result": result.stdout.strip()}

    def navigate(self, url: str) -> dict:
        """Navigate to a URL and return page title + snapshot."""
        script = f"""
import asyncio, json
async def run():
    from playwright.async_api import async_playwright
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto("{url}", wait_until="networkidle", timeout=30000)
        title = await page.title()
        content = await page.inner_text("body")
        await browser.close()
        print(json.dumps({{"title": title, "content_length": len(content), "content_preview": content[:500]}}))
asyncio.run(run())
"""
        return self._call_playwright(script)

    def snapshot(self, url: str) -> dict:
        """Get the full text content of a page."""
        script = f"""
import asyncio, json
async def run():
    from playwright.async_api import async_playwright
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto("{url}", wait_until="domcontentloaded", timeout=30000)
        text = await page.inner_text("body")
        await browser.close()
        print(json.dumps({{"text": text[:5000]}}))
asyncio.run(run())
"""
        return self._call_playwright(script)

    def screenshot(self, url: str, output: str = "/tmp/s7g_screenshot.png") -> dict:
        """Take a screenshot of a page."""
        script = f"""
import asyncio, json
async def run():
    from playwright.async_api import async_playwright
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=True)
        page = await browser.new_page(viewport={{"width": 1280, "height": 720}})
        await page.goto("{url}", wait_until="networkidle", timeout=30000)
        await page.screenshot(path="{output}", full_page=True)
        await browser.close()
        print(json.dumps({{"saved_to": "{output}"}}))
asyncio.run(run())
"""
        return self._call_playwright(script)

    def search(self, query: str) -> dict:
        """Search the web via Google and return top results."""
        import urllib.parse
        q = urllib.parse.quote(query)
        return self.navigate(f"https://www.google.com/search?q={q}&num=5")

    def extract(self, url: str, selector: str) -> dict:
        """Extract text matching a CSS selector."""
        script = f"""
import asyncio, json
async def run():
    from playwright.async_api import async_playwright
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto("{url}", wait_until="domcontentloaded", timeout=30000)
        els = await page.query_selector_all("{selector}")
        texts = [await el.inner_text() for el in els[:20]]
        await browser.close()
        print(json.dumps({{"matches": texts}}))
asyncio.run(run())
"""
        return self._call_playwright(script)

    def run(self, action: str, **kwargs) -> dict:
        """Dispatch to the appropriate browser action."""
        dispatch = {
            "navigate": self.navigate,
            "snapshot": lambda: self.snapshot(kwargs.get("url", "")),
            "screenshot": lambda: self.screenshot(kwargs.get("url", ""),
                                                   kwargs.get("output", "/tmp/s7g_screenshot.png")),
            "search": lambda: self.search(kwargs.get("query", "")),
            "extract": lambda: self.extract(kwargs.get("url", ""),
                                             kwargs.get("selector", "")),
        }
        handler = dispatch.get(action)
        if not handler:
            return {"ok": False, "error": f"Unknown action: {action}. "
                    f"Available: {list(dispatch.keys())}"}
        return handler()


# ── Specialized Browser Agents ─────────────────────────────────────

class MonitorAgent(BrowserAgent):
    """Monitor web pages for changes (prices, status, content)."""

    def __init__(self):
        super().__init__(name="monitor-agent")

    def check_price(self, url: str, selector: str) -> dict:
        result = self.extract(url, selector)
        if result.get("ok"):
            return {"ok": True, "url": url, "prices": result["result"].get("matches", [])}
        return result


class ScraperAgent(BrowserAgent):
    """Extract structured data from websites."""

    def __init__(self):
        super().__init__(name="scraper-agent")

    def scrape_table(self, url: str, table_selector: str = "table") -> dict:
        return self.extract(url, f"{table_selector} tr")


class ComplianceAgent(BrowserAgent):
    """Monitor regulatory websites for changes."""

    def __init__(self):
        super().__init__(name="compliance-agent")

    def check_regulation(self, url: str, keyword: str) -> dict:
        result = self.snapshot(url)
        text = result.get("text", "")
        found = keyword.lower() in text.lower()
        return {"ok": True, "url": url, "keyword": keyword, "found": found}
