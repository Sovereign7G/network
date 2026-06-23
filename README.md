# Sovereign 7G Network

**DePIN settlement layer for AI agents.** 30 autonomous agents managing DeFi, DePIN, cross-chain settlement, Hyperliquid arbitrage, and Polymarket prediction markets across Base, Solana, Ethereum, and ICP.

[![npm](https://img.shields.io/npm/v/@s7g-network/plugin-s7g)](https://www.npmjs.com/package/@s7g-network/plugin-s7g)
[![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)

## What It Does

- **30 autonomous agents** — liquidity management, yield harvesting, arbitrage, risk assessment, governance
- **9 ElizaOS actions** — DeFi, Hyperliquid, Polymarket — installable via `@s7g-network/plugin-s7g`
- **ACP Protocol** — Agent Communication Protocol endpoint at `/.well-known/agent.json`
- **Cross-chain USDC** — via CCTP bridge (Base ↔ Ethereum ↔ Solana)
- **Hyperliquid integration** — Funding rate arbitrage, LP positions
- **Polymarket integration** — Prediction market arbitrage
- **Multi-venue perp arbitrage** — Hyperliquid, Kalshi, Deribit
- **SNS domain** — `api.7g.sol` — censorship-resistant, no ICANN, no renewal

## Quick Start

```bash
# Install the ElizaOS plugin
npm install @s7g-network/plugin-s7g

# Or use the Python SDK
pip install s7g
```

## Architecture

```
agents/          # 30 autonomous agents (swarm.py)
sdk/             # Python SDK (72 methods)
contracts/       # 29 Solidity contracts on Base
eliza/           # ElizaOS plugin (@s7g-network/plugin-s7g)
hl_feeds/        # Hyperliquid, Kalshi, Deribit, Polymarket feeds
monitoring/      # Telegram + Discord alert bots
bridge/          # CCTP cross-chain bridge
identity/        # ENS/HNS/SNS resolution
partners/        # ACP partner connectors
```

## ElizaOS Actions

| Action | Description |
| :--- | :--- |
| `S7G_GET_LIQUIDITY` | Pool liquidity status |
| `S7G_GET_YIELD` | Best yield opportunities |
| `S7G_ARBITRAGE` | Execute arbitrage |
| `S7G_RISK` | Stablecoin de-peg risk |
| `S7G_EXECUTE` | Run any agent task |
| `HL_ARBITRAGE` | Hyperliquid funding arbitrage |
| `HL_LIQUIDITY` | Hyperliquid LP management |
| `HL_YIELD` | Cross-venue yield comparison |
| `PM_ARBITRAGE` | Polymarket prediction arbitrage |

## Security

16 red team rounds completed. 88 findings — all fixed. Auth, rate limiting, async writes, graceful shutdown. See `s7g-red-team-audit` skill for details.

## License

MIT
