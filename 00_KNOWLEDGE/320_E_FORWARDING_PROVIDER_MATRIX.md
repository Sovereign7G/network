# 🏛️ [320_E] Sovereign Concierge: International Package Forwarding Provider Matrix

## 🏛️ Rationale
Physical sovereignty requires the ability to procure hardware, secure devices, and spare parts from any global marketplace—regardless of whether a vendor ships internationally. Package forwarding services act as the **physical routing layer** of the Sovereign Concierge, bridging the gap between US/UK-only merchants and globally distributed Age Republic infrastructure nodes.

This document provides a formally evaluated comparison matrix of all viable forwarding providers, ranked by their utility to the Age Republic's hardware procurement pipeline.

---

## 📊 Provider Evaluation Matrix

| Provider | Monthly Fee | Free Storage | Buy-For-Me | Warehouses | Consolidation | API Readiness | Sovereign Priority |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **ShipToBox** | Free | 30 days | ✅ Yes | US (DE, OR) | ✅ Yes | Full API | 🥇 **Tier 1** |
| **Stackry** | Free | 45 days | ❌ No | US (Portland, ME) | ✅ Yes (saves ~80%) | API available | 🥇 **Tier 1** |
| **Shipito** | Free (Basic) | 45 days | ✅ Yes | US (CA, OR, Austria) | ✅ Yes | API + Webhooks | 🥇 **Tier 1** |
| **Planet Express** | Free | 30 days | ✅ "Shop For Me" | US (CA) | ✅ Low fees | Beta API | 🥈 **Tier 2** |
| **Ship7** | Free | 60 days | ✅ Yes | US + UK | ✅ Yes | Manual | 🥈 **Tier 2** |
| **Forward2me** | Free | 28 days | ❌ No | US, UK, EU, Japan | ✅ Yes | API available | 🥈 **Tier 2** |
| **Fishisfast** | Free | 180 days | ❌ No | US (DE) | ✅ Yes | Planned | 🥉 **Tier 3** |
| **Reship** | Free | 30 days | ❌ No | US, Canada | ✅ Yes | Manual | 🥉 **Tier 3** |
| **Shippn** | Free | Varies | ✅ Host network | Community hosts globally | ❌ Limited | Manual | 🥉 **Tier 3** |
| **Aramex Shop & Ship** | Paid | 30 days | ✅ Yes | US, UK, China | ✅ Yes | Enterprise API | 🥉 **Tier 3** |

---

## 🏛️ Tier 1 Providers: Deep Analysis

### ShipToBox (Primary — Already Integrated)
* **Strengths**: Full "Buy For Me" proxy purchase, Delaware tax-free warehouse, documented REST API.
* **Best For**: GPU procurement where the merchant blocks international cards.
* **Limitation**: Smaller warehouse network vs. Shipito.
* **Integration Status**: ✅ `06_INFRA/shiptobox_forwarder.py` operational.

### Stackry (Secondary — Consolidation Specialist)
* **Strengths**: Zero fees, 45-day free storage, consolidation discounts up to 80%.
* **Best For**: Bulk DAO hardware orders (50+ units) that arrive from different vendors over weeks.
* **Limitation**: No "Buy For Me" program—requires your own card.
* **Integration Status**: ⏳ Planned for Phase 2.7.

### Shipito (Tertiary — Multi-Warehouse)
* **Strengths**: Three warehouse locations (California, Oregon tax-free, Austria for EU), ships to 200+ countries, webhook support.
* **Best For**: European node deployments (Austria warehouse avoids transatlantic double-hop).
* **Limitation**: Premium tiers required for fastest processing.
* **Integration Status**: ⏳ Planned for Phase 2.7.

---

## 🏛️ Tier 2 Providers: Situational Deployment

### Planet Express
* **Best For**: Small, lightweight items (hardware wallets, USB keys, SSD drives).
* **Why**: Low consolidation fees, competitive rates on sub-5lb packages.

### Ship7
* **Best For**: UK-origin procurement (UK warehouse available).
* **Why**: 60-day free storage gives longer consolidation windows for slow UK suppliers.

### Forward2me
* **Best For**: Multi-region sourcing (Japan warehouse for specialized electronics).
* **Why**: Only provider with a Japan address—critical for sourcing Sony/Mitsubishi industrial components.

---

## 🔑 Critical Decision Factors for the Sovereign Concierge

### 1. "Buy For Me" Capability
When a US merchant declines an international credit card, the forwarding provider purchases the item using their own payment method and bills you separately.

**Providers with Buy-For-Me**: ShipToBox, Shipito, Ship7, Planet Express, Aramex.
**Without**: Stackry, Forward2me, Fishisfast, Reship.

### 2. Tax-Free Warehouses
Delaware (DE) and Oregon (OR) have **zero state sales tax**. This saves 6–10% on every hardware purchase.

**Tax-free locations**: ShipToBox (DE), Shipito (OR), Fishisfast (DE), Stackry (ME — 5.5% tax applies).

### 3. Consolidation Economics
Combining multiple packages into a single shipment saves 40–80% on international freight. Essential for bulk DAO orders.

$$\text{Savings} = 1 - \frac{\text{Cost}(\text{consolidated})}{\sum_{i=1}^{n} \text{Cost}(\text{package}_i)} \approx 0.4 \text{ to } 0.8$$

### 4. Storage Duration
Longer storage = more flexibility for multi-vendor consolidation windows.

| Duration | Providers |
| :--- | :--- |
| **180 days** | Fishisfast |
| **60 days** | Ship7 |
| **45 days** | Stackry, Shipito |
| **30 days** | ShipToBox, Planet Express, Reship, Aramex |
| **28 days** | Forward2me |

---

## 🔄 Multi-Provider Routing Logic

The Concierge should automatically select the optimal provider based on order characteristics:

```
IF item requires Buy-For-Me (card declined):
    → Route to ShipToBox or Shipito

IF order is bulk DAO (>10 packages, multi-vendor):
    → Route to Stackry (best consolidation discounts)
    → OR Fishisfast (180-day storage for slow arrivals)

IF destination is Europe:
    → Route to Shipito Austria warehouse (avoids US→EU double customs)
    → OR Forward2me UK warehouse

IF item is small/lightweight (<2 lbs):
    → Route to Planet Express (lowest rates for light items)

IF source is Japan:
    → Route to Forward2me (only provider with Japan warehouse)

DEFAULT:
    → Route to ShipToBox (best API, tax-free DE)
```

---

## 📚 Source References
1. ShipToBox Blog: [Best MyUS Alternatives](https://www.shiptobox.com/blog/best-myus-alternatives/)
2. Ship7: [MyUS Alternative Comparison](https://www.ship7.com/international-shopping-alternatives/myus-alternative-check-ship7-with-the-best-rates)
3. Planet Express: [MyUS Alternative Review](https://planetexpress.com/shopping/the-best-myus-alternative-try-planet-express/)
4. Shippn Blog: [MyUS Alternative Analysis](https://www.shippn.com/blog/myus-alternative/amp/)
5. Farwadly: [MyUS Alternatives 2025](https://www.farwadly.com/blog/myus-alternatives-in-2025/)

---
**Status: SIPHONED | Anchored to ERA 216.0 | FORWARDING PROVIDER INTELLIGENCE INTEGRATED**
