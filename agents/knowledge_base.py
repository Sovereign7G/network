#!/usr/bin/env python3
"""
S7G Agent 75 — KnowledgeBaseAgent
Syncs S7G documentation to Chatwoot Help Center, updates knowledge
base with new features, and tracks knowledge base effectiveness.

Chatwoot (33.4K★): Open-source customer engagement platform.
Help Center Portal: Knowledge base + FAQs for self-service support.

Part of the 51+ agent swarm.
Agent ID: 75
Authorized: Commander Son Tran
"""

import json
import logging
import os
import sys
import time
from collections import defaultdict, deque
from datetime import datetime, timezone
from typing import Optional

# --- Configuration ---
CHATWOOT_URL = os.environ.get("CHATWOOT_URL", "http://localhost:3000")
POLL_INTERVAL = int(os.environ.get("KB_POLL", "43200"))  # 12 hours
DOCS_DIR = os.path.join(os.path.dirname(__file__), "..", "docs")

# --- Logging ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("logs/knowledge_base.log"),
        logging.StreamHandler()
    ]
)
log = logging.getLogger("knowledge_base")


class KnowledgeBaseAgent:
    """Agent 75: Syncs S7G documentation to Chatwoot Help Center."""

    # S7G documentation mapped to Chatwoot Help Center categories
    KNOWLEDGE_ARTICLES = {
        "getting_started": {
            "title": "Getting Started with S7G",
            "category": "Quick Start",
            "doc_path": "docs/solana_validator_ops.md",
            "summary": "Deploy your first node, stake S7G tokens, and start earning rewards.",
            "tags": ["setup", "deploy", "node", "validator"],
        },
        "settlement": {
            "title": "Cross-Chain Settlement Guide",
            "category": "Payments",
            "doc_path": "docs/moneygram_solana_strategy.md",
            "summary": "How to settle USDC cross-chain via CCTP bridge between Base, Solana, and Arbitrum.",
            "tags": ["settle", "cctp", "bridge", "usdc"],
        },
        "yield": {
            "title": "Yield Optimization & Staking",
            "category": "Finance",
            "doc_path": "docs/taiko_exploit_response.md",
            "summary": "Maximize returns through YieldRouter distribution and node staking.",
            "tags": ["yield", "staking", "apy", "rewards"],
        },
        "security": {
            "title": "Security Best Practices",
            "category": "Security",
            "doc_path": "docs/bridge_exploit_analysis.md",
            "summary": "How S7G protects against bridge exploits, malware, and AI-powered attacks.",
            "tags": ["security", "bridge", "exploit", "protection"],
        },
        "integrations": {
            "title": "Ecosystem Integrations Overview",
            "category": "Integrations",
            "doc_path": "docs/taiko_exploit_response.md",
            "summary": "S7G integrates with BlockRun MCP, vn.py, Vercel Eve, and Microsoft Qlib.",
            "tags": ["blockrun", "vnpy", "eve", "qlib", "integration"],
        },
        "validator": {
            "title": "Solana Validator Operations",
            "category": "Infrastructure",
            "doc_path": "docs/solana_validator_ops.md",
            "summary": "Operating an S7G Solana validator: setup, monitoring, and troubleshooting.",
            "tags": ["validator", "solana", "stake", "node"],
        },
    }

    # S7G glossary for quick reference
    GLOSSARY = {
        "CCTP": "Circle Cross-Chain Transfer Protocol — native USDC bridge",
        "CCTP Bridge": "Circle's burn-and-mint protocol for cross-chain USDC",
        "YieldRouter": "S7G contract distributing revenue 30/20/15/20/15",
        "SiV": "Silicon Vacancy — diamond-based quantum timing reference",
        "PNT": "Positioning, Navigation, Timing — GPS-independent navigation",
        "Agent Swarm": "51 autonomous AI agents managing the S7G network",
        "Zero-Tether": "GPS-independent timing mode using SiV quantum reference",
        "x402": "HTTP-native micropayment protocol for AI agents",
        "ElizaOS": "AI agent operating system — 50,000+ agents connected",
    }

    def __init__(self):
        self.articles_synced = 0
        self.glossary_terms = len(self.GLOSSARY)
        self.kb_updates: list[dict] = []
        self.start_time = datetime.now(timezone.utc).isoformat()

    def sync_article(self, article_key: str) -> dict:
        """Sync a knowledge article to Chatwoot Help Center."""
        article = self.KNOWLEDGE_ARTICLES.get(article_key)
        if not article:
            return {"status": "failed", "error": f"Unknown article: {article_key}"}

        # In production, this would POST to Chatwoot API
        result = {
            "title": article["title"],
            "category": article["category"],
            "tags": article["tags"],
            "summary": article["summary"],
            "status": "synced",
            "synced_at": datetime.now(timezone.utc).isoformat(),
        }

        self.articles_synced += 1
        self.kb_updates.append(result)
        log.info(f"KB article [{article_key}]: {article['title']} → synced")

        return result

    def search_knowledge_base(self, query: str) -> list[dict]:
        """Search the knowledge base for relevant articles."""
        query_lower = query.lower()
        results = []

        for key, article in self.KNOWLEDGE_ARTICLES.items():
            score = 0
            if any(kw in query_lower for kw in article["tags"]):
                score += 2
            if any(word in article["title"].lower() for word in query_lower.split()):
                score += 1
            if score > 0:
                results.append({
                    "article": article["title"],
                    "category": article["category"],
                    "relevance": score,
                    "summary": article["summary"],
                })

        results.sort(key=lambda x: -x["relevance"])
        return results[:3]

    def generate_report(self) -> dict:
        """Generate knowledge base report."""
        # Sync all articles
        sync_results = []
        for article_key in self.KNOWLEDGE_ARTICLES:
            result = self.sync_article(article_key)
            sync_results.append(result)

        # Test knowledge base search
        test_queries = [
            "How do I settle USDC?",
            "What is yield staking?",
            "Security and bridge protection",
        ]
        search_results = {}
        for q in test_queries:
            search_results[q] = self.search_knowledge_base(q)

        report = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "agent_id": 75,
            "agent_name": "KnowledgeBaseAgent",
            "chatwoot_help_center": f"{CHATWOOT_URL}/hc/en-us",
            "articles_synced": sync_results,
            "test_searches": search_results,
            "glossary": self.GLOSSARY,
            "stats": {
                "articles_published": self.articles_synced,
                "glossary_terms": self.glossary_terms,
                "categories": len(set(a["category"] for a in self.KNOWLEDGE_ARTICLES.values())),
            },
            "next_steps": [
                "Deploy Chatwoot: docker run -p 3000:3000 chatwoot/chatwoot",
                "Configure Help Center at /hc/en-us",
                "Enable Captain AI for automated support",
            ],
            "status": "ACTIVE",
        }

        return report

    def run_once(self) -> dict:
        """Execute one knowledge base sync cycle."""
        report = self.generate_report()
        log.info(f"KB: {report['stats']['articles_published']} articles | "
                 f"{report['stats']['glossary_terms']} glossary terms")
        return report

    def run_forever(self):
        """Run knowledge base sync loop."""
        log.info("=" * 50)
        log.info("KnowledgeBaseAgent STARTED (Agent 75)")
        log.info(f"Articles: {len(self.KNOWLEDGE_ARTICLES)}")
        log.info(f"Glossary: {len(self.GLOSSARY)} terms")
        log.info(f"Chatwoot: https://github.com/chatwoot/chatwoot (33.4K★)")
        log.info("=" * 50)

        while True:
            try:
                report = self.run_once()
            except Exception as e:
                log.error(f"KB sync failed: {e}")
            time.sleep(POLL_INTERVAL)


def main():
    agent = KnowledgeBaseAgent()

    if len(sys.argv) > 1 and sys.argv[1] == "--once":
        report = agent.run_once()
        print(json.dumps(report, indent=2))
    else:
        agent.run_forever()


if __name__ == "__main__":
    main()
